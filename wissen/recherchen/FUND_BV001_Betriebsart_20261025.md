# FUND F30 – Bedeutung BV001 = 4 / BV011 = 3 (Bivalenz, HAICO V1.18.004)
Orchestrator-Recherche 25.10.2026 04:55–05:15 MEZ (Claude, nur öffentliche Seiten, keine Downloads). Katalog: F30 (Teil von F12).

## Belegt (Quelle wörtlich geprüft)
- **Die BV-Codes sind iDM-Navigator-Parameter.** iDM-Anleitung „TERRA Wärmepumpen mit Navigatorregelung 1.7“, Kap. 4.1.5 Bivalenz:
  „BV002 Bivalenzpunkt 1 (0°C)“, „BV003 Bivalenzpunkt 2 (-10°C)“, Bereich „-20°C bis +20°C“.
  Quellen: https://www.manualslib.de/manual/242350/Idm-Energiesysteme-Terra.html?page=20 , https://silo.tips/download/terra-wrmepumpen-mit
  → Gleiche Namen wie in unserer HAICO-Firmware (BV002/BV003). Werkswerte Navigator 0 / -10 °C, **bei uns live -10 / -20 °C** (X26 0x8702/0x8703) = von Hoval/Inbetriebnahme abweichend gesetzt (sicher für Live-Wert, Herkunft wahrscheinlich pax-Vorgabe).
- **Bivalenzstrategien im Navigator** (1.7 und 2.0, S. 53): „Parallel“ (unter BP1 zweiter Wärmeerzeuger dazu, wenn WP die Soll-VL über eine gewisse Zeit nicht erreicht), „Alternativ“ (unter BP1 WP nicht mehr angesteuert), „Parallel/Alternativ“ (unter BP1 parallel, unter BP2 nur noch zweiter Wärmeerzeuger). Zusätzlich Notbetrieb „Nur Bivalenz“ bei verriegelnder WP-Störung.
  Quelle: https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- Der Strategie-Parameter selbst (Code, Nummerierung) steht in **keiner** der Anleitungen; „Die einstellbaren Parameter richten sich nach der Maschinenkonfiguration“ (Terra 1.7, S. 20).

## Wahrscheinlich / Vermutung
- **Vermutung:** BV001 ist die Bivalenz-Konfiguration/-Strategie als Aufzählung. Navigator kennt 3 Strategien + „keine“ (+ evtl. „Nur Bivalenz“/3. Wärmeerzeuger) – das passt zur Zahl der Werte 0..4 im X26-Katalog (V1.18). Die V1.11-Logik (1 → BV002, 2 → BV003, sonst Merker 0) passt **nicht** 1:1 auf die Navigator-Semantik; Zuordnung 4 = ? bleibt offen.
- **Folge für uns:** Eine Strategie „Alternativ“ oder „Parallel/Alternativ“ würde unter BP1/BP2 die **WP abschalten** (nicht nur Stab zuschalten). Mit BP -10/-20 °C wäre das in Alpenort (~960 m) nur in seltenen Frostnächten relevant – aber genau das soll der W3-Wächter beobachten (V103d: WP-Lauf und Stab bei AT < -10 und < -20 °C notieren).
- BV011 = 3: nichts öffentlich gefunden (Argon-Altbestand nennt „Heizstab-Freigabe für Abtauung 0..1“, ungeprüft).

## Nicht gefunden
- BV001, BV007..BV011 als Codes: weder Terra 1.7, Navigator 2.0 noch AERO-ALM-Montageanleitung (siblik.com IDM193401…AERO ALM 2-8.pdf) nennen sie. docplayer-Kopie Navigator 2.0 per robots gesperrt.
- Suchen: 6 (2 standard, 3 extended, 1 standard Modbus) – „öffentlich nicht auffindbar“ für die Werte 3/4 (Stand 25.10.2026).

## Was bringt uns das