# ANALYSE F7: Legionellenschaltung 05-017 (Stand 23.10.2026, 21:57)

Lauf: Orchestrator, nur lesend (HoxPi-MCP read/search, Volllogger per `hoxpi_ssh.py`, Datenpunktliste per openpyxl). Nichts an der Anlage geschrieben.
Hilfsskripte: `[lokaler Pfad]`, `[lokaler Pfad]`, `[lokaler Pfad]` (auf dem Pi als `/tmp/or_f7.awk`, `/tmp/or_f7.sh`).

## Kurzantwort
- **05-017 ist über Modbus nicht lesbar** (sicher): weder im HoxPi-Katalog (`search_registers` „Legionell“, „Legionella“, „legio“ = 0 Treffer) noch in der offiziellen Liste `[lokaler Pfad] Heating & Cooling\Hoval Modbus Datenpunktliste Stand April 2026 (1).xlsx` (alle Blätter, Filter „legionel|05-017|antileg|desinf“ = 0 Treffer). Wochentag/Uhrzeit/Temperatur also **nur am Bediengerät** ablesbar.
- **Hoval-Legionellenlauf in 4 Wochen: keiner** (wahrscheinlich). Volllogger 25.09.–23.10.2026: WW-Soll (Reg 1499) war an **keinem** Tag über 57,0 °C (SG-Wert). Eine aktive Wochen-Schaltung hätte 4× einen Soll ≥ 60 °C erzeugen müssen. → 05-017 ist sehr wahrscheinlich **aus** (oder hebt 1499 nicht an, Restunsicherheit).
- **Ist ≥ 60 °C gab es** 25.09.–01.10. täglich nachmittags (max. 61,9 °C), aber bei Soll 54,8–57 °C und UKA (19870) = 0 → nicht von der WP/Hoval, **wahrscheinlich PV-Heizstab** im Speicher. **Seit 02.10. (3 Wochen) nie mehr ≥ 60 °C**, Maximum 57,3 °C.
- **Reicht das bei 52 °C?** Die Hoval-Funktion liefert nichts. Abgesichert ist der Speicher erst durch die neue Loxone-Legionellenlogik (Heizstab So 12–16, Ziel 59 °C, umgesetzt 23.10.) – erster Lauf **So 25.10.2026**, noch nicht abgenommen. Zirkulationsleitung und Zirk-Rücklauf bleiben ungeprüft.

## Parameter (Live 23.10.2026, gelesen ca. 21:57 über HoxPi-MCP)
| Nummer | Name | Live-Wert | Uhrzeit | Quelle | Sicherheit |
|---|---|---|---|---|---|
| 05-017 | Legionellenschaltung (aktiv/Tag/Uhrzeit/Temp.) | **nicht lesbar** | – | HoxPi-Katalog + offizielle Datenpunktliste: kein Datenpunkt | sicher (nicht exponiert) |
| Reg 1499 | Warmwasser-Soll (berechnet) | 50,0 °C | 21:57 | `read_register` | sicher |
| Reg 1500 | Warmwasser-Ist SF (oben) | 51,5 °C | 21:57 | `read_register` | sicher |
| Reg 27483 | Warmwasser-Ist SF2 (Abschaltfühler) | 48,7 °C | 21:57 | `read_register` | sicher |
| Reg 1504 | Status Warmwasserregelung | 0 = Abgeschaltet | 21:57 | `read_register` | sicher |
| Reg 1497 | Normal-WW-Temperatur | 50,0 °C | 21:5x | `search_registers` | sicher |
| Reg 1498 | Spar-WW-Temperatur | 45 °C | 21:5x | `search_registers` | sicher |
| Reg 1496 | Betriebswahl WW | 4 | 21:5x | `search_registers` | sicher |

Hinweis: Die Enum von Reg 1504 (offizielle Liste) kennt **keinen** Zustand „Legionellen“ (0–8, 12, 13). Ein Legionellenlauf ist also auch über den Status nicht direkt erkennbar, nur indirekt über den Soll (1499).
Hinweis 2: Reg 1504 war im Volllogger in allen Trefferzeilen 0, auch während Ladungen – als Indikator ungeeignet (Vermutung: WEZ meldet nur grob).

## Volllogger 25.09.–23.10.2026 (`~/hoxpi_fulllog/`, 5 min, Rohwert ×10)
Alle 29 Tage vorhanden (je 288 Zeilen, 23.10. bis 21:55 = 264). Suchkriterium: 1499 ≥ 58,0 °C **oder** 1500 ≥ 58,0 °C.

**A) Soll ≥ 58 °C (= Hoval-Legionellenlauf): keiner.** max(1499) je Tag: 25.09.–01.10. und 03.–23.10. jeweils 57,0 °C; Werte dazwischen 54,6–55,9 und 50/52 °C. Belegt: **kein** Hoval-Legionellenlauf im Zeitraum.

