#!/usr/bin/env python3
"""gen_esp32_nvs.py — NVS-Konfiguration fuer das HoxPi-ESP32-Gateway erzeugen (ohne Board, ohne Neubau).

Das Gateway liest beim Start den NVS-Namespace "hoxpi" (main/hoval_cfg.h):
    poll_wez   u16  Sekunden zwischen zwei WEZ-Runden        (5..3600)
    poll_hv    u16  Sekunden zwischen zwei HomeVent-Runden   (1..3600)
    poll_delay u16  Millisekunden zwischen zwei GET-Frames   (10..2000)
    wr_en      u8   0/1 Schreibpfad Modbus -> CAN
    whitelist  str  "1490,1497,..." Register, die Modbus-Clients schreiben duerfen
Fehlt ein Schluessel, gilt das Kompilat (Kconfig / regmap_gen.h). Dieses Skript schreibt nur die
Schluessel, die du angibst - so bleibt z. B. die kompilierte Whitelist erhalten, wenn du nur das
Poll-Intervall aenderst.

Ausgabe = CSV fuer den ESP-IDF-Generator nvs_partition_gen.py, dann flashen:
    python3 tools/gen_esp32_nvs.py -w whitelist.json --poll-wez 30 --enable-write -o nvs_config.csv
    python3 $IDF_PATH/components/nvs_flash/nvs_partition_generator/nvs_partition_gen.py generate nvs_config.csv nvs.bin 0x6000
    esptool.py -p /dev/ttyUSB0 write_flash 0x9000 nvs.bin
(0x9000/0x6000 = Offset/Groesse der nvs-Partition in der Standard-Partitionstabelle "Single factory app";
 bei eigener partitions.csv dort nachsehen. `idf.py erase-flash` loescht die Werte wieder -> Kompilat.)

Whitelist-Quellen: -w whitelist.json ({"allowed": [...]}, wie HoxPi-Bridge) oder --whitelist "1490,1497".
Mit -r registers.json werden die Register gegen die Tabelle geprueft (unbekannte -> Fehler, wie das Gateway
sie beim Start verwerfen wuerde).
"""
import argparse, csv, json, os, sys

RANGES = {"poll_wez": (5, 3600), "poll_hv": (1, 3600), "poll_delay": (10, 2000)}
WL_MAX = 128          # HCFG_WL_MAX
WL_TEXT_MAX = 1024    # HCFG_WL_TEXT_MAX


def parse_wl_text(text):
    out = []
    for tok in text.replace(";", ",").replace(" ", ",").split(","):
        tok = tok.strip()
        if not tok:
            continue
        if not tok.isdigit() or int(tok) > 65535:
            raise SystemExit("Whitelist: ungueltiger Eintrag %r" % tok)
        v = int(tok)
        if v not in out:
            out.append(v)
    return out


def load_wl_json(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    allowed = d.get("allowed", d) if isinstance(d, dict) else d
    if not isinstance(allowed, list):
        raise SystemExit("%s: erwartet {\"allowed\": [...]}" % path)
    out = []
    for v in allowed:
        v = int(v)
        if not 0 <= v <= 65535:
            raise SystemExit("%s: Register %r ausserhalb 0..65535" % (path, v))
        if v not in out:
            out.append(v)
    return out


def check_against_registers(wl, path):
    with open(path, encoding="utf-8") as f:
        regs = json.load(f)
    known = {}
    rows = regs.get("registers", regs) if isinstance(regs, dict) else regs
    for r in rows:
        try:
            known[int(r["reg"] if "reg" in r else r["register"])] = r
        except (KeyError, TypeError, ValueError):
            continue
    bad = [v for v in wl if v not in known]
    if bad:
        raise SystemExit("Whitelist: nicht in %s: %s (das Gateway wuerde sie beim Start verwerfen)" % (path, bad))
    nonwr = [v for v in wl if not known[v].get("writable", known[v].get("rw", True))]
    if nonwr:
        print("Hinweis: laut Liste nicht schreibbar (bleiben, wie bei HoxPi): %s" % nonwr, file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", default="nvs_config.csv", help="CSV fuer nvs_partition_gen.py (Standard nvs_config.csv)")
    ap.add_argument("--poll-wez", type=int, help="WEZ-Poll-Intervall in s (5..3600)")
    ap.add_argument("--poll-hv", type=int, help="HomeVent-Poll-Intervall in s (1..3600)")
    ap.add_argument("--poll-delay", type=int, help="Abstand zwischen GET-Frames in ms (10..2000)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--enable-write", action="store_true", help="wr_en = 1")
    g.add_argument("--disable-write", action="store_true", help="wr_en = 0")
    w = ap.add_mutually_exclusive_group()
    w.add_argument("-w", "--whitelist-json", help="whitelist.json der HoxPi-Bridge ({\"allowed\": [...]})")
    w.add_argument("--whitelist", help="Register direkt, z. B. \"1490,1497,27509\" (leer = nichts schreibbar)")
    ap.add_argument("-r", "--registers", help="registers.json zum Pruefen der Whitelist")
    ap.add_argument("--print", action="store_true", help="CSV nur anzeigen, nicht schreiben")
    a = ap.parse_args()

    rows = [("hoxpi", "namespace", "", "")]
    for key, val in (("poll_wez", a.poll_wez), ("poll_hv", a.poll_hv), ("poll_delay", a.poll_delay)):
        if val is None:
            continue
        lo, hi = RANGES[key]
        if not lo <= val <= hi:
            raise SystemExit("%s=%d ausserhalb %d..%d" % (key, val, lo, hi))
        rows.append((key, "data", "u16", str(val)))
    if a.enable_write or a.disable_write:
        rows.append(("wr_en", "data", "u8", "1" if a.enable_write else "0"))

    wl = None
    if a.whitelist_json:
        wl = load_wl_json(a.whitelist_json)
    elif a.whitelist is not None:
        wl = parse_wl_text(a.whitelist)
    if wl is not None:
        if len(wl) > WL_MAX:
            raise SystemExit("Whitelist: %d Eintraege > %d (HCFG_WL_MAX)" % (len(wl), WL_MAX))
        if a.registers:
            check_against_registers(wl, a.registers)
        text = ",".join(str(v) for v in wl)
        if len(text) > WL_TEXT_MAX:
            raise SystemExit("Whitelist-Text %d Zeichen > %d" % (len(text), WL_TEXT_MAX))
        rows.append(("whitelist", "data", "string", text))

    if len(rows) == 1:
        raise SystemExit("nichts zu schreiben - mindestens einen Wert angeben (siehe --help)")

    if a.print:
        out = sys.stdout
        wr = csv.writer(out, lineterminator="\n")
        wr.writerow(("key", "type", "encoding", "value"))
        wr.writerows(rows)
    else:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f, lineterminator="\n")
            wr.writerow(("key", "type", "encoding", "value"))
            wr.writerows(rows)
        print("%s geschrieben (%d Schluessel%s)." % (a.out, len(rows) - 1, ", Whitelist %d Register" % len(wl) if wl is not None else ""))
        print("Weiter: python3 $IDF_PATH/components/nvs_flash/nvs_partition_generator/nvs_partition_gen.py generate %s nvs.bin 0x6000" % a.out)
        print("        esptool.py write_flash 0x9000 nvs.bin    # Offset/Groesse der nvs-Partition pruefen")


if __name__ == "__main__":
    main()
