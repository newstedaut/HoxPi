# ANALYSE Heiz-Sollwertkette 1490 → 1529 → 1531 gegen Außentemperatur (Orchestrator 22.10.2026 13:00, nur lesend)

Daten: Volllogger `~/hoxpi_fulllog/2026-10-01..22.csv(.gz)` (5 min, 6204 Zeilen, 491 mit Heizanforderung), Außen aus `kuehltest.csv` (1 min),
X26-Mitschnitt `~/rs485_sniff/log/rs485_2026-10-22.log`. Skript/Ausgabe: `[lokaler Pfad]` / `.out`.

## Ergebnisse
| Punkt | Befund | Einstufung |
|---|---|---|
| Überhöhung | 30684/30685 = 3,0 K, an allen 22 Tagen unverändert | sicher |
| 1529 (00-022 HK-Soll) | = 1490 + 2,6…3,0 K, auf **0,5-K-Raster** abgerundet (31,5 → 34,5; 31,4 → 34,0) | sicher (408 von 491 Zeilen; Rest = Übergänge/WW) |
| 18724 (WEZ-Soll Anforderung) | = 1529 in 471 von 491 Zeilen | sicher |
| 1490 gegen Außen | r = **+0,05**, Steigung 0,006 K/K über 2…21 °C | sicher: **keine Heizkurve** |
| 1490 je Tag | Tagesmedian springt 29,4…35,2 °C (z. B. 04.–08.10. ~35, 10.–11.10. ~30,5, 21.10. 29,4) | sicher; Ursache nicht geprüft |
| Muster X26 | Byte n von Obj 0x20 = Datenpunkt 00-0nn = Modbus 1507+n (22 → 1529, 24 → 1531) | wahrscheinlich (2 von 2) |


## Bewertung
- Die Wärmepumpe heizt nicht nach Außentemperatur, sondern nach dem Wert, den Loxone in 1490 („Vorlauf Soll Konstantanforderung") schreibt. Der Wert wechselt tageweise, nicht mit der Außentemperatur.
- Bei 2–10 °C außen reichen derzeit 30–35 °C Vorlauf-Soll. Im Winter (−10 °C) wird ein fester Wert entweder zu knapp (Räume halten nicht) oder im Übergang zu hoch (schlechtere Arbeitszahl).

## Vorschlag (nur Vorschlag, nichts geschrieben)
1. In Loxone prüfen, woher 1490 kommt (Baustein/Formel). Ziel: außentemperaturgeführte Kurve statt Festwert, z. B. **+15 °C → 28 °C, 0 °C → 33 °C, −10 °C → 37 °C** (linear, Fußbodenheizung), plus die vorhandene Raumkorrektur.
2. Danach WEZ-Überhöhung 30684/30685 3,0 → 1,5 K (siehe `ANALYSE_Takt_Heizkurve_20261021.md`) – erst die Kurve, dann die Überhöhung, sonst sieht man nicht, was wirkt.
3. Loop (lesend): Byte 23/25/26 von Obj 0x20 gegen 1530/1532/1533 legen, um das Muster „Byte n = 00-0nn" zu bestätigen.

**Was bringt uns das:** Eine Kurve hebt den Vorlauf nur, wenn es kalt ist. Im Übergang 2–3 K weniger Vorlauf ≈ 5–8 % weniger Heizstrom; im Winter keine kalten Räume durch zu niedrigen Festwert. Byte 22/24 im X26-Mitschnitt liefern die ganze Sollwertkette im 0,5-s-Takt ohne Modbus-Abfrage.