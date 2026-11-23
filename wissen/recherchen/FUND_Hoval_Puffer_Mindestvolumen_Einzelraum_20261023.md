# FUND Hoval UltraSource B comfort C 17 – Puffer, Mindestvolumen, Einzelraumregelung (Orchestrator-Recherche 23.10.2026 13:00)

Hauptquelle: Hoval „Technische Information“ UltraSource B CH-DE 2026/27, https://cdn.hoval.com/ultrasource-b-cf-cp_ch-de_hybris_original.pdf (Schweizer Ausgabe 2026, C17 dort weiter mit R410A). Rechercheagent; Stichprobe Claude per pdftotext (✔ = selbst wortgleich gesehen).

## Belegt (Hoval)
1. ✔ Puffer Pflicht: „ein Energiepufferspeicher zwingend erforderlich (Abtauenergie)“ (S. 37).
2. ✔ Verzicht nur bei direktem Kreis mit konstanter Durchflussmenge, „(⅔ müssen unabsperrbar sein)“ (S. 37).
3. ✔ Tabelle „Empfohlene Mindestgrössen Energiepufferspeicher“: UltraSource B comfort C (17) → EnerVal **300** (C8/C11 nur 100) (S. 38).
4. Mindestgrößen enthalten laut Hoval Mindestlaufzeiten und Abtauenergie; EVU-Sperrvolumen extra (S. 37/39, Agent).
5. ✔ „lässt maximal 3 Starts pro Stunde zu“ (Anwendungsbeispiele S. 49/50, Sole-WP); EW-Begrenzung 3×/h (S. 48, Agent).
6. Einzelraumregelung: FBH ohne Thermostatventile erfüllt die Anforderung, sonst Entkopplung über Puffer; Split-Checkliste: Direkteinbindung nur mit Differenzdruck-Überströmventil + Vorschaltgefäß (S. 42/48/49, Agent).
7. C17 Nenn-Heizwassermenge 2,2 m³/h (ΔT 5 K, A7W35), max. 3,7 m³/h, Restförderhöhe 37 kPa (S. 17, Agent). Kein Mindestvolumenstrom genannt.
8. Puffer-Abgleich: Durchfluss im voll geöffneten Heizkreis darf nicht größer sein als im Speicherkreis, sonst Mischtemperaturen im VL (S. 43, Agent).
9. Modulation C17 A2W35 7,4–17,4 kW; >12 m Kältemittelleitung → Mindestdrehzahl 40 % (S. 7/35, Agent; deckt sich mit FUND_C17_Leistung… ✔ früher geprüft).

## Wahrscheinlich
- EnerVal = Hovals Energiepufferspeicher → EnerVal 300 = Puffer, CombiVal ESR 400 = WW (deckt sich mit `ANALYSE_Speicherrollen_Volumen_aus_Messdaten_20261023.md` und FUND_EnerVal_CombiVal…). Puffer läge dann **genau auf dem Hoval-Minimum**.
- Hoval-Standard = Trennspeicher (hydraulische Entkopplung), kein Reihenspeicher im Rücklauf.

## Nicht gefunden
- Mindestanlagenvolumen ohne Puffer (l/kW), Mindestvolumenstrom, Abtauenergie in kWh, Mindestlaufzeit in min / max. Starts pro Tag.
- AT-Planungsunterlage 2021 und Montage-/Bedienungsanleitung nicht lesbar (BlobNotFound / Proxy).

## Vergleich (nicht Hoval, Agent, ungeprüft)
Viessmann Vitocal 200-S/-A: 50 l Mindestvolumen, 1400 l/h. Daikin Altherma 3 Split: 20 l + Überströmventil. Stiebel WPL 13/18/23: Puffer v. a. für Abtauung, ohne Puffer Kreise offen lassen / Überströmventil, 0,4–0,6 m³/h.

## Was bringt uns das
1. Typenschilder klären; ist EnerVal 300 der Puffer, ist kein Zusatzvolumen gegen Takten eingeplant.
2. Prüfen, ob die HK-Grundfos-Pumpen mehr fördern als der WP-/Speicherkreis (≤ 2,2 m³/h) – sonst Mischtemperatur im VL, frühere RL-Abschaltung.
3. Starts (≈ 7/Tag) weit unter 3/h – Hebel bleibt Laufzeit je Start (Führungsraum offen lassen, Mindestlaufzeit ab Verdichterstart).