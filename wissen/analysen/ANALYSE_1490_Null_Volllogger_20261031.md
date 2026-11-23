# ANALYSE: Reg 1490 = 0 im Volllogger 24.–31.10.2026 – echter Wert oder Artefakt? (Katalog F54, Teilpunkt 2, OR 31.10.2026 ~10:00)

Nur gelesen. Nichts an Anlage, Bus, Bridge, Cron oder Loxone verändert.

## Quellen
- Volllogger `/home/<user>/hoxpi_fulllog/2026-10-24.csv.gz` … `2026-10-29.csv.gz`, `2026-10-30.csv`, `2026-10-31.csv` (Pi <LAN-IP>), 24.10. 00:00:02 – 31.10. 09:55:01, **2148 Zeilen** (Auftrag nannte 2136 = Stand eines früheren Abrufs; 947 Nullen identisch)
- Logger-Code `/home/<user>/hoxpi_fulllog.py` (Cron `*/5`), Bridge-Code `/home/<user>/hoval-bridge/hoval_bridge.py` (Dienst `hoval-bridge.service`, `--enable-write`), Registerkatalog `/home/<user>/hoval-bridge/registers.json`
- Bridge-Journal `journalctl -u hoval-bridge` (volatil, nur seit Boot 30.10.2026 13:28:01)
- Live `mcp__remote-devices__hoxpi__read_register` 1490/1520/1501 am 31.10.2026 ~09:58
- Vorgänger: `[lokaler Pfad]` (F21), `[lokaler Pfad]`
- Skripte: `[lokaler Pfad]` (Zählung/Muster), `_b.py` (Kreuzprüfung 1520/1501/Verdichter), `_c.py` (Journal-SET gegen Volllogger), `_d.py` (Einfrierprüfung 29.10.) – auf dem Pi aus `/tmp/` gelaufen

## Kernbefund
**1490 = 0 ist ein echter Wert: Loxone schreibt 0, wenn der Klimacontroller UG keine Heizanforderung hat** (Formel „1490 inkl. Ofen-Nachlauf“, siehe F21: `IF(I2>0;MAX(I1;24);IF(I1>0;I1;IF(I3>0;MAX(I4;20);0)))`). Kein Logger- und kein Bridge-Artefakt.

| Aussage | Sicherheit | Beleg |
|---|---|---|
| Logger erzeugt keine Null: bei Lesefehler schreibt er `""` (leer), nicht 0 | sicher | `hoxpi_fulllog.py`, Funktion `rd()` → `return ""`; 0 leere 1490-Zellen im Zeitraum |
| Bridge-Datastore 1490 = letzter Loxone-Schreibwert (FC6 → `setValues` → Datastore + CAN-SET); 0 ist ausdrücklich erlaubt (`ZERO_OK_REGS = {1490, 1491, 19482, 23755}`) | sicher | `hoval_bridge.py` Z. 107, 186–192, 527 ff. |
| Ab 30.10. 13:28:28: **246 von 246** Volllogger-Zeilen = letzter Journal-Eintrag „SET reg 1490 <- x“; **70 von 70** Nullen haben ein vorausgehendes „SET reg 1490 <- 0“ | sicher | `_c.py`; 328 SETs, Abstand Median 300 s (= RepeatRate AMQ46), 71× Wert 0, 0× ABGELEHNT |
| Hoval selbst bestätigt die Nullen: bei 935 der 947 Nullen sind auch **1520 (HK-Soll Hoval) = 0 und 1501 (Status HK) = 0 „Abgeschaltet“** | sicher | `_b.py`, Kombi (1490=0,1520=0,1501=0) = 935 |
| Die 12 Abweichungen sind Übergänge bzw. ein CAN-Einfrieren, keine falschen Nullen | sicher (Übergänge) / wahrscheinlich (Einfrieren) | siehe unten |
| Bridge-Startwert 0 (`init = {r: 0 …}`) könnte nach Neustart kurz 0 liefern – im Zeitraum nicht beobachtet (Warm-Cache, kein leerer Block um 30.10. 13:28) | wahrscheinlich | 30.10. 13:25–13:35 keine 1490-Nullzeile im Muster (Block-Liste) |

