# F62 - Wie wird das OG mit Wärme versorgt? (Analyse-Agent, 01.11.2026)

Nur gelesen. An Hoval, Loxone, Pi und Dateien nichts geändert, außer dieser Datei.

## Frage
HK1 = UG (Grundfos ALPHA1 25-60 180), HK2 ist in der Hoval abgeschaltet. Wie bekommt das obere Stockwerk Wärme?
Hypothesen: (a) OG hängt am selben Kreis/Verteiler wie HK1, (b) eigene Pumpe/Mischer ohne Hoval, (c) anders.

## Kurzergebnis
**(c): Das obere Stockwerk bekommt keine WP-Wärme. Die Wärmepumpe beheizt über HK1 nur das UG (ein FBH-Verteiler, 12 Kreise, alle UG-Räume plus Hütte).** HK2 ist hydraulisch und elektrisch fertig vorbereitet (Pumpe "MK2/HK2", ESBE-Mischer, VF2, TTE-FE, Steigleitung im Schacht), läuft aber nicht, und an HK2 hängt in Loxone kein einziger Raum. [wahrscheinlich, nahe sicher]
Die Prämisse "2 Stockwerke à ~100 m² FBH, beide beheizt" stimmt so nicht: Laut Vault gilt "Wärmepumpe heizt nur das UG", das EG wird nur in der Küche per Split-Klima und im Bad/WC elektrisch geheizt, das OG (Dachboden mit Zimmer OG) meist gar nicht. [wahrscheinlich, Quelle: des Betreibers eigene Angaben, im Vault notiert]

## Gesuchte Quellen
| Nr | Quelle (voller Pfad) | Treffer |
|---|---|---|
| 1 | `[lokaler Pfad]` | Zeile 16: zweite ALPHA1 25-60 180 mit Aufkleber "HK2" (aus) + zwei ESBE-Mischerantriebe |
| 2 | `[lokaler Pfad]` (nur URLs) und `[lokaler Pfad]` | Nr 54, 117, 125, 149, 152, 155, 160, 211, 235, 239, 240, 261 |
| 3 | Fotos angesehen: `[lokaler Pfad]`, `...\gp_HG-D-_U-7xQ449KT.jpg`, `...\gp_2SsGt2kwDJUR2gKT.jpg` | siehe Befund |
| 4 | `[eigene Notizen]` | nur Verweis auf `[eigene Notizen]` (Z. 292), nichts zu HK2 |
| 5 | `[eigene Notizen]` Abschnitt 5 | "Wärmepumpe heizt nur das UG", EG Split-Klima Küche, OG meist unbeheizt, Infrarot Zimmer OG; Umbau OG mit FBH geplant |
| 6 | `[eigene Notizen]` Z. 110 | Technikschacht UG-Bad -> EG-Flur West mit 2 KWL-Hauptrohren fürs OG und Heizkreis Vor-/Rücklauf |
| 7 | `[eigene Notizen]` | Loxone-Namen "Vorlaufist HC1 (UG)", "Vorlaufist HC2 (OG)" |
| 8 | `[eigene Notizen] (~960 m).md` Z. 85, `[eigene Notizen]` Z. 264 | "das OG ist heute unbeheizt", Punkt 8 "Umbau OG mit Fußbodenheizung" |
| 9 | Vorbefunde `[lokaler Pfad]`, `...\ANALYSE_Hydraulik_Volumenstrom_Puffermischung_20261023.md`, `...\ANALYSE_Loxone_Fuehler_Inventar_Heizung_20261023.md`, `...\ANALYSE_F56_Heizlast_Kennlinie_20261101.md` | HK2 in allen 2196 Logpunkten aus; 1-Wire "Thermometer_HK2_OG_Vorlauf" nur in Projektdatei |
| 10 | Loxone-MCP (`list_rooms`, `control_find`, `control_state`), 01.11.2026 | Räume, IRR, Klimacontroller UG/HC2, HK2-Kacheln |
| 11 | HoxPi-MCP `read_register` 1479, 1502, 19707, 19659, 1514, 1513, 19706, 01.11.2026 | siehe Stichprobe |

