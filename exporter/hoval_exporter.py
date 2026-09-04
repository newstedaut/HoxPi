#!/usr/bin/env python3
"""HoxPi Prometheus-Exporter: liest kuratierte Register der Bridge (Modbus localhost:502)."""
import http.server, socketserver, socket, struct, threading

# name -> (reg, scale, signed)
R16 = {
 "hoval_aussentemp_c": (1477, 0.1, True),
 "hoval_vorlauf_c": (18760, 0.1, True),
 "hoval_ruecklauf_c": (1535, 0.1, True),
 "hoval_ww_ist_c": (1500, 0.1, True),
 "hoval_ww_soll_c": (1499, 0.1, True),
 "hoval_raum_ist_c": (1510, 0.1, True),
 "hoval_p_el_kw": (25611, 0.01, True),
 "hoval_p_th_kw": (25612, 1, True),
 "hoval_modulation_pct": (18726, 1, False),
 "hoval_hc1_status": (1501, 1, False),
 "hoval_hc2_status": (1502, 1, False),
 "hoval_ww_status": (1504, 1, False),
 "hoval_wp_detailstatus": (18723, 1, False),   # U8 WEZ-Statuscode (Backlog #14: vorher 0,1 -> 5.1/1.6 statt 51/16)
 "hoval_sg_status": (27537, 1, False),
 "hoval_sg_befehl": (27545, 1, False),
 "hoval_offset_ww_k": (27509, 0.1, True),
 "hoval_offset_hk1_k": (27528, 0.1, True),
 "hoval_offset_kk1_k": (27531, 0.1, True),
 "hoval_uka": (19870, 1, False),
 "hoval_kwl_feuchte_abluft_pct": (23627, 1, False),
 "hoval_kwl_temp_abluft_c": (23633, 0.1, True),
 "hoval_kwl_luefter_pct": (23634, 1, False),
 "hoval_kwl_co2_pct": (28940, 1, False),
 "hoval_fa_cop": (27490, 0.1, False),
 "hoval_quelle_vl_c": (27491, 0.1, True),
 "hoval_quelle_rl_c": (27492, 0.1, True),
 "hoval_wasserdruck_bar": (1538, 0.1, True),
 "hoval_fa_kuehl_soll_c": (1524, 0.1, True),
 "hoval_fa_wez_temp_c": (1525, 0.1, True),
 "hoval_fa_ruecklauf_c": (1535, 0.1, True),
 # --- FA-Ebene fg=60/fn=254 + Anlageleistung (Backlog #8, 02.09.2026) ---
 "hoval_wez_status": (1539, 1, False),
 "hoval_fehlercode": (1534, 1, False),
 "hoval_stoerungsflag": (1540, 1, False),
 "hoval_leistung_soll_heizen_pct": (18764, 0.1, True),
 "hoval_leistung_soll_ww_pct": (18765, 0.1, True),
 "hoval_leistung_soll_kuehlen_pct": (18766, 0.1, True),
 "hoval_leistung_soll_aktiv_pct": (18767, 0.1, True),
 "hoval_leistung_anforderung": (18768, 1, False),
}
# Rohwerte, die "kein Wert" bedeuten (zusaetzlich zu 0x8000/0xFFFF)
INVALID16 = {
 "hoval_leistung_soll_heizen_pct": {-1270}, "hoval_leistung_soll_ww_pct": {-1270},
 "hoval_leistung_soll_kuehlen_pct": {-1270}, "hoval_leistung_soll_aktiv_pct": {-1270},
 "hoval_fa_ruecklauf_c": {0},  # 0 = kein Wert (FA antwortet nach Netz-Ein nicht)
}
# name -> (highreg, scale[, signed])
R32 = {
 "hoval_cop": (31667, 0.1),
 "hoval_energie_el_mwh": (25613, 0.001),
 "hoval_waerme_heizen_mwh": (27484, 0.001),
 "hoval_waerme_kuehlen_mwh": (27486, 0.001),
 "hoval_waerme_ww_mwh": (27488, 0.001),
 "hoval_schaltzyklen": (1518, 1),
 # --- fg=60/fn=7 Hydraulik + Laufzeitzaehler (Backlog #8, 02.09.2026) ---
 "hoval_betriebsstunden_heizen_h": (31711, 0.1),   # dp1033, Skala 0,1 h
 "hoval_betriebsstunden_kuehlen_h": (31713, 0.1),  # dp1034 (Hovals Name an 31663 ist falsch)
 "hoval_betriebsstunden_ww_h": (31715, 0.1),       # dp1035
 "hoval_wp_vorlauf_c": (31892, 0.1, True),         # dp257 WP-Vorlauf (S32)
 "hoval_wp_ruecklauf_c": (31894, 0.1, True),       # dp258 WP-Ruecklauf (S32)
 "hoval_wp_pumpe_pct": (27495, 1),                 # dp271 Drehzahl WP-Umwaelzpumpe, 0xFFFFFFFF = aus -> 0
 "hoval_volumenstrom_lmin": (31707, 0.1),          # dp302 Volumenstrom gemittelt
}
# --- Kaeltekreis fg=60/fn=7 (Backlog R7, 04.09.2026): 16-bit-Einzelwort in der Bridge, gegen pCO-DB 0106/0107/0108/0202/0206 geeicht.
#     Zustandsabhaengig: antwortet der Regler nicht, liefert die Bridge fuer alle fuenf 0 -> Gruppe weglassen (kein 0-Wert publizieren).
KK16 = {
 "hoval_kk_lufteintritt_c": (31903, 0.1, True),    # dp262 Lufteintritt Verdampfer
 "hoval_kk_sauggas_c": (31905, 0.1, True),         # dp263 Sauggas vor Verdichter
 "hoval_kk_heissgas_c": (31907, 0.1, True),        # dp264 Heissgas/Verdichterfuehler
 "hoval_kk_ueberhitzung_k": (31913, 0.01, True),   # dp514 Ueberhitzung 0,01 K
 "hoval_kk_niederdruck_bar": (31915, 0.01, True),  # dp518 Niederdruck relativ 0,01 bar
}
COUNTER32 = ("mwh", "zyklen", "betriebsstunden")
HELP = {
 "hoval_hc1_status": "0=Aus 1..3=Heizen 9..11=Kuehlen 12=Stoerung 26=SmartGrid",
 "hoval_wp_detailstatus": "Register 18723 FA-Status = WEZ-Statuscode wie hoval_wez_status (0/1/2/4/16/17/51/98), seit 03.09.2026 Faktor 1",
 "hoval_wez_status": "0=Aus 1=Heizen 2=Kuehlen 4=Warmwasser 16=Wiedereinschaltsperre 17=Verriegelung(Stoerung) 51=Startvorbereitung 98=Startphase(W:61)",
 "hoval_fehlercode": "255=OK, 0=kein Wert (FA antwortet nicht, z. B. nach Netz-Ein), sonst gepackt: code+1 = Klasse*64+Nr (Klasse 1=W 2=B 3=E), Klartext in hoval_fehlercode_info",
 "hoval_fehlercode_info": "aktiver Hoval-Fehler als Label code=W/B/E:nn (nur wenn 1534 != 255)",
 "hoval_stoerungsflag": "Register 1540: 0=keine, 8=Blockierung/Verriegelung aktiv",
 "hoval_leistung_soll_aktiv_pct": "aktiver Leistungs-Sollwert (-100=keine Anforderung; -127=ungueltig wird unterdrueckt)",
 "hoval_wp_pumpe_pct": "Drehzahl WP-Umwaelzpumpe (0=aus)",
 "hoval_ruecklauf_c": "Ruecklauf 1535 (Kaeltekreisregler); liefert 1535 nach Netz-Ein 0, wird der WP-Ruecklauf 60-7-258 (31894/31895) ausgegeben",
 "hoval_fa_ruecklauf_c": "Ruecklauf 1535 roh (60-254-29), fehlt solange die FA nach Netz-Ein nicht antwortet",
 "hoval_kk_lufteintritt_c": "Kaeltekreis Lufteintritt Verdampfer 60-7-262 (pCO 0106); Gruppe fehlt, wenn der Regler die fn=7-Punkte nicht beantwortet",
 "hoval_kk_sauggas_c": "Kaeltekreis Sauggas vor Verdichter 60-7-263 (pCO 0107)",
 "hoval_kk_heissgas_c": "Kaeltekreis Heissgas/Verdichterfuehler 60-7-264 (pCO 0108)",
 "hoval_kk_ueberhitzung_k": "Kaeltekreis Ueberhitzung Sauggas 60-7-514 (pCO 0202), 0,01 K",
 "hoval_kk_niederdruck_bar": "Kaeltekreis Niederdruck relativ 60-7-518 (pCO 0206), 0,01 bar",
 "hoval_kuehl_phase": "Kuehlen: 0 keine Anforderung, 1 angefordert + Kaeltekreisregler wartet (WP-Vorlauf 1525 < 19,5 C), 2 Startmarke erreicht (Freigabe folgt), 3 Kuehlen aktiv (WEZ-Status != 0)",
 "hoval_kuehl_wartet": "1 = Kuehlen angefordert, Verdichter steht noch (Phase 1 oder 2); kein Fehler, der Regler startet erst ab WP-Vorlauf 19,5 C",
 "hoval_ww_status": "0=Aus 1=Laden 8=Laden reduziert 12=SmartGrid",
 "hoval_sg_status": "0=Normal 1=Vorzug 2=Gesperrt 3=Abnahmezwang",
}
_tid = [0]
_conn = {"sock": None}
_lock = threading.Lock()
def _sock():
    if _conn["sock"] is None:
        s = socket.create_connection(("127.0.0.1", 502), 3); s.settimeout(3)
        _conn["sock"] = s
    return _conn["sock"]