**B) Ist ≥ 60 °C (Speicher tatsächlich ≥ 60 °C):**
| Datum | Wochentag | Zeitraum 1500 ≥ 60 °C (ca.) | max 1500 | max 27483 | Soll 1499 dabei | UKA 19870 | Deutung |
|---|---|---|---|---|---|---|---|
| 25.09. | Fr | 14:40–19:05 | 61,7 °C (15:10) | 61,9 °C | 55,9 → 50,0 | 0 | PV-Heizstab (wahrscheinlich) |
| 26.09. | Sa | 14:30–>16:50 | 61,9 °C (14:50) | 61,9 °C | 54,8 | 0 | dto. |
| 27.09. | So | 15:45–>17:50 | 61,4 °C (16:20) | 61,7 °C | 57,0 | 0 | dto. |
| 28.09. | Mo | 14:20–18:50 | 61,7 °C (15:10) | 61,9 °C | 57,0 → 50,0 | 0 | dto. |
| 29.09. | Di | 17:00–21:40 | 61,7 °C (17:25) | 62,0 °C | 57,0 → 50,0 | 0 | dto. |
| 30.09. | Mi | 15:55–>16:20 | 61,9 °C (16:20) | 62,0 °C | 54,6 | 0 | dto. |
| 01.10. | Do | 15:05–16:45 | 61,7 °C (15:30) | 61,9 °C | 54,8 | 0 | dto. |
| 02.10.–23.10. | – | **nie** | 58,9 °C am 02.10. 00:15 (Restwärme 01.10.), ab 03.10. ≤ 57,3 °C | ≤ 56,4 °C | 50–57 | – | keine 60 °C mehr |

(„–>“: Ende im Trefferfenster des Skripts abgeschnitten, Ende nicht genau bestimmt.)
Deutung „PV-Heizstab“: Ist liegt bis 7 K über dem Hoval-Soll, Umschaltventil 19870 = 0 (kein WW-Betrieb der WP), immer nachmittags 14–18 Uhr → wahrscheinlich, nicht direkt gemessen (kein Heizstab-Signal im Volllogger geprüft).

## Bewertung: Reicht es, wenn das WW-Soll abends auf 52 °C sinkt?
| Aussage | Sicherheit | Beleg |
|---|---|---|
| Die Hoval-Legionellenschaltung 05-017 hilft derzeit nicht: in 4 Wochen kein Soll ≥ 58 °C. | wahrscheinlich (05-017 selbst nicht lesbar) | Volllogger 1499, Abschnitt A |
| Seit 02.10. war der Speicher nie ≥ 60 °C; Desinfektion fand 3 Wochen lang nicht statt. | sicher (für Fühler SF/SF2) | Volllogger 1500/27483 |
| 52 °C liegt im EFH (DVGW W 551 „Kleinanlage“) über der Untergrenze 50 °C, unter der Empfehlung 60 °C; keine Rechtspflicht für private EFH. | wahrscheinlich (Normtext nur über Sekundärquellen) | `[lokaler Pfad]` |
| Mit 52 °C + wöchentlich ≥ 60 °C im ganzen Speicher ist der **Speicher** hygienisch vertretbar. | wahrscheinlich | dto., energiesparhaus.at / ÖNORM-Sekundärzitat |
| Die neue Loxone-Logik (Heizstab So 12–16, 2-Punkt-Ziel 59 °C) erfüllt das nur knapp: 59 °C < 60 °C, und der Heizstab sitzt oben → unterer Speicherteil wird wahrscheinlich nicht 60 °C. | Vermutung (Lage Heizstab/Schichtung nicht gemessen) | `[lokaler Pfad]` (Stand 23.10. 21:30) |
| Zirk-Rücklauf ≥ 50 °C bei 52 °C Speicher (nur 2 K Spielraum) ist unbelegt – kein Fühler. | sicher (nicht gemessen) | `ANALYSE_Loxone_Fuehler_Inventar_Heizung_20261023.md` |

**Gesamturteil:** Nein, nicht allein über Hoval. 52 °C abends ist vertretbar, **wenn** die Loxone-Sonntagsladung wirklich ≥ 60 °C oben erreicht (Abnahme 25.10.) und die Zirkulationspumpe in dieser Zeit mitläuft. Bis dahin: Status „bedingt“.

## Was bringt uns das
- Klarheit: Die Hoval desinfiziert nicht (wahrscheinlich 05-017 aus). Die Legionellen-Vorsorge liegt vollständig bei Loxone/Heizstab – kein Doppelbetrieb, keine versteckte 60–65-°C-WP-Ladung, die die WW-Arbeitszahl drückt.
- Im Sommer/Herbst hat der PV-Heizstab den Speicher täglich ≥ 60 °C gebracht (bis 01.10.). Im Winter fällt das weg → genau jetzt braucht es die Sonntagslogik.
- Energie: 1×/Woche ~405 l wirksam (0,47 kWh/K, F1 25.10.2026; vorher hier 379 l / 4,4 kWh) von ~50 auf 60 °C ≈ 4,7 kWh Wärme (Heizstab, COP 1) ≈ 0,7 kWh/Tag. Das frisst grob die Hälfte bis zwei Drittel der Ersparnis aus 57→52 °C (FUND-Schätzung 0,7–1,0 kWh el/Tag, Volumen dort auf 0,47 kWh/K umzurechnen). Schätzung, nicht gemessen.

## Offene Reste
1. **05-017 am Bediengerät ablesen** (der Betreiber, 1 Foto): Menü Warmwasser → Legionellenschaltung: Ein/Aus, Wochentag, Uhrzeit, Temperatur. Erst dann „sicher“ statt „wahrscheinlich aus“.
2. **Abnahme So 25.10.2026 12–16 Uhr:** Volllogger 1500 und 27483 ≥ 60 °C? Abschaltung danach? Prüf-Skript: `[lokaler Pfad]` (Datumsmuster anpassen).
3. Ziel der Loxone-Logik von 59 auf ≥ 60–61 °C (oben) prüfen; Haltezeit festlegen.
4. Zirkulationspumpe während der Sonntagsladung zwangsweise laufen lassen (Loxone), sonst bleibt die Leitung unbehandelt.
5. Zirk-Rücklauffühler nachrüsten (siehe Fühlerinventar), um 52 °C abzusichern.
6. PV-Heizstab-Signal im Volllogger/Loxone suchen, um die Deutung „PV-Heizstab“ von „wahrscheinlich“ auf „sicher“ zu heben.