## Befund A - auf Fotos sichtbar
| Foto | Was zu sehen ist | Sicherheit |
|---|---|---|
| `gp_x1Tvl-PThisniQcl.jpg` (Nr 239) | **Ein** FBH-Verteiler, 12 Kreise mit Durchflussmessern, beschriftet: WC, Büro, Vorsorge (Mitte), Vorsorge (Mitte), Bad, Wirtschaftsraum, Gartenhaus, VZ Wohnen, RZ Wohnen, Zimmer OG, Vorsorge Süd, Elternzimmer. Zuleitung unten rechts in roter Dämmung. | Beschriftung [sicher sichtbar]. Zuordnung UG: [wahrscheinlich] - WC/Büro/Bad/Wohnen/2 Zimmer OG entsprechen den UG-Räumen im Aufmaß (`[eigene Notizen]` Z. 582-590), "Gartenhaus" = Hütte, "Wirtschaftsraum" = Heizraum. Die CSV-Vermutung "OG" wegen Eltern-/Zimmer OG ist damit widerlegt: Zimmer OG 1 und Zimmer OG 2 liegen im UG (Haus-Wissen Z. 73, 87). |
| `gp_HG-D-_U-7xQ449KT.jpg` (Nr 125) | Verteilergruppe: links Rohr mit Hülse "HK2" + Mischerantrieb + Fühlerkabel "HK2", rechts "HK1" mit Schild "Heizkreis 1 Absperrung Vorlauf/Rücklauf **Untergeschoss**". HK2-Rohre gehen gedämmt nach oben weg. Alle 4 Thermometer ~20-25 °C. Dosen "Loxone OneWire" und "Taupunktfühler". | [sicher sichtbar]; dass die HK2-Rohre zur Steigleitung führen: [wahrscheinlich] |
| `gp_9UW33XBBtT7G4e3r.jpg` (Nr 54), `gp_mNivjZytYOp-AWEx.jpg` (Nr 160), `gp_KtzS7vr0pOGO-h4H.jpg` (Nr 149) | Zwei Grundfos ALPHA1 25-60 180, handschriftlich "MK 1" und "MK 2", je ein ESBE-Stellmotor. MK1/HK1 an (22-23 W), MK2/HK2 Display dunkel. | laut Beschreibung [sicher]; nicht selbst angesehen |
| `gp_L2xAcKGobe2xXDJQ.jpg` (Nr 152), `gp_lBN9hZPrBEwjL7Wz.jpg` (Nr 155) | Rohbau: zwei rote gedämmte Rohre (PEF 28/9) im Schacht neben KWL-Schläuchen. | laut Beschreibung; "VL/RL zum OG" ist dort [wahrscheinlich] |
| `gp_sNhpKxx_c9rwQc1c.jpg` (Nr 211), `gp_WfMVHfpyLfbaWODa.jpg` (Nr 235), `gp_Z41SqUa9rqoNLXf_.jpg` (Nr 261) | Hoval-Schema [Schema-Nr.] (31.07.2020): 2 Mischerkreise MK1/MK2, MK2 gelb = optional; TTE-FE für HK2 (VF2, YK2, Pumpe MK2); HK2-Parameter im IBN-Blatt vorgesehen. | laut Beschreibung [sicher] |
| `gp_eaJTe25kBlGEH8AA.jpg` (Nr 101) | Bediengerät-Menü "Heizkreise **Obergeschoss**" | laut Beschreibung [wahrscheinlich] |

Nicht gefunden: ein zweiter FBH-Verteiler (EG/OG) auf irgendeinem Foto.

## Befund B - aus Daten belegt
- **Hoval HK2 aus** (HoxPi, 01.11.2026): 1479 Betriebswahl = 0 (Standby), 1502 Status = 0 (Abgeschaltet), 19707 Pumpe = 0, 19659 Mischer = -100 % (zu), 1514 VF2 = 19,3 °C (Raumniveau, Fühler lebt). Gleichzeitig HK1: 19706 Pumpe = 1, 1513 VL = 27,8 °C. [sicher]
- Über die ganze Logdauer (2196 Punkte bis 23.10.) war HK2 nie aktiv (Vorbefund `ANALYSE_Mischer_HK1_HK2_Regelguete_20261023.md` Abschnitt 2). [sicher]
- **Loxone**: Räume = Abstellraum, Aussenbereich, Badezimmer, Büro, Energie, Flur, Garage, Hütte, Zimmer OG 1, Zimmer OG 2, Technikraum, Terrasse UG, Treppe, WC UG, Wohnzimmer, Zentral. **Kein OG- oder EG-Wohnraum** mit Raumregler. [sicher]
- **Klimacontroller UG** (<UUID>) führt alle 8 Heiz-Raumregler: Wohnzimmer, Badezimmer, WC UG, Büro, Zimmer OG 1, Hütte, Technikraum, Zimmer OG 2 (State `controls`). demandHeat 33, stage 2. [sicher]
- **Klimacontroller HC2** (<UUID>) existiert, hat aber `controls = []` (kein Raum zugeordnet), demandHeat 0. "HK2 Vorlauf soll (Loxone)" = 16,1 °C, "HK2 Betriebsart" = Abgeschaltet, "HK2 Pumpe" = Aus. [sicher]
- 1-Wire-Fühler "Thermometer_HK2_OG_Vorlauf" ist in der Projektdatei eingelernt, hat aber keine Kachel (Vorbefund Fühler-Inventar). [sicher] Die Loxone-Benennung "HC2 (OG)" zeigt, dass HK2 als OG-Kreis gedacht ist. [wahrscheinlich]

