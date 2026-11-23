# F61: Stellantriebe UG/OG lesbar machen (Analyse 01.11.2026, nur lesen)

## Frage
F61 (`[lokaler Pfad]`): Welche Loxone-Controls/States liefern die Ventilstellung bzw. Heiz-/Kühlanforderung je Raum lesbar, gibt es Verlauf/Statistik, und wie loggt man das für das Heizkurven-Urteil im Winter mit? Ausgangslage: 02_Status_Offen OR-22.10. „Stellantriebe sind keine lesbaren Controls“.

## Datenquellen
- Loxone-MCP (Live-Miniserver): `list_rooms`, `control_find`, `control_describe`, `control_state`, `control_history`, `control_statistics`. Nur lesend, keine Befehle.
- Projektdatei (nur Select-String, nicht ganz eingelesen): `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` (neueste, 25.10.2026 22:44, 1.760.734 Byte). Vergleich: `[lokaler Pfad]` ist älter.
- Vorwissen: `[lokaler Pfad]` (Klimacontroller `OutHeat1` -> Reg 1490).

## Methode
1. Alle Intelligenten Raumregler (Typ `IRoomControllerV2`) per `control_find` aufgezählt (9 Stück).
2. `control_describe` / `control_state` für Raumregler Wohnzimmer, WC UG und Klimacontroller UG; States `active`, `tempActual`, `tempTarget`, `currentMode` für alle Räume.
3. `control_history` und `control_statistics` je für Raumregler und Klimacontroller.
4. Projektdatei: Suche nach `Stellantrieb|Ventil`, dann Verdrahtung der `OutputRef` zu den `TreeAactor` zurückverfolgt.

Loxone-Bausteine: Intelligente Raumregelung https://www.loxone.com/dede/kb/intelligente-raumregelung/ · Klimacontroller https://www.loxone.com/dede/kb/klima-controller/ · Stellantrieb Tree https://www.loxone.com/dede/kb/stellantrieb-tree/ · Formel https://www.loxone.com/dede/kb/formel/

## Ergebnis

### Kernaussage
- **[sicher, Projektdatei]** Es gibt 9 **Loxone Stellantriebe Tree** (Baustein `TreeAactor` AQ1, 0–10 -> 0–100 %, alle „Heizkreisverteiler“). Sie haben `Display StateOnly="true"` und sind **nicht** visualisiert. Deshalb fehlen sie in der App-Struktur (LoxAPP3) und damit im Loxone-MCP (`control_find "Stellantrieb Ventil"` findet nichts). Die Aussage von OR-22.10. stimmt.
- **[sicher, Projektdatei]** Jeder Stellantrieb (außer Wohnzimmer) hängt direkt am Ausgang **`AQhc1`** seines Raumreglers (Heizen/Kühlen-Quellausgang 1 = Klimacontroller UG). `AQhc1` selbst wird von der API **nicht** als State ausgegeben (fehlt in `control_describe` states).
- **[sicher, Projektdatei]** Wohnzimmer (2 Antriebe VZ und RZ) hängt nicht direkt am Raumregler, sondern an der Formel `Ofen_An_Formel` (Z. 12377): `IF(I4>1;0;IF(I3>0;I3;IF(I2-I1>5;2.5;0)))` mit I3 = Raumregler-WZ `AQhc1`, I1/I2 = zwei Temperaturen, I4 = Formel „Heizen/Kühlen“. Die WZ-Ventilstellung kann also vom Raumregler abweichen (Ofen -> 25 %).
- **[sicher, Live]** Lesbar ist je Raum: Raumregler-State `active` (Heiz-/Kühlphase aktiv 0/1) und im Klimacontroller UG der State **`controls`** (JSON mit `demand` je Raumregler-UUID) sowie `demandHeat` (%) gegen `threshold` (30 %). Das ist die Ventil-**Anforderung**, nicht die gemessene Ventilstellung.
- **[wahrscheinlich]** `demand` ist die Öffnung 0..1 je Raum (laut Loxone-Doku: Mittel aus Öffnungsgrad × Raumgröße). Beobachtet nur 0 und 1; `demandHeat` = 33 % bei 4 von 8 Räumen mit 1 passt zu einer Flächengewichtung (bei Gleichgewicht wären es 50 %). Ob Zwischenwerte vorkommen, ist offen.