## Zählungen 24.10. 00:00 – 31.10. 09:55 (5-min-Raster)
- 1490 = 0: **947**, 1490 > 0: 1201, leer: 0. Nicht-Null-Bereich roh 153…327 (15,3…32,7 °C), kein Wert unter Katalog-Min 100.
- Kombination (1490=0 / 1520=0 / 1501=0): 935 alle drei 0; 10× nur 1490=0; 2× 1490=0 und 1501=0, 1520>0; 1193 alle drei > 0; 6× nur 1520=0; 2× 1520=0 und 1501=0, 1490>0.
- Tage (Null/gesamt): 24.: 146/288, 25.: 125/300 (Zeitumstellung), 26.: 111/288, 27.: 194/288, 28.: 161/288, 29.: 114/288, 30.: 50/288, 31.: 46/120.
- Uhrzeit (Null/gesamt): 00 h 87/96, 01 h 89/96, 02 h 88/108, 03 h 56/96, 04 h 26/96, 05 h 6/96, **06 h 0/96**, 07 h 3/96, 08–09 h 13/96, 10–20 h 16–48/84, 21–22 h 65/84, 23 h 75/84 → **klares Nachtmuster**: abends ab 21 h bis 03 h meist keine Anforderung, morgens 05–07 h fast immer Anforderung.
- 31 Null-Blöcke; längster 27.10. 12:40 – 28.10. 03:35 (180 Zeilen = 15 h), weitere lange: 24.10. 20:55–25.10. 03:50 (96), 28.10. 19:10–29.10. 03:30 (101).

### 1490 = 0 während Verdichterlauf (25611 > 0,50 kW; Achtung 25611 hat decimal 2, Rohwert /100)
Verdichter läuft in 674 Zeilen, davon **91 mit 1490 = 0**:
- **79 × 1539 = 4** (WW-Ladung): 1525 steigt dabei bis 57,5 °C (z. B. 24.10. 14:45–15:00, 25.10. 01:15–01:40, 26.10. 16:20–16:40). WW-Ladung läuft unabhängig von der HK1-Anforderung – plausibel und echt (sicher).
- **10 × 1539 = 17** am 29.10. 09:55–10:40: alle CAN-Werte eingefroren (siehe unten).
- **2 × 1539 = 1** (Heizen): 29.10. 10:50 (erste Zeile nach dem Auftauen, 1520/1501 schon 0) und 29.10. 21:25 (25611 = 2,00 kW, 1520=0, 1501=0) → Abschaltmoment: Loxone hat 0 geschrieben, Verdichter läuft im 5-min-Raster noch aus (Vermutung, Raster zu grob).
- Ergebnis: **kein laufender Heizlauf mit 1490 = 0** außer diesen Rand-/Einfrierzeilen (sicher).
- Umgekehrt: von 228 WW-Zeilen (1539=4) haben 81 1490 = 0, 147 1490 > 0 – WW-Ladung setzt 1490 nicht auf 0, die Nullen kommen nur von Loxone.

### Die 12 Ausreißer (1490=0, aber 1520 oder 1501 > 0)
- 25.10. 11:15:02 und 25.10. 23:45:02: 1490 schon 0, 1520 noch 330/350 → nächste Zeile alles 0. **Übergang**: Hoval-Werte sind bis 60 s alt (Rundumabfrage), Loxone-Write sofort im Datastore (sicher).
- 29.10. 09:55:02 – 10:40:01 (10 Zeilen): 1520=345, 1501=23, 1525=39,5, 1539=17, 25611=1,85 kW starr. `_d.py`: von 09:45 bis 10:40 ändern sich je Zeile nur 1–3 Spalten (23632/23633/23634/23627 und **1490**), um 10:45 plötzlich 78 Spalten → **CAN-Werte im Datastore eingefroren (wahrscheinlich CAN-Stall), 1490 aber weiter von Loxone beschrieben**. Der Datastore zeigte in diesem Fenster einen Mix aus aktuellen Loxone-Writes und altem Hoval-Stand. Beginn des Einfrierens vor 09:45 nicht ermittelt.

