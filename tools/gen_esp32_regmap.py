#!/usr/bin/env python3
"""Erzeugt die Registertabelle fuers ESP32-Gateway (esp32-gateway/main/regmap_gen.h)
aus registers.json (+ optional whitelist.json).

registers.json entsteht lokal mit tools/gen_registers.py aus Hovals Datenpunktliste
und ist NICHT im Repo (Urheberrecht Hoval AG) - der erzeugte Header ist es deshalb
ebenfalls nicht (.gitignore). Im Repo liegt nur regmap_example.h mit wenigen
allgemein bekannten Registern, damit das Projekt ohne Liste kompiliert.

Was der Generator uebernimmt (dieselben Regeln wie bridge/hoval_bridge.py):
  * 32-bit-Paare STRUKTURELL erkennen: gleiche (unit_id,fg,fn,dp), Typ U32/S32 und
    direkt aufeinanderfolgende reg-Nummern -> zweite Zeile = Low-Wort (Flag LOW_HALF),
    Namenszusatz "_low"/" low" zusaetzlich. Nur die High-Zeile wird dekodiert; das
    Low-Wort landet in reg+1 (hp_to_regs).
  * Bereichspruefung: min/max fehlen oder 0/0 -> Flag NO_RANGE (keine Pruefung).
  * Modbus-Bereiche: zusammenhaengende Registerbloecke, Luecken <= --merge-gap Woerter
    werden mitgenommen (weniger Bereiche fuer esp-modbus, kaum RAM).
  * Whitelist: whitelist.json {"allowed":[...]} oder die eingebaute HoxPi-Liste.

Aufruf:
  python3 gen_esp32_regmap.py registers.json [-w whitelist.json] [-o regmap_gen.h] [--merge-gap 32]
  python3 gen_esp32_regmap.py registers.json --stats      nur Kennzahlen
"""
import argparse, json, re, sys
from datetime import datetime

TYPES = {"U8": 0, "S8": 1, "U16": 2, "S16": 3, "U32": 4, "S32": 5, "LIST": 6}
LOW_SUFFIX = re.compile(r"[_ ]low$", re.I)

# Eingebaute Whitelist = WRITE_WHITELIST aus bridge/hoval_bridge.py (Stand 02.09.2026)
DEFAULT_WHITELIST = [1478, 1479, 1481, 1482, 1496, 1497, 1498,
                     27509, 27528, 27529, 27530, 27545, 27546, 28839,
                     1561, 1510, 1511, 1490, 1491, 19482, 23755, 27510, 27511, 27531, 27532]


