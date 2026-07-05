#!/usr/bin/env python3
# Hoval-Pi Dashboard v4 - Hoval-Branding (hell, rot), Bereiche klar getrennt
import http.server, socketserver, html, json, datetime, time as _time, threading
from urllib.parse import urlparse, parse_qs

REG_PATH = "/home/admin/hoval-bridge/registers.json"
MODBUS_HOST, MODBUS_PORT = "127.0.0.1", 502
HOVAL_RED = "#e2001a"

# ---------- Sprache (DE/EN) ----------
_ctx = threading.local()
def L(de, en=None):
    """Gibt je nach aktueller Sprache DE oder EN zurück. Ohne EN -> Fallback DE."""
    if getattr(_ctx, "lang", "de") == "en" and en is not None:
        return en
    return de
def curlang():
    return getattr(_ctx, "lang", "de")

# ---------- Status-Texte ----------
ST_HC  = {0:"Aus",1:"Heizen normal",2:"Heizen Komfort",3:"Heizen Eco",4:"Frostschutz",
          5:"Zwangsabnahme",6:"Zwangsreduktion",7:"Ferien",8:"Party",9:"Kühlen normal",
          12:"Störung",13:"Handbetrieb",22:"Kühlen extern",23:"Heizen extern",26:"SmartGrid"}
ST_DHW = {0:"Aus",1:"Laden normal",2:"Laden Komfort",5:"Störung",6:"Zapfung",
          8:"Laden reduziert",12:"SmartGrid",13:"SmartGrid Zwang"}
ST_HP  = {0:"Aus",1:"Heizen",2:"Aktiv-Kühlen",3:"Sperre",4:"WW-Laden",5:"Frostschutz",
          6:"WEZ-Temp zu tief",7:"VL zu hoch",8:"Abtauen",9:"Passiv-Kühlen",
          11:"Hochdruck-Störung",12:"Niederdruck-Störung",16:"Wiederanlauf",17:"EVU-Sperre",
          18:"Vorlaufzeit",19:"Nachlaufzeit",51:"Kondensatorpumpe",55:"Inverter-Störung"}
# Enum-Texte (Register-spezifisch, aus offizieller Hoval-Tabelle, dt.)
ENUM = {
 1478:{0:"Standby",1:"Woche 1",2:"Woche 2",4:"Konstant",5:"Sparbetrieb",7:"Hand Heizen",8:"Hand Kühlen"},
 1496:{0:"Standby",1:"Woche 1",2:"Woche 2",4:"Konstant",6:"Sparbetrieb"},
 23622:{0:"Standby",1:"Woche 1",2:"Woche 2",4:"Konstantbetrieb",5:"Sparbetrieb"},
 23631:{0:"Aus / Standby",1:"Normalbetrieb",2:"VOC-Modus",3:"Feuchte-Modus",4:"Frostschutz",
        5:"CoolVet (Kühlen)",6:"Fehler",7:"Sommerfeuchte",8:"Ausschaltstop"},
}

# ---------- Bereiche (2-stufig: Bereich -> Untergruppen -> Werte) ----------
# Wert: (reg, Name, Einheit/Status, Nachkomma, signed)  |  Hinweis: (None, Text, "note", 0, False)
DOMAINS = [
 ("Wärmepumpe", "🔥", [
   (None, [
     (1477,"Außentemperatur","°C",1,True),
     (1540,"Betriebsstatus","ST_HP",0,False),
     (18726,"Modulation Verdichter","%",0,False),
     (25611,"Elektrische Leistung","kW",2,True),
     (25612,"Heizleistung","kW",0,True),
     (27467,"Effizienz (Arbeitszahl)","",1,False),
     (18738,"Wasserdruck","bar",1,True),
     (18742,"Rücklauf Wärmeerzeuger","°C",1,True),
     (1525,"WEZ-Temperatur","°C",1,True),
   ]),
 ]),
 ("Heizung & Kühlung", "🌡️", [
   (None, [
     (1478,"Betriebsart","ENUM",0,False),
     (1501,"Status Heizkreis","ST_HC",0,False),
     (1510,"Raumtemperatur Ist","°C",1,True),
     (1493,"Raum-Sollwert","°C",1,True),
     (1513,"Vorlauf-Temperatur","°C",1,True),
     (1535,"Rücklauf-Temperatur","°C",1,True),
     (1520,"Sollwert Heizkreis","°C",1,True),
     (1524,"Sollwert Kühlmodus","°C",1,True),
     (19658,"Mischer HK1","%",0,False),
     (19659,"Mischer HK2","%",0,False),
   ]),
 ]),
 ("Warmwasser", "🚿", [
   (None, [
     (1496,"Betriebsart","ENUM",0,False),
     (1500,"Warmwasser Ist","°C",1,True),
     (27483,"Warmwasser Ist (Fühler 2)","°C",1,True),
     (1499,"Warmwasser Sollwert","°C",1,True),
     (1497,"Normal-Temperatur","°C",1,True),
     (1498,"Eco-Temperatur","°C",0,False),
     (1504,"Status Warmwasser","ST_DHW",0,False),
   ]),
 ]),
 ("Wohnraumlüftung", "💨", [
   ("Betrieb & Stufen", [
     (23622,"Betriebswahl","",0,False),
     (23625,"Lüftung aktuell (Ist)","%",0,False),
     (23623,"Normalstufe (Soll)","%",0,False),
     (23624,"Eco-Stufe (Soll)","%",0,False),
     (23626,"Feuchte-Sollwert","%",0,False),
     (23631,"Status Regelung","",0,False),
   ]),
   ("🌳 Außenluft — Frischluft von draußen (rein)", [
     (23632,"Außenluft-Temperatur","°C",1,True),
     (23629,"VOC Außenluft","%",0,False),
   ]),
   ("➡️ Zuluft — in die Räume", [
     (None,"Zuluft-Temperatur und -Feuchte stellt Hoval nicht über Modbus bereit (die HomeVent regelt das intern über die Wärmerückgewinnung).","note",0,False),
   ]),
   ("🏠 Abluft — Raumluft aus den Räumen (raus)", [
     (23633,"Abluft-Temperatur","°C",1,True),
     (23627,"Feuchte Abluft","%",0,False),
     (23628,"VOC Abluft","%",0,False),
     (28940,"CO₂ Abluft","%",0,False),
   ]),
   ("🌬️ Fortluft — Ausstoß nach draußen", [
     (23634,"Lüfter (Abluft → Fortluft)","%",0,False),
   ]),
 ]),
]

# Kurzbeschreibungen je Datenpunkt (Register -> Text). Für nicht gelistete Register
# wird automatisch ein Text aus den Metadaten erzeugt -> jeder Wert hat einen Tooltip.
DESC = {
 1477:"Aktuelle Außentemperatur (Fühler der Wärmepumpe). Basis für die witterungsgeführte Heizkurve.",
 1540:"Betriebszustand der Wärmepumpe (z. B. Heizen, Kühlen, Warmwasser, Abtauen, Standby).",
 18726:"Aktuelle Verdichterleistung in Prozent. 0 % = aus, 100 % = Volllast.",
 25611:"Momentan aufgenommene elektrische Leistung (Stromverbrauch der Wärmepumpe).",
 25612:"Momentan abgegebene Wärmeleistung an Heizung bzw. Warmwasser.",
 27467:"Arbeitszahl (COP): abgegebene Wärme geteilt durch eingesetzten Strom. Höher = effizienter.",
 18738:"Wasserdruck im Heizkreis. Normal ca. 1–2 bar. Zu niedrig → Wasser nachfüllen.",
 18742:"Temperatur des zur Wärmepumpe zurückfließenden Heizwassers.",
 1525:"Temperatur am Wärmeerzeuger selbst (interner Vorlauf der Wärmepumpe).",
 1478:"Gewählte Betriebsart des Heizkreises (Automatik, Komfort, Eco, Aus …).",
 1501:"Aktueller Zustand des Heizkreises (Heizen, Kühlen, Aus …).",
 1510:"Aktuell gemessene Raumtemperatur des Heizkreises.",
 1493:"Aktuell gültiger Soll-Wert der Raumtemperatur (ergibt sich aus der Betriebsart).",
 1513:"Vorlauf: Temperatur des warmen Wassers, das in die Fußbodenheizung fließt.",
 1535:"Rücklauf: Temperatur des aus der Fußbodenheizung zurückkommenden Wassers.",
 1520:"Soll-Vorlauftemperatur des Heizkreises (aus der Heizkurve berechnet).",
 1524:"Soll-Vorlauftemperatur im Kühlbetrieb (träge Fußbodenkühlung).",
 19658:"Mischventil-Stellung Heizkreis 1 (Hoval: Mischer HC1) — mischt Vor- und Rücklauf auf die Soll-Vorlauftemperatur. Welcher Stock/Raum das ist, ordnest du selbst zu (Datei labels.json).",
 19659:"Mischventil-Stellung Heizkreis 2 (Hoval: Mischer HC2) — mischt Vor- und Rücklauf auf die Soll-Vorlauftemperatur.",
 1496:"Gewählte Betriebsart der Warmwasserbereitung (Automatik, Normal, Eco, Aus).",
 1500:"Aktuelle Temperatur im Warmwasserspeicher (oberer Fühler).",
 27483:"Warmwassertemperatur am zweiten/unteren Speicherfühler.",
 1499:"Aktuell gültige Soll-Warmwassertemperatur.",
 1497:"Solltemperatur Warmwasser im Normalbetrieb. Über Loxone einstellbar (schreibbar).",
 1498:"Solltemperatur Warmwasser im Eco-/Sparbetrieb.",
 1504:"Aktueller Zustand der Warmwasserbereitung (Laden, bereit, Aus …).",
 23622:"Gewählte Betriebsart der Wohnraumlüftung.",
 23625:"Aktuelle Lüfterleistung in Prozent.",
 23623:"Soll-Lüfterstufe im Normalbetrieb.",
 23624:"Soll-Lüfterstufe im Eco-/Sparbetrieb.",
 23626:"Soll-Luftfeuchte – darüber erhöht die Lüftung ggf. die Stufe.",
 23631:"Aktueller Regelzustand der Lüftung.",
 23632:"Temperatur der angesaugten Frischluft von draußen.",
 23629:"Luftqualität (flüchtige organische Stoffe, VOC) der Außenluft.",
 23633:"Temperatur der aus den Räumen abgesaugten Luft.",
 23627:"Luftfeuchte der Raumabluft – Basis für die Feuchteregelung.",
 23628:"Luftqualität der Raumabluft (Geruch/Schadstoffe, VOC).",
 28940:"CO₂-Gehalt der Raumluft – Indikator für verbrauchte Luft.",
 23634:"Leistung des Fortluftventilators (Ausstoß der verbrauchten Luft nach draußen).",
}

# Übersetzung der Bezeichnungen (Bereiche, Unterüberschriften, Wertnamen) für die Werte-Seite
TR_LABEL = {
 "Wärmepumpe":"Heat pump","Heizung & Kühlung":"Heating & Cooling","Warmwasser":"Hot water","Wohnraumlüftung":"Ventilation",
 "Betrieb & Stufen":"Operation & levels",
 "🌳 Außenluft — Frischluft von draußen (rein)":"🌳 Outdoor air — fresh air from outside (in)",
 "➡️ Zuluft — in die Räume":"➡️ Supply air — into the rooms",
 "🏠 Abluft — Raumluft aus den Räumen (raus)":"🏠 Extract air — room air from the rooms (out)",
 "🌬️ Fortluft — Ausstoß nach draußen":"🌬️ Exhaust air — expelled outside",
 "Außentemperatur":"Outdoor temperature","Betriebsstatus":"Operating status","Modulation Verdichter":"Compressor modulation",
 "Elektrische Leistung":"Electrical power","Heizleistung":"Heating power","Effizienz (Arbeitszahl)":"Efficiency (COP)",
 "Wasserdruck":"Water pressure","Rücklauf Wärmeerzeuger":"Return (heat generator)","WEZ-Temperatur":"Heat generator temp.",
 "Betriebsart":"Operating mode","Status Heizkreis":"Heating circuit status","Raumtemperatur Ist":"Room temperature (actual)",
 "Raum-Sollwert":"Room setpoint","Vorlauf-Temperatur":"Flow temperature","Rücklauf-Temperatur":"Return temperature",
 "Sollwert Heizkreis":"Heating circuit setpoint","Sollwert Kühlmodus":"Cooling setpoint",
 "Mischer HK1":"Mixer HC1","Mischer HK2":"Mixer HC2",
 "Warmwasser Ist":"Hot water (actual)","Warmwasser Ist (Fühler 2)":"Hot water (sensor 2)","Warmwasser Sollwert":"Hot water setpoint",
 "Normal-Temperatur":"Normal temperature","Eco-Temperatur":"Eco temperature","Status Warmwasser":"Hot water status",
 "Betriebswahl":"Operation selection","Lüftung aktuell (Ist)":"Ventilation actual","Normalstufe (Soll)":"Normal level (set)",
 "Eco-Stufe (Soll)":"Eco level (set)","Feuchte-Sollwert":"Humidity setpoint","Status Regelung":"Control status",
 "Außenluft-Temperatur":"Outdoor air temperature","VOC Außenluft":"VOC outdoor air","Abluft-Temperatur":"Extract air temperature",
 "Feuchte Abluft":"Extract air humidity","VOC Abluft":"VOC extract air","CO₂ Abluft":"CO₂ extract air",
 "Lüfter (Abluft → Fortluft)":"Fan (extract → exhaust)",
 "Zuluft-Temperatur und -Feuchte stellt Hoval nicht über Modbus bereit (die HomeVent regelt das intern über die Wärmerückgewinnung).":
   "Hoval does not expose supply-air temperature and humidity over Modbus (the HomeVent regulates this internally via heat recovery).",
}
def tl(s):
    return L(s, TR_LABEL.get(s))

