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
 "hoval_wasserdruck_bar": (18738, 0.1, True),
 "hoval_p_el_kw": (25611, 0.01, True),
 "hoval_p_th_kw": (25612, 1, True),
 "hoval_modulation_pct": (18726, 1, False),
 "hoval_hc1_status": (1501, 1, False),
 "hoval_hc2_status": (1502, 1, False),
 "hoval_ww_status": (1504, 1, False),
 "hoval_wp_detailstatus": (18723, 0.1, False),
 "hoval_sg_status": (27537, 1, False),
 "hoval_sg_befehl": (27545, 1, False),
 "hoval_offset_ww_k": (27509, 0.1, False),
 "hoval_offset_hk1_k": (27528, 0.1, False),
 "hoval_offset_kk1_k": (27531, 0.1, False),
 "hoval_uka": (19870, 1, False),
}
# name -> (highreg, scale)
R32 = {
 "hoval_cop": (31667, 0.1),
 "hoval_energie_el_mwh": (25613, 0.001),
 "hoval_waerme_heizen_mwh": (27484, 0.001),
 "hoval_waerme_ww_mwh": (27488, 0.001),
 "hoval_schaltzyklen": (1518, 1),
}
HELP = {
 "hoval_hc1_status": "0=Aus 1..3=Heizen 9..11=Kuehlen 12=Stoerung 26=SmartGrid",
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
    for name, (reg, sc, sg) in R16.items():
        w = rd(reg)
        if not w: continue
        v = w[0]
        if v in (0x8000, 0xFFFF): continue
        if sg and v > 32767: v -= 65536
        if name in HELP: out.append(f"# HELP {name} {HELP[name]}")
        out.append(f"# TYPE {name} gauge")
        out.append(f"{name} {round(v*sc, 3)}")
    for name, (reg, sc) in R32.items():
        w = rd(reg, 2)
        if not w or len(w) < 2: continue
        v = (w[0] << 16) | w[1]
        typ = "counter" if "mwh" in name or "zyklen" in name else "gauge"
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