### Tabelle je Raum (Live-Werte 01.11.2026 15:58 UTC = 16:58 MEZ)
Raumregler-UUID = Control-UUID (Typ `IRoomControllerV2`). `demand` aus Klimacontroller UG State `controls`. Stellantrieb = `TreeAactor` (nicht lesbar), Quelle laut Projektdatei.

| Raum | Raumregler-UUID | Stellantrieb (TreeAactor-UUID, Seriennr.) | Eingang des Antriebs | tempActual | tempTarget | currentMode | active | demand |
|---|---|---|---|---|---|---|---|---|
| Wohnzimmer | <UUID> | <UUID> (VZ, <Seriennr>) + <UUID> (RZ, <Seriennr>) | Formel Ofen_An_Formel AQ (I3 = AQhc1) | 21,9 | 21,5 | 1 | 0 | 0 |
| Badezimmer | <UUID> | <UUID> (<Seriennr>) | AQhc1 | 23,2 | 23,5 | 1 | 1 | 1 |
| WC UG | <UUID> | <UUID> (<Seriennr>) | AQhc1 | 21,9 | 22,5 | 4 | 1 | 1 |
| Büro | <UUID> | <UUID> (<Seriennr>) | AQhc1 | 22,0 | 21,5 | 1 | 1 | 1 |
| Technikraum | <UUID> | <UUID> (<Seriennr>) | AQhc1 | 19,64 | 19,5 | 1 | 1 | 1 |
| Zimmer OG 1 | <UUID> | <UUID> (<Seriennr>) | AQhc1 | 21,4 | 21,0 | 1 | 0 | 0 |
| Zimmer OG 2 | <UUID> | <UUID> (<Seriennr>) | AQhc1 | 20,7 | 20,5 | 1 | 0 | 0 |
| Hütte | <UUID> | <UUID> (<Seriennr>) | AQhc1 | 18,1 | 12,0 | 1 | 0 | 0 |
| Garage | <UUID> | keiner gefunden | – | 10,2 | 5,0 | 4 | 0 | nicht im Klimacontroller |

Klimacontroller UG (<UUID>, Typ ClimateControllerUS): `demandHeat` = 33, `threshold` = 30, `mode` = 2, `stage` = 2, `demandCool` = 0, `actualOutdoorTemp` = 6,3.

- **[sicher]** Werte aus `control_state`, Zeitstempel 15:58 UTC.
- **[sicher]** `active` und `demand` stimmen in allen 8 Räumen überein.
- **[wahrscheinlich]** `active` = 1 bedeutet „Heizphase aktiv, Ventil > 0“; Gegenrichtung (Ventil auf, aber active 0) nicht gesehen.
- **[Vermutung]** Zuordnung UG/OG: nur aus Raumnamen ableitbar (WC UG sicher UG); nicht geprüft, deshalb keine Spalte.
- **[sicher]** 9 TreeAactor in der Datei, 9 OutputRefs gefunden, alle zugeordnet (Bad, Büro, Hütte, Zimmer OG 1, Zimmer OG 2, Technikraum, WC UG, WZ ×2).

