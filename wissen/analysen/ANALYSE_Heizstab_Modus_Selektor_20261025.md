
Live (nur gelesen): X26-Mitschnitt `~/rs485_sniff/log/rs485_2026-10-25.log`, `rs485_pcodb.py --series` (Skript `HoxPi-Doku\or_f12live_20261025_0420.sh`).

## (b) Was steht an P+0x740 … P+0x74F (je Instanz i = 0/1)
|---|---|---|---|---|---|
| 0x742+i | **BV001 / BV101** | u8 0..2 | BV001 = **4** (0x8701, Bereich live 0/4) | Schwellwahl: 1 → BV002/BV102 (P+0x744+2i), 2 → BV003/BV103 (P+0x748+2i); 0 **oder jeder andere Wert** → Merker := 0 | Code sicher |
| 0x744+2i | BV002 / BV102 | i16 | BV002 = −10 °C (0x8702) | Schwelle bei Selektor 1 | sicher |
| 0x748+2i | BV003 / BV103 | i16 | BV003 = −20 °C (0x8703) | Schwelle bei Selektor 2 | sicher |
| 0x74E+i | BV008 / BV108 | u8 | 10 (0x8705) | Sperrverzögerung | Zuordnung sicher, Rolle aus D-06 (nicht neu geprüft) |


### Folgerung für unsere Anlage (V1.11-Logik auf Live-Werte gelegt)
- CF008 = 3 → beide AT-Funktionen wären für Instanz 0 aktiv.
- **BV001 = 4 liegt außerhalb des V1.11-Bereichs 0..2.** In V1.11 führt jeder Wert außer 1/2 zu Merker = 0 → **beide AT-Merker würden nie gesetzt, die Schwellen −10/−20 °C wären wirkungslos** (sicher für V1.11).
- Der X26-Katalog der TopTronic (02.09., also V1.18) nennt für 0x8701 den Bereich 0..4 und für 0x8708 (BV011, live 3) 0..3 statt 0..1 → **V1.18.004 kennt mehr Selektorwerte** (wahrscheinlich). Was „4" in V1.18 bedeutet, ist **offen** (Vermutung: eigene Betriebsart, z. B. AT-unabhängig oder beide Schwellen). Die bisherige Vorhersage V103b/c („Stab erst bei AT < −10 °C") stützt sich damit auf eine Zuordnung, die in V1.18 anders sein kann.

| Befund | Stelle | Sicherheit |
|---|---|---|

## Was bringt uns das
- Der offene Parameter P+0x74C ist jetzt benannt (**BV007 = 10 min**) — die Heizstab-Bedingung im Gradminuten-Zweig ist vollständig mit Parameternummern beschrieben.
- Wichtiger: Mit **BV001 = 4** wären die AT-Schwellen in V1.11 abgeschaltet. Ob unsere Anlage (V1.18) die −10/−20-°C-Schwellen überhaupt nutzt, ist damit **unsicher** — der W3-Wächter darf im Winter nicht nur bei AT < −10 °C auf Stab/Verdichtersperre achten, sondern muss jeden Stab-Einsatz und jede Verdichtersperre mit AT notieren (V103d).
- Keine Handlung an der Anlage nötig. Falls der Betreiber BV001 je ansehen will: nur am HAICO-Servicemenü ablesen, nichts verstellen.

## Offen


| Befund | Stelle | Sicherheit |
|---|---|---|



| Befund | Stelle | Sicherheit |
|---|---|---|
| Ist-Konfiguration: PV008, PV027, PV002, CA020 stehen **nicht** in der pax-Abweichungsliste (59 Abweichungen, darunter BV001 = 4, das live bestaetigt ist) -> sehr wahrscheinlich Default 0 | R49_pax_Diff | wahrscheinlich (live nicht gelesen, X26-Adresse unbekannt) |