def load_rows(path):
    rows = json.load(open(path, encoding="utf-8"))
    out = []
    for r in rows:
        try:
            reg = int(r["reg"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append({
            "reg": reg, "unit_id": int(r.get("unit_id") or 0),
            "fg": int(r.get("fg") or 0), "fn": int(r.get("fn") or 0), "dp": int(r.get("dp") or 0),
            "name": str(r.get("name") or ""), "type": str(r.get("type") or "").upper(),
            "decimal": int(r.get("decimal") or 0),
            "min": r.get("min"), "max": r.get("max"),
            "writable": str(r.get("writable") or "No").strip().lower() in ("yes", "true", "1", "x", "w"),
            "unit": str(r.get("unit") or ""),
        })
    out.sort(key=lambda x: x["reg"])
    # doppelte reg-Nummern: erste gewinnt (wie RegMap.by_reg in hoval_bridge.py)
    seen, uniq = set(), []
    for r in out:
        if r["reg"] in seen:
            continue
        seen.add(r["reg"]); uniq.append(r)
    return uniq


def mark_low_halves(rows):
    """Strukturelle Paar-Erkennung wie HovalBridge._effective_rows."""
    groups = {}
    for r in rows:
        if r["type"] in ("U32", "S32"):
            groups.setdefault((r["unit_id"], r["fg"], r["fn"], r["dp"]), []).append(r)
    n = 0
    for g in groups.values():
        g.sort(key=lambda x: x["reg"])
        i = 0
        while i < len(g) - 1:
            if g[i + 1]["reg"] == g[i]["reg"] + 1:
                g[i + 1]["low"] = True; n += 1; i += 2
            else:
                i += 1
    for r in rows:
        if r["type"] in ("U32", "S32") and LOW_SUFFIX.search(r["name"].strip()) and not r.get("low"):
            r["low"] = True; n += 1
    return n


def areas(rows, merge_gap):
    regs = sorted({r["reg"] for r in rows} | {r["reg"] + 1 for r in rows if r["type"] in ("U32", "S32")})
    out, start, prev = [], regs[0], regs[0]
    for x in regs[1:]:
        if x - prev > merge_gap + 1:
            out.append((start, prev - start + 1)); start = x
        prev = x
    out.append((start, prev - start + 1))
    return out


def c_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def emit(rows, wl, ar, src, out):
    w = out.write
    w("/* regmap_gen.h — GENERIERT von tools/gen_esp32_regmap.py, nicht von Hand aendern.\n")
    w(" * Quelle: %s, %s. Enthaelt Daten aus Hovals Datenpunktliste -> NICHT ins Repo.\n */\n" %
      (src, datetime.now().strftime("%Y-%m-%d %H:%M")))
    w("#include \"hoval_proto.h\"\n\n")
    w("const hp_reg_t hp_regs[] = {\n")
    w("/*   reg, unit,  fg,  fn,    dp, type, dec, flags,        min,        max   name */\n")
    for r in rows:
        flags = []
        if r["writable"]: flags.append("HP_F_WRITABLE")
        if r.get("low"):  flags.append("HP_F_LOW_HALF")
        mn, mx = r["min"], r["max"]
        no_range = mn is None or mx is None or (mn == 0 and mx == 0)
        if no_range: flags.append("HP_F_NO_RANGE"); mn, mx = 0, 0
        t = TYPES.get(r["type"], 7)
        w("    {%5d, %4d, %3d, %3d, %5d, %d, %d, %s, %10d, %10d}, /* %s%s */\n" % (
            r["reg"], r["unit_id"], r["fg"], r["fn"], r["dp"], t, r["decimal"],
            "|".join(flags) or "0", int(mn), int(mx),
            c_str(r["name"]).replace("*/", "* /"), (" [" + r["unit"] + "]") if r["unit"] else ""))
    w("};\nconst uint16_t hp_regs_count = %d;\n\n" % len(rows))
    w("/* Modbus-Bereiche (Holding Register) fuer den esp-modbus-Slave */\n")
    w("const hp_area_t hp_areas[] = {\n")
    for s, n in ar:
        w("    {%5d, %5d},\n" % (s, n))
    w("};\nconst uint16_t hp_areas_count = %d;\n\n" % len(ar))
    w("/* Schreib-Whitelist (Register, die Modbus-Clients schreiben duerfen) */\n")
    w("const uint16_t hp_whitelist[] = { %s };\n" % ", ".join(str(x) for x in wl))
    w("const uint16_t hp_whitelist_count = %d;\n" % len(wl))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("registers", help="registers.json (aus gen_registers.py)")
    ap.add_argument("-w", "--whitelist", help="whitelist.json ({\"allowed\": [...]})")
    ap.add_argument("-o", "--out", default="regmap_gen.h")
    ap.add_argument("--merge-gap", type=int, default=32, help="Luecken bis n Woerter zu einem Bereich zusammenfassen")
    ap.add_argument("--stats", action="store_true", help="nur Kennzahlen ausgeben")
    a = ap.parse_args()

    rows = load_rows(a.registers)
    if not rows:
        sys.exit("keine Register in %s" % a.registers)
    lows = mark_low_halves(rows)
    wl = DEFAULT_WHITELIST
    if a.whitelist:
        try:
            wl = sorted(int(x) for x in json.load(open(a.whitelist, encoding="utf-8")).get("allowed", []))
        except (OSError, ValueError, AttributeError) as e:
            sys.exit("whitelist.json unlesbar: %s" % e)
    known = {r["reg"] for r in rows}
    unknown_wl = [x for x in wl if x not in known]
    ar = areas(rows, a.merge_gap)
    words = sum(n for _, n in ar)

    print("Register: %d (davon %d Low-Woerter von 32-bit-Paaren), reg %d..%d" %
          (len(rows), lows, rows[0]["reg"], rows[-1]["reg"]))
    print("Typen: %s" % ", ".join("%s=%d" % (t, sum(1 for r in rows if r["type"] == t)) for t in TYPES))
    print("Modbus-Bereiche: %d (merge-gap %d) = %d Woerter = %.1f KB RAM" % (len(ar), a.merge_gap, words, words * 2 / 1024))
    print("Whitelist: %d Register%s" % (len(wl), (" - NICHT in der Tabelle: %s" % unknown_wl) if unknown_wl else ""))
    if a.stats:
        return
    with open(a.out, "w", encoding="utf-8") as f:
        emit(rows, wl, ar, a.registers, f)
    print("geschrieben: %s" % a.out)


if __name__ == "__main__":
    main()
