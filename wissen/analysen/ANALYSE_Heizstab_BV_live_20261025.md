# ANALYSE F12 – Bivalenz-/Heizstab-Parameter BV live gelesen (25.10.2026 01:05, Orchestrator)

Katalog: F12 (Heizstab-Freigabe bei Kälte). Vorlauf: `[lokaler Pfad]` (dort: „BV-Werte nur vor Ort im Servicemenü“ – **damit überholt**).

## Kern
Die TopTronic liest die pCO-DB-Seite **0x87** des Kältereglers zyklisch über X26 (~alle 6,5 min). Darin stehen die BV-Parameter. Passiv aus dem Mitschnitt, nur gelesen, nichts gesendet.

| pCO-DB | Min/Max (Katalog 02.09.) | Einheit | Live 24.10. (220/220 gleich, 01:45–23:55) | Zuordnung V1.11 (`SPEZ_HAICO_Parameter.csv`) | Werkswert V1.11 |
|---|---|---|---|---|---|
| 0x8700 | 1 / 30 | – | 0 | ? (passt nicht zu BV001 0/2) | – |
| 0x8701 | 0 / 4 | – | 4 | ? | – |
| 0x8708 / 8709 / 870a / 870b | 0/3, 0/1, 0/1, 0/1 | – | 3 / 1 / 0 / 0 | ? (BV011/BV090/BV091-Kandidaten) | – |
| 0x870e | 60 / 75 | °C | 75 | ? | – |
| 0x8712 | 10,0 / 25,0 | °C | 17,0 | ? | – |
| 0x871e | 5 / 995 | h | 36 | ? | – |

Sicherheit:
- **Werte sicher** (220 von 220 Lesungen am 24.10. gleich, Quelle `~/rs485_sniff/log/rs485_2026-10-24.log.gz`, Decoder `~/rs485_sniff/rs485_pcodb.py --series`, Auswerteskript `[lokaler Pfad]`).
- **Zuordnung 0x8702–0x8707 = BV002/003/007/008/009/010 wahrscheinlich:** gleiche Reihenfolge, Min/Max und Datentyp exakt wie die V1.11-Parametertabelle; vier von sechs Werten = V1.11-Werkswert. BV002/BV003 weichen ab (-10/-20 statt -5/-10) → Hoval-Einstellung bzw. V1.18.004-Werkswert (Vermutung).
- Bedeutung nach iDM-Logik (Vermutung, Code-Beleg folgt mit Argon-Paket D-06): Bivalenzpunkt 1 = unter dieser AT darf der 2. Wärmeerzeuger zuschalten; Bivalenzpunkt 2 = darunter WP-Abschaltung bzw. nur 2. Erzeuger; BV007/BV008 = Freigabe-/Sperrverzögerung; BV009 = 180 passt zur Arbeitshypothese „180 K·min VL-Defizit“ aus V103.

## Vorhersage (ersetzt V103-Zahlen, zu prüfen durch W3-Wächter im Winter)
**V103b:** Der 6-kW-Stab der WP wird erst freigegeben, wenn **AT < -10 °C** (BV002) **und** die Bedingung mindestens **10 min** ansteht (BV007) bzw. ein Defizit von **180** (BV009, Einheit offen) aufgelaufen ist – oder bei WP-Störung. Alpenort (~960 m) erreicht -10 °C an einzelnen Wintertagen → Einsätze möglich, aber selten. Bei AT < -20 °C (BV003) ist mit WP-Abschaltung/Alleinbetrieb Stab zu rechnen (Vermutung).

## Was bringt uns das
Die Heizstab-Schwelle ist jetzt eine gemessene Zahl (-10 °C) statt „nur vor Ort“. Damit kann der Winterwächter gezielt an Frosttagen < -10 °C auf Stab-Einsatz schauen, und eine spätere Entscheidung (Bivalenzpunkt tiefer, z. B. -15 °C, um Stromkosten zu sparen) hat eine Grundlage. **Nichts geändert** – eine Änderung wäre ein Kälteregler-Parameter (tabu, nur der Betreiber/Hoval-Service).

## Offen
- 0x8700/8701/8708–871e zuordnen (Katalog-Folgefrage).