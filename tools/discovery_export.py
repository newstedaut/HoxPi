#!/usr/bin/env python3
"""Discovery-Export fuer hoval_datapoints (community_additions).

Der HoxPi-Discovery-Scanner (discovery.py) probt den CAN-Bus per GET und
schreibt jeden antwortenden Datenpunkt nach discovery_found.json
("fg-fn-dp": "rohwert-hex"). Die meisten Funde stehen laengst in Hovals
Datenpunktliste (registers.json) und sind damit uninteressant. Dieses Skript
filtert die ECHTEN Neufunde heraus (nicht im Katalog) und erzeugt daraus eine
CSV im Format von github.com/newstedaut/hoval_datapoints/community_additions:

    fg,fn,dp,name_de,name_en,type,decimal,unit,note

Veroeffentlicht werden sollen nur benannte, verifizierte Datenpunkte. Deshalb
kommen Name/Typ/Einheit/Notiz aus einer kuratierten Datei discovery_names.json
(Vorlage: discovery_names.example.json). Ohne --all-new landen NUR Eintraege
in der CSV, die dort stehen UND "verified": true tragen. Mit --all-new werden
auch unbenannte Neufunde ausgegeben, aber mit "UNVERIFIED" in der Notiz.

Aufruf (auf dem Pi oder mit --found/--registers auf Kopien):
  python3 discovery_export.py --stats                 Zusammenfassung, keine Datei
  python3 discovery_export.py                         CSV nach stdout (nur verifizierte)
  python3 discovery_export.py --all-new -o neu.csv    alle Neufunde in Datei
  python3 discovery_export.py --names meine_namen.json

Roh-Wert-Deutung (nur Hilfe fuer die Benennung, keine Interpretation):
  1 Byte -> U8, 2 Byte -> U16/S16, 4 Byte -> U32/S32, druckbares ASCII -> STR.
"""
import argparse, csv, io, json, os, sys

DEF_FOUND = "/home/admin/discovery_data/discovery_found.json"
DEF_REG = os.path.join(os.environ.get("HOXPI_BRIDGE_DIR", "/home/admin/hoval-bridge"), "registers.json")
DEF_NAMES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "discovery_names.json")
COLS = ["fg", "fn", "dp", "name_de", "name_en", "type", "decimal", "unit", "note"]


def load_json(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"{what} nicht gefunden: {path}")
    except json.JSONDecodeError as e:
        sys.exit(f"{what} ist kein gueltiges JSON ({path}): {e}")


def katalog_keys(reg, unit_id=1):
    rows = reg["registers"] if isinstance(reg, dict) and "registers" in reg else reg
    keys = set()
    for r in rows:
        try:
            if int(r.get("unit_id", 1)) != unit_id:
                continue  # der Scanner probt nur eine Geraeteadresse (Standard: WEZ)
            keys.add((int(r["fg"]), int(r["fn"]), int(r["dp"])))
        except (KeyError, TypeError, ValueError):
            pass
    return keys


def decode_raw(hexval):
    """Liefert (roh_int_oder_str, typ_vorschlag, laenge_bytes)."""
    try:
        b = bytes.fromhex(hexval)
    except (ValueError, TypeError):
        return hexval, "?", 0
    if len(b) >= 3 and all(32 <= c < 127 for c in b):
        return b.decode("ascii"), "STR", len(b)
    n = int.from_bytes(b, "big") if b else 0
    typ = {1: "U8", 2: "U16", 4: "U32"}.get(len(b), f"RAW{len(b)}")
    return n, typ, len(b)


def parse_key(key):
    try:
        fg, fn, dp = (int(x) for x in key.split("-"))
        return fg, fn, dp
    except ValueError:
        return None