### Verlauf
- **[sicher]** `control_statistics`: Raumregler und Klimacontroller liefern Fehler „neither statisticV2 nor statistic.outputs – not chartable“. Keine Miniserver-Statistik für diese States.
- **[sicher]** `control_history` Raumregler (Aktivitätslog, max. 20 Einträge, ereignisbasiert): Wohnzimmer reicht vom 30.10. 01:04 UTC bis 01.11. 02:08 UTC, also rund 2–3 Tage. Inhalt nur Ereignisse wie „Klimacontroller UG wird zum Heizen verwendet – Ventile/Klappen aktiviert“ bzw. „… nicht mehr verwendet – Ventile geschlossen, Standby wegen unzureichender Anforderung“. Keine Prozentwerte.
- **[sicher]** Klimacontroller UG: kein Aktivitätslog (`hasHistory` fehlt).
- **[sicher]** `control_state history=N` ist nur ein RAM-Puffer seit Start des MCP-Prozesses (heute ab 15:58 UTC, 3 Einträge). Nicht dauerhaft.

## Stichprobe (zum Gegenprüfen)
| Abfragezeit (UTC) | Control | UUID | State | Wert |
|---|---|---|---|---|
| 2026-11-01 15:58:12 | Klimacontroller UG | <UUID> | `demandHeat` | 33 (threshold 30) |
| 2026-11-01 15:58:17 | Badezimmer (Raumregler) | <UUID> | `active` | 1 |

## Vorschlag (nicht umgesetzt)
1. **Pi-Rekorder liest Loxone lesend mit (empfohlen).** Ein kleiner Dienst auf dem HoxPi verbindet sich per Loxone-WebSocket (wie der MCP) und schreibt alle 5 min (Takt wie Volllogger) eine CSV-Zeile: je Raum `tempActual`, `tempTarget`, `active`, `currentMode`, dazu Klimacontroller `controls` (je Raum `demand`), `demandHeat`, `threshold`, `stage`. Ablage z. B. `~/hoxpi_fulllog/loxone_irr_YYYYMMDD.csv`, Zeitachse = Volllogger, damit sie neben Reg 1490/VL/RL liegt. Nur Lesen, kein Eingriff in die Projektdatei. [wahrscheinlich ausreichend für das Heizkurven-Urteil: Anteil „Ventil auf“ je Raum und Stunde gegen Außentemperatur und Raum-Ist-Soll]
2. **Echte Ventilstellung (0–100 %) sichtbar machen.** Nur mit Projektänderung möglich, deshalb Entscheidung der Betreiber: entweder je TreeAactor „In Visualisierung verwenden“ aktivieren, oder je Raum einen Baustein Status/Analogwert (InfoOnlyAnalog mit Statistik) an `AQhc1` bzw. an den Formel-Ausgang WZ hängen. Dann liefern `control_state` und `control_statistics` den Wert direkt. Vorher Backup und Skill `loxone-xml-umbau`. [sicher: braucht Umbau; Vermutung: ca. 10 Bausteine]
3. **Vorhandene Statistik nutzen:** nicht möglich, die Raumregler haben keine Statistik (siehe Verlauf). Das Aktivitätslog reicht nur ~2–3 Tage und hat keine Prozentwerte. [sicher]
4. Für das Wohnzimmer zusätzlich `Ofen_An_Formel` beachten: Bei Ofen öffnet die WZ-FBH auf 25 % unabhängig vom Raumregler. Die Anforderung im Klimacontroller zeigt das nicht. [sicher, Projektdatei]

## Offen
- Kommen bei `demand` Zwischenwerte (z. B. 0,4) vor, oder schalten die Raumregler nur auf/zu? Klärt der Rekorder aus Vorschlag 1 nach einem Tag. [offen]
- Gewichtung von `demandHeat` (Raumgrößen-Parameter je Raumregler) nicht ausgelesen. [offen]
- Zuordnung der Räume zu UG/OG und welcher Heizkreis das OG versorgt (siehe Anlagenbeschreibung, HK2 aus). [offen]
- Live-Miniserver = Projektdatei vom 25.10. 22:44 angenommen. [wahrscheinlich]
- Link Stellantrieb Tree (loxone.com/dede/kb/stellantrieb-tree/) nicht abgerufen. [Vermutung: Pfad richtig]