## 3 Beispielzeilen roh (zeit,1490,1520,1501,1525,1539,25611,1491)
```
2026-10-24 00:00:02,0,0,0,325,0,0,165      Nacht, keine Anforderung, alles 0
2026-10-24 14:45:01,0,0,0,545,4,263,165    WW-Ladung 2,63 kW, HK1-Soll 0 (WW-Vorrang)
2026-10-31 04:45:02,0,0,0,345,0,0,165      Nacht, letzte Nullzeile im Zeitraum
```
Journal-Beleg dazu (30.10.): `2026-10-30 20:59:09 … INFO SET reg 1490 (Flow setpoint constant req. heating) <- 0 (raw)`; Volllogger 30.10. 21:00:02 → 1490 = 0 (erste Zeile des Blocks 21:00–21:20).

## Live 31.10.2026 ~09:58 (nur gelesen)
1490 = 297 (29,7 °C), 1520 = 325 (32,5 °C), 1501 = 23 „Heizbetrieb Extern/Konstantanforderung“. Letzter Journal-Write `2026-10-31 09:57:29 SET reg 1490 <- 297` → Datastore = letzter Loxone-Write (sicher). `read_register` liefert kein reg_age; für 1490 ist das Alter ohnehin das des letzten Loxone-Writes (≤ 300 s).

## Was bringt uns das
- Die 947 Nullen sind **Heizpausen des Klimacontrollers UG** (Loxone-Doku: https://www.loxone.com/dede/kb/klima-controller/), keine Datenlücken. Für Auswertungen: 1490 = 0 als „keine HK1-Anforderung“ werten, **nicht** als fehlenden Wert verwerfen oder interpolieren.
- 44 % Pausenanteil, nachts 21–03 h fast durchgehend: passt zu F21 (Sot 30 %, Räume nachts am Soll) und zur Überdimensionierung. Morgens 05–07 h immer Anforderung (Nachtabsenkung/Morgenaufheizen, wahrscheinlich).
- Robuster Pausenindikator für Skripte: **1501 = 0** (Hoval-seitig) oder 1490 = 0; beide stimmen in 937/947 Fällen überein, Rest = Übergänge.
- Datenqualität: CAN-Einfrieren 29.10. ~09:45–10:40 ist ein separater Fund (betrifft alle Hoval-Register, nicht 1490). Für Auswertungen Zeilen mit „≤ 3 geänderte Spalten über ≥ 3 Zeilen bei laufendem Verdichter“ als stale markieren (vgl. `[lokaler Pfad]`).

## Offen
1. Journal-Beleg (SET <- 0) nur ab 30.10. 13:28 (Journal volatil, Reboot). Für 24.–30.10. stützt sich der Befund auf Code + 1520/1501-Kreuzprüfung (sicher genug). Persistentes Journal wäre eine Option – Entscheidung der Betreiber, nichts geändert.
2. Ursache und Beginn des CAN-Einfrierens 29.10. vormittags (can0-watchdog-Journal nicht mehr vorhanden). Nächster Schritt: Volllogger 29.10. 06:00–09:45 auf Beginn prüfen.
3. Reboot des Pi am 30.10. 13:28 – Ursache nicht geprüft.
4. 29.10. 21:25 (Verdichter 2,0 kW bei 1490=0, 1539=1): Abschaltnachlauf nur Vermutung; mit `ww_hires.csv`/`kuehltest.csv` (1-min) prüfbar.

Status F54/2: **erledigt** (echter Wert, sicher).