def desc(reg, name="", unit="", writable=None):
    d = DESC.get(reg)
    if d: return d
    parts = []
    if name: parts.append(f"{name}.")
    parts.append(f"Hoval-Datenpunkt, Modbus-Register {reg}")
    if unit: parts.append(f"Einheit: {unit}")
    if writable in (True, 1, "Yes", "yes", "Y", "y", "true", "True", "WAHR"):
        parts.append("über Loxone schreibbar")
    return " · ".join(parts)

def regmap():
    try: return {r["reg"]: r for r in json.load(open(REG_PATH, encoding="utf-8"))}
    except Exception: return {}

WHITELIST_PATH = "/home/admin/hoval-bridge/whitelist.json"
def load_whitelist():
    try:
        return set(int(x) for x in json.load(open(WHITELIST_PATH, encoding="utf-8")).get("allowed", []))
    except Exception:
        return set()
def save_whitelist(s):
    import tempfile, os as _os
    data = {"allowed": sorted(int(x) for x in s),
            "hinweis": "Schreib-Whitelist der HoxPi-Bridge. Wird ueber das Dashboard (Seite Register) verwaltet. Aenderungen wirken ohne Neustart.",
            "geaendert": datetime.datetime.now().isoformat(timespec="seconds")}
    fd, tmp = tempfile.mkstemp(dir=_os.path.dirname(WHITELIST_PATH))
    with _os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    _os.replace(tmp, WHITELIST_PATH)

REG_TEXTS_PATH = "/home/admin/hoval-bridge/reg_texts.json"
_rtc = {"v": None}
def reg_texts():
    if _rtc["v"] is None:
        try: _rtc["v"] = json.load(open(REG_TEXTS_PATH, encoding="utf-8"))
        except Exception: _rtc["v"] = {}
    return _rtc["v"]
def rt_name(reg, fallback=""):
    t = reg_texts().get(str(reg), {})
    n = (t.get("ne") if curlang() == "en" else t.get("nd")) or t.get("nd")
    return n or fallback
def rt_desc(reg):
    t = reg_texts().get(str(reg), {})
    if curlang() == "en":
        return t.get("ed") or t.get("dd") or ""
    return t.get("dd") or ""

def net_info():
    import subprocess
    try:
        con = subprocess.run(["nmcli","-t","-f","NAME,DEVICE","con","show","--active"],
                             capture_output=True, text=True, timeout=6).stdout
        name = next((l.rsplit(":",1)[0] for l in con.splitlines() if l.endswith(":eth0")), None)
        if not name: return None
        g = subprocess.run(["nmcli","-g","ipv4.method,ipv4.addresses,ipv4.gateway,ipv4.dns","con","show",name],
                           capture_output=True, text=True, timeout=6).stdout.splitlines()
        cur = subprocess.run(["ip","-4","-br","addr","show","eth0"], capture_output=True, text=True, timeout=6).stdout.split()
        return {"con": name, "method": (g[0] if len(g) > 0 else ""), "addr": (g[1] if len(g) > 1 else ""),
                "gw": (g[2] if len(g) > 2 else ""), "dns": (g[3] if len(g) > 3 else ""),
                "live": (cur[2] if len(cur) > 2 else "?")}
    except Exception:
        return None

# ---------- 2FA (TOTP) für Schreibaktionen ----------
AUTH_PATH = "/home/admin/hoval-bridge/auth.json"
SESSIONS = {}          # token -> ablauf (unix)
_auth_pending = {}     # {"secret": ...} während des Setups
_auth_tries = []       # timestamps fehlgeschlagener Versuche (Rate-Limit)

def auth_secret():
    try:
        return json.load(open(AUTH_PATH, encoding="utf-8")).get("secret")
    except Exception:
        return None

def auth_enabled():
    return auth_secret() is not None

