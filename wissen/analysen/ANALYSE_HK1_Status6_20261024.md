# ANALYSE HK1-Status 6 (Reg 1501), Katalogfrage F9, 24.10.2026

**Kurz:** Status 6 heißt offiziell „Zwangsdrosselung (bei Zwang < -50%)“. Von 265 Volllogger-Punkten mit 1501 = 6 liegen **253 (95,5 %) in einer WW-Ladung**. Die übrigen 12 Punkte sind 2 Nachlaufpunkte direkt nach WW-Ende und 2 kurze Blöcke beim Übergang aus dem Kühlbetrieb (24.08. und 12.09.). Die Annahme „Zwangsdrosselung = WW-Vorrang“ stimmt damit fast vollständig. Nebenfund: Reg 19870 ist **kein** WW-Indikator.

## 1. Enum-Text (sicher)
Quelle 1: HoxPi `read_register(1501)`, Name „Status Heizkreisregelung“, Typ U8, nicht schreibbar.
Quelle 2: `[lokaler Pfad]`, Zeile 1501 (fg 1, fn 0, dp 2051, Funktion „Heizkreis 1“), gleicher Text.

Wörtlich (Auszug): `#0 = Abgeschaltet#1 = Normal Heizbetrieb ... #5 = Zwangsabnahme (bei Zwang > +50%)#6 = Zwangsdrosselung  (bei Zwang < -50%)#7 = Ferienbetrieb ... #9 = Normal K?hlbetrieb ... #22 = K?hlbetrieb Extern/Konstantanforderung#23 = Heizbetrieb Extern/Konstantanforderung#26 = Vorzugsbetrieb SmartGrid`

WW-Gegenstück Reg 1504 „Status Warmwasserregelung“ (HoxPi `read_register(1504)`): `#0 = Abgeschaltet#1 = Normal Ladebetrieb#2 = Komfort Ladebetrieb#3 = Zwangsdrosselung (bei E-Zwang < -50%)#4 = Zwangsladung ...#8 = Reduzierter Ladebetrieb#12 = Vorzugsbetrieb SmartGrid#13 = Abnahmezwang SmartGrid`.

## 2. Datenbasis (sicher)
- Volllogger `~/hoxpi_fulllog/2026-*.csv(.gz)` auf dem Pi, **2026-07-30 22:26 bis 2026-10-24 00:55**, **24.467 Punkte** (5-min-Raster).
- Spalten: 1501 (HK1-Status), 1504 (WW-Status), 1539 (WEZ-Status; 4 = WW-Betrieb, siehe `ANALYSE_Mischer_HK1_HK2_Regelguete_20261023.md`), 19870, 19706 (HK1-Pumpe). Statuswerte sind Rohwerte ohne ×10.
- WW-Ladung definiert als **1539 = 4 oder 1504 ∈ {1, 2, 4, 8, 12, 13}**.
- Skripte: `[lokaler Pfad]` (holt die Spalten, Ergebnis `...\Emulation\or_f9_20261024_extrakt.csv`), `[lokaler Pfad]`.

## 3. Ergebnis Status 6 (sicher, aus Daten)
| Größe | Wert |
|---|---|
| Punkte mit 1501 = 6 | **265** in 41 Blöcken (Aug 4, Sep 66, Okt 195) |
| davon in WW-Ladung | **253 = 95,5 %** (246 mit 1539 = 4; weitere 7 nur über 1504 = 1) |
| HK1-Pumpe 19706 bei Status 6 | immer 0 (265/265) |
| 19870 bei Status 6 | immer 0 (265/265) |

Umgekehrt: Von 1.736 Punkten mit 1539 = 4 zeigt 1501 nur 246-mal Status 6. Sonst 0 (961, HK1 nicht angefordert), 22/9/27 (181/162/64, Sommer-Kühlbetrieb), 1 (100), 23 (13), 26 (9). **Sicher:** Status 6 tritt nur auf, wenn HK1 im Heizbetrieb angefordert ist und eine Drosselung kommt. Im Kühlbetrieb wird HK1 bei WW nicht auf 6 gesetzt.

