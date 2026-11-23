# ANALYSE OG-Versorgung / HK2 - Katalogfrage F2 (23.10.2026, Analyse-Agent, nur lesend)

## Kurzfazit
- **Wahrscheinlich bis sicher: Das OG wird von der Wärmepumpe gar nicht beheizt.** Es gibt keinen hydraulischen Weg zum OG, der in Betrieb ist: keine Pumpe läuft, kein Kreis ist geregelt.
- **Sicher (Daten):** HK2 hat in der Hoval nie gearbeitet. Pumpe 19707 = 0, Status 1502 = 0, Betriebswahl 1479 = 0, und der Vorlauf VF2 (1514) liegt auf Raumniveau (19 °C).
- **Sicher (Projektdatei):** In Loxone gibt es keinen Pumpen- oder Relaisausgang für das OG bzw. HK2. Der „Klimacontroller HC2“ hat keine Raumregler (`controls = []`). Alle 8 Raumregler hängen am „Klimacontroller UG“.
- **Sicher (deine eigene Angabe im Vault, 06.08.2026):** „Wärmepumpe heizt nur das UG (Fußbodenheizung). EG wird nur in der Küche geheizt, per Split-Klima. OG meist gar nicht; bei Bedarf 2 × 900 W Infrarot im Zimmer OG.“
- **Begriffsfalle (sicher, Vault 10.10.2026):** UG = Keller, EG = Mittelgeschoss, **OG = Dachboden**. Alte Namen mit „OG“ für das Mittelgeschoss sind Fehlbenennungen. „HK2 OG“ in Hoval und Loxone ist daher wahrscheinlich ein Platzhalter für einen geplanten Kreis und keine laufende Versorgung.
- **1-Wire „Thermometer_HK2_OG_Vorlauf“:** Ob er lebt, ist **nicht live belegbar**. Er hat keine App-Kachel und wird nicht geloggt. Sein einziger Abnehmer ist eine Formel „Heizen/Kühlen“, deren Ausgang nirgends verdrahtet ist. Für die Regelung ist er damit bedeutungslos.
- **Korrektur:** Die Projektanweisung „Fußbodenheizung: 2 Stockwerke à ca. 100 m²“ passt nicht zur Messlage. Beheizt wird per WP nur das UG über HK1.

## Belege
### A. Aus Daten belegt (HoxPi / Volllogger)
| Zeit (lokal) | Quelle | Wert | Bedeutung |
|---|---|---|---|
| 23.10.2026 18:55:01 | Pi `~/hoxpi_fulllog/2026-10-23.csv`, letzte Zeile | 1479 = 0, 1491 = 165, 1494 = 50, 1502 = 0, 1513 = 343, 1514 = 189 | HK2 Standby/abgeschaltet, VF2 18,9 °C; HK1-VL 34,3 °C zum Vergleich |
| 23.10.2026 ~18:59 | HoxPi-MCP `read_register` | 19707 = 0 (HK2-Pumpe), 1514 = 190 → 19,0 °C | Pumpe aus, VF2 auf Raumniveau |
| 16.–23.10.2026 | `ANALYSE_Mischer_HK1_HK2_Regelguete_20261023.md` (2196 Punkte) | 1479/1502/19563/19707 immer 0, Mischer 19659 dauernd −100 (zu), 1514 = 17,6–26,2 °C | Kreis über die ganze Woche nie aktiv |