## Plausibilität aus F56 (Wärmemenge vs. Fläche)
- F56 Fit D: Q = 64,1 - 3,76·AT kWh/d, also 157 W/K, rund 5 kW bei -15 °C (`ANALYSE_F56_Heizlast_Kennlinie_20261101.md`).
- Bezogen auf ~100 m² UG plus Hütte (~9 m²): rund **45-50 W/m² bei -15 °C**. Auf 200 m² wären es 23-25 W/m². [Rechnung sicher]
- Beides ist für sich möglich. Für ein UG allein ist der Wert hoch, er passt aber gut zur Vault-Angabe "Zwischendecken ungedämmt, Wärme wandert von unten nach oben": Das UG heizt das EG über die Decke mit, die Wärme geht über den offenen Dachboden verloren. [Vermutung]
- Die Wärmemenge allein entscheidet die Frage also nicht. Entscheidend sind die Fotos (ein Verteiler, UG-Räume) und die Daten (HK2 nie aktiv, kein Raum an HC2). [wahrscheinlich]
- Folge für frühere Analysen: Rechnungen mit "200 m² beheizt" oder 7 kWh_th/K Estrichmasse gelten nicht. Richtig ist ~100 m² UG-Estrich (~3,5 kWh_th/K, `ANALYSE_Heizstrom_Tageszeit_PV_Vorheizen_20261023.md`). [wahrscheinlich]

## Ergebnis
| Hypothese | Urteil |
|---|---|
| (a) OG am selben Kreis/Verteiler wie HK1 | **nein** [wahrscheinlich] - der einzige gezeigte Verteiler hat nur UG-Kreise und 3 Reserven ("Vorsorge") |
| (b) eigene Pumpe/Mischer ohne Hoval | **nein** [wahrscheinlich] - die zweite Pumpe ist die Hoval-HK2-Pumpe (TTE-FE, MK2) und steht still; eine dritte Heizkreispumpe ist auf keinem Foto |
| (c) anders | **ja**: OG/EG werden von der WP gar nicht beheizt. HK2 ist eine fertige, stillgelegte Vorrüstung für den OG-Umbau mit FBH. EG: Split-Klima Küche + Elektro Bad/WC; OG: Infrarot Zimmer OG, sonst unbeheizt. [wahrscheinlich, nahe sicher] |

Konsequenz für den Projektkontext: Die Zeile "Fußbodenheizung: 2 Stockwerke à ca. 100 m²" sollte lauten: "FBH aktiv nur im UG (~100 m², 12 Kreise inkl. Hütte, HK1). HK2 (OG) vorgerüstet, aber außer Betrieb; EG/OG ohne WP-Wärme." [Vorschlag, Entscheidung der Betreiber]

## Stichprobe (01.11.2026, live gelesen)
| Quelle | Wert |
|---|---|
| HoxPi 1479 / 1502 / 19707 / 19659 / 1514 | 0 / 0 / 0 / -100 % / 19,3 °C (HK2 aus) |
| HoxPi 19706 / 1513 | 1 / 27,8 °C (HK1 läuft) |
| Loxone "HK1 Vorlauf soll (Loxone)" / "HK2 Vorlauf soll (Loxone)" | 30,0 °C / 16,1 °C |
| Loxone Klimacontroller UG `controls` | 8 Raumregler (alle IRR außer Garage), demand 1 bei Bad, WC UG, Büro, Technikraum |
| Loxone Klimacontroller HC2 `controls` | leer |

## Offen / Fragen an der Betreiber
Gesucht wurde in: BAUTEILE_BEKANNT.md, Fotoalbum (CSV-Beschreibungen + 3 Fotos angesehen), Vault (CLAUDE.md, PV-Autarkie-Winter, Haus-Wissen, Aufmaß, SD-Statistik, Autarkie-Fahrplan), Loxone-MCP, HoxPi-MCP, Vorbefunde in `[lokaler Pfad]`.
1. **Gibt es im EG oder OG überhaupt schon verlegte Fußbodenheizung bzw. einen zweiten Verteilerkasten?** Auf keinem Foto zu finden. Wenn nein, ist F62 erledigt: WP beheizt nur das UG.
2. **Wo endet die HK2-Steigleitung** (2 rote Rohre im Schacht UG-Bad -> EG-Flur West)? Ist sie oben verschlossen oder schon an etwas angeschlossen?
3. Gilt die Vault-Angabe aus `[eigene Notizen]` ("WP heizt nur das UG, EG Küche Split-Klima, OG meist unbeheizt") auch für diesen Winter 2026/27?
4. Nebenpunkt: Der 1-Wire-Fühler "Thermometer_HK2_OG_Vorlauf" hat in der Projektdatei `MaxVal="10"` und keine Kachel. Für den OG-Umbau später prüfen, jetzt ohne Wirkung.