def _drop():
    try: _conn["sock"].close()
    except Exception: pass
    _conn["sock"] = None
def rd(addr, words=1):
    # Persistente Modbus-Verbindung wiederverwenden (verhindert TIME_WAIT-Anhaeufung).
    # Bei Fehler Verbindung verwerfen und einmal neu versuchen.
    with _lock:
        _tid[0] = (_tid[0] + 1) & 0xFFFF
        for _ in range(2):
            try:
                s = _sock()
                s.sendall(struct.pack(">HHHBBHH", _tid[0], 0, 6, 1, 3, addr, words))
                r = s.recv(260)
                if not r or (r[7] & 0x80): return None
                return [struct.unpack(">H", r[9+2*i:11+2*i])[0] for i in range(words)]
            except Exception:
                _drop()
        return None

def metrics():
    out = []
    import json as _j
    try: _copf = _j.load(open("/home/admin/hoxpi-features.json")).get("cop_filter",{}).get("enabled",True)
    except Exception: _copf = True
    # COP-Startfilter: dp 45 liefert in den ersten ~25 s eines Laufs Unsinn (Pel ~0) -> COP = 0, solange Pel < 0,5 kW
    _pel = rd(25611)
    _cop_ok = (not _copf) or (bool(_pel) and _pel[0] not in (0x8000, 0xFFFF) and _pel[0] >= 50)
    for name, (reg, sc, sg) in R16.items():
        w = rd(reg)
        if not w: continue
        v = w[0]
        if v in (0x8000, 0xFFFF): continue
        if name == "hoval_ruecklauf_c" and v == 0:  # 1535 nach Netz-Ein stumm (0 = kein Wert) -> WP-Ruecklauf 60-7-258 (S32)
            w2 = rd(31894, 2)
            if not w2 or len(w2) < 2: continue
            v = (w2[0] << 16) | w2[1]
            if v in (0xFFFFFFFF, 0x80000000): continue
            if v > 0x7FFFFFFF: v -= 0x100000000
            if not -500 <= v <= 1500: continue
        if sg and v > 32767: v -= 65536
        if v in INVALID16.get(name, ()): continue
        if _copf and name in ("hoval_fa_cop",) and not (0 <= v*sc <= 20): continue  # COP-Plausibilitaet
        if name == "hoval_fa_cop" and not _cop_ok: v = 0  # COP-Startfilter
        if name in HELP: out.append(f"# HELP {name} {HELP[name]}")
        out.append(f"# TYPE {name} gauge")
        out.append(f"{name} {round(v*sc, 3)}")
        if name == "hoval_fehlercode" and v not in (0, 255):  # 0 = kein Wert (FA antwortet nicht, z. B. nach Netz-Ein)
            # gepackter Hoval-Code: code+1 = Klasse*64 + Nr  (W/B/E = Warnung/Blockierung/Verriegelung)
            c = int(v) + 1
            out.append(f"# HELP hoval_fehlercode_info {HELP['hoval_fehlercode_info']}")
            out.append("# TYPE hoval_fehlercode_info gauge")
            out.append('hoval_fehlercode_info{code="%s:%02d"} 1' % ("IWBE"[(c >> 6) & 3], c & 63))
    # Backlog 15c: Kuehl-Phase (Wartezustand des Kaeltekreisreglers, Kriterium wie Dashboard #15b)
    #   0 keine Kuehlanforderung | 1 angefordert, wartet (WP-VL 1525 < 19,5) | 2 Startmarke erreicht | 3 Kuehlen aktiv
    try:
        _hk, _uka, _wez, _vl = rd(1501), rd(19870), rd(1539), rd(1525)
        _ph = None
        if _hk and _uka and _wez:
            if _hk[0] != 22: _ph = 0
            elif _wez[0] != 0 or (_pel and _pel[0] not in (0x8000, 0xFFFF) and _pel[0] >= 50): _ph = 3  # F1: 1539 stumm -> Pel
            elif _uka[0] != 1: _ph = 0
            elif _vl and _vl[0] not in (0x8000, 0xFFFF):
                _v = (_vl[0] - 65536 if _vl[0] > 32767 else _vl[0]) / 10.0
                _ph = 2 if _v >= 19.5 else 1
        if _ph is not None:
            out.append(f"# HELP hoval_kuehl_phase {HELP['hoval_kuehl_phase']}")
            out.append("# TYPE hoval_kuehl_phase gauge")
            out.append(f"hoval_kuehl_phase {_ph}")
            out.append(f"# HELP hoval_kuehl_wartet {HELP['hoval_kuehl_wartet']}")
            out.append("# TYPE hoval_kuehl_wartet gauge")
            out.append(f"hoval_kuehl_wartet {1 if _ph in (1, 2) else 0}")
    except Exception:
        pass
    # Kaeltekreis-Gruppe (R7): nur ausgeben, wenn mindestens ein Punkt antwortet (alle 0 = Regler stumm)
    _kk = {}
    for name, (reg, sc, sg) in KK16.items():
        w = rd(reg)
        _kk[name] = None if (not w or w[0] in (0x8000, 0xFFFF)) else w[0]
    if any(v not in (None, 0) for v in _kk.values()):
        for name, (reg, sc, sg) in KK16.items():
            v = _kk[name]
            if v is None: continue
            if sg and v > 32767: v -= 65536
            if name in HELP: out.append(f"# HELP {name} {HELP[name]}")
            out.append(f"# TYPE {name} gauge")
            out.append(f"{name} {round(v*sc, 3)}")
    for name, spec in R32.items():
        reg, sc = spec[0], spec[1]; sg = len(spec) > 2 and spec[2]
        w = rd(reg, 2)
        if not w or len(w) < 2: continue
        v = (w[0] << 16) | w[1]
        if v == 0xFFFFFFFF:
            if name == "hoval_wp_pumpe_pct": v = 0
            else: continue
        if v == 0x80000000: continue
        if sg and v > 0x7FFFFFFF: v -= 0x100000000
        if _copf and name == "hoval_cop" and not (0 <= v*sc <= 20): continue  # COP-Plausibilitaet
        if name == "hoval_cop" and not _cop_ok: v = 0  # COP-Startfilter
        typ = "counter" if any(k in name for k in COUNTER32) else "gauge"
        if name in HELP: out.append(f"# HELP {name} {HELP[name]}")
        out.append(f"# TYPE {name} {typ}")
        out.append(f"{name} {round(v*sc, 4)}")
    return "\n".join(out) + "\n"

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404); self.end_headers(); return
        data = metrics().encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

class Srv(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True

with Srv(("", 9101), H) as s:
    s.serve_forever()
