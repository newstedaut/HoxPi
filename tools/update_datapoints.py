#!/usr/bin/env python3
"""Auto-Update der Hoval-Datenpunktliste fuer HoxPi.

Laedt die aktuelle offizielle Datenpunktliste (xlsx) von Hoval, vergleicht sie
mit dem installierten Stand und erzeugt bei Aenderung registers.json +
reg_texts.json neu (via gen_registers.py / gen_reg_texts.py). So bleibt die
Registerkarte automatisch aktuell — etwa nach einem Firmware-Update der Anlage
durch den Hoval-Service. Datenpunkte, die die Regler-Firmware (noch) nicht
kennt, antworten am CAN einfach nie und bleiben leer; sie stoeren nicht.

Aufruf:
  python3 update_datapoints.py --check            nur pruefen, nichts aendern
  python3 update_datapoints.py --apply            bei Aenderung neu erzeugen (+Backup)
  python3 update_datapoints.py --apply --restart  danach hoval-bridge neu starten

Unit-IDs werden aus der vorhandenen registers.json uebernommen (Fallback 1,520,143).
Die xlsx selbst wird nur temporaer verarbeitet und NICHT dauerhaft gespeichert
(Urheberrecht Hoval AG).
"""
import hashlib, json, os, subprocess, sys, tempfile, urllib.request

URL = "https://cdn.hoval.com/toptronice-gateway-modbus-datapoints_hybris_original.xlsx"
BASE = os.environ.get("HOXPI_BRIDGE_DIR", "/home/admin/hoval-bridge")
REG = os.path.join(BASE, "registers.json")
TXT = os.path.join(BASE, "reg_texts.json")
STATE = os.path.join(BASE, "datapoints_version.json")
TOOLS = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def list_version(path):
    """Version + SW-Stand aus dem Deckblatt der xlsx lesen."""
    try:
        import openpyxl
        ws = openpyxl.load_workbook(path, read_only=True).worksheets[0]
        cells = [str(r[0]) for r in ws.iter_rows(min_row=1, max_row=10, max_col=1,
                                                 values_only=True) if r[0]]
        ver = next((c for c in cells if c.startswith("V")), "?")
        sw = next((c for c in cells if "SW" in c), "?")
        return f"{ver} ({sw})"
    except Exception:
        return "?"


def main():
    args = set(sys.argv[1:])
    if not args or not args & {"--check", "--apply"}:
        print(__doc__)
        return 1

    state = {}
    if os.path.exists(STATE):
        try:
            state = json.load(open(STATE))
        except Exception:
            pass

    with tempfile.TemporaryDirectory() as tmp:
        xlsx = os.path.join(tmp, "datapoints.xlsx")
        print(f"Lade {URL} ...")
        urllib.request.urlretrieve(URL, xlsx)
        digest = sha256(xlsx)
        ver = list_version(xlsx)
        print(f"Online-Stand: {ver} | sha256 {digest[:16]}…")
        if state.get("sha256") == digest:
            print("Bereits aktuell — nichts zu tun.")
            return 0
        print(f"Neu gegenueber installiertem Stand ({state.get('version', 'unbekannt')}).")
        if "--apply" not in args:
            print("(--apply zum Uebernehmen)")
            return 2

        # Unit-IDs aus vorhandener registers.json uebernehmen
        unit_ids = "1,520,143"
        if os.path.exists(REG):
            try:
                uids = sorted({r["unit_id"] for r in json.load(open(REG, encoding="utf-8"))})
                unit_ids = ",".join(str(u) for u in uids)
            except Exception:
                pass
        print(f"Erzeuge Registerkarte fuer Unit-IDs {unit_ids} ...")

        new_reg = os.path.join(tmp, "registers.json")
        new_txt = os.path.join(tmp, "reg_texts.json")
        subprocess.run([sys.executable, os.path.join(TOOLS, "gen_registers.py"),
                        xlsx, unit_ids, new_reg], check=True)
        subprocess.run([sys.executable, os.path.join(TOOLS, "gen_reg_texts.py"),
                        xlsx, new_reg, new_txt], check=True)

        # Sanity-Check: neue Karte darf nicht drastisch schrumpfen
        old_n = len(json.load(open(REG, encoding="utf-8"))) if os.path.exists(REG) else 0
        new_n = len(json.load(open(new_reg, encoding="utf-8")))
        print(f"Register: {old_n} -> {new_n}")
        if old_n and new_n < old_n * 0.9:
            print("ABBRUCH: neue Liste deutlich kleiner als bisher — bitte manuell pruefen.")
            return 3

        for src, dst in ((new_reg, REG), (new_txt, TXT)):
            if os.path.exists(dst):
                os.replace(dst, dst + ".bak")
            # os.replace geht nicht ueber Dateisystemgrenzen (tmpfs) -> kopieren
            with open(src, "rb") as fs, open(dst, "wb") as fd:
                fd.write(fs.read())
        json.dump({"sha256": digest, "version": ver}, open(STATE, "w"))
        print(f"Uebernommen. Backups: {REG}.bak / {TXT}.bak")

        if "--restart" in args:
            print("Starte hoval-bridge neu ...")
            subprocess.run(["systemctl", "restart", "hoval-bridge"], check=False)
            print("Hinweis: Bridge lehnt Schreibzugriffe ab, bis jedes Register "
                  "einmal vom CAN gelesen wurde (Kalt-Cache-Schutz).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
