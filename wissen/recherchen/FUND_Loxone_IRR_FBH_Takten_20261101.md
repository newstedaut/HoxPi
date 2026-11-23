# FUND Loxone IRR + FBH + Takten (F59) – 01.11.2026
Recherche-Subagent im OR-Lauf 01.11.2026 15:30; gegengelesen Claude. loxone.com/dede/kb und deutsche Loxforum-Seiten lieferten aus der Cloud-Umgebung 403 → Inhalte aus ES/EN-Fassung derselben KB-Seiten. Nachlesen der DE-Seiten über des Betreibers Browser sinnvoll.
Unsere Kette: Loxone schreibt HK1-Soll 1490; Hoval startet bei RL ≈ Soll − 1,5 K (+ ~13–18 min), stoppt bei RL ≈ Soll + 3 K; Läufe 30–35 min, Pausen 20 min–5 h.

## Belegt
[Klima Controller](https://www.loxone.com/dede/kb/klima-controller/) [1]:
- Mode −1 aus / 0 Auto / 1 nur Heizen / 2 nur Kühlen. MinHr = Mindestlaufzeit (min) vor Standby/Gegenmodus, Standard 0. Sot = Einschaltschwelle der gemittelten Raumanforderung, Standard 30 %.
- Anforderung = (Soll − Ist) × Raumfläche; Räume mit Präsenz bevorzugt. Pulsbetrieb Don 750 s / Doff 300 s (≥ 180 s), aktiv ab MaxTp %, MaxTp = 0 aus. Wiederanlaufsperre 3 min + Fod (120 s).
- Aot = 1 nutzt 48-h-Mittel ϑoa mit ϑLimH 15 °C / ϑLimC 10 °C (Mechanismus des Kühlfallen-Umbaus 23.10.). Sv/Vd nur bei Quellentyp Wärmepumpe.
- Bei Luft/Wasser mit Pufferwasser rät Loxone vom automatischen Heizen/Kühlen-Wechsel ab.
[Intelligente Raumregelung IRR v2](https://www.loxone.com/dede/kb/irr-v2/) [2][3]:
- Ausgänge H/C/HC (0…10) für Stellantriebe; H1–3/C1–3/HC1–3 Quellenausgänge zum Klima Controller; HCm Modus.
- PWM-Ausgänge mit Intervall Pwm (0 = automatisch, ≥ 1 min). ϑd Komfort-Abweichung 0,5–5 K (Std. 1,5), ϑe Eco (Std. 2).
- Unter der Klima-Controller-Schwelle kann eine Mindestöffnung erzwungen werden, bis die Quelle nach Mindestlaufzeit abschaltet (Parametername nicht genannt). Hs/Cs Aufheiz-/Abkühlrate (0 = gelernt). Vs Ventil-Stillstandsschutz 14 d.
- [Übersicht Raumklima](https://www.loxone.com/dede/kb/uebersicht-raumklima/): Raumregler → Klima Controller → [Intelligente Temperatursteuerung](https://www.loxone.com/dede/kb/intelligente-temperatursteuerung/) → Mischer; Takten/WP nicht behandelt. [4]
- Loxforum: gegen Kurzstarts Schwellwertschalter am IRC-Analogausgang (z. B. ein 5 / aus 4); Wirkung im Thread nicht belegt. [5]
- energiesparhaus.at, Mehrheitsmeinung: Einzelraumregelung bei FBH + modulierender WP verstärkt eher das Takten; besser hydraulischer Abgleich, Kreise am Verteiler. Loxone-Mitarbeiter hält dagegen (System lernt Trägheit). [6][7]
- Gegen Takten: sehr kurze Kreise zudrehen/zusammenlegen, keine hydraulische Weiche, Puffer nur bei fehlendem Mindestvolumen (Parallelpuffer), Vorlauf tief; flachere Heizkurve, Heizgrenze aus ~16-h-Mittel, Heizfenster (ein Nutzer: ~30 → 12–13 Starts/Tag). Puffer strittig (JAZ). [8][9]
- iDM: Mindestlaufzeit 2–5 min, Mindeststillstand 3–10 min; > 6 Starts/h = Zeichen für Überdimensionierung/zu enges Totband. [10]

## Wahrscheinlich
- Loxone-Taktschutz (MinHr, Sot, Doff, 3-min-Sperre) wirkt bei uns nicht auf den Verdichter: H/C des Klima Controllers sind laut `[lokaler Pfad]` nicht zur WP verdrahtet. Wirksam sind nur 1490 (Höhe/Änderung) und Masse/Volumenstrom über die Stellantriebe.
- Schließende Stellantriebe verkürzen Läufe (weniger Masse → RL erreicht Soll + 3 K schneller). [6][8]
- Unser Takt (30–35 min Lauf, ≥ 20 min Pause) liegt weit unter der iDM-Warnschwelle 6 Starts/h. [10]

## Nicht gefunden
- Offizielle Loxone-Empfehlung "Stellantriebe offen lassen"/"Abgleich statt Raumregelung"/Grundlastkreis; Parametername der IRR-Mindestöffnung; Inhalte der DE-Loxforum-Threads (403); haustechnikdialog.

## Vorschläge ohne Umsetzung (der Betreiber entscheidet)
| # | Vorschlag | Ort | Erwartete Wirkung | Sicherheit |
|---|---|---|---|---|
| 1 | UG-Kreise großteils dauerhaft offen, nur 1–2 Räume über IRR schließen, Verteilung über Abgleich | [IRR v2](https://www.loxone.com/dede/kb/irr-v2/) H-Ausgang | mehr Masse → längere Läufe, seltener Starts | wahrscheinlich [6][8] |
| 2 | Kein kurzes PWM an thermischen Antrieben (Pwm groß oder aus) | IRR v2 Pwm | weniger Volumenstromsprünge | Vermutung |
| 3 | 1490 nur langsam ändern (Rampe ≤ 0,5 K/h), Raumkorrektur glätten | Loxone-Logik vor AQ 1490 | weniger Zusatzstarts durch Soll-Sprünge | wahrscheinlich |
| 4 | Nach Verdichter-Stopp 1490 für X min ~2 K senken (eigene Sperrzeit) | Loxone-Logik | erzwungene Mindestpause; Komfortrisiko bei Kälte | Vermutung |
| 5 | Klima Controller im Winter Mode 1, Aot = 1, Sot ≥ 30 % | [Klima Controller](https://www.loxone.com/dede/kb/klima-controller/) | kein Heiz/Kühl-Wechsel | sicher [1] |
| 6 | Pufferfühler 62/63 aktivieren (Hoval, nur mit Fachmann/Freigabe) | Hoval | größere Hysterese; JAZ-Kosten | Vermutung |
| 7 | Vorher/Nachher Starts je Tag aus Volllogger zählen | `~/hoxpi_fulllog/` | Messung statt Theorie | – |

## Quellen
1. https://www.loxone.com/eses/kb/controlador-clima/ (ES zu https://www.loxone.com/dede/kb/klima-controller/)
2. https://www.loxone.com/enen/kb/irc-v2/ (EN zu https://www.loxone.com/dede/kb/irr-v2/)
3. https://www.loxone.com/enen/kb/intelligent-room-controller/
4. https://www.loxone.com/dede/kb/uebersicht-raumklima/
5. https://www.loxforum.com/forum/software-configuration-user-interface/375307-intelligent-room-controller-gen1-keeps-activating-my-heat-pump
6. https://www.energiesparhaus.at/forum/70145
7. https://www.energiesparhaus.at/forum/58625
8. https://www.energiesparhaus.at/forum-waermepumpe-falsch-dimensioniert/66005
9. https://www.energiesparhaus.at/forum-ueberdimensionierte-waermepumpe/24763
10. https://www.idm-energie.at/en/heat-pump-control/on-off-control/