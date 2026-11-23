# Vorher/Nachher Umbau 23.10.2026 – Zwischenstand nach 20 h (24.10.2026 17:15)

Nur gelesen. Quellen: Prometheus 1-min-Export vom HoxPi (`[lokaler Pfad]`, erzeugt mit `[lokaler Pfad]`), Auswertung `[lokaler Pfad]`, Volllogger-Kopien im selben Datenordner, Loxone-MCP Klimacontroller UG, Raumlogger `[lokaler Pfad]`.

- **Vorher:** 16.10. 17:00 – 23.10. 17:00 (7,0 Tage, Außen-Mittel 10,3 °C, 67,6 Kd)
- **Nachher:** 23.10. 21:24 – 24.10. 17:14 (0,83 Tage, Außen-Mittel 6,4 °C, 11,2 Kd)
- Heizgradstunden: Σ max(0; 20 − T_außen) je Minute → Kd. Nachher ist pro Tag **40 % kälter** (13,6 statt 9,7 Kd/d).
- Lauf = zusammenhängender Block `wez_status` ∈ {1, 4, 51}; Art nach Mehrheit (1 Heizen, 4 WW). Strom/Wärme = ∫ p_el / p_th ([Nummer]) über 1 min. Gegenprobe gegen Zähler: el 82 / 11 kWh (Integral 79,5 / 11,1) – passt.

| Kennzahl | Vorher (7 d) | Nachher (20 h) | Sicherheit |
|---|---|---|---|
| Verdichterstarts/Tag (Zähler) | 8,0 | 9,7 | sicher gemessen |
| Starts je Kd (Zähler) | 0,83 | 0,71 | wahrscheinlich besser, n = 8 |
| Heizläufe/Tag · je Kd | 3,4 · 0,36 | 6,0 · 0,45 | sicher gemessen |
| Heizlauf Mittel / Median | 31 / 25 min | 33 / 34 min | Vermutung (5 Läufe) |
| Kurzläufe < 20 min | 7 (1,0/d) | 0 | wahrscheinlich besser |
| WW-Läufe/Tag, Mittel | 4,0, 41 min | 3,6, 44 min | Abend fehlt noch |
| Strom kWh/Tag | 11,4 | 13,5 | sicher, aber kälter |
| Heizstrom je Kd | 0,32 kWh | 0,47 kWh | siehe Text |
| WW-Strom/Tag | 8,2 kWh | 7,1 kWh | Vermutung (Abend fehlt) |
| AZ gesamt / Heizen / WW | 3,50 / 4,70 / 3,04 | 3,60 / 4,48 / 2,81 | Außentemperatur erklärt |
| Kühlanforderung / Kühlphase | 0 min | 0 min (demandCool 0) | sicher |
| Raum 1510 Minuten < 21,0 °C | 209 min/d | 109 min/d | wahrscheinlich besser |

## Was man schon sieht
2. **Mehr Heizwärme ist gewollt, kein Verlust (wahrscheinlich):** Heizwärme je Kd 1,50 → 2,10 kWh. Vorher waren die Räume durch die Kühlfalle zeitweise zu (1510 an 1466 min unter 21 °C). Jetzt wird wieder geheizt – das kostet Strom, ist aber Komfort.
3. **Keine Kurzläufe mehr (wahrscheinlich):** 5 Heizläufe 23–44 min, kein Lauf < 20 min. Ob das MinHr 60 ist oder Zufall, zeigen erst 7 Tage.
4. **Arbeitszahlen (sicher gemessen, nicht bewertbar):** Heizen 4,70 → 4,48 und WW 3,04 → 2,81 passt zu 4 K kälterer Luft. Kein Effekt der Änderungen ablesbar.

## Was nach 1 Tag NICHT geht
- **WW-Verschiebung:** Die Ladung um 05:27 gab es trotzdem – das war keine Kalenderladung, sondern Hysterese (oben 45,1 °C, Soll 50). 10:36 ebenso (46,5 °C). Die 13–16-Uhr-Ladung kam 14:26 (52 °C, 41 min). Ob die Morgenladung im Schnitt wegfällt: offen.
- **PV-Regel, Boost 57, Heizstab-Legionellen (So 12–16):** noch nicht gelaufen bzw. kein Prognosetag ≥ 20 kWh im Fenster.
- **Strom/Tag und Starts/Tag:** n = 8 Starts, Kälteeinbruch, Wochenende – Streuung größer als jeder erwartete Effekt (MinHr: −0,4…0,6 Starts/d).

## Beobachtung (Vermutung)
Die WW-Ladung 14:26–15:07 fällt in die Heizphase am Nachmittag: WZ fiel bis 20,9 °C (Loxone 15:56), 1510 bis 20,7 °C. Bei WW-Vorrang steht die Heizkreispumpe. Mit kälteren Tagen beobachten.

## In 7 Tagen erneut prüfen (ab 31.10.)
1. Skript erneut laufen lassen (Export neu ziehen), Nachher = 23.10. 21:24 – 30.10. 21:24.
2. Starts je Kd und Heizläufe < 20 min gegen Vorher; Heizlauf-Median ≥ 35 min?
3. WW-Starts nach Uhrzeit: Anteil 03–08 Uhr (vorher 8 von 28) und 13–16 Uhr.
4. WW oben min 18–22 Uhr jeden Abend ≥ 45 °C? Abendcheck ausgelöst?
5. WW-Strom/Tag und WW-AZ bei vergleichbarer Außentemperatur (Tage mit gleichem Kd vergleichen).
6. Sonntag 25.10. 12–16: Heizstab-Legionellen gelaufen? (PV-Heizstab im Speicher taucht in 25611 nicht auf → Nachweis über WW oben 1500 / SF2 und Loxone-Ausgang)
7. WZ-Minimum am Nachmittag während der WW-Ladung.

## Abschluss volle Woche (Claude, 31.10.2026 18:10)
Unabhängige Stichprobe cc_vn_stichprobe_20261031.py gegen C:\\Users\\<user>\\Claude\\data\\vorhernachher_20261024\\vn_export_20261024.csv (Stand 31.10. 06:57) bestätigt Argons MD-01-Wochenvergleich exakt:
vorher 16.–23.10. 17:00: 52 Läufe (24 H / 28 WW), 7 Kurzläufe, Heizen Median 24,5 min, 79,53 kWh, 67,59 Kd → 1,18 kWh/Kd; nachher 24.–30.10.: 80 Läufe (54 H / 26 WW), 7 Kurzläufe, Heizen Median 30,5 min, 117,88 kWh, 93,33 Kd → 1,26 kWh/Kd. [sicher]
Nächster Hebel: 07-001 von 3 K auf 2 K (MD-03/MD-04), Entscheidung der Betreiber, Rückweg 3 K, Abnahme: Δ WP-VL − HK1-Soll am Laufende sinkt von ~8,7 auf ~7,7 K, Unterdeckung HK1 < 2 % der Heizminuten.