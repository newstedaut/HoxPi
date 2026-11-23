# ANALYSE F97: Heizkurve HC1, Steilheit 0,9 oder 0,3?

Stand: 02.11.2026 ca. 18:05 MEZ, Orchestrator (selbst, kein Subagent). Nur gelesen. An Loxone, Hoval, Pi nichts geaendert.

## Ergebnis
1. **Steilheit 0,9 ist widerlegt** [sicher fuer Datei und Messung]. In der Projektdatei ist 0,9 nur der Standardwert von `Outer`, dem verbundenen Aussentemperatur-Eingang, und damit wirkungslos.
2. **Wirksam ist 0,3** (`Transconductance`, Z. 13231) [wahrscheinlich, die Zuordnung Attribut zu Parameter S ist nicht offiziell dokumentiert; die Messung passt].
3. **Falsche 0,9 stehen noch an drei Stellen:** Projektanweisung, Bausteinkommentar NDOC Z. 13218, `ANALYSE_Raumventile_Heizkurve_Winter_20261022.md`. Die Aussage dort "die Raumkorrektur zieht die Kurve 0,9 herunter" ist damit hinfaellig [wahrscheinlich].
4. **Max 40 C begrenzt im Winter nicht:** Bei -15 C ergibt die Kurve rund 35 C, mit Anhebung rund 37,5 C [Rechnung, Formel nachgebildet].

## Belege
**Datei** `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` (01.11.2026 23:36), [Vorlauftemperaturregler](https://www.loxone.com/dede/kb/vorlauftemperaturregler/) HC1 Z. 13218:
| Attribut | Def | Doku-Parameter | Zuordnung |
|---|---|---|---|
| `Outer` (Z. 13219, mit Eingang) | 0.9 | Aussentemperatur | Eingang verbunden, Def ohne Wirkung [wahrscheinlich] |
| `Transconductance` (Z. 13231) | 0.3 | S Steilheit | nach Ausschluss |
| `Translate` (Z. 13232) | leer | N Parallelverschiebung | nach Ausschluss |
| `PrevInc` / `BufferInc` / `Treshold` / `Gain` / `Max` | 2 / 5 / 35 / 1 / 40 | I / B / Str / G / Max | Werte decken sich mit `FUND_F66_Heatmixer2_Parameter_20261101.md` |

**Messung** Volllogger-Kopien `[lokaler Pfad]` bis 01.11., Zeilen mit 1490 > 0, n = 1.635 [sicher als Zaehlung], Skript `or_f97_1755.py`. Rechnung mit der nachgebildeten Formel aus FUND_F66, die die Doku-Beispiele auf 0,2 K trifft [Vermutung fuer die Formel]; Raumsoll 23,5 C:
| 1477 C | n | Median 1490 | S 0,3 | S 0,9 |
|---|---|---|---|---|
| 0-2 | 32 | 33,0 | 30,8 | 40 (Max) |
| 2-4 | 171 | 32,1 | 30,3 | 40 (Max) |
| 4-6 | 623 | 32,0 | 29,8 | 40 (Max) |
| 6-8 | 460 | 30,1 | 29,2 | 40 (Max) |
| 8-10 | 258 | 29,5 | 28,6 | 38,9 |
| 10-12 | 91 | 29,2 | 28,0 | 37,1 |

Die Spalten S 0,3 und S 0,9 nehmen je die Bandmitte. Die Mediane mischen tiefe und hohe Stufe (F95), liegen also 1-2 K ueber S 0,3. Der Abstand zu S 0,9 betraegt 7-10 K. Steigung der Mediane -0,38 K/K, bei S 0,3 rund -0,3 K/K, bei S 0,9 rund -1 K/K.

**Live** 02.11. ca. 17:58: 1477 = 5,1 C, 1490 = 29,8 C. Rechnung S 0,3 mit Raumsoll 23,5: 29,75 C. Mit S 0,9 muesste das hoechste Raumsoll rund 17 C sein, das kleinste bekannte Komfortsoll ist 19,5 C (Technikraum) [Rechnung].

## Vorhersage fuer die Frostnacht (Bitte an den Loop, als V-Nummer uebernehmen)
1490 ohne Ofen und ohne Sonderzweig, S 0,3:
| 1477 C | tiefe Stufe (Rs 23,5) | hohe Stufe (Rs 25,5) |
|---|---|---|
| 0 | 31,1 | 33,6 |
| -5 | 32,4 | 34,9 |
| -15 | 35,0 | 37,5 |

Widerlegt, wenn 1490 bei 1477 <= 0 C um mehr als 1,5 K davon abweicht und keine andere Stufe das erklaert. Raumabweichung ist darin nicht enthalten.

## Offen
- Formel und XML-Zuordnung sind nicht offiziell belegt. Beides trifft die Messung, ein Blick in Loxone Config waere der direkte Beweis.
- Ob 0,3 im echten Frost reicht, sagt diese Analyse nicht: Sie sagt nur, welchen Vorlauf die Kurve liefert. Pruefung ueber Raumtemperaturen bei Frost.

## Was bringt uns das
| Punkt | Wirkung |
|---|---|
| Rechengrundlage | Heizlast-, Zwilling- und Kurvenaussagen rechnen ab jetzt mit 0,3. Kein Rueckbau noetig, nur 0,9 aus den Texten nehmen |
| Winter | Vorlauf bleibt voraussichtlich 5 K unter Max, das ist gut fuer die Arbeitszahl. Wird es bei Frost im UG zu kalt, ist die Steilheit der erste Hebel. Das ist deine Entscheidung, Rueckweg 0,3 |
| Vorschlag ohne Umsetzung | Projektanweisung auf "Steilheit 0,3, Max 40" aendern; Kommentar Z. 13218 beim naechsten Umbau mitkorrigieren (Backup und Skill `loxone-xml-umbau` zuerst) |