### B. Loxone live (MCP, 23.10.2026 16:56–16:59 UTC = 18:56–18:59 lokal)
| Control | UUID | Wert | Aussage |
|---|---|---|---|
| Klimacontroller HC2 | <UUID> | `controls = []`, demandHeat 0, stage 0 | Keine Raumregler zugeordnet (sicher) |
| Klimacontroller UG | <UUID> | 8 Regler: Wohnzimmer, Badezimmer, WC UG, Büro, Zimmer OG 1, Hütte, Technikraum, Zimmer OG 2 | Alle Raumregler sitzen am UG-Kreis (sicher) |
| HK2 Pumpe | <UUID> | „Aus“ | deckt sich mit 19707 = 0 |
| HK2 Vorlauf ist | <UUID> | 18,9 °C | Raumniveau, kein Durchfluss |
| Thermometer_HK1_UG_Vorlauf (1-Wire) | <UUID> | 33,25 °C, error 0 | Der Schwesterfühler lebt |
| BadWC_EG (Zähler) | <UUID> | Jahr 345,7 kWh, gesamt 1872,7 kWh | Das EG-Bad wird **elektrisch** beheizt |
- Räume (`list_rooms`): Es gibt keinen OG- oder EG-Raum mit Raumregler. Die einzigen Stockwerkskennungen sind „WC UG“ und „Terrasse UG“.

### C. Loxone-Projektdatei (nur gelesen)
Datei: `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone`, Stand 23.10.2026 17:15, 17 031 Zeilen.
- Z. 6340/6341: `Lox1wireDevice` „Thermometer_HK2_OG_Vorlauf“, ROMID 28CE2F540D0000C3, Sensor AWI4. **Ohne** `Visu="true"`, ohne `StatsType`, deshalb weder Kachel noch Statistik.
- `MaxVal="10"` haben **alle** 1-Wire-Fühler, auch HK1 (Z. 6325), und HK1 liefert 33,25 °C. Die Vermutung aus `ANALYSE_Loxone_Fuehler_Inventar_Heizung_20261023.md`, MaxVal würde den Wert begrenzen, ist damit **widerlegt**. MaxVal ist hier nur die Anzeigeskala.
- Z. 10427: InputRef des Fühlers, Ausgang AQ → nur Z. 10801. Das ist die Formel „Heizen/Kühlen“ (Z. 10799, `IF(I1>26;1;IF(I1<21;2;0))`). Ihr Ausgang AQ (<UUID>) kommt in der Datei **nur einmal vor** (Z. 10806), ist also nicht weiterverdrahtet. Sicher: Der Fühler steuert nichts.
- Pumpen/Relais: Die Titelsuche nach Stellantrieb|Ventil|Relais|Pumpe|Heiz findet „HK1 Pumpe“ und „HK2 Pumpe“ nur als **Modbus-Lese-Sensoren**/States aus der Hoval und keinen Loxone-Ausgang für eine OG- oder HK2-Pumpe. Die Relais „Aktor (Relais) 11–14“ und „Heizstab“ sind andere Verbraucher (siehe Titel).
- Der einzige Heizungsmischer-Baustein ist „Vorlautemperatur HC1 - Fußboden Heizen+Kühlen“ (Heatmixer2, Z. 13450), gekoppelt an den Klimacontroller UG. Doku: https://www.loxone.com/dede/kb/klimacontroller/ und https://www.loxone.com/dede/kb/intelligente-raumregelung/

### D. Vault (deine Angaben, Zitate)
- `[eigene Notizen]`, Abschnitt 5 („Stand 06.08.2026, Fassung 3, Heizsituation korrigiert … nach deinen Angaben“): „Wärmepumpe heizt nur das UG (Fußbodenheizung). EG wird nur in der Küche geheizt, per Split-Klima … OG meist gar nicht; bei Bedarf 2 × 900 W Infrarot im Zimmer OG. Zwischendecken ungedämmt …“
- `[eigene Notizen]`, „Geschossnamen – verbindlich (10.10.2026)“: „UG = Keller … EG = Mittelgeschoss … OG = Dachboden. Alte Namen mit ‚OG‘ für das Mittelgeschoss sind Fehlbenennungen.“
- `[eigene Notizen]` Z. 264: „Umbau OG mit Fußbodenheizung“ ist ein **geplantes** Vorhaben und nicht der Bestand.
- `[eigene Notizen]` Z. 17: „Vorlaufist HC2 (OG)“. Das ist nur die Benennung und belegt keinen Betrieb.