def _totp(secret_b32, t=None, step=30, digits=6):
    import hmac, hashlib, struct, base64
    key = base64.b32decode(secret_b32)
    counter = int((_time.time() if t is None else t) // step)
    h = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    o = h[19] & 0xF
    code = (struct.unpack(">I", h[o:o + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)

def totp_ok(secret, code):
    code = (code or "").strip().replace(" ", "")
    now = _time.time()
    return any(_totp(secret, now + d * 30) == code for d in (-1, 0, 1))

def auth_rate_ok():
    now = _time.time()
    _auth_tries[:] = [t for t in _auth_tries if now - t < 300]
    return len(_auth_tries) < 8

def new_session():
    import secrets as _secrets
    tok = _secrets.token_hex(16)
    SESSIONS[tok] = _time.time() + 30 * 86400
    return tok

def gen_secret():
    import secrets as _secrets, base64
    return base64.b32encode(_secrets.token_bytes(20)).decode()

def qr_svg(uri):
    try:
        import qrcode, qrcode.image.svg, io
        img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgPathImage, box_size=5)
        b = io.BytesIO(); img.save(b)
        s = b.getvalue().decode()
        s = s[s.find("<svg"):]
        import re as _re
        s = _re.sub(r'width="[^"]*"', 'width="230"', s, count=1)
        s = _re.sub(r'height="[^"]*"', 'height="230"', s, count=1)
        return s
    except Exception:
        return ""

# ---------- 1-Klick-Setup fuer Claude Desktop ----------
def claude_setup_ps1(host):
    return """$ErrorActionPreference = 'Stop'
Write-Host '=== HoxPi -> Claude Desktop Einrichtung ==='
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  Write-Host 'Node.js fehlt! Die Download-Seite wird geoeffnet - installieren, dann Setup erneut ausfuehren.'
  Start-Process 'https://nodejs.org/'
  exit 1
}
Write-Host 'Beende Claude (falls offen) ...'
Get-Process claude -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 5
# Ziel-Configs: klassisch + Microsoft-Store (MSIX-virtualisiert), beide bedienen
$targets = @()
$classic = Join-Path $env:APPDATA 'Claude'
if (Test-Path $classic) { $targets += (Join-Path $classic 'claude_desktop_config.json') }
$pkg = Get-ChildItem (Join-Path $env:LOCALAPPDATA 'Packages') -Directory -Filter 'Claude_*' -ErrorAction SilentlyContinue | Select-Object -First 1
if ($pkg) {
  $vdir = Join-Path $pkg.FullName 'LocalCache\\Roaming\\Claude'
  New-Item -ItemType Directory -Force -Path $vdir | Out-Null
  $targets += (Join-Path $vdir 'claude_desktop_config.json')
}
if ($targets.Count -eq 0) { $targets = @(Join-Path $classic 'claude_desktop_config.json') }
foreach ($p in $targets) {
  Write-Host ('Konfiguration: ' + $p)
  if (Test-Path $p) { $cfg = Get-Content $p -Raw | ConvertFrom-Json; Copy-Item $p ($p + '.bak') -Force }
  else { $cfg = [PSCustomObject]@{} }
  if (-not $cfg.PSObject.Properties['mcpServers']) {
    $cfg | Add-Member -MemberType NoteProperty -Name mcpServers -Value ([PSCustomObject]@{})
  }
  $hox = [PSCustomObject]@{ command = 'npx'; args = @('-y','mcp-remote','http://HOSTIP:8808/mcp','--allow-http') }
  if ($cfg.mcpServers.PSObject.Properties['hoxpi']) { $cfg.mcpServers.hoxpi = $hox }
  else { $cfg.mcpServers | Add-Member -MemberType NoteProperty -Name hoxpi -Value $hox }
  $json = $cfg | ConvertTo-Json -Depth 10
  try { Set-Content -Path $p -Value $json -Encoding UTF8 }
  catch { Start-Sleep 3; Set-Content -Path $p -Value $json -Encoding UTF8 }
}
Write-Host 'HoxPi eingetragen. Claude wird gestartet...'
$gestartet = $false
if ($pkg) {
  $app = Get-StartApps | Where-Object { $_.AppID -like ($pkg.Name + '*') } | Select-Object -First 1
  if ($app) { Start-Process ('shell:AppsFolder\\' + $app.AppID); $gestartet = $true }
}
if (-not $gestartet) {
  $exe = Join-Path $env:LOCALAPPDATA 'AnthropicClaude\\claude.exe'
  if (Test-Path $exe) { Start-Process $exe; $gestartet = $true }
}
if (-not $gestartet) { Write-Host 'Bitte Claude manuell starten.' }
Write-Host 'FERTIG! In Claude einfach fragen: Wie geht es meiner Heizung?'
""".replace("HOSTIP", host)

def claude_setup_bat(host):
    lines = ["@echo off",
             "echo === HoxPi: Claude Desktop wird eingerichtet ===",
             "powershell -NoProfile -ExecutionPolicy Bypass -Command \"Invoke-RestMethod http://HOSTIP/hoxpi-claude-setup.ps1 | Invoke-Expression\"".replace("HOSTIP", host),
             "echo.",
             "pause"]
    return "\r\n".join(lines) + "\r\n"

def claude_setup_sh(host):
    return """#!/bin/bash
# HoxPi -> Claude Desktop (macOS). Ausfuehren: bash hoxpi-claude-setup.sh
command -v node >/dev/null || { echo "Node.js fehlt: https://nodejs.org"; exit 1; }
osascript -e 'quit app "Claude"' 2>/dev/null; sleep 2
python3 - << 'EOF'
import json, os, shutil
p = os.path.expanduser('~/Library/Application Support/Claude/claude_desktop_config.json')
cfg = {}
if os.path.exists(p):
    shutil.copy(p, p + '.bak')
    cfg = json.load(open(p))
cfg.setdefault('mcpServers', {})['hoxpi'] = {
    "command": "npx", "args": ["-y", "mcp-remote", "http://HOSTIP:8808/mcp", "--allow-http"]}
json.dump(cfg, open(p, 'w'), indent=2)
print('HoxPi eingetragen.')
EOF
open -a Claude 2>/dev/null || echo "Bitte Claude manuell starten."
echo "FERTIG! In Claude einfach fragen: Wie geht es meiner Heizung?"
""".replace("HOSTIP", host)

# Eigene Zuordnung pro Anlage: labels.json = {"19659":"Untergeschoss", ...}
LABELS_PATH = "/home/admin/hoval-bridge/labels.json"
_lblc = {"t": 0, "v": {}}
def get_labels():
    now = _time.time()
    if now - _lblc["t"] < 15: return _lblc["v"]
    try: v = {str(k): val for k, val in json.load(open(LABELS_PATH, encoding="utf-8")).items()}
    except Exception: v = {}
    _lblc["t"] = now; _lblc["v"] = v; return v

def read_modbus(regs):
    out = {r: None for r in regs}
    try:
        from pymodbus.client import ModbusTcpClient
        c = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
        if not c.connect(): return out, False
        for reg in regs:
            rr = c.read_holding_registers(reg, count=1, slave=1)
            if not rr.isError(): out[reg] = rr.registers[0]
        c.close(); return out, True
    except Exception:
        return out, False

_allcache = {"t": 0, "v": {}}
def read_all(regs):
    now = _time.time()
    if now - _allcache["t"] < 8 and _allcache["v"]: return _allcache["v"]
    vals = {}
    try:
        from pymodbus.client import ModbusTcpClient
        c = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=4)
        if c.connect():
            for reg in regs:
                rr = c.read_holding_registers(reg, count=1, slave=1)
                if not rr.isError(): vals[reg] = rr.registers[0]
            c.close()
    except Exception: pass
    if vals: _allcache["t"] = now; _allcache["v"] = vals
    return vals

def fmt(raw, unit, dec, signed):
    if raw is None: return "—", "muted"
    if unit == "ST_HC":  return ST_HC.get(raw, f"Code {raw}"), ("bad" if raw == 12 else "ok")
    if unit == "ST_DHW": return ST_DHW.get(raw, f"Code {raw}"), ("bad" if raw == 5 else "ok")
    if unit == "ST_HP":  return ST_HP.get(raw, f"Code {raw}"), "ok"
    if raw in (0xFFFF, 0x8000): return "—", "muted"
    if (not signed) and dec == 0 and raw == 0xFF: return "—", "muted"
    v = raw - 65536 if (signed and raw > 32767) else raw
    if dec: v = v / (10 ** dec)
    if v in (3276.7, -3276.8, 6553.5): return "—", "muted"
    s = f"{v:.{dec}f}".replace(".", ",") if dec else f"{v}"
    return f"{s} {unit}".strip(), "val"

def decode_reg(r, raw):
    if raw is None: return "—", True
    t = (r.get("type") or "").upper(); dec = r.get("decimal") or 0
    if t in ("U32", "S32"): return "—", True
    if raw in (0xFFFF, 0x8000): return "—", True
    if t in ("U8", "S8"): raw &= 0xFF
    if t == "U8" and dec == 0 and raw == 0xFF: return "—", True
    v = raw
    if t == "S16" and raw > 32767: v = raw - 65536
    elif t == "S8" and raw > 127: v = raw - 256
    if dec: v = v / (10 ** dec)
    if v in (3276.7, -3276.8, 6553.5): return "—", True
    s = (f"{v:.{dec}f}".replace(".", ",") if dec else f"{v}")
    return f"{s} {r.get('unit') or ''}".strip(), False

HA_UNITS = {"°C","%","bar","kW","kWh","Wh","W","V","A","Hz","h","min","l/h","m³/h","rpm","ppm","K","%RH"}

def ha_yaml(host="192.168.1.168"):
    m = regmap()
    L = ["# HoxPi -> Home Assistant (Modbus TCP) - automatisch erzeugt",
         "# Einbau: Datei nach  <config>/packages/hoxpi.yaml  kopieren.",
         "# In configuration.yaml muss stehen:",
         "#   homeassistant:",
         "#     packages: !include_dir_named packages",
         "# Danach Home Assistant neu starten - alle Sensoren erscheinen automatisch.",
         "modbus:",
         "  - name: hoxpi",
         "    type: tcp",
         f"    host: {host}",
         "    port: 502",
         "    delay: 2",
         "    message_wait_milliseconds: 30",
         "    timeout: 5",
         "    sensors:"]
    for reg in sorted(m):
        r = m[reg]
        t = (r.get("type") or "").upper()
        if t in ("U32", "S32", ""):  # nur sauber unterstuetzte 16-bit-Register
            continue
        dec = int(r.get("decimal") or 0)
        dtype = "int16" if t in ("S8", "S16") else "uint16"
        scale = {0:"1",1:"0.1",2:"0.01",3:"0.001"}.get(dec, str(10 ** (-dec)))
        name = (r.get("name") or f"Register {reg}").replace('"', "'").strip()
        unit = (r.get("unit") or "").strip()
        L += [f'      - name: "HoxPi {name}"',
              f"        unique_id: hoxpi_{reg}",
              f"        slave: 1",
              f"        address: {reg}",
              f"        input_type: holding",
              f"        data_type: {dtype}",
              f"        scale: {scale}",
              f"        precision: {dec}"]
        if unit in HA_UNITS:
            L.append(f'        unit_of_measurement: "{unit}"')
        L.append(f"        scan_interval: 30")
    return "\n".join(L) + "\n"

CSS = f"""
*{{box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;margin:0;background:#eceff3;color:#222b36}}
header{{background:#fff;border-bottom:3px solid {HOVAL_RED};padding:.7rem 1.3rem;
 display:flex;align-items:center;gap:1.3rem;flex-wrap:wrap;position:sticky;top:0;z-index:9;
 box-shadow:0 1px 6px rgba(0,0,0,.06)}}
.logo{{display:inline-flex;flex-direction:column;line-height:1.05}}
.logo .word{{font-weight:800;font-size:1.28rem;color:#1c2531;letter-spacing:.3px}}
.logo .xg{{color:#69b41e}}
.logo .bar{{display:flex;gap:3px;margin-top:4px}}
.logo .bar i{{height:4px;width:19px;border-radius:2px}}
.logo .bar i:nth-child(1){{background:#e2001a}}
.logo .bar i:nth-child(2){{background:#c2185b}}
.logo .bar i:nth-child(3){{background:#69b41e}}
.brand{{color:#6c7787;font-weight:500;font-size:.9rem}}
nav{{display:flex;gap:.3rem;flex-wrap:wrap}}
nav a{{color:#5a6675;text-decoration:none;padding:.4rem .8rem;border-radius:7px;font-size:.93rem;font-weight:500}}
nav a:hover{{background:#f3f4f7;color:{HOVAL_RED}}}
nav a.act{{background:{HOVAL_RED};color:#fff}}
main{{max-width:1040px;margin:0 auto;padding:1.3rem}}
h1{{font-size:1.5rem;margin:.3rem 0 1.1rem;color:#1c2531}}
.domain{{background:#fff;border-radius:15px;box-shadow:0 2px 10px rgba(20,30,50,.07);
 margin:1.3rem 0;border:1px solid #e6e9ef}}
.dh{{display:flex;align-items:center;gap:.7rem;padding:.9rem 1.2rem;border-radius:15px 15px 0 0;
 background:linear-gradient(90deg,{HOVAL_RED},#ff4d34);color:#fff}}
.dh .ic{{font-size:1.5rem;filter:saturate(0) brightness(5)}}
.dh h2{{margin:0;font-size:1.2rem;font-weight:700}}
.dbody{{padding:1rem 1.2rem 1.2rem}}
.sub{{font-size:.9rem;color:#8893a2;font-weight:700;text-transform:uppercase;letter-spacing:.4px;
 margin:1.1rem 0 .5rem;border-left:3px solid #c2185b;padding-left:.5rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:.6rem}}
.card{{background:#f7f9fc;border:1px solid #e6ebf1;border-radius:11px;padding:.65rem .85rem;position:relative;cursor:help}}
.tt{{position:absolute;left:0;top:calc(100% + 6px);z-index:50;display:none;width:235px;
 background:#1c2531;color:#fff;font-size:.78rem;font-weight:400;line-height:1.45;
 padding:.5rem .65rem;border-radius:8px;box-shadow:0 8px 24px rgba(20,30,50,.28);
 text-transform:none;letter-spacing:normal;white-space:normal}}
.tt::before{{content:"";position:absolute;left:18px;top:-5px;width:9px;height:9px;
 background:#1c2531;transform:rotate(45deg)}}
.card:hover .tt{{display:block}}
.card .n{{font-size:.8rem;color:#6c7787}}
.card .v{{font-size:1.32rem;font-weight:650;margin-top:.15rem;color:#1c2531}}
.val{{color:#1c2531}}.ok{{color:#0a8f4f}}.bad{{color:#d6202f}}.muted{{color:#aab2bd}}
.note-card{{grid-column:1/-1;background:#fff7e6;border:1px solid #f0d9a8;border-radius:11px;
 padding:.7rem .9rem;color:#8a6d2e;font-size:.9rem}}
table{{border-collapse:collapse;width:100%;font-size:.9rem;margin-top:.4rem;background:#fff;border-radius:10px;overflow:hidden}}
th,td{{border-bottom:1px solid #eceff3;padding:.45rem .6rem;text-align:left}}
th{{color:#7a8694;font-weight:600;background:#f7f9fc}}
td code{{color:#c2185b;font-weight:600}}
.pill{{display:inline-block;background:#f3f4f7;border:1px solid #e1e5ec;border-radius:6px;padding:.1rem .5rem;font-size:.8rem;color:#5a6675}}
.note{{background:#eef6ff;border:1px solid #cfe2f7;border-radius:11px;padding:.8rem 1.1rem;color:#2b5378;font-size:.92rem}}
.note.warn{{background:#fff3e6;border-color:#f3cf9e;color:#8a5a1e}}
.note.ok{{background:#eafaf1;border-color:#bce7cd;color:#1c6b3f}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.7rem;margin:.7rem 0}}
p{{line-height:1.6;color:#3a4554}} ul{{line-height:1.7;color:#3a4554}}
h2.sec{{font-size:1.15rem;color:{HOVAL_RED};margin:1.6rem 0 .5rem}}
footer{{color:#9aa3af;font-size:.8rem;text-align:center;padding:1.6rem}}
svg{{width:100%;max-width:920px;display:block;margin:.4rem auto}}
.ze{{display:inline-block;background:#eef2ff;color:#3a4ea8;border:1px solid #d4ddf7;border-radius:5px;
 padding:.02rem .35rem;font-size:.72rem;margin-left:.35rem;vertical-align:middle}}
.langsw{{display:flex;gap:.4rem;align-items:center;margin-left:auto}}
.langsw a{{display:inline-flex;border:2px solid transparent;border-radius:5px;overflow:hidden;
 opacity:.5;line-height:0;box-shadow:0 1px 3px rgba(0,0,0,.18)}}
.langsw a.on{{opacity:1;border-color:#1c2531}}
.langsw svg{{display:block;margin:0;width:34px;height:22px}}
"""

FLAG_DE = ('<svg viewBox="0 0 36 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
 '<rect x="0" y="0" width="18" height="8" fill="#000"/><rect x="0" y="8" width="18" height="8" fill="#dd0000"/>'
 '<rect x="0" y="16" width="18" height="8" fill="#ffce00"/>'
 '<rect x="18" y="0" width="18" height="8" fill="#ed2939"/><rect x="18" y="8" width="18" height="8" fill="#fff"/>'
 '<rect x="18" y="16" width="18" height="8" fill="#ed2939"/></svg>')
FLAG_EN = ('<svg viewBox="0 0 36 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
 '<rect x="0" y="0" width="18" height="24" fill="#012169"/>'
 '<path d="M0,0 L18,24 M18,0 L0,24" stroke="#fff" stroke-width="4"/>'
 '<path d="M0,0 L18,24 M18,0 L0,24" stroke="#c8102e" stroke-width="1.6"/>'
 '<rect x="6.5" y="0" width="5" height="24" fill="#fff"/><rect x="0" y="9.5" width="18" height="5" fill="#fff"/>'
 '<rect x="7.7" y="0" width="2.6" height="24" fill="#c8102e"/><rect x="0" y="10.7" width="18" height="2.6" fill="#c8102e"/>'
 '<rect x="18" y="0" width="18" height="24" fill="#fff"/>'
 '<rect x="18" y="0" width="18" height="4" fill="#b22234"/><rect x="18" y="8" width="18" height="4" fill="#b22234"/>'
 '<rect x="18" y="16" width="18" height="4" fill="#b22234"/>'
 '<rect x="18" y="0" width="9" height="11" fill="#3c3b6e"/>'
 '<circle cx="20" cy="2.3" r="0.7" fill="#fff"/><circle cx="23" cy="2.3" r="0.7" fill="#fff"/><circle cx="25.8" cy="2.3" r="0.7" fill="#fff"/>'
 '<circle cx="21.5" cy="5" r="0.7" fill="#fff"/><circle cx="24.3" cy="5" r="0.7" fill="#fff"/>'
 '<circle cx="20" cy="7.7" r="0.7" fill="#fff"/><circle cx="23" cy="7.7" r="0.7" fill="#fff"/><circle cx="25.8" cy="7.7" r="0.7" fill="#fff"/></svg>')

def page(title, active, body, refresh=False, path="/"):
    rf = '<meta http-equiv=refresh content=10>' if refresh else ''
    lg = curlang()
    nav = "".join(f'<a class="{ "act" if active==k else "" }" href="{u}">{t}</a>'
                  for k,u,t in [("home","/",L("Start","Home")),("werte","/werte","Live"),
                                ("alle","/alle",L("Alle Werte","All values")),
                                ("register","/register",L("Register","Registers")),
                                ("integration","/integration","Integration"),
                                ("sicherheit","/sicherheit",L("Sicherheit","Security")),
                                ])
    sw = (f'<div class="langsw">'
          f'<a class="{"on" if lg=="de" else ""}" href="{path}?lang=de" title="Deutsch">{FLAG_DE}</a>'
          f'<a class="{"on" if lg=="en" else ""}" href="{path}?lang=en" title="English">{FLAG_EN}</a></div>')
    return f"""<!doctype html><html lang={lg}><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">{rf}
<title>HoxPi · {title}</title><style>{CSS}</style></head><body>
<header><span class="logo"><svg height="44" viewBox="0 0 150 54" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="HoxPi"><polyline points="44,22 70,7 96,22" fill="none" stroke="#41bdf5" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text text-anchor="end" x="95" y="44" font-size="21" font-weight="700" font-family="system-ui,-apple-system,Segoe UI,Roboto,sans-serif"><tspan fill="#e2001a">H</tspan><tspan fill="#1c2531">o</tspan><tspan fill="#69b41e">x</tspan><tspan fill="#c2185b">P</tspan></text><rect x="97.2" y="33" width="2.5" height="10.5" rx="1.25" fill="#c2185b"/><path d="M98.7,25 C98.2,22 99.4,19.5 101.6,18.6 C100.2,20.6 99.8,22.8 98.7,25 z" fill="#4ea51f"/><line x1="98.8" y1="24.6" x2="101.4" y2="18.9" stroke="#2f6e12" stroke-width="0.4"/><circle cx="98.45" cy="25.7" r="1.2" fill="#e8463f"/><circle cx="100.45" cy="26.85" r="1.2" fill="#d8201c"/><circle cx="96.45" cy="26.85" r="1.2" fill="#d8201c"/><circle cx="98.45" cy="28.0" r="1.2" fill="#d8201c"/><circle cx="100.45" cy="29.15" r="1.2" fill="#b81818"/><circle cx="96.45" cy="29.15" r="1.2" fill="#b81818"/><circle cx="98.45" cy="30.3" r="1.1" fill="#a01414"/><circle cx="98.0" cy="25.4" r="0.4" fill="#ffd9d4"/><circle cx="98.0" cy="27.6" r="0.4" fill="#ffd9d4"/><rect x="44" y="48" width="18" height="3.5" rx="1.75" fill="#e2001a"/><rect x="64" y="48" width="18" height="3.5" rx="1.75" fill="#c2185b"/><rect x="84" y="48" width="18" height="3.5" rx="1.75" fill="#69b41e"/></svg></span><span class="brand">{L("für","for")} Hoval® TopTronic® E</span><nav>{nav}</nav>{sw}</header>
<main>{body}</main>
<footer>{L("HoxPi · offenes Gateway für Hoval® TopTronic® E · unabhängiges Open-Source-Projekt, nicht mit der Hoval AG verbunden","HoxPi · open gateway for Hoval® TopTronic® E · independent open-source project, not affiliated with Hoval AG")} · <a href="https://buymeacoffee.com/bernhardsu9" target="_blank" style="color:#8a94a5">☕ {L("Projekt unterstützen","Support the project")}</a> · {datetime.datetime.now():%d.%m.%Y %H:%M}</footer>
</body></html>"""

def schema():
    return f"""
<svg viewBox="0 0 920 210" xmlns="http://www.w3.org/2000/svg">
 <defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
   <path d="M0,0 L7,3 L0,6 Z" fill="{HOVAL_RED}"/></marker></defs>
 <style>.bx{{fill:#fff;stroke:#e0a6ac;stroke-width:1.5}} .ti{{fill:#1c2531;font:600 14px Segoe UI,sans-serif}}
  .su{{fill:#6c7787;font:11px Segoe UI,sans-serif}} .lb{{fill:{HOVAL_RED};font:600 11px Segoe UI,sans-serif}}
  line{{stroke:{HOVAL_RED};stroke-width:2;marker-end:url(#ar)}}</style>
 <rect class="bx" x="12" y="55" width="150" height="100" rx="11" stroke="#e2001a" stroke-width="2"/>
 <text class="ti" x="30" y="92">{L("Wärmepumpe","Heat pump")}</text><text class="su" x="30" y="112">{L("+ Wohnraum-","+ ventil-")}</text>
 <text class="su" x="30" y="128">{L("lüftung","ation")}</text><text class="su" x="30" y="146">(TopTronic E)</text>
 <line x1="162" y1="105" x2="240" y2="105"/><text class="lb" x="170" y="96">CAN 50k</text>
 <rect class="bx" x="243" y="62" width="132" height="86" rx="11"/>
 <text class="ti" x="258" y="98">USB-CAN</text><text class="su" x="258" y="118">SH-C30G</text>
 <line x1="375" y1="105" x2="425" y2="105"/>
 <rect class="bx" x="428" y="52" width="178" height="106" rx="11" stroke="#c2185b" stroke-width="2"/>
 <text class="ti" x="445" y="86">Raspberry Pi</text><text class="su" x="445" y="106">{L("HoxPi-Brücke","HoxPi bridge")}</text>
 <text class="su" x="445" y="124">{L("CAN → Register","CAN → registers")}</text>
 <line x1="606" y1="105" x2="660" y2="105" style="marker-end:none"/><text class="lb" x="600" y="98">Modbus :502</text>
 <line x1="660" y1="105" x2="690" y2="74"/>
 <line x1="660" y1="105" x2="690" y2="160"/>
 <rect class="bx" x="693" y="44" width="170" height="60" rx="11" stroke="#69b41e" stroke-width="2"/>
 <text class="ti" x="710" y="72">Loxone</text><text class="su" x="710" y="90">Miniserver</text>
 <rect class="bx" x="693" y="130" width="170" height="60" rx="11" stroke="#41bdf5" stroke-width="2"/>
 <text class="ti" x="710" y="158">Home Assistant</text><text class="su" x="710" y="176">{L("Modbus-Integration","Modbus integration")}</text>
</svg>"""

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_GET(self):
        pr = urlparse(self.path); p = pr.path; q = parse_qs(pr.query)
        setcookie = False
        if "lang" in q:
            lang = "en" if q["lang"][0] == "en" else "de"; setcookie = True
        elif "lang=en" in self.headers.get("Cookie", ""):
            lang = "en"
        else:
            lang = "de"
        _ctx.lang = lang
        if p in ("/hoxpi-claude-setup.bat", "/hoxpi-claude-setup.ps1", "/hoxpi-claude-setup.sh"):
            host = (self.headers.get("Host") or "192.168.1.168").split(":")[0]
            if p.endswith(".bat"):
                data = claude_setup_bat(host).encode("utf-8")
            elif p.endswith(".sh"):
                data = claude_setup_sh(host).encode("utf-8")
            else:
                data = claude_setup_ps1(host).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            if not p.endswith(".ps1"):
                self.send_header("Content-Disposition", 'attachment; filename="' + p.strip("/") + '"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data); return
        if p == "/hoxpi-ha.yaml":
            data = ha_yaml().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type","application/x-yaml; charset=utf-8")
            self.send_header("Content-Disposition",'attachment; filename="hoxpi.yaml"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data); return
        if p == "/werte":    body, rf, act = self.werte(), True, "werte"
        elif p == "/alle":   body, rf, act = self.alle(), True, "alle"
        elif p == "/register": body, rf, act = self.register(), False, "register"
        elif p in ("/integration","/loxone","/homeassistant","/anleitung"): body, rf, act = self.integration() + self.stats_section() + self.mcp_section() + self.netz_section() + self.anleitung().replace('<h1>', '<h2 class="sec" style="font-size:1.35rem;margin-top:2.2rem">', 1).replace('</h1>', '</h2>', 1), False, "integration"
        elif p == "/sicherheit": body, rf, act = self.sicherheit(), False, "sicherheit"
        else:                body, rf, act = self.home(), False, "home"
        out = page(act.title(), act, body, rf, path=p).encode("utf-8")
        self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8")
        if setcookie: self.send_header("Set-Cookie", f"lang={lang}; Path=/; Max-Age=31536000")
        self.end_headers(); self.wfile.write(out)

    def do_POST(self):
        pr = urlparse(self.path)
        if pr.path == "/api/auth/setup":
            self.api_auth_setup(); return
        if pr.path == "/api/auth/login":
            self.api_auth_login(); return
        if pr.path == "/api/auth/off":
            self.api_auth_off(); return
        if auth_enabled() and not self.session_ok():
            self.json_out({"ok": False, "fehler": "Nicht angemeldet - bitte auf der Seite 'Sicherheit' den 2FA-Code eingeben / Not signed in - enter your 2FA code on the 'Security' page"}, 401)
            return
        if pr.path == "/api/stats":
            self.api_stats(); return
        if pr.path == "/api/network":
            self.api_network(); return
        if pr.path != "/api/whitelist":
            self.send_response(404); self.end_headers(); return
        try:
            ln = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(ln) or b"{}")
            reg = int(body["reg"]); allow = bool(body["allow"])
            r = regmap().get(reg)
            if not r or str(r.get("writable")).lower() != "yes":
                out = {"ok": False, "fehler": "Register laut Hoval-Katalog nicht beschreibbar"}
            else:
                wl = load_whitelist()
                (wl.add(reg) if allow else wl.discard(reg))
                save_whitelist(wl)
                out = {"ok": True, "reg": reg, "allow": allow, "anzahl": len(wl)}
        except Exception as e:
            out = {"ok": False, "fehler": str(e)}
        data = json.dumps(out).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def register(self):
        m = regmap(); wl = load_whitelist()
        vals = read_all(sorted(m.keys()))
        secs = [(L("W\u00e4rmepumpe (WEZ, UnitId 1)","Heat pump (WEZ, UnitId 1)"), 1),
                (L("Wohnrauml\u00fcftung (HV, UnitId 520)","Ventilation (HV, UnitId 520)"), 520),
                (L("Puffermodul (PS, UnitId 143)","Buffer module (PS, UnitId 143)"), 143)]
        out = ['<h1>' + L("Register & Schreibfreigaben","Registers & write permissions") + '</h1>']
        out.append('<div class="note warn"><b>' + L("So funktioniert es:","How it works:") + '</b> ' +
          L("Haken = Loxone/Home Assistant darf dieses Register schreiben (Whitelist). Die Bridge pr\u00fcft zus\u00e4tzlich immer Wertebereich, Rate-Limit und Kalt-Cache-Schutz. \u00c4nderungen wirken sofort \u2013 ohne Neustart. \U0001F512 = laut Hoval-Katalog grunds\u00e4tzlich nur lesbar.",
            "Checked = Loxone/Home Assistant may write this register (whitelist). The bridge always enforces value range, rate limit and cold-cache protection on top. Changes take effect immediately \u2013 no restart. \U0001F512 = read-only per Hoval catalog.") + '</div>')
        out.append('<p>' + L("Suche:","Search:") + ' <input oninput="flt(this.value)" placeholder="Register / Name" style="padding:.4rem .6rem;border:1px solid #dbe1ea;border-radius:8px;width:270px"> ' +
                   '&middot; <label><input type="checkbox" onchange="fltw(this.checked)"> ' + L("nur schreibbare","writable only") + '</label> ' +
                   '&middot; ' + L("freigegeben:","allowed:") + ' <b id="wlcount">' + str(len(wl)) + '</b></p>')
        for title, uid in secs:
            regs = sorted(r for r in m if m[r]["unit_id"] == uid)
            if not regs: continue
            out.append('<div class="domain"><div class="dh"><span class="ic">\U0001F4CB</span><h2>' + html.escape(title) + ' &middot; ' + str(len(regs)) + '</h2></div><div class="dbody">')
            if uid == 143:
                out.append('<div class="note warn">' + L("PS-Service-Register (teils Hardware-Ausg\u00e4nge!) \u2013 nur freigeben, wenn du genau wei\u00dft, was du tust. PS-Modul aktuell abgesteckt.",
                                                          "PS service registers (some are hardware outputs!) \u2013 only allow if you know exactly what you are doing. PS module currently unplugged.") + '</div>')
            out.append('<table><tr><th>Reg</th><th>' + L("Bezeichnung","Name") + '</th><th>' + L("Typ","Type") + '</th><th>' + L("Einheit","Unit") + '</th><th>' + L("Wert (roh)","Value (raw)") + '</th><th>' + L("Katalog","Catalog") + '</th><th>' + L("Schreiben erlaubt","Write allowed") + '</th></tr>')
            for reg in regs:
                r = m[reg]
                wr = str(r.get("writable")).lower() == "yes"
                raw = vals.get(reg)
                rawtxt = "&mdash;" if raw is None else str(raw)
                if wr:
                    cell = '<input type="checkbox" onchange="tgl(this,' + str(reg) + ')"' + (' checked' if reg in wl else '') + '>'
                    kat = '<span class="pill" style="background:#eafaf1;border-color:#bce7cd;color:#1c6b3f">' + L("schreibbar","writable") + '</span>'
                else:
                    cell = '\U0001F512'
                    kat = '<span class="pill">' + L("nur lesen","read-only") + '</span>'
                out.append('<tr class="rr" data-w="' + ('1' if wr else '0') + '"><td><code>' + str(reg) + '</code></td><td title="' + html.escape(rt_desc(reg) or desc(reg, r.get("name") or "", str(r.get("unit") or ""), r.get("writable"))) + '" style="cursor:help">' + html.escape(rt_name(reg, r.get("name") or "")) + '</td><td>' + html.escape(r.get("type") or "") + '</td><td>' + html.escape(str(r.get("unit") or "")) + '</td><td>' + rawtxt + '</td><td>' + kat + '</td><td>' + cell + '</td></tr>')
            out.append('</table></div></div>')
        out.append("""<script>
var only=false;
function flt(v){v=(v||"").toLowerCase();window._q=v;document.querySelectorAll("tr.rr").forEach(function(tr){var ok=tr.textContent.toLowerCase().indexOf(v)>=0&&(!only||tr.dataset.w=="1");tr.style.display=ok?"":"none";});}
function fltw(c){only=c;flt(window._q||"");}
function sortTables(){
 document.querySelectorAll("table th").forEach(function(th){
  th.style.cursor="pointer"; th.title="Klicken zum Sortieren / click to sort";
  th.addEventListener("click",function(){
   var table=th.closest("table");
   var idx=Array.prototype.indexOf.call(th.parentNode.children,th);
   var rows=Array.prototype.slice.call(table.querySelectorAll("tr.rr"));
   var asc=th.dataset.asc!=="1";
   table.querySelectorAll("th").forEach(function(h){delete h.dataset.asc;h.textContent=h.textContent.replace(/ [\u25B2\u25BC]$/,"");});
   th.dataset.asc=asc?"1":"0";
   th.textContent=th.textContent+(asc?" \u25B2":" \u25BC");
   rows.sort(function(a,b){
    var x=a.children[idx].textContent.trim(),y=b.children[idx].textContent.trim();
    var nx=parseFloat(x.replace(",",".")),ny=parseFloat(y.replace(",","."));
    var c=(!isNaN(nx)&&!isNaN(ny))?nx-ny:x.localeCompare(y,"de");
    return asc?c:-c;
   });
   rows.forEach(function(r){table.appendChild(r);});
  });
 });
}
sortTables();
function tgl(cb,reg){
 var allow=cb.checked;
 if(allow&&!confirm("Register "+reg+" wirklich zum Schreiben freigeben?")){cb.checked=false;return;}
 fetch("/api/whitelist",{method:"POST",body:JSON.stringify({reg:reg,allow:allow})}).then(function(r){return r.json();}).then(function(j){
  if(!j.ok){alert("Fehler: "+j.fehler);cb.checked=!allow;}
  else{document.getElementById("wlcount").textContent=j.anzahl;}
 }).catch(function(e){alert("Fehler: "+e);cb.checked=!allow;});
}
</script>""")
        return "".join(out)

    def integration(self):
        return f"""<h1>{L("Integration \u2013 Loxone & Home Assistant","Integration \u2013 Loxone & Home Assistant")}</h1>
<p>{L("HoxPi verh\u00e4lt sich nach au\u00dfen wie ein <b>originaler Hoval-Modbus-TCP-Gateway</b>. Beide Systeme verbinden sich einfach per Modbus-TCP \u2013 nichts muss \u201egepusht\u201c werden, die Register liegen einfach bereit.","HoxPi behaves like an <b>original Hoval Modbus-TCP gateway</b>. Both systems simply connect via Modbus-TCP \u2013 nothing has to be pushed, the registers are just there.")}</p>
<div class="grid3">
 <div class="card"><div class="n">{L("IP-Adresse","IP address")}</div><div class="v" style="font-size:1.05rem">192.168.1.168</div></div>
 <div class="card"><div class="n">Port</div><div class="v" style="font-size:1.05rem">502</div></div>
 <div class="card"><div class="n">{L("Lesen / Schreiben","Read / write")}</div><div class="v" style="font-size:1.05rem">FC 3 / FC 6</div></div>
</div>

<div class="domain"><div class="dh" style="background:#69b41e;background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">\U0001F7E9</span><h2>Loxone</h2></div><div class="dbody">
<p>{L("In <b>Loxone Config</b> ein <b>Modbus-TCP-Ger\u00e4t</b> anlegen (IP/Port oben), dann die fertigen Hoval-<b>Templates</b> aus der Loxone Library laden \u2013 sie erwarten genau diesen Gateway und passen 1:1. Werte sind <b>Rohwerte</b> (z.\u2009B. \u00b0C \u00d710), die Templates skalieren selbst.","Create a <b>Modbus TCP device</b> in <b>Loxone Config</b> (IP/port above), then load the ready-made Hoval <b>templates</b> from the Loxone Library \u2013 they expect exactly this gateway and fit 1:1. Values are <b>raw</b> (e.g. \u00b0C \u00d710); the templates scale themselves.")}</p>
<table><tr><th>{L("Anlagenteil","System part")}</th><th>Template</th><th>{L("wann","when")}</th></tr>
<tr><td>{L("W\u00e4rmepumpe (Heizen, K\u00fchlen, WW)","Heat pump (heating, cooling, DHW)")}</td>
<td><a href="https://library.loxone.com/detail/template-hoval-at-769/overview" target="_blank">Hoval Heating &amp; Cooling</a></td>
<td><b>{L("immer","always")}</b></td></tr>
<tr><td>{L("Wohnrauml\u00fcftung (HomeVent)","Ventilation (HomeVent)")}</td>
<td><a href="https://library.loxone.com/detail/hoval-template-884/overview" target="_blank">Hoval Ventilation</a></td>
<td>{L("wenn L\u00fcftung in Loxone soll","if ventilation should be in Loxone")}</td></tr>
<tr><td>{L("Energiemanagement / SG-Ready","Energy management / SG-Ready")}</td>
<td><a href="https://library.loxone.com/detail/hoval-energy-management-1845/overview" target="_blank">Hoval Energy Management</a></td>
<td>{L("f\u00fcr PV-\u00dcberschuss-Steuerung","for PV surplus control")}</td></tr></table>
<div class="note" style="margin-top:.8rem">{L("Schreiben (Sollwerte, SG-Offsets) funktioniert nur f\u00fcr Register, die auf der Seite <b>Register</b> freigegeben sind (Haken).","Writing (setpoints, SG offsets) only works for registers allowed on the <b>Registers</b> page (checkbox).")}</div>
</div></div>

<div class="domain"><div class="dh" style="background:#41bdf5;background-image:linear-gradient(90deg,rgba(255,255,255,.18),rgba(255,255,255,0))"><span class="ic">\U0001F3E0</span><h2>Home Assistant</h2></div><div class="dbody">
<p>{L("Fertige Konfiguration herunterladen \u2013 alle Sensoren erscheinen automatisch, bereits richtig skaliert (\u00b0C, %, kW \u2026).","Download the ready-made configuration \u2013 all sensors appear automatically, already scaled (\u00b0C, %, kW \u2026).")}</p>
<div style="text-align:center;margin:1rem 0">
 <a href="/hoxpi-ha.yaml" download style="display:inline-block;background:#41bdf5;color:#08334a;font-weight:700;padding:.7rem 1.4rem;border-radius:11px;text-decoration:none">\u2B07 hoxpi.yaml</a></div>
<ol style="line-height:1.8;color:#3a4554">
<li>{L("Datei nach <code>&lt;config&gt;/packages/hoxpi.yaml</code> kopieren (Ordner ggf. anlegen).","Copy the file to <code>&lt;config&gt;/packages/hoxpi.yaml</code> (create the folder if needed).")}</li>
<li>{L("In <code>configuration.yaml</code> einmalig:","Once in <code>configuration.yaml</code>:")}<pre style="background:#f3f4f7;border:1px solid #e1e5ec;border-radius:8px;padding:.6rem .8rem;font-size:.85rem">homeassistant:
  packages: !include_dir_named packages</pre></li>
<li>{L("Home Assistant neu starten \u2013 alle Werte als <code>sensor.hoxpi_*</code>.","Restart Home Assistant \u2013 all values as <code>sensor.hoxpi_*</code>.")}</li>
</ol>
<div class="note warn">{L("Andere Pi-IP? Dann in der Datei den <code>host:</code> anpassen.","Different Pi IP? Adjust <code>host:</code> in the file.")}</div>
</div></div>

<div class="note ok" style="margin-top:1rem">{L("Alle 514 Register mit deutscher Bezeichnung, Beschreibung und Live-Wert findest du auf der Seite <b>Register</b>.","All 514 registers with name, description and live value are on the <b>Registers</b> page.")}</div>"""

    def api_network(self):
        import subprocess, re as _re, threading as _th
        try:
            ln = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(ln) or b"{}")
            ni = net_info()
            if not ni: raise ValueError("eth0-Verbindung nicht gefunden")
            name = ni["con"]
            ip4 = r"^(\d{1,3}\.){3}\d{1,3}$"
            if body.get("mode") == "auto":
                cmd = ["nmcli","con","mod",name,"ipv4.method","auto","ipv4.addresses","","ipv4.gateway","","ipv4.dns",""]
            else:
                ip, pfx, gw, dns = body.get("ip",""), str(body.get("prefix","24")), body.get("gw",""), body.get("dns","")
                if not _re.match(ip4, ip): raise ValueError("IP-Adresse ungueltig")
                if not pfx.isdigit() or not 8 <= int(pfx) <= 30: raise ValueError("Praefix ungueltig (8-30)")
                if gw and not _re.match(ip4, gw): raise ValueError("Gateway ungueltig")
                if dns and not all(_re.match(ip4, d.strip()) for d in dns.split(",")): raise ValueError("DNS ungueltig")
                cmd = ["nmcli","con","mod",name,"ipv4.method","manual","ipv4.addresses",f"{ip}/{pfx}"]
                if gw: cmd += ["ipv4.gateway", gw]
                if dns: cmd += ["ipv4.dns", dns]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if r.returncode != 0: raise ValueError("nmcli: " + (r.stderr or r.stdout).strip()[:200])
            _th.Timer(2.0, lambda: subprocess.run(["nmcli","con","up",name], capture_output=True, timeout=30)).start()
            out = {"ok": True, "hinweis": "Gespeichert - wird in 2 s angewendet. Bei neuer IP: Dashboard unter der neuen Adresse oeffnen!"}
        except Exception as e:
            out = {"ok": False, "fehler": str(e)}
        data = json.dumps(out).encode()
        self.send_response(200); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def netz_section(self):
        ni = net_info()
        if not ni: return ""
        auto = "auto" in (ni.get("method") or "")
        addr = (ni.get("addr") or "").split(",")[0]
        ip, pfx = (addr.split("/") + ["24"])[:2] if addr else ("", "24")
        live = ni.get("live") or ""
        return ('<div class="domain"><div class="dh" style="background:#1c2531;background-image:linear-gradient(90deg,rgba(255,255,255,.12),rgba(255,255,255,0))"><span class="ic">\U0001F310</span><h2>'
          + L("Netzwerk / IP-Adresse","Network / IP address") + '</h2></div><div class="dbody">'
          + '<p>' + L("Aktuell: <b>","Currently: <b>") + html.escape(live) + '</b> (' + (L("automatisch per DHCP","automatic via DHCP") if auto else L("statisch","static")) + ', ' + html.escape(ni["con"]) + ')</p>'
          + '<div class="note warn"><b>' + L("Vorsicht:","Caution:") + '</b> ' + L("Nach dem Speichern wird die Einstellung sofort angewendet. Bei einer neuen IP ist das Dashboard danach nur unter der neuen Adresse erreichbar - und Loxone/Home Assistant muessen angepasst werden! Eine falsche IP kann den Pi unerreichbar machen (dann hilft nur Monitor/Tastatur oder SD-Karte).","The setting is applied immediately after saving. With a new IP the dashboard is only reachable at the new address - and Loxone/Home Assistant must be updated! A wrong IP can make the Pi unreachable.") + '</div>'
          + '<p><label><input type="radio" name="nm" value="auto"' + (' checked' if auto else '') + ' onchange="nmode()"> ' + L("Automatisch (DHCP) - IP kommt vom Router","Automatic (DHCP) - IP from router") + '</label><br>'
          + '<label><input type="radio" name="nm" value="manual"' + ('' if auto else ' checked') + ' onchange="nmode()"> ' + L("Statische IP:","Static IP:") + '</label></p>'
          + '<div id="nstat" style="' + ('display:none' if auto else '') + ';margin:.5rem 0 .8rem 1.4rem">'
          + 'IP <input id="nip" value="' + html.escape(ip or live.split("/")[0]) + '" style="width:130px"> / <input id="npfx" value="' + html.escape(pfx) + '" style="width:44px"> &nbsp; '
          + 'Gateway <input id="ngw" value="' + html.escape(ni.get("gw") or "") + '" style="width:130px"> &nbsp; '
          + 'DNS <input id="ndns" value="' + html.escape(ni.get("dns") or "") + '" style="width:130px"></div>'
          + '<button onclick="nsave()" style="background:#e2001a;color:#fff;border:0;border-radius:8px;padding:.55rem 1.2rem;font-weight:700;cursor:pointer">' + L("Netzwerk speichern & anwenden","Save & apply network") + '</button>'
          + '<span id="nmsg" style="margin-left:.8rem;color:#6c7787"></span>'
          + """<script>
function nmode(){document.getElementById('nstat').style.display=document.querySelector('input[name=nm]:checked').value=='manual'?'':'none';}
function nsave(){
 var mode=document.querySelector('input[name=nm]:checked').value;
 var b={mode:mode};
 if(mode=='manual'){b.ip=document.getElementById('nip').value.trim();b.prefix=document.getElementById('npfx').value.trim();b.gw=document.getElementById('ngw').value.trim();b.dns=document.getElementById('ndns').value.trim();}
 var warn=mode=='manual'?('Statische IP '+b.ip+'/'+b.prefix+' setzen?'):'Auf DHCP (automatisch) umstellen?';
 if(!confirm(warn+'\\nBei neuer IP ist diese Seite danach nur unter der neuen Adresse erreichbar!'))return;
 fetch('/api/network',{method:'POST',body:JSON.stringify(b)}).then(function(r){return r.json();}).then(function(j){
  document.getElementById('nmsg').textContent=j.ok?j.hinweis:('Fehler: '+j.fehler);
 }).catch(function(e){document.getElementById('nmsg').textContent='Antwort offen - ggf. neue IP aufrufen. ('+e+')';});
}
</script>"""
          + '</div></div>')

    STAT_SVCS = ["hoval-exporter", "prometheus", "grafana-server"]

    def api_stats(self):
        import subprocess
        try:
            ln = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(ln) or b"{}")
            on = bool(body.get("on"))
            act = ["enable", "--now"] if on else ["disable", "--now"]
            for s in self.STAT_SVCS:
                subprocess.run(["systemctl"] + act + [s], capture_output=True, timeout=90)
            states = {s: subprocess.run(["systemctl", "is-active", s], capture_output=True, text=True, timeout=10).stdout.strip()
                      for s in self.STAT_SVCS}
            out = {"ok": True, "on": on, "dienste": states}
        except Exception as e:
            out = {"ok": False, "fehler": str(e)}
        data = json.dumps(out).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def stats_section(self):
        import subprocess
        st = {}
        for s in self.STAT_SVCS:
            try:
                st[s] = subprocess.run(["systemctl", "is-active", s], capture_output=True, text=True, timeout=5).stdout.strip()
            except Exception:
                st[s] = "?"
        on = all(v == "active" for v in st.values())
        pills = " ".join('<span class="pill">' + s.replace("-server", "") + ": " + ("&#10003;" if v == "active" else "&#10007;") + '</span>'
                         for s, v in st.items())
        return ('<div class="domain"><div class="dh" style="background:#f46800;background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">\U0001F4C8</span><h2>'
          + L("Statistik (Grafana)", "Statistics (Grafana)") + '</h2></div><div class="dbody">'
          + '<p>' + L("Langzeit-Diagramme (Temperaturen, Leistung, COP, Smart Grid, Tagesenergie). Datenkette: Bridge \u2192 Exporter (:9101) \u2192 Prometheus (:9090, 400 Tage) \u2192 Grafana (:3000). Ansehen ohne Login (Viewer); zum Bearbeiten Login admin (Passwort beim ersten Login \u00e4ndern).",
              "Long-term charts (temperatures, power, COP, Smart Grid, daily energy). Chain: bridge \u2192 exporter (:9101) \u2192 Prometheus (:9090, 400 days) \u2192 Grafana (:3000). Viewing without login; editing via admin login.") + '</p>'
          + '<p>' + pills + '</p>'
          + ('<a id="gflink" href="#" target="_blank" style="display:inline-block;background:#f46800;color:#fff;font-weight:700;padding:.6rem 1.3rem;border-radius:10px;text-decoration:none">' + L("Grafana \u00f6ffnen", "Open Grafana") + '</a> ' if on else '')
          + '<button onclick="stoggle(' + ('false' if on else 'true') + ')" style="background:' + ('#6c7787' if on else '#0a8f4f') + ';color:#fff;border:0;border-radius:10px;padding:.6rem 1.3rem;font-weight:700;cursor:pointer;margin-left:.4rem">'
          + (L("Statistik deaktivieren", "Disable statistics") if on else L("Statistik aktivieren", "Enable statistics")) + '</button>'
          + '<span id="smsg" style="margin-left:.8rem;color:#6c7787"></span>'
          + """<script>
var g=document.getElementById('gflink'); if(g) g.href=location.protocol+'//'+location.hostname+':3000/d/hoxpi';
function stoggle(on){
 if(!confirm(on?'Statistik-Dienste (Exporter, Prometheus, Grafana) aktivieren?':'Statistik-Dienste stoppen und deaktivieren? Bereits gesammelte Daten bleiben erhalten.'))return;
 document.getElementById('smsg').textContent='...';
 fetch('/api/stats',{method:'POST',body:JSON.stringify({on:on})}).then(function(r){return r.json();}).then(function(j){
  if(j.ok){location.reload();}else{document.getElementById('smsg').textContent='Fehler: '+j.fehler;}
 }).catch(function(e){document.getElementById('smsg').textContent='Fehler: '+e;});
}
</script>"""
          + '</div></div>')

    def json_out(self, obj, status=200, cookie=None):
        data = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(data)

    def session_ok(self):
        for part in self.headers.get("Cookie", "").split(";"):
            part = part.strip()
            if part.startswith("hoxpi_session="):
                tok = part.split("=", 1)[1]
                exp = SESSIONS.get(tok)
                if exp and exp > _time.time():
                    return True
        return False

    def _read_json(self):
        ln = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(ln) or b"{}")

    def api_auth_setup(self):
        try:
            body = self._read_json()
            if auth_enabled():
                self.json_out({"ok": False, "fehler": "2FA ist schon aktiv"}); return
            sec = _auth_pending.get("secret")
            if not sec:
                self.json_out({"ok": False, "fehler": "Kein Setup gestartet - Seite Sicherheit neu laden"}); return
            if not auth_rate_ok():
                self.json_out({"ok": False, "fehler": "Zu viele Versuche - 5 Minuten warten"}, 429); return
            if not totp_ok(sec, body.get("code", "")):
                _auth_tries.append(_time.time())
                self.json_out({"ok": False, "fehler": "Code falsch - Uhrzeit am Handy pruefen und neu versuchen"}); return
            import os as _os
            fd = _os.open(AUTH_PATH, _os.O_WRONLY | _os.O_CREAT | _os.O_TRUNC, 0o600)
            with _os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump({"secret": sec, "aktiviert": datetime.datetime.now().isoformat(timespec="seconds")}, f)
            _auth_pending.clear()
            tok = new_session()
            self.json_out({"ok": True}, cookie=f"hoxpi_session={tok}; Path=/; Max-Age=2592000; HttpOnly; SameSite=Lax")
        except Exception as e:
            self.json_out({"ok": False, "fehler": str(e)})

    def api_auth_login(self):
        try:
            body = self._read_json()
            sec = auth_secret()
            if not sec:
                self.json_out({"ok": False, "fehler": "2FA ist nicht eingerichtet"}); return
            if not auth_rate_ok():
                self.json_out({"ok": False, "fehler": "Zu viele Versuche - 5 Minuten warten"}, 429); return
            if not totp_ok(sec, body.get("code", "")):
                _auth_tries.append(_time.time())
                self.json_out({"ok": False, "fehler": "Code falsch"}); return
            tok = new_session()
            self.json_out({"ok": True}, cookie=f"hoxpi_session={tok}; Path=/; Max-Age=2592000; HttpOnly; SameSite=Lax")
        except Exception as e:
            self.json_out({"ok": False, "fehler": str(e)})

    def api_auth_off(self):
        try:
            body = self._read_json()
            sec = auth_secret()
            if not sec:
                self.json_out({"ok": False, "fehler": "2FA ist nicht aktiv"}); return
            if not (self.session_ok() and totp_ok(sec, body.get("code", ""))):
                _auth_tries.append(_time.time())
                self.json_out({"ok": False, "fehler": "Angemeldete Sitzung + gueltiger Code noetig"}); return
            import os as _os
            _os.remove(AUTH_PATH)
            SESSIONS.clear()
            self.json_out({"ok": True})
        except Exception as e:
            self.json_out({"ok": False, "fehler": str(e)})

    def sicherheit(self):
        js = """<script>
function apost(url, body, msgid){
 document.getElementById(msgid).textContent='...';
 fetch(url,{method:'POST',body:JSON.stringify(body)}).then(function(r){return r.json();}).then(function(j){
  if(j.ok){location.reload();}else{document.getElementById(msgid).textContent=j.fehler;}
 }).catch(function(e){document.getElementById(msgid).textContent='Fehler: '+e;});
}
</script>"""
        out = ['<h1>' + L("Sicherheit", "Security") + '</h1>']
        if not auth_enabled():
            sec = _auth_pending.setdefault("secret", gen_secret())
            uri = "otpauth://totp/HoxPi?secret=" + sec + "&issuer=HoxPi"
            qr = qr_svg(uri)
            out.append('<div class="note warn">' + L(
              "Schreibaktionen (Register-Freigaben, Netzwerk, Statistik-Schalter) sind aktuell <b>ohne Anmeldung</b> moeglich - ok im vertrauensvollen Heimnetz, aber besser mit Schutz.",
              "Write actions (register permissions, network, statistics toggle) are currently possible <b>without sign-in</b> - fine in a trusted home network, but better protected.") + '</div>')
            out.append('<div class="domain"><div class="dh"><span class="ic">\U0001F510</span><h2>' + L("Zwei-Faktor-Schutz einrichten (empfohlen)", "Set up two-factor protection (recommended)") + '</h2></div><div class="dbody">')
            out.append('<ol style="line-height:1.9">')
            out.append('<li>' + L("Authenticator-App oeffnen (Google Authenticator, Microsoft Authenticator, Aegis, 1Password ...)", "Open an authenticator app (Google Authenticator, Microsoft Authenticator, Aegis, 1Password ...)") + '</li>')
            out.append('<li>' + L("QR-Code scannen", "Scan the QR code") + (' <b>' + L("oder Schluessel manuell eingeben:", "or enter the key manually:") + '</b>' if not qr else ':') + '</li></ol>')
            if qr:
                out.append('<div style="background:#fff;display:inline-block;padding:10px;border:1px solid #e1e5ec;border-radius:10px">' + qr + '</div>')
            out.append('<p><code style="font-size:1.05rem;letter-spacing:1px">' + html.escape(sec) + '</code></p>')
            out.append('<p>3. ' + L("Den 6-stelligen Code aus der App eingeben:", "Enter the 6-digit code from the app:") + ' <input id="scode" inputmode="numeric" maxlength="6" style="width:90px;padding:.4rem;font-size:1.1rem;letter-spacing:2px"> '
                       '<button onclick="apost(\'/api/auth/setup\',{code:document.getElementById(\'scode\').value},\'smsg\')" style="background:#0a8f4f;color:#fff;border:0;border-radius:8px;padding:.55rem 1.2rem;font-weight:700;cursor:pointer">' + L("Aktivieren", "Enable") + '</button> <span id="smsg" style="color:#d6202f"></span></p>')
            out.append('<div class="note">' + L("Danach verlangen alle Schreibaktionen einmalig den Code; die Anmeldung haelt 30 Tage pro Browser (Cookie). Lesen bleibt frei.", "Afterwards all write actions require the code once; the sign-in lasts 30 days per browser (cookie). Reading stays open.") + '</div>')
            out.append('</div></div>')
        else:
            logged = self.session_ok()
            out.append('<div class="note ok">' + L("2FA ist <b>aktiv</b>. Schreibaktionen erfordern eine Anmeldung.", "2FA is <b>enabled</b>. Write actions require sign-in.") + '</div>')
            if logged:
                out.append('<p>' + L("Du bist auf diesem Geraet <b>angemeldet</b> (30 Tage).", "You are <b>signed in</b> on this device (30 days).") + '</p>')
            else:
                out.append('<div class="domain"><div class="dh"><span class="ic">\U0001F511</span><h2>' + L("Anmelden", "Sign in") + '</h2></div><div class="dbody"><p>'
                           + L("6-stelliger Code aus der Authenticator-App:", "6-digit code from your authenticator app:")
                           + ' <input id="lcode" inputmode="numeric" maxlength="6" style="width:90px;padding:.4rem;font-size:1.1rem;letter-spacing:2px"> '
                           '<button onclick="apost(\'/api/auth/login\',{code:document.getElementById(\'lcode\').value},\'lmsg\')" style="background:#e2001a;color:#fff;border:0;border-radius:8px;padding:.55rem 1.2rem;font-weight:700;cursor:pointer">' + L("Anmelden", "Sign in") + '</button> <span id="lmsg" style="color:#d6202f"></span></p></div></div>')
            out.append('<div class="domain"><div class="dh" style="background:#6c7787"><span class="ic">\u26A0</span><h2>' + L("2FA deaktivieren", "Disable 2FA") + '</h2></div><div class="dbody"><p>'
                       + L("Nur mit aktiver Anmeldung + aktuellem Code:", "Requires active sign-in + current code:")
                       + ' <input id="ocode" inputmode="numeric" maxlength="6" style="width:90px;padding:.4rem"> '
                       '<button onclick="apost(\'/api/auth/off\',{code:document.getElementById(\'ocode\').value},\'omsg\')" style="background:#6c7787;color:#fff;border:0;border-radius:8px;padding:.5rem 1rem;cursor:pointer">' + L("Deaktivieren", "Disable") + '</button> <span id="omsg" style="color:#d6202f"></span></p>'
                       + '<div class="note warn">' + L("Handy verloren? Auf der Pi <code>sudo rm /home/admin/hoval-bridge/auth.json</code> ausfuehren und den Dashboard-Dienst neu starten - dann ist der Schutz zurueckgesetzt.", "Lost your phone? Run <code>sudo rm /home/admin/hoval-bridge/auth.json</code> on the Pi and restart the dashboard service to reset protection.") + '</div></div></div>')
        out.append(js)
        return "".join(out)

    def mcp_section(self):
        import subprocess
        try:
            st = subprocess.run(["systemctl", "is-active", "hoxpi-mcp"], capture_output=True, text=True, timeout=5).stdout.strip()
        except Exception:
            st = "?"
        if st != "active":
            return ""
        pre = ('"hoxpi": {\n  "command": "npx",\n  "args": ["-y", "mcp-remote", "http://HOSTIP:8808/mcp", "--allow-http"]\n}')
        return ('<div class="domain"><div class="dh" style="background:#7c4dbe;background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">\U0001F916</span><h2>'
          + L("KI-Assistent (MCP)", "AI assistant (MCP)") + '</h2></div><div class="dbody">'
          + '<p>' + L("HoxPi hat eine eingebaute <b>KI-Schnittstelle</b>: Ein Assistent wie Claude kann die Anlage live inspizieren, Werte erkl\u00e4ren, die Historie auswerten und Fehler eingrenzen \u2013 in normaler Sprache (\u201eWarum l\u00e4dt das Warmwasser nicht?\u201c). Einzige Voraussetzung auf dem PC: <a href=\"https://nodejs.org\" target=\"_blank\">Node.js</a>.",
              "HoxPi has a built-in <b>AI interface</b>: an assistant like Claude can inspect the system live, explain values, analyse history and narrow down faults \u2013 in plain language. Only requirement on the PC: <a href=\"https://nodejs.org\" target=\"_blank\">Node.js</a>.") + '</p>'
          + '<div style="margin:.6rem 0 1rem">'
          + '<a href="/hoxpi-claude-setup.bat" style="display:inline-block;background:#7c4dbe;color:#fff;font-weight:700;padding:.7rem 1.4rem;border-radius:10px;text-decoration:none">\u2B07 ' + L("Claude-Einrichtung (Windows)", "Claude setup (Windows)") + '</a> '
          + '<a href="/hoxpi-claude-setup.sh" style="display:inline-block;background:#9b7bd4;color:#fff;font-weight:600;padding:.7rem 1.1rem;border-radius:10px;text-decoration:none;margin-left:.4rem">\u2B07 macOS</a>'
          + '</div>'
          + '<p>' + L("Windows: Datei herunterladen, <b>doppelklicken</b> \u2013 sie tr\u00e4gt HoxPi in Claude ein und startet Claude neu. macOS: <code>bash hoxpi-claude-setup.sh</code> im Terminal. Danach in Claude einfach fragen: \u201eWie geht\u2019s meiner Heizung?\u201c",
              "Windows: download the file and <b>double-click</b> \u2013 it registers HoxPi in Claude and restarts Claude. macOS: run <code>bash hoxpi-claude-setup.sh</code>. Then just ask Claude: \u201cHow is my heating doing?\u201d") + '</p>'
          + '<details><summary style="cursor:pointer;color:#5a6675">' + L("Manuell einrichten (Profis)", "Manual setup (pros)") + '</summary>'
          + '<p>' + L("Claude beenden, dann in <code>claude_desktop_config.json</code> unter <code>mcpServers</code>:", "Quit Claude, then add under <code>mcpServers</code> in <code>claude_desktop_config.json</code>:") + '</p>'
          + '<pre id="mcpjson" style="background:#f3f4f7;border:1px solid #e1e5ec;border-radius:8px;padding:.7rem .9rem;font-size:.85rem;overflow:auto">' + html.escape(pre) + '</pre>'
          + '<script>var _mj=document.getElementById("mcpjson");_mj.textContent=_mj.textContent.replace("HOSTIP",location.hostname);</script></details>'
          + '<div class="note" style="margin-top:.8rem">' + L("Werkzeuge: Status, Diagnose, Register lesen/suchen, Historie (Grafana-Daten), Whitelist ansehen. <b>Schreiben ist standardm\u00e4\u00dfig deaktiviert</b> \u2013 aktivierbar in /home/admin/hoxpi-mcp/config.json (enable_write); jede \u00c4nderung braucht zus\u00e4tzlich eine Best\u00e4tigung und l\u00e4uft durch alle Bridge-Sicherungen. Hinweis: Claudes gehostete \u201eCustom Connectors\u201c verlangen eine \u00f6ffentliche https-Adresse \u2013 im Heimnetz ist dieser lokale Weg der richtige.",
              "Tools: status, diagnosis, read/search registers, history (Grafana data), view whitelist. <b>Writing is disabled by default</b> (config.json: enable_write); every change also needs explicit confirmation and passes all bridge safeguards. Note: Claude's hosted \u201cCustom Connectors\u201d require a public https address \u2013 on a home network this local route is the way to go.") + '</div>'
          + '</div></div>')

    def home(self):
        return f"""<h1>{L("Deine Hoval-Anlage im Netzwerk","Your Hoval system on the network")}</h1>
<p>{L("Dieser Raspberry Pi liest <b>Wärmepumpe</b> und <b>Wohnraumlüftung</b> über den Hoval-CAN-Bus aus und stellt alle Werte als <b>Modbus-TCP</b> bereit — wie der originale Hoval-Gateway. So können <b>Loxone</b> und <b>Home Assistant</b> die Anlage lesen (und gezielt steuern), ganz ohne Cloud.","This Raspberry Pi reads the <b>heat pump</b> and <b>ventilation</b> over the Hoval CAN bus and exposes every value as <b>Modbus-TCP</b> — just like the original Hoval gateway. So <b>Loxone</b> and <b>Home Assistant</b> can read (and selectively control) the system, entirely without cloud.")}</p>
{schema()}
<div class="grid3" style="margin-top:1rem">
  <div class="card"><div class="n">{L("Datenfluss","Data flow")}</div><div class="v" style="font-size:1rem">CAN → Pi → Modbus</div></div>
  <div class="card"><div class="n">{L("Adresse (Modbus-TCP)","Address (Modbus-TCP)")}</div><div class="v" style="font-size:1.05rem">192.168.1.168:502</div></div>
  <div class="card"><div class="n">{L("Status","Status")}</div><div class="v ok" style="font-size:1.05rem">{L("aktiv · liest live","active · reading live")}</div></div>
</div>
<div class="domain"><div class="dh" style="background:#c2185b;background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">🛒</span><h2>{L("Hardware-Vorschlag","Hardware suggestion")}</h2></div><div class="dbody">
<p>{L("Das braucht man, um HoxPi nachzubauen — günstige Standardteile:","What you need to build HoxPi — inexpensive standard parts:")}</p>
<table><tr><th>{L("Teil","Part")}</th><th>{L("Hinweis","Note")}</th></tr>
<tr><td>{L("Einplatinen-Rechner","Single-board computer")}</td><td>{L("Raspberry Pi 4 (2 GB reichen)","Raspberry Pi 4 (2 GB is enough)")}</td></tr>
<tr><td>{L("USB-CAN-Adapter","USB-CAN adapter")}</td><td>DSD-TECH SH-C30G</td></tr>
<tr><td>{L("PoE-Splitter (optional)","PoE splitter (optional)")}</td><td>{L("5 V, <b>mindestens 3 A</b> (der Pi 4 braucht 5 V/3 A)","5 V, <b>at least 3 A</b> (the Pi 4 needs 5 V/3 A)")}</td></tr>
<tr><td>{L("Gehäuse","Case")}</td><td>{L("passend für Raspberry Pi 4","for Raspberry Pi 4")}</td></tr>
<tr><td>{L("microSD-Karte","microSD card")}</td><td>{L("ab 16 GB","16 GB or more")}</td></tr>
</table>
<div class="note" style="margin-top:.8rem">{L("PoE ist optional — der Pi kann auch per USB-Netzteil (5 V/3 A) laufen. Anschluss am Hoval-CAN erfolgt am <b>WEZ-Modul</b> (Klemme + ⏚ H L). Details auf der Seite <b>Integration</b>.","PoE is optional — the Pi can also run from a USB power supply (5 V/3 A). The Hoval CAN is tapped at the <b>WEZ module</b> (terminal + ⏚ H L). Details on the <b>Integration</b> page.")}</div>
</div></div>
<h2 class="sec">{L("Die Seiten","The pages")}</h2>
<ul>
<li><b>Live</b> \u2013 {L("Live-Werte in Klartext, nach Bereichen gruppiert.","live values in plain text, grouped by area.")}</li>
<li><b>{L("Alle Werte","All values")}</b> \u2013 {L("jeder dekodierte Datenpunkt mit Bezeichnung, Beschreibung (Maus drueber!) und Wert.","every decoded data point with label, description (hover!) and value.")}</li>
<li><b>Register</b> \u2013 {L("alle 514 Register, sortier- und durchsuchbar, mit Schreibfreigabe per Haken.","all 514 registers, sortable and searchable, with write permission checkboxes.")}</li>
<li><b>Integration</b> \u2013 {L("Loxone & Home Assistant anbinden, Netzwerk/IP einstellen, komplette Anleitung.","connect Loxone & Home Assistant, set network/IP, full guide.")}</li>
</ul>"""

    def werte(self):
        regs = [it[0] for _,_,subs in DOMAINS for _,items in subs for it in items if it[0] is not None]
        vals, ok = read_modbus(regs)
        if not ok:
            return f'<h1>{L("Werte","Values")}</h1><div class="note warn">⚠️ {L("Brücke (Modbus :502) nicht erreichbar.","Bridge (Modbus :502) not reachable.")}</div>'
        out = [f'<h1>{L("Live-Werte","Live values")}</h1>']
        dcol = {"Wärmepumpe":"#e2001a","Heizung & Kühlung":"#e2001a","Warmwasser":"#c2185b","Wohnraumlüftung":"#69b41e"}
        for title, icon, subs in DOMAINS:
            c = dcol.get(title, "#e2001a")
            out.append(f'<div class="domain"><div class="dh" style="background:{c};background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">{icon}</span><h2>{html.escape(tl(title))}</h2></div><div class="dbody">')
            for subtitle, items in subs:
                if subtitle:
                    out.append(f'<div class="sub">{html.escape(tl(subtitle))}</div>')
                out.append('<div class="cards">')
                for reg, name, unit, dec, signed in items:
                    if reg is None:
                        out.append(f'<div class="note-card">ℹ️ {html.escape(tl(name))}</div>')
                        continue
                    raw = vals.get(reg)
                    if reg in ENUM:
                        txt = ENUM[reg].get(raw, f"Code {raw}") if raw is not None else "—"
                        cls = "val" if raw is not None else "muted"
                    else:
                        txt, cls = fmt(raw, unit, dec, signed)
                    d = html.escape(desc(reg, name, unit))
                    _z = get_labels().get(str(reg))
                    _nm = html.escape(tl(name)) + (f'<span class="ze">{html.escape(_z)}</span>' if _z else "")
                    out.append(f'<div class="card" title="{d}"><div class="n">{_nm}</div>'
                               f'<div class="v {cls}">{html.escape(txt)}</div><span class="tt">{d}</span></div>')
                out.append('</div>')
            out.append('</div></div>')
        out.append(f'<div class="note" style="margin-top:1rem">{L("Aktualisiert alle 10 s · — = kein Sensor / nicht belegt.","Updated every 10 s · — = no sensor / not assigned.")}</div>')
        return "".join(out)

    def alle(self):
        m = regmap()
        if not m: return f'<h1>{L("Alle Werte","All values")}</h1><div class="note warn">{L("Register-Map nicht ladbar.","Register map not loadable.")}</div>'
        vals = read_all(sorted(m.keys()))
        if not vals: return f'<h1>{L("Alle Werte","All values")}</h1><div class="note warn">⚠️ {L("Brücke (Modbus :502) nicht erreichbar.","Bridge (Modbus :502) not reachable.")}</div>'
        secs = [(L("Wärmepumpe (UnitId 1)","Heat pump (UnitId 1)"),"🔥",1),(L("Wohnraumlüftung (UnitId 520)","Ventilation (UnitId 520)"),"💨",520)]
        out = [f'<h1>{L("Alle Live-Werte","All live values")}</h1>',
               f'<p>{L("Automatisch aus dem CAN-Bus dekodiert — jeder Datenpunkt mit Register, Hoval-Bezeichnung und Wert. — = kein Sensor / nicht belegt.","Automatically decoded from the CAN bus — every data point with register, Hoval label and value. — = no sensor / not assigned.")}</p>']
        tr=0; ts=0
        for title, icon, uid in secs:
            regs = sorted(r for r in m if m[r]["unit_id"]==uid)
            real=[]
            for reg in regs:
                if reg not in vals: continue
                txt,sent = decode_reg(m[reg], vals[reg])
                if sent: ts+=1; continue
                tr+=1; real.append((reg, rt_name(reg, m[reg]["name"] or ""), txt))
            c = "#69b41e" if uid==520 else "#e2001a"
            out.append(f'<div class="domain"><div class="dh" style="background:{c};background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">{icon}</span><h2>{html.escape(title)} · {len(real)} {L("Werte","values")}</h2></div><div class="dbody">')
            out.append(f'<table><tr><th>{L("Register","Register")}</th><th>{L("Bezeichnung","Label")}</th><th>{L("Wert","Value")}</th></tr>')
            for reg,name,txt in real:
                d = html.escape(rt_desc(reg) or desc(reg, name, m[reg].get("unit",""), m[reg].get("writable")))
                out.append(f'<tr><td><code>{reg}</code></td><td title="{d}" style="cursor:help">{html.escape(name)}</td><td class="val">{html.escape(txt)}</td></tr>')
            out.append('</table></div></div>')
        out.append(f'<div class="note ok" style="margin-top:1rem"><b>{tr}</b> {L("aktive Werte","active values")} · {ts} {L("Register ohne Sensor (—) · aktualisiert alle 10 s.","registers without sensor (—) · updated every 10 s.")}</div>')
        return "".join(out)

    def loxone(self):
        m = regmap()
        regs = [it[0] for _,_,subs in DOMAINS for _,items in subs for it in items if it[0] is not None]
        vals, ok = read_modbus(regs)
        rows=""
        for title,_,subs in DOMAINS:
            for _,items in subs:
                for reg,name,unit,dec,signed in items:
                    if reg is None: continue
                    txt,_c = fmt(vals.get(reg) if ok else None, unit, dec, signed)
                    typ = m.get(reg,{}).get("type","?")
                    d = html.escape(desc(reg, name, unit, m.get(reg,{}).get("writable")))
                    rows += (f"<tr><td><code>{reg}</code></td><td title=\"{d}\" style=\"cursor:help\">{html.escape(name)}</td>"
                             f"<td>{html.escape(txt)}</td><td><span class=pill>{typ}</span></td></tr>")
        return f"""<h1>Anbindung an Loxone</h1>
<p>Der Pi verhält sich wie ein <b>Hoval-Modbus-TCP-Gateway</b>. In Loxone Config ein
<b>Modbus-TCP-Gerät</b> anlegen und die Holding-Register (Funktion 3) lesen. Die Registernummern
entsprechen exakt der offiziellen Hoval-Modbus-Tabelle — die offiziellen Loxone-Hoval-Templates passen 1:1.</p>
<div class="grid3">
 <div class="card"><div class="n">IP-Adresse</div><div class="v" style="font-size:1.05rem">192.168.1.168</div></div>
 <div class="card"><div class="n">Port</div><div class="v" style="font-size:1.05rem">502</div></div>
 <div class="card"><div class="n">Lesen</div><div class="v" style="font-size:1.05rem">FC 3</div></div>
 <div class="card"><div class="n">Schreiben</div><div class="v" style="font-size:1.05rem">gezielt frei</div></div>
</div>
<h2 class="sec">Register-Auswahl (Live-Werte)</h2>
<table><tr><th>Register</th><th>Bedeutung</th><th>Wert</th><th>Typ</th></tr>{rows}</table>
<div class="note" style="margin-top:1rem">Insgesamt <b>439 Register</b> (368 Wärmepumpe + 71 Lüftung). Werte sind
<b>Rohwerte</b> wie beim Hoval-Gateway — Loxone skaliert (z. B. °C ×10) im Template.</div>"""

    def homeassistant(self):
        return f"""<h1>Anbindung an Home Assistant</h1>
<p>HoxPi spricht <b>Modbus-TCP</b>, das Home Assistant von Haus aus unterstützt. Du musst nichts
von Hand abtippen: Lade die fertige Konfiguration herunter, leg sie in den <code>packages</code>-Ordner,
HA neu starten — <b>alle Sensoren erscheinen automatisch</b>, bereits richtig skaliert (°C, %, kW …).</p>
<div style="text-align:center;margin:1.3rem 0">
 <a href="/hoxpi-ha.yaml" download style="display:inline-block;background:#41bdf5;color:#08334a;
  font-weight:700;font-size:1.05rem;padding:.8rem 1.6rem;border-radius:11px;text-decoration:none;
  box-shadow:0 4px 14px rgba(65,189,245,.35)">⬇ hoxpi.yaml herunterladen</a>
 <div style="color:#6c7787;font-size:.85rem;margin-top:.5rem">fertige Modbus-Konfiguration, automatisch aus der Hoval-Tabelle erzeugt</div>
</div>
<div class="domain"><div class="dh" style="background:#41bdf5;background-image:linear-gradient(90deg,rgba(255,255,255,.18),rgba(255,255,255,0))"><span class="ic">🏠</span><h2>In 3 Schritten importieren</h2></div><div class="dbody">
<ol style="line-height:1.8;color:#3a4554">
<li>Datei <code>hoxpi.yaml</code> herunterladen (Button oben) und nach
 <code>&lt;config&gt;/packages/hoxpi.yaml</code> kopieren (Ordner <code>packages</code> ggf. anlegen).</li>
<li>In <code>configuration.yaml</code> einmalig die Packages aktivieren:
<pre style="background:#f3f4f7;border:1px solid #e1e5ec;border-radius:8px;padding:.7rem .9rem;overflow:auto;font-size:.85rem">homeassistant:
  packages: !include_dir_named packages</pre></li>
<li><b>Home Assistant neu starten.</b> Danach findest du alle Werte als <code>sensor.hoxpi_*</code>.</li>
</ol></div></div>
<div class="grid3">
 <div class="card"><div class="n">IP-Adresse</div><div class="v" style="font-size:1.05rem">192.168.1.168</div></div>
 <div class="card"><div class="n">Port</div><div class="v" style="font-size:1.05rem">502</div></div>
 <div class="card"><div class="n">Protokoll</div><div class="v" style="font-size:1.05rem">Modbus-TCP · FC 3</div></div>
</div>
<div class="note ok" style="margin-top:1rem">Anders als bei Loxone sind die Werte hier schon <b>fertig skaliert</b> –
Temperaturen in °C, Leistungen in kW usw. – weil Home Assistant das in der YAML übernimmt.</div>
<div class="note warn" style="margin-top:.8rem">Hinweis: Einen echten „Ein-Klick"-Import gibt es bei Modbus in HA (noch) nicht –
das Herunterladen + Ablegen der Datei ist der schnellste offiziell unterstützte Weg.
Falls deine Pi-IP nicht <code>192.168.1.168</code> ist, in der Datei oben den <code>host:</code> anpassen.</div>"""

    def anleitung(self):
        return f"""<h1>Anleitung — Installation & Anbindung</h1>
<p>Von der Verkabelung bis zur fertigen Anbindung in Loxone oder Home Assistant. HoxPi verhält sich
nach außen wie ein <b>originaler Hoval-Modbus-Gateway</b> — deshalb funktionieren die offiziellen Vorlagen 1:1.</p>

<div class="domain"><div class="dh" style="background:#c2185b;background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">🔌</span><h2>1 · Hardware anschließen</h2></div><div class="dbody">
<ul style="line-height:1.8">
<li>USB-CAN-Adapter (DSD-TECH SH-C30G) in den Raspberry Pi stecken.</li>
<li>Die drei CAN-Adern am Hoval <b>WEZ-Modul</b>, Klemme „+ ⏚ H L", <b>parallel</b> mit aufklemmen
(der bestehende Bus läuft unverändert weiter): <b>H = blau, L = orange, ⏚ = grün</b>.</li>
<li>Am WEZ-Modul liegt der echte <b>TopTronic-E-CAN</b> (50 kbit/s, 64 Ω terminiert).
<b>Nicht</b> an Klemme X4 — das ist RS485, kein CAN.</li>
<li>Pi mit Strom versorgen (PoE-Splitter am Netzwerkkabel oder USB-Netzteil).</li>
</ul></div></div>

<div class="domain"><div class="dh" style="background:#e2001a;background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">💻</span><h2>2 · Software / Pi</h2></div><div class="dbody">
<p>Auf dem Pi laufen mehrere Dienste mit Autostart: <code>can0</code> (CAN-Schnittstelle), die
<b>HoxPi-Brücke</b> (CAN → Modbus-TCP :502) , dieses Dashboard (Port 80) sowie optional Exporter/Prometheus/Grafana für die Statistik. Einmal eingerichtet
startet alles nach jedem Strom-Aus von selbst.</p>
<div class="note">Pi im Netzwerk erreichbar unter <code>192.168.1.168</code> · Dashboard: einfach diese Seite.
Bridge-Status: läuft &amp; liest live.</div></div></div>

<div class="domain"><div class="dh" style="background:#69b41e;background-image:linear-gradient(90deg,rgba(255,255,255,.15),rgba(255,255,255,0))"><span class="ic">🟩</span><h2>3 · Loxone anbinden</h2></div><div class="dbody">
<p>In <b>Loxone Config</b> ein <b>Modbus-TCP-Gerät</b> anlegen → IP <code>192.168.1.168</code>, Port <code>502</code>.
Dann die passenden Hoval-<b>Templates</b> aus der <b>Loxone Library</b> einbinden (so heißen die fertigen
Geräte-Integrationen dort — nicht „Vorlagen"). Welches Template du brauchst, hängt vom Anlagenteil ab:</p>
<table><tr><th>Anlagenteil</th><th>Loxone-Template</th><th>wann nehmen</th></tr>
<tr><td>Wärmepumpe<br>(Heizen, Kühlen, Warmwasser)</td>
<td><a href="https://library.loxone.com/detail/template-hoval-at-769/overview" target="_blank">Hoval Heating &amp; Cooling</a></td>
<td><b>immer</b> — das ist die Hauptintegration: Vorlauftemperaturen der Heizkreise und Warmwasser werden hierüber geregelt.</td></tr>
<tr><td>Wohnraumlüftung<br>(HomeVent)</td>
<td><a href="https://library.loxone.com/detail/hoval-template-884/overview" target="_blank">Hoval Ventilation</a></td>
<td>wenn die <b>Lüftung</b> in Loxone sichtbar/steuerbar sein soll (Stufen, Feuchte, Temperaturen).</td></tr>
<tr><td>Energiemanagement</td>
<td><a href="https://library.loxone.com/detail/hoval-energy-management-1845/overview" target="_blank">Hoval Energy Management</a></td>
<td><b>optional</b> — nur wenn Loxone die WP energieoptimiert fahren soll (z. B. PV-Überschuss, Lastverschiebung).</td></tr>
</table>
<div class="note" style="margin-top:.8rem">Für deine Anlage: <b>Heating &amp; Cooling</b> (Wärmepumpe) + <b>Ventilation</b> (Lüftung).
Energy Management nur bei Bedarf. Jedes Template hat im Download-Bereich eine deutsche „Praxisanleitung Hoval-Loxone".</div>
<div class="note ok" style="margin-top:.6rem">Die Templates erwarten einen <b>Hoval-Modbus-Gateway</b> — genau den spielt HoxPi.
Registernummern stimmen exakt mit der Hoval-Tabelle, also passen sie ohne Anpassung.
Werte sind <b>Rohwerte</b> (z. B. °C ×10) — das Template skaliert selbst. Mehr dazu: der Loxone-Abschnitt weiter oben.</div></div></div>

<div class="domain"><div class="dh" style="background:#41bdf5;background-image:linear-gradient(90deg,rgba(255,255,255,.18),rgba(255,255,255,0))"><span class="ic">🏠</span><h2>4 · Home Assistant anbinden</h2></div><div class="dbody">
<p>Fertige Konfiguration im Home-Assistant-Abschnitt weiter oben herunterladen
(<code>hoxpi.yaml</code>), in den <code>packages</code>-Ordner legen, HA neu starten — alle Sensoren
erscheinen automatisch und sind bereits skaliert (°C, %, kW …).</p></div></div>

<div class="domain"><div class="dh" style="background:#1c2531;background-image:linear-gradient(90deg,rgba(255,255,255,.12),rgba(255,255,255,0))"><span class="ic">💡</span><h2>5 · Tipps &amp; Hinweise</h2></div><div class="dbody">
<ul style="line-height:1.8">
<li>Der CAN-Abgriff ist <b>passiv &amp; parallel</b> — die bestehende Anlage bleibt unberührt.</li>
<li>HoxPi startet <b>schreibgeschützt</b>. Steuern (Sollwerte ändern) lässt sich gezielt freischalten,
nur für sinnvolle, geprüfte Werte.</li>
<li>Andere Pi-IP? Dann in der Home-Assistant-Datei den <code>host:</code> und in Loxone die Geräte-IP anpassen.</li>
<li>Alles bleibt <b>lokal</b>, kein Cloud-Zugang nötig.</li>
</ul></div></div>"""

class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

with Server(("", 80), H) as s:
    s.serve_forever()
