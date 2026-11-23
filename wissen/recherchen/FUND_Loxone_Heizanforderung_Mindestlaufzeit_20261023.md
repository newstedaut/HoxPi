# FUND Loxone Heizanforderung Mindestlaufzeit (23.10.2026)
Orchestrator-Rechercheagent 23.10.2026 ~11:00, nur öffentliche Seiten. Prüfvermerk Claude: EN-KB https://www.loxone.com/enen/kb/climate-controller/ per WebFetch selbst gelesen – MinHr (min, Default 0), Sot (%, Default 30), MaxTp (%, Default 0 = aus) und 3-min-Sperre nach Abschalten wortgleich ✓. DE-Seite /dede/kb/klima-controller/ lieferte beim Gegenlesen nur „vorübergehend nicht verfügbar“. Forenzitate ungeprüft.
**Wichtig (Projektdatei, Orchestrator):** Bei der Betreiber steht MinHr am Klimacontroller HC1 schon seit 08./11.10. auf 40 min – siehe `HoxPi-Doku\ANALYSE_Loxone_MinHr40_Startverzug_20261023.md`.

## Belegt
**Klimacontroller / „Heiz- und Kühlsteuerung“** (https://www.loxone.com/dede/kb/klima-controller/, EN https://www.loxone.com/enen/kb/climate-controller/)
- Ausgang H (0/1), Entscheidung „abhängig von den Anforderungen der zugewiesenen Intelligenten Raumregler“.
- **MinHr** (min, Standard 0): Mindestlaufzeit vor Wechsel in Standby; „Mindestöffnungen der Raumregler werden sichergestellt“.
- **Sot** (%, Standard 30): durchschnittliche Ventilöffnung muss Sot überschreiten → nur für den **Start**.
- **MaxTp** (%, Standard 0 = aus): darunter Takten mit Don 750 s / Doff 300 s.
- Nach Abschalten von H/C: zusätzlich zu Fod **3 min Sperre** – kein einstellbarer Mindeststillstand.
- Mh: Heizung bleibt aktiv, bis MinHr erreicht. Eh: IRR dürfen überheizen (ϑExc).
- Bedarf je Raum = (Ziel − Ist) × Raumgröße [°m²]; kein Parameter „Anzahl Räume“.

**Intelligente Raumregelung** (https://www.loxone.com/dede/kb/intelligente-raumregelung/)
- Mindestöffnung wird erzwungen, bis die Quelle nach Ablauf der Mindestlaufzeit aus ist.
- Pwm (Standard 0 = auto, 10–60 min). ϑd 1,5 K nur Heiz/Kühl-Umschaltung, keine Heiz-Hysterese. ϑExc 1 K.

**LoxForum** (ungeprüft)
- 310713: Heizlast springt zwischen 0 % und > 30 %; mit MinHr > 0 unter V13 Ventile im Sekundentakt auf/zu. https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/310713-12-1-klimacontroller-mischerkreis-taktet-bei-geringer-anforderung-permanent
- 458073: WP-Taktung – Puffer, größere Hysteresen, SG-Ready abhängig vom Klimacontroller. https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/458073
- 464929: Ausschaltverzögerung hinter Ausgang H. https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/464929

## Wahrscheinlich
- Für das Abschalten von H gibt es keine eigene Schwelle; MinHr ist der einzige eingebaute Nachlauf.
- Sot 30 → 40 % startet seltener mit mehr Bedarf (längere Läufe, etwas mehr Raumschwankung).
- Monoflop/Ausschaltverzögerung hinter H hält die WP am Laufen, auch wenn IRR-Ventile schon zu sind → Hydraulik/Mindestdurchfluss prüfen.

## Nicht gefunden
- Einstellbarer Mindeststillstand, Ausschaltschwelle/-hysterese am Klimacontroller; Heiz-Hysterese in der IRR.
- KB-Seiten zu Ausschaltverzögerung/Schwellwertschalter (Website nach Cyberangriff teils offline); Monoflop-Seite derzeit leer.
- Offizielle Loxone-Empfehlung WP + Takten; Wirkung „Heizungstyp = Wärmepumpe“.

## Konkreter Vorschlag (angepasst an den Ist-Stand MinHr 40)
1. MinHr HC1 40 → **60 min**, MaxTp 0 lassen.
2. Optional Sot 30 → 40 %, 1–2 Wochen messen (Starts, Laufdauer, Raumtemperatur).
3. Nach Umstellung IRR-Stellantriebe in der MinHr-Phase beobachten (Forum-Fehlerbild).
4. Alternativ Monoflop (https://www.loxone.com/dede/kb/monoflop/) ab echtem Verdichterstart, 40 min, ODER mit H.
5. Eh bei PV-Überschuss ist bereits verdrahtet („Smart Grid Auslösen“, laut Baustein-Notiz).