def build_rows(found, kat, names, all_new):
    rows, stats = [], {"funde": len(found), "katalog": 0, "neu": 0, "benannt": 0, "verifiziert": 0, "kaputt": 0}
    for key, hexval in sorted(found.items(), key=lambda kv: parse_key(kv[0]) or (999, 999, 999)):
        k = parse_key(key)
        if k is None:
            stats["kaputt"] += 1
            continue
        if k in kat:
            stats["katalog"] += 1
            continue
        stats["neu"] += 1
        raw, typ_guess, nbytes = decode_raw(hexval)
        info = names.get(key) or {}
        if info:
            stats["benannt"] += 1
        verified = bool(info.get("verified"))
        if verified:
            stats["verifiziert"] += 1
        if not verified and not all_new:
            continue
        note = (info.get("note") or "").strip()
        if not verified:
            tag = "UNVERIFIED. " if info else f"UNVERIFIED (unnamed, {nbytes} byte raw 0x{hexval}). "
            note = (tag + note).strip()
        rows.append({
            "fg": k[0], "fn": k[1], "dp": k[2],
            "name_de": info.get("name_de") or "unbekannt",
            "name_en": info.get("name_en") or "unknown",
            "type": info.get("type") or typ_guess,
            "decimal": info.get("decimal", 0),
            "unit": info.get("unit") or "",
            "note": note,
            "_raw": raw,
        })
    return rows, stats


def main():
    ap = argparse.ArgumentParser(description="Neufunde des Discovery-Scanners als community_additions-CSV")
    ap.add_argument("--found", default=DEF_FOUND, help="discovery_found.json")
    ap.add_argument("--registers", default=DEF_REG, help="registers.json (Katalog)")
    ap.add_argument("--names", default=DEF_NAMES, help="kuratierte Namen/Verifikation (JSON)")
    ap.add_argument("--unit-id", type=int, default=1, help="Geraeteadresse, die der Scanner probt (1 = WEZ)")
    ap.add_argument("--all-new", action="store_true", help="auch unbenannte/unverifizierte Neufunde (als UNVERIFIED)")
    ap.add_argument("--stats", action="store_true", help="nur Zusammenfassung ausgeben")
    ap.add_argument("-o", "--out", help="CSV-Datei (Standard: stdout)")
    a = ap.parse_args()

    found = load_json(a.found, "discovery_found.json")
    if not isinstance(found, dict):
        sys.exit("discovery_found.json hat nicht das erwartete Format {\"fg-fn-dp\": \"hex\"}")
    kat = katalog_keys(load_json(a.registers, "registers.json"), a.unit_id)
    names = {}
    if os.path.exists(a.names):
        names = load_json(a.names, "discovery_names.json")
        names = {k: v for k, v in names.items() if not k.startswith("_")}
    elif a.names != DEF_NAMES:
        sys.exit(f"Namensdatei nicht gefunden: {a.names}")

    rows, st = build_rows(found, kat, names, a.all_new)
    if a.stats or not rows:
        print(f"Funde gesamt: {st['funde']}  im Katalog: {st['katalog']}  Neufunde: {st['neu']}  "
              f"davon benannt: {st['benannt']}  verifiziert: {st['verifiziert']}"
              + (f"  unlesbare Schluessel: {st['kaputt']}" if st["kaputt"] else ""), file=sys.stderr)
        if a.stats:
            for r in rows:
                print(f"  {r['fg']}-{r['fn']}-{r['dp']:<6} {r['type']:<5} raw={r['_raw']!r:<18} {r['name_de']}"
                      + ("" if "UNVERIFIED" not in r["note"] else "  [UNVERIFIED]"), file=sys.stderr)
            return 0
        if not rows:
            print("Keine ausgabefaehigen Zeilen (ohne --all-new nur benannte + verifizierte Neufunde).", file=sys.stderr)
            return 0

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="") as f:
            f.write(buf.getvalue())
        print(f"{len(rows)} Zeile(n) -> {a.out}  (Neufunde {st['neu']}, verifiziert {st['verifiziert']})", file=sys.stderr)
    else:
        sys.stdout.write(buf.getvalue())
    return 0


if __name__ == "__main__":
    sys.exit(main())
