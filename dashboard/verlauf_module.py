#!/usr/bin/env python3
"""Standalone-Modul: verlauf_page() und verlauf_api_handler()
Wird von hoval_status.py importiert über:
  from verlauf_module import verlauf_page, verlauf_api_handler
"""
import json, re, time

PROM = "http://127.0.0.1:9090"

METRICS = [
    ("hoval_vorlauf_c",      "Vorlauf °C",   "Flow °C",     "#e2001a"),
    ("hoval_ruecklauf_c",    "Rücklauf °C", "Return °C","#c2185b"),
    ("hoval_aussentemp_c",   "Außentemp °C","Outdoor °C","#41bdf5"),
    ("hoval_ww_ist_c",       "WW-Ist °C",    "DHW actual °C","#ff9800"),
    ("hoval_p_el_kw",        "Leistung el. kW",   "Power el. kW",    "#555"),
    ("hoval_p_th_kw",        "Leistung th. kW",   "Power th. kW",    "#69b41e"),
    ("hoval_cop",            "COP",               "COP",             "#9c27b0"),
    ("hoval_modulation_pct", "Modulation %",      "Modulation %",    "#607d8b"),
]


def verlauf_api_handler(q):
    """Gibt (status, body_bytes, content_type) zurück."""
    import urllib.request as ur
    metric = (q.get("metric", [""])[0] or "").strip()
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', metric):
        return 400, b'{"error":"bad metric"}', "application/json"
    hours = max(1, min(720, int(q.get("hours", ["24"])[0])))
    end   = int(time.time())
    start = end - hours * 3600
    step  = max(60, hours * 3600 // 300)
    url   = f"{PROM}/api/v1/query_range?query={metric}&start={start}&end={end}&step={step}"
    try:
        with ur.urlopen(url, timeout=5) as r:
            raw = r.read()
        return 200, raw, "application/json"
    except Exception as e:
        return 502, json.dumps({"error": str(e)}).encode(), "application/json"


def verlauf_page(lang="de"):
    """Gibt HTML-Body-String zurück (lang = "de" | "en")."""
    en = (lang == "en")
    metrics_js = json.dumps([
        {"m": m, "label": (len_ if en else lde), "color": col}
        for m, lde, len_, col in METRICS
    ])
    t_title = "History" if en else "Verlauf"
    t_sub = ("Temperatures, power and COP of the last 24&nbsp;h / 7&nbsp;days / 30&nbsp;days." if en
             else "Temperaturen, Leistung und COP der letzten 24&nbsp;h / 7&nbsp;Tage / 30&nbsp;Tage.")
    j_nodata = "No data" if en else "Keine Daten"
    j_loading = "Loading data\u2026" if en else "Lade Daten\u2026"
    j_updated = "Updated: " if en else "Aktualisiert: "
    j_error = "Error: " if en else "Fehler: "
    return f"""<h1>&#128200; {t_title}</h1>
<p style="color:#6c7787;margin:.2rem 0 1.2rem">{t_sub}</p>

<div style="display:flex;gap:.5rem;margin-bottom:1.2rem;flex-wrap:wrap">
  <button onclick="vload(24)"  id="b24"  class="rbtn act">24 h</button>
  <button onclick="vload(168)" id="b168" class="rbtn">7 d</button>
  <button onclick="vload(720)" id="b720" class="rbtn">30 d</button>
</div>

<style>
.rbtn{{padding:.4rem 1.1rem;border:2px solid #dde2ec;border-radius:8px;background:#fff;
      cursor:pointer;font-weight:600;font-size:.92rem;color:#555;transition:all .15s}}
.rbtn.act{{border-color:#e2001a;background:#e2001a;color:#fff}}
.vgraph{{background:#fff;border-radius:12px;box-shadow:0 1px 4px #0001;
         padding:1rem 1.2rem 1.2rem;margin-bottom:1rem}}
.vgraph h3{{margin:0 0 .6rem;font-size:1rem;color:#1c2531}}
svg.vchart text{{font-family:system-ui,sans-serif;font-size:11px;fill:#6c7787}}
</style>

<div id="vcharts"></div>
<div id="vstat" style="color:#aaa;font-size:.85rem;margin-top:.5rem"></div>

<script>
var VMETRICS={metrics_js};
var vcur=24;
function vfmt(ts,hours){{
  var d=new Date(ts*1000);
  if(hours<=24) return d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0');
  return (d.getDate()).toString().padStart(2,'0')+'.'+(d.getMonth()+1).toString().padStart(2,'0')+' '+d.getHours().toString().padStart(2,'0')+'h';
}}
function vdraw(area,values,color,hours){{
  if(!values||values.length<2){{area.innerHTML='<span style="color:#aaa;font-size:.85rem">{j_nodata}</span>';return;}}
  var W=Math.max(300,area.getBoundingClientRect().width||600),H=130;
  var PADl=42,PADr=10,PADt=8,PADb=26;
  var iW=W-PADl-PADr,iH=H-PADt-PADb;
  var nums=values.map(function(v){{return parseFloat(v[1]);}}).filter(Number.isFinite);
  var mn=Math.min.apply(null,nums),mx=Math.max.apply(null,nums),rng=mx-mn||1;
  mn-=rng*.05;mx+=rng*.05;rng=mx-mn;
  var ts0=parseFloat(values[0][0]),ts1=parseFloat(values[values.length-1][0]),tsR=ts1-ts0||1;
  function px(ts){{return PADl+((parseFloat(ts)-ts0)/tsR)*iW;}}
  function py(v) {{return PADt+iH-((parseFloat(v)-mn)/rng)*iH;}}
  var pts=values.map(function(v){{return px(v[0]).toFixed(1)+','+py(v[1]).toFixed(1);}}).join(' ');
  var ticks='',xticks='';
  for(var i=0;i<=4;i++){{
    var tv=mn+rng*i/4,ty=py(tv).toFixed(1);
    ticks+='<line x1="'+PADl+'" x2="'+(PADl+iW)+'" y1="'+ty+'" y2="'+ty+'" stroke="#eee" stroke-width="1"/>';
    ticks+='<text x="'+(PADl-4)+'" y="'+(parseFloat(ty)+3.5).toFixed(1)+'" text-anchor="end">'+tv.toFixed(1)+'</text>';
  }}
  for(var j=0;j<=4;j++){{
    var xts=ts0+tsR*j/4,xpx=(PADl+j/4*iW).toFixed(1);
    xticks+='<text x="'+xpx+'" y="'+(H-6)+'" text-anchor="middle">'+vfmt(xts,hours)+'</text>';
  }}
  var last=nums[nums.length-1];
  area.innerHTML='<svg class="vchart" width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'">'
    +ticks+xticks
    +'<polyline points="'+pts+'" fill="none" stroke="'+color+'" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>'
    +'<text x="'+(W-PADr)+'" y="'+(PADt+11)+'" text-anchor="end" font-weight="700" fill="'+color+'" font-size="12">'+last.toFixed(2)+'</text>'
    +'</svg>';
}}
function vload(hours){{
  vcur=hours;
  ['b24','b168','b720'].forEach(function(id){{document.getElementById(id).classList.remove('act');}});
  document.getElementById(hours===24?'b24':hours===168?'b168':'b720').classList.add('act');
  var box=document.getElementById('vcharts');
  box.innerHTML='';
  document.getElementById('vstat').textContent='{j_loading}';
  var done=0;
  VMETRICS.forEach(function(m){{
    var wrap=document.createElement('div');wrap.className='vgraph';
    var h3=document.createElement('h3');h3.textContent=m.label;wrap.appendChild(h3);
    var area=document.createElement('div');area.style.width='100%';wrap.appendChild(area);
    box.appendChild(wrap);
    fetch('/api/verlauf_data?metric='+m.m+'&hours='+hours)
      .then(function(r){{return r.json();}})
      .then(function(d){{
        var res=d.data&&d.data.result&&d.data.result[0];
        vdraw(area,res?res.values:null,m.color,hours);
        if(++done===VMETRICS.length) document.getElementById('vstat').textContent='{j_updated}'+new Date().toLocaleTimeString();
      }})
      .catch(function(e){{area.textContent='{j_error}'+e;done++;}});
  }});
}}
window.addEventListener('load',function(){{vload(24);}});
window.addEventListener('resize',function(){{vload(vcur);}});
</script>"""
