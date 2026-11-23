# FUND Loxone IRR + FBH + Takten (F59), Teil 2 – 01.11.2026
Recherche-Subagent im OR-Lauf 01.11.2026 (Teil 2). Ergänzt `[lokaler Pfad]` (Teil 1, 10 URLs, dort genannte URLs hier nicht wiederholt außer als Bezug).
Nur öffentliche Seiten, nichts an Loxone oder Anlage geändert.

**Erreichbarkeit loxone.com/dede/kb diesmal:** teilweise. `https://www.loxone.com/dede/kb/intelligente-raumregelung/` = erreichbar (200). `/dede/kb/klima-controller/`, `/dede/kb/irr-v2/`, `/dede/kb/intelligente-temperatursteuerung/` = weiter Fehler (client_error/403). EN-Seiten `loxone.com/enen/kb/climate-controller/`, `/enen/kb/irc-v2/`, `/enen/kb/intelligent-temperature-controller/`, `/enen/kb/zoned-heating-comfort/` = erreichbar. Deutsches Loxforum, haustechnikdialog.de, hausbau-forum.de, `/enen/question/` = Fehler (client_error); WebSearch liefert nur Titel, keine Snippets → daraus nichts zitierbar.

## Belegt (offizielle Loxone-Doku)
### Klima Controller (EN, https://www.loxone.com/enen/kb/climate-controller/)
- **MinHr** Mindestlaufzeit, min, Std. 0: „The minimum runtime must be met before switching to standby (All inputs OFF) or the opposite mode.“
- **Sot** Einschaltschwelle, %, Std. 30, 0…100: „Average valve openings of the Intelligent Room Controllers must exceed (Sot) in order to start operation.“
- **MaxTp** Puls-Schwelle %, Std. 0 (= aus); **Don** 750 s; **Doff** 300 s (min. 180 s). Nach Abschalten H/C: „a delay of 3 minutes is active in addition to (Fod)“, Fod Std. 120 s.
- **Mode** −1 aus / 0 Auto-Umschaltung nach IRR-Anforderung / 1 „heating only if there is sufficient demand“ / 2 nur Kühlen.
- **Otm** 0 aus / 1 48-h-Mittel Außentemp. / 2 Systemvariable „Expected Average Outdoor Temperature 48h“ / 3 aktuelle Außentemp. **ϑLimH Std. 18 °C**, **ϑLimC Std. 15 °C**: oberhalb ϑLimH „the system will not switch to heating mode, even if there is a demand“ (analog Kühlen). Hinweis: Teil 1 nannte aus der ES-Fassung 15/10 °C – EN-Seite zeigt 18/15 °C (Versionsunterschied wahrscheinlich; im eigenen Projekt nachsehen).
- Anforderung je Raum = (Soll − Ist) × Raumfläche in °m²; belegte Räume priorisiert. Automatische Bewertung „only occurs when the minimum opening threshold is exceeded“.
- **ϑminHP** Std. −22 °C (darunter nur Zusatzheizung Ah); **Tt2s** 60 min, **ϑminS2** −6 °C (Stufe 2; bei Typ Wärmepumpe sofort unter ϑminS2). Kein Abschnitt zu Puffer, Vorlauf-Anforderung oder Takten.
### Intelligente Raumregelung (DE, https://www.loxone.com/dede/kb/intelligente-raumregelung/, Bausteinversion 12.0/12.1)
- Quellenausgänge: „Würde die Einschaltschwelle des Klima Controllers unterschritten, kann eine Mindestöffnung erzwungen werden, bis das Gerät nach Ablauf der Mindestlaufzeit ausgeschaltet wurde.“ → Mindestöffnung ist **kein eigener Parameter**, sondern Folge von Sot + MinHr.
- Pwm: „Zeitdauer für einen Ein-Ausschaltzyklus wenn ein Ausgang als PWM konfiguriert ist.“ Standards dort: ϑch 21, ϑcc 23, ϑeh/ϑec 2, Vs 14 d, Hs/Cs 0 = gelernt, Pwm 0 = automatisch (0…1440 min).
### IRC v2 (EN, https://www.loxone.com/enen/kb/irc-v2/)
- **ϑd** Komfort-Abweichung Std. 1,5 K (0,5…5): „If this range is exceeded for more than 1 minute, switching between heating and cooling is required“ → ϑd ist die Heiz/Kühl-Umschaltgrenze (Kühlfalle!), keine Ventil-Hysterese.
- Einzige genannte Hysterese: 0,4 °C am Beschattungsausgang Shd. Keine Ventil-Hysterese als Parameter.
### Intelligente Temperatursteuerung (EN, https://www.loxone.com/enen/kb/intelligent-temperature-controller/)
### Zonenheizung (EN, https://www.loxone.com/enen/kb/zoned-heating-comfort/)
- Loxone-Aussage: stetige Stellantriebe 0–100 % vermeiden, die Quelle „by short cycling“ zu belasten; „The Switch On Threshold, set at 30% as default, will signal the boiler or air heat pump to switch on“. Kein Hinweis auf Ventile-offen/Referenzraum.