### E. Auf Foto sichtbar
- Nichts. `[lokaler Pfad]` enthält nur Google-Photos-URLs ohne Beschreibung, und kein Foto ist als Verteiler/HK2/OG benannt. Deshalb habe ich kein Bild geöffnet. Ob am Verteiler im Technikraum ein zweiter Abgang (HK2) **physisch** vorhanden und vorbereitet ist, ist **nicht** per Foto belegt.

## Was bringt uns das
- Die Heizkurven- und Effizienzbewertung bezieht sich **nur auf das UG (HK1)**. Wärme ins EG und OG kommt nur indirekt über die ungedämmten Zwischendecken, ins EG zusätzlich über Split-Klima und den elektrischen Bad-Kreis. Das erklärt einen Teil der „Grundlast“ außerhalb der WP.
- Die Heizlast-Abschätzung und das Argument „3- bis 5-fach überdimensioniert“ beziehen sich faktisch auf ca. 100 m² und nicht auf 200 m². Die Überdimensionierung ist eher **größer** als angenommen.
- HK2 und der 1-Wire-HK2-Fühler können in Loxone/HoxPi als **„inaktiv/Reserve“** markiert werden. Ein Anlegefühler „Rücklauf HK2“ (Vorschlag aus dem Fühler-Inventar) ist überflüssig.
- Den Fühler `Thermometer_HK2_OG_Vorlauf` brauchen wir erst, wenn der Dachboden-/EG-Umbau mit FBH kommt. Bis dahin kann er (nur mit Freigabe) umgewidmet werden, z. B. als HK1-Rücklauf.
- **Zur Korrektur der Projektanweisung** (macht die Hauptsitzung, nicht dieser Agent): Statt „FBH 2 Stockwerke à ca. 100 m²“ besser „WP-FBH nur UG (~100 m²); EG Küche Split-Klima, EG-Bad elektrisch; OG = Dachboden, Infrarot Zimmer OG; HK2 = Reserve, nie in Betrieb“.

## Frage an der Betreiber
Keine nötig. Das Fertig-Kriterium ist aus Daten und deiner eigenen Vault-Angabe erfüllt.
Ein Restpunkt, nur zur Info und ohne Eile: Ob am Verteiler/Mischer im Technikraum ein HK2-Abgang physisch verrohrt ist (z. B. als Vorbereitung für den Umbau), zeigt kein Foto. Für die Regelung spielt das keine Rolle.
Durchsucht: BAUTEILE_BEKANNT.md, 02_Status_Offen.md, ANALYSE_Loxone_Fuehler_Inventar_Heizung_20261023.md, ANALYSE_Mischer_HK1_HK2_Regelguete_20261023.md, Fotos_Album\_index.txt, Vault (*.md ohne HoxPi_Docs), Loxone live (Räume, Raumregler, Klimacontroller, HK2-Controls, Zähler), Projektdatei UMBAU.Loxone, HoxPi 1514/19707, Volllogger 2026-10-23.csv.

## Stichprobe für den Prüfer
1. **Volllogger:** Auf dem Pi `~/hoxpi_fulllog/2026-10-23.csv`, Zeile mit `zeit = 2026-10-23 18:55:01`. Spalte `1514` = **189** (×10 → 18,9 °C), Spalte `1502` = **0**, Spalte `1479` = **0**. Nachlesen mit: `python [lokaler Pfad] 'grep 18:55:01 ~/hoxpi_fulllog/2026-10-23.csv | head -c 200'` (Spalte n = Register − 1475).
2. **Projektdatei:** `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone`. Z. 6341 trägt `Title="Thermometer_HK2_OG_Vorlauf"` ohne `Visu="true"`. Die UUID `<UUID>` (Ausgang der Formel „Heizen/Kühlen“) kommt in der ganzen Datei **genau einmal** vor (Z. 10806), ist also unverdrahtet. Prüfen mit `Select-String -SimpleMatch '<UUID>'`.