## 4. Ausnahmen (12 Punkte, sicher aus Daten, Deutung je markiert)
| Zeit | 1501 | 1504 | 1539 | Deutung |
|---|---|---|---|---|
| 2026-08-24 07:45–08:00 (4 Pkt.) | 6 | 0,0,3,3 | 16, 98, 98, 98 | vorher 22 (Kühlen), ab 08:05 WW-Ladung (1504 = 1, 1539 = 4). 1504 = 3 heißt „WW-Zwangsdrosselung“. **Wahrscheinlich** die Vorbereitung bzw. Umschaltphase vor der WW-Ladung |
| 2026-09-12 01:30–01:55 (6 Pkt.) | 6 | 0 | 0, 16, 16, 51, 98, 98 | vorher 22 (Kühlen), danach 0. Keine WW-Ladung im Raster. **Vermutung:** Umschaltung Kühlen → Heizen (1539 16/51/98, Bedeutung nicht im Katalog) mit Drosselanforderung des Erzeugers |
| 2026-09-15 06:25 | 6 | 0 | 0 | erster Punkt nach WW-Ende (06:20 noch 1539 = 4). **Sicher** Nachlauf/Abtastversatz |
| 2026-10-14 07:10 | 6 | 0 | 0 | wie oben (07:05 noch 1539 = 4) |

Rechnet man die beiden Nachlaufpunkte zur WW-Ladung, sind es 255/265 = **96,2 %**. Seit Heizbeginn (ab 12.09. 02:00) liegt **jeder** Status-6-Punkt in einer WW-Ladung oder im ersten Punkt danach (sicher).

## 5. Alle beobachteten Werte von 1501 (sicher)
| Wert | Bedeutung (offiziell) | Punkte | Anteil |
|---|---|---|---|
| 0 | Abgeschaltet | 13.388 | 54,7 % |
| 22 | Kühlbetrieb Extern/Konstantanforderung | 3.165 | 12,9 % |
| 9 | Normal Kühlbetrieb | 2.621 | 10,7 % |
| 23 | Heizbetrieb Extern/Konstantanforderung | 2.215 | 9,1 % |
| 1 | Normal Heizbetrieb | 1.466 | 6,0 % (nur August) |
| 27 | **nicht in der offiziellen Liste** | 1.236 | 5,1 % (Juli/Aug., immer mit 19870 = 1) |
| 6 | Zwangsdrosselung (bei Zwang < -50%) | 265 | 1,1 % |
| 26 | Vorzugsbetrieb SmartGrid | 111 | 0,5 % (nur August) |

Seit Oktober kommen nur noch 0, 23 und 6 vor (sicher), passend zu Zeile 14 in `[lokaler Pfad]`.

## 6. Nebenfund Reg 19870 (wahrscheinlich, Korrektur der Projektdoku)
Offizieller Name laut CSV: „Status Kühlventil aktiv UKA“ (dp 22024). Im Logger ist 19870 = 1 nur bei 1501 = 22/9/27 (Kühlen, 6.540 Punkte) plus 7 Punkte bei 0, aber **nie** bei 1539 = 4 (0 von 1.736). 19870 zeigt also das Kühl-Umschaltventil, **nicht** Heizen/WW. Die Angabe „Umschaltventil Heizen/WW = Reg 19870“ in den Projektanweisungen sollte der Betreiber prüfen und korrigieren. Als WW-Indikator taugen 1539 = 4 und 1504 = 1.

## Was bringt uns das
- F9 ist beantwortet: Status 6 ist die offizielle HK-Zwangsdrosselung. In der Heizperiode ist sie praktisch gleichbedeutend mit der WW-Vorrangschaltung (sicher). Für Auswertungen kann „1501 = 6“ als Marker „HK1 wegen WW gesperrt“ dienen. Kühl-Übergänge und der erste Punkt nach WW-Ende müssen dabei ausgeklammert werden.
- Die Unterversorgung nach WW (Mischer-Analyse vom 23.10.) ist damit eindeutig der WW-Vorrang und keine eigene HK-Störung. Ansatzpunkt bleibt die Lage der WW-Ladezeiten (z. B. 14:15 statt 05:05/07:25/16:05 bei laufendem HK1).
- Werte, die noch offen sind: 1501 = 27 und die 1539-Codes 16/51/98 stehen nicht im Katalog (offen). Außerdem 19870 in der Doku korrigieren.