## Belegt (Foren, Erfahrungswerte – Meinungen, keine Messungen)
- knx-user-forum.de, FBH + Luft-WP + Einzelraumregelung (https://knx-user-forum.de/forum/%C3%B6ffentlicher-bereich/knx-eib-forum/knx-einsteiger/1539375-fussbodenheizung-w%C3%A4rmepumpe-knx): EML #3 „dass die Stellantriebe der beheizten Räume im Heizbetrieb möglichst weit offen stehen.“ Wilantis #10 „Ventile bei gut gedämmten Häusern mit relativ niedrigen FBH-Vorlauftemperaturen immer auf.“ scw2wi #14 „Ich würde die ERR nicht zur Regelung verwenden, sondern um bestimmte Räume im Winter oder Sommer abzudrehen.“ Eigen #6: Heizkurve in 1-K-Schritten senken. Markus1780: geregelte Ventile bringen die WP zum Takten.
- loxone-english (Google Groups), „Making room controller not turn on and off heating as frequently“ (https://groups.google.com/g/loxone-english/c/zVpZ8WdBguM): Taktdauer am digitalen IRC-Ausgang nicht einstellbar → Analogausgang über eigenen PWM-Baustein; Warnung Michael (Loxone-Antwort): Relaisausgänge, die alle paar Minuten schalten, „will die within a few months“.
- energiesparhaus.at „LWP taktet und taktet“ (https://www.energiesparhaus.at/forum-lwp-taktet-und-taktet-und-taktet/69988): Vaillant VWL 75/6, FBH, alle Kreise offen, trotzdem Start alle 30 min / 7–8 min Lauf; Konsens Überdimensionierung (Kleinstleistung > Last, Taktverhältnis ~1:3,8 bei 12 °C), Abhilfe nur kleinere WP bzw. größere Hysterese/Startschwelle. → Ventile offen allein löst Überdimensionierung nicht.

## Wahrscheinlich
- Bei uns ist die Takt-Ursache die Hoval-Hysterese (Start RL ≈ Soll − 1,5 K, Stopp ≈ Soll + 3 K, Teil 1) bei Kleinstleistung ~7 kW > Last; Loxone-Parameter MinHr/Sot/MaxTp/Doff wirken nur, wenn H des Klima Controllers die WP schaltet – laut `[lokaler Pfad]` nicht verdrahtet (Teil 1). Wirksam bleiben: Höhe/Glätte von 1490 und die offene Masse über die Stellantriebe.
- Die „Mindestöffnung“ der IRR greift nur zusammen mit dem Klima Controller (Sot/MinHr) – ohne H-Verdrahtung zur WP wirkungslos für den Verdichter, hält aber Ventile während MinHr offen (mehr Masse).
- ϑd (Std. 1,5 K) ist mitverantwortlich für die Kühlfalle (Heizen/Kühlen-Umschalten nach 1 min Überschreitung) – Umbau 23.10. (Otm/48 h) zielt richtig; ϑLimH/ϑLimC-Standard laut EN 18/15 °C (nicht 15/10).

## Nicht gefunden
- Offizieller Parametername für Ventil-Mindestöffnung (gibt es laut DE- und EN-Doku nicht); Ventil-Hysterese der IRR; Loxone-Empfehlung „Grundlastkreis“ oder Referenzraum.
- Inhalte DE-Loxforum (u. a. 310713 „KlimaController/Mischerkreis taktet bei geringer Anforderung“, 214228 „Dimplex Wärmepumpe und Loxone Raumregelung“, 458073, 464929), haustechnikdialog (276290), hausbau-forum: alle client_error aus der Cloud. Nachlesen über des Betreibers Browser lohnt v. a. 310713 und 214228.
- Klima-Controller-Parameter „Vorlauf-Anhebung“: existiert im Klima Controller nicht; Vorlauf-Logik nur in der Intelligenten Temperatursteuerung (I, Boost, Min/Max ohne Standardwerte).

## Vorschläge (nur Vorschlag, der Betreiber entscheidet, keine Umsetzung)
| # | Vorschlag | Ort | Erwartete Wirkung | Sicherheit |
|---|---|---|---|---|
| 1 | Im UG 1–2 große Wohnräume als „Grundlastkreise“ dauerhaft offen (Stellantrieb fest 100 % im Heizbetrieb), IRR nur noch für Bad/Schlafräume zum Abdrehen | IRR-Ausgang H bzw. Festwert in Loxone | mehr aktive Estrichmasse → längere Läufe; Forum-Konsens | wahrscheinlich (knx-user-forum #3/#10/#14) |
| 2 | Raumkorrektur in der 1490-Logik dämpfen (Mittelwert 30–60 min, Änderung ≤ 0,5 K/h); Heizkurve lieber in 1-K-Schritten senken als per Raumkorrektur hochziehen | Loxone-Logik vor AQ 1490 | weniger Zusatzstarts durch Soll-Sprünge | wahrscheinlich |
| 3 | IRR-Pwm bei thermischen Stellantrieben nicht auf kurze Werte; bei stetigen Antrieben 0–10 V statt PWM | IRR v2 Parameter Pwm | weniger Volumenstrom-Sprünge, Relais schonen | Vermutung (Loxone-Doku + Google-Groups) |
| 4 | Klima Controller: Mode 1 (nur Heizen) im Winter, Otm = 1, ϑLimH im eigenen Projekt prüfen (Std. 18 °C laut EN), ϑd auf 2–2,5 K heben, damit kein Kühl-Umschalten bei Sonne/Ofen | Klima Controller UG / IRR v2 | Kühlfalle zu; Ventile bleiben im Heizmodus offen | sicher (Funktion) / wahrscheinlich (Wirkung) |
| 5 | Wirkung messen: Starts/Tag und Laufdauer 7 Tage vorher/nachher aus Volllogger | `~/hoxpi_fulllog/` | Messung statt Theorie | – |

## Quellen (neu in Teil 2)
1. https://www.loxone.com/dede/kb/intelligente-raumregelung/ (erreichbar)
2. https://www.loxone.com/enen/kb/climate-controller/
3. https://www.loxone.com/enen/kb/intelligent-temperature-controller/
4. https://www.loxone.com/enen/kb/zoned-heating-comfort/
5. https://www.loxone.com/enen/kb/irc-v2/ (in Teil 1 genannt, hier Parametertabelle neu ausgewertet)
6. https://knx-user-forum.de/forum/%C3%B6ffentlicher-bereich/knx-eib-forum/knx-einsteiger/1539375-fussbodenheizung-w%C3%A4rmepumpe-knx
7. https://groups.google.com/g/loxone-english/c/zVpZ8WdBguM
8. https://www.energiesparhaus.at/forum-lwp-taktet-und-taktet-und-taktet/69988
Nicht erreichbar (nur Titel): https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/310713-12-1-klimacontroller-mischerkreis-taktet-bei-geringer-anforderung-permanent ; https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/214228-dimplex-wärmepumpe-und-loxone-raumregelung ; https://www.haustechnikdialog.de/Forum/t/276290/Wandheizung-mit-smarter-Einzelraumregleung-statt-hydraulischem-Abgleich-