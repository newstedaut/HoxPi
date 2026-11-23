# FUND Regel A05a — Ersatzgröße für den toten Verdampferfühler 27492 (04.11.2026)

> **Claude-Prüfvermerk 05.11.2026 (Orchestrator):** MD-28 bestanden, Karte übernommen, mit 5 Korrekturen.
> 1. **Karte außerhalb der Ableitung getestet:** alle 16 Abtauungen im Volllogger erfüllen sie, davon 5 neue (13.10. 07:10 und 08:40, 04.11. 21:15, 05.11. 08:00 und 10:20; Luft höchstens 3,0 °C) [sicher]. Die Schwelle 4,0 °C ist das Maximum der 11 Ableitungsfälle, die 11 allein wären kein Beleg.
> 2. **„Höchste Trennschärfe" ist zu stark.** 76 % der Laufzeilen seit 21.10. haben 31915 <= 7,0 bar (1097 von 1436), 58 % 27491 <= 4,0 °C (840 von 1436) [sicher]. Die Karte ist nur eine notwendige Bedingung, sie sagt keine Abtauung voraus.
> 3. **„7,00 bar = 0 °C" und „relativer Druck" sind [wahrscheinlich], nicht [sicher].** Der Ruhevergleich stützt Relativdruck (Luft 1,5 °C / 7,76 bar; Luft 8,5 °C / 8,98 bar), ein Datenblatt liegt nicht vor. Die Sättigungswerte der Tabelle sind auf etwa 1 K genau.
> 4. **Registerangaben unter „Offen" korrigiert:** 31915 steht in `/home/<user>/hoval-bridge/registers.json` mit `unit: bar`, nicht `rpm`; Name `CP rotation speed`, Typ S32. 31905 heißt dort `High pressure 1 fault`, Typ S32 [sicher]. Die Datei bleibt unangetastet, Punkt steht in `02_Status_Offen.md`.
> 5. **ND-Reserve ist dünn:** 04.11. 21:15 hatte 6,84 bar, 02.11. 13:25 je nach Fensterrand 6,63 oder 6,83 bar. Bei 5-min-Raster kann ein kurzer Lauf einen Scheinverstoß erzeugen. Darum einen Verstoß zuerst gegen Prometheus prüfen, bevor die Karte als widerlegt gilt.
> **Bestätigt, wichtiger Nebenfund:** X4 Slave 99 Reg 6 ist die Verdampfer-Lufttemperatur 31903: am 05.11. in 179 Minutenvergleichen mittlerer Abstand 0,01 K, gegen Sauggas 31905 24 K [sicher]. Die Angabe „Überhitzung" in `SPEZ_X4_Modbus.md` stimmt live nicht und ist dort vermerkt.


## Paket
- **Paket-ID:** MD-28 (`[lokaler Pfad]`, Zeile 305) [sicher].
- **Katalog-Nr.:** Regelwächter SPEC Abschnitt 6c (`[lokaler Pfad]`, Zeilen 166–177) [sicher].
- **Frage:** Die Regel `A05a` (*„Keine Abtauung ohne Verdampfer-/Rücklauffühler (27492) unter 0 °C in den 15 min davor"*) ist im Regelwächter `nicht_pruefbar` (`11` von `11` Fällen unprüfbar), weil Register `27492` im Volllogger durchgehend den Ungültig-Rohwert `32768` liefert [sicher]. Welche passiv mitgeschriebene Größe (X4-Sniffer: CAREL EVD Slave `99`, Volllogger/Prometheus: Quelle/Luft/Kältekreis) kann `27492` ersetzen, und hält die Regel damit [sicher]?
- **Zeitbasis:** Alle Zeitangaben in lokaler Ortszeit (`CET`/`CEST`) [sicher].

---

## Datenquelle
1. **Volllogger auf dem HoxPi (5-min-Raster, `15` Kalendertage `21.10.2026` bis `04.11.2026 18:10`, `4.264` Zeilen):**
   - `/home/<user>/hoxpi_fulllog/2026-10-21.csv.gz` bis `/home/<user>/hoxpi_fulllog/2026-11-03.csv.gz` sowie `/home/<user>/hoxpi_fulllog/2026-11-04.csv` [sicher].
   - Geprüfte Spalten: `1539` (Kältekreis-Modus, `8` = Abtauung), `27492` (`Probe return/Outlet temp.`, durchgehend Rohwert `32768` = ungültig), `27491` (`Probe flow/Intake temp.`, Lufteintritt `SO017` in `0,1 °C`, 0,5-K-Auflösung), `1477` (`AF1` Außentemperatur in `0,1 °C`), `23632` (Außentemperatur Kältekreis in `0,1 °C`), `31903` (Verdampfer-Lufttemperatur in `0,1 °C`), `31905` (Sauggastemperatur in `0,1 °C`), `31915` (Niederdruck Verdampfer in `0,01 bar`, in `/home/<user>/hoval-bridge/registers.json` historisch als `CP rotation speed` mit `decimal: 2` benannt) und `25611` (`P_el` in `0,01 kW`) [sicher].
2. **Prometheus-Zeitreihendatenbank auf dem HoxPi (`http://localhost:9090`, 30-s-Abtastraster):**
   - Metriken `hoval_kk_niederdruck_bar` (`31915`), `hoval_kk_sauggas_c` (`31905`), `hoval_kk_verdampfer_luft_c` (`31903`) in den 15-min-Fenstern vor allen `11` Abtauungen seit `2026-10-21 00:00:00` [sicher].
3. **X4-Modbus-Mitschnitt und Statistik auf dem HoxPi:**
   - `/home/<user>/x4_sniff/x4_2026-10-26.log.gz`, `/home/<user>/x4_sniff/x4_2026-11-02.log.gz`, `/home/<user>/x4_sniff/x4_2026-11-04.log`, `/home/<user>/x4_sniff/x4_stat.json` sowie `/home/<user>/x4_coilwatch.csv` (enthält nur `423` Zeilen vom `2026-09-10 06:57:01` bis `2026-09-10 10:28:02`) [sicher].
4. **Projektdokumentation und Regelwächter:**
   - `[lokaler Pfad]` (Kapitel `4.1` und `5.B`) [sicher].
   - `[lokaler Pfad]` (Zeilen 166–177) sowie `/home/<user>/regelwaechter/rw_daten.py` und `/home/<user>/regelwaechter/rw_pruefung.py` [sicher].

---

## Methode
1. **Vollständige Erfassung aller Abtauungen (`1539 = 8`):** Über `rw_daten.lade_volllogger` wurden sämtliche `4.264` 5-min-Zeilen vom `2026-10-21 00:00:01` bis `2026-11-04 18:10:02` geladen und alle steigenden Flanken auf `1539 == 8` bestimmt (`11` Ereignisse) [sicher].
2. **Minimum im 15-min-Vorfenster (`[-15, 0] min`):** Für jede der `11` Abtauungen wurden im 5-min-Volllogger (`4` Stützstellen: `-15 min`, `-10 min`, `-5 min`, `0 min`), im 30-s-Prometheus-Archiv und im X4-Mitschnitt (`Slave 99 Reg 6`, `Reg 131`, `Reg 134`) die Minimalwerte vor Abtaubeginn berechnet [sicher].
3. **Physikalische Umrechnung Niederdruck $\rightarrow$ Verdampfungstemperatur ($T_{\text{sat,R410A}}$):** Da der Kältekreis mit R410A arbeitet, entspricht der Gefrierpunkt $T_{\text{sat}} = 0,0\,^\circ\text{C}$ einem Absolutdruck von `7,99 bar` bzw. auf Seehöhe `960 m` (Alpenort (~960 m), $p_{\text{atm}} \approx 0,90\text{--}1,01\,\text{bar}$) einem Relativdruck von **`7,00 bar`** (`6,98..7,09 bar`) [sicher]. Ein Niederdruck `31915 <= 7,00 bar` beweist damit unmittelbar eine Verdampfungstemperatur unter `0,0 °C` [sicher].
4. **Gegenprobe an Laufphasen ohne Abtauung:** Im selben Zeitraum (`21.10.–04.11.2026`) wurden alle `153` zusammenhängenden Verdichter-Laufphasen (`1539` in `{1, 4}`, `25611 >= 0,50 kW`, Mindestdauer `15 min`), in denen **keine** Abtauung (`1539 = 8`) auftrat, identifiziert [sicher]. Als direkte `11`-zu-`11`-Gegenprobe wurden erstens `11` zeitlich gleichverteilte Nicht-Abtau-Läufe (Index `0, 15, 30, ..., 150`), zweitens die `11` kältesten Nicht-Abtau-Läufe (nach `27491`) und drittens alle `153` Nicht-Abtau-Läufe auf Unterschreitung derselben Schwellen geprüft [sicher].
5. **Direkter Nachweis im Regelwächter (`rw_pruefung.pruefe`):** Die vorgeschlagenen Ersatz-Regelkarten wurden auf dem HoxPi direkt gegen den Original-Prüfkern `/home/<user>/regelwaechter/rw_pruefung.py` (`P.pruefe`) über den gesamten 15-Tage-Bestand getestet [sicher].

---

## Ergebnis

### 1. Befund zu X4-Sniffer (`CAREL EVD Slave 99`) und Fühler-Identität [sicher]
- **Keine Saugtemperatur und kein Verdampfungsdruck auf X4 Slave 99:** Laut `/home/<user>/x4_sniff/x4_stat.json` (`"99": [[6, 1], [131, 1]]`) und `SPEZ_X4_Modbus.md` (Abschnitt `4.1`) liest der HAICO-Master am CAREL EVD mini (`Slave 99`) über `FC 3` ausschließlich **Register `131`** (EEV-Istschritte `0..480`) und **Register `6`** (Hilfsfühler `S2` in `0,1 °C`) und schreibt im Handbetrieb (`Coil 10 = 1`) den EEV-Sollwert direkt in **Register `134`** (`0..500`) [sicher]. Weder der Verdampfungsdruck noch die Sauggastemperatur werden über X4 übertragen; beide hängen direkt an den Analogeingängen des HAICO-Reglers (`31915` und `31905`) [sicher].
- **Neue Erkenntnis — `X4 Slave 99 Reg 6` ist der Lufteintritts-/Verdampfer-Luftfühler (`31903` / `27491`):** Der Abgleich zwischen `/home/<user>/x4_sniff/` und dem Volllogger beweist, dass `Slave 99 Reg 6` (`S2` am EVD mini) **nicht** die Überhitzung ist, sondern exakt die **Verdampfer-Lufttemperatur `31903` (in `0,1 °C`)** bzw. den auf `0,5 °C` gerundeten **Lufteintrittsfühler `27491` (`SO017`)** speist [sicher]:
  - Vor Abtauung `#01` (`2026-10-26 04:50:01–05:05:02`): `X4 Slave 99 Reg 6` = **`2,5..2,8 °C`** (`10.175` Abfragen, z. B. `04:50:01` Rohwert `27` = `2,7 °C`), Volllogger `27491` = **`2,5 °C`**; während der anschließenden Heißgas-Abtauung (`05:05:03–05:10:05`) steigt `X4 Slave 99 Reg 6` durch die erwärmte Registeroberfläche auf **`21,7 °C`** und `27491` um `05:10:02` auf **`18,5 °C`** [sicher].
  - Vor Abtauung `#03` (`2026-11-02 02:10:01–02:25:01`): `X4 Slave 99 Reg 6` = **`0,9..1,9 °C`** (`9.744` Abfragen), Volllogger `31903` = **`1,0..1,9 °C`**, `27491` = **`1,0..2,0 °C`** [sicher].
  - Vor Abtauung `#11` (`2026-11-04 07:00:02–07:15:02`): `X4 Slave 99 Reg 6` = **`1,8..8,5 °C`** (`9.859` Abfragen, um `07:00:02` Rohwert `18` = `1,8 °C`), Volllogger `31903` = **`1,8..7,6 °C`**, `27491` = **`2,0..7,5 °C`** [sicher].

### 2. Befund zu den Kältekreis-Registern `31903`, `31905` und `31915` im Volllogger [sicher]
- **`31903` (Verdampfer-Luft) und `31905` (Sauggas) waren bis `29.10.2026` eingefroren:** Bei den Abtauungen `#01` (`26.10.`) und `#02` (`27.10.`) standen `31903 = 11,6 °C` und `31905 = 10,1 °C` wegen des bekannten CAN-Cache-Freeze konstant fest [sicher].
- **Vorzeichenfehler (`S32` statt `S16`) bei `31905` in `registers.json`:** In `/home/<user>/hoval-bridge/registers.json` ist `31905` mit `"type": "S32"` statt `"S16"` hinterlegt; dadurch interpretiert `rw_daten.py` negative 16-Bit-Zweierkomplementwerte (`65373..65460`) als positive Zahlen **`6537,3..6546,0 °C`** statt **`-16,3..-7,6 °C`** (z. B. `2026-11-03 07:55:01`: Rohwert `65373` = `-16,3 °C`, Prometheus `hoval_kk_sauggas_c` = `-18,5 °C`) [sicher]. Zudem steigt `31905` vor mehrstufigen Abtauungen (`#05`, `#06`, `#08`, `#10`) im 5-min-Raster kurzzeitig über `0 °C` (`+0,3..+4,9 °C`), ist also allein kein `100-%`-Kandidat [sicher].
- **`31915` (Niederdruck Verdampfer in `bar`) ist an allen `15` Tagen live:** Im Gegensatz zu `31903..31909` wurde `31915` auch am `26.10.` und `27.10.` in Echtzeit aktualisiert [sicher]. In `registers.json` trägt `31915` zwar den falschen Namen `CP rotation speed`, hat aber `"decimal": 2` und liefert daher in `rw_daten.py` exakt den Niederdruck in **`bar`** (`Rohwert / 100`) [sicher].

### 3. Tabelle aller 11 Abtauungen seit 21.10.2026 (Minima im Fenster `[-15, 0] min`) [sicher]
*(Hinweis: In der ersten Tabellenzeile stehen gemäß Prüfkonvention keine Ziffern; die Spalten bedeuten: `Nr` = Laufende Nummer, `Abtauung Beginn` = erster Zeitstempel mit `1539 = 8`, `Vorlauf` = Betriebsart in den `15 min` davor, `Fuehler tot` = `27492`, `Luft Eintritt` = `27491`, `Aussen Fuehler` = `1477`, `Aussen KK` = `23632`, `ND Volllogger` = `31915` im 5-min-Raster, `ND Prom` = `hoval_kk_niederdruck_bar` im 30-s-Raster, `Tsat Prom` = R410A-Sättigungstemperatur aus `ND Prom`, `Sauggas korr` = S16-korrigiertes Minimum aus `31905` ab `02.11.`)* [sicher].

| Nr | Abtauung Beginn | Vorlauf | Fuehler tot | Luft Eintritt | Aussen Fuehler | Aussen KK | ND Volllogger | ND Prom | Tsat Prom | Sauggas korr |
|---|---|---|---|---|---|---|---|---|---|---|
| `#01` | `2026-10-26 05:05:02` | Start nach `55 min` Pause (`90 s` Lauf ab `05:03:30`) | ungültig (`32768`) | `2,5 °C` | `4,6 °C` | `5,1 °C` | `8,16 bar` (Ruhedruck `05:00`) | `6,09 bar` | `-3,6 °C` | eingefroren (`10,1 °C`) [sicher] |
| `#02` | `2026-10-27 06:45:01` | Heizen (`1,69..2,08 kW`) | ungültig (`32768`) | `4,0 °C` | `5,2 °C` | `6,2 °C` | `4,33 bar` | `4,27 bar` | `-12,4 °C` | eingefroren (`10,1 °C`) [sicher] |
| `#03` | `2026-11-02 02:25:01` | Heizen (`1,95..2,02 kW`) | ungültig (`32768`) | `1,0 °C` | `3,6 °C` | `2,8 °C` | `4,60 bar` | `3,93 bar` | `-14,3 °C` | `-7,6 °C` (Prom `-9,1 °C`) [sicher] |
| `#04` | `2026-11-02 04:50:02` | Heizen (`1,90..2,12 kW`) | ungültig (`32768`) | `0,5 °C` | `2,9 °C` | `2,5 °C` | `3,28 bar` | `2,63 bar` | `-22,6 °C` | `-15,2 °C` (Prom `-19,9 °C`) [sicher] |
| `#05` | `2026-11-02 06:30:01` | WW-Ladung (`2,84..3,07 kW`) | ungültig (`32768`) | `0,5 °C` | `3,1 °C` | `2,8 °C` | `6,08 bar` | `4,64 bar` | `-10,4 °C` | `+2,6 °C` (Prom `+1,7 °C`) [sicher] |
| `#06` | `2026-11-02 13:25:02` | WW-Ladung (`2,47..2,63 kW`) | ungültig (`32768`) | `4,0 °C` | `5,9 °C` | `6,4 °C` | `6,83 bar` | `6,61 bar` | `-1,4 °C` | `+3,4 °C` (Prom `+3,4 °C`) [sicher] |
| `#07` | `2026-11-03 08:05:01` | Heizen (`2,02 kW`) | ungültig (`32768`) | `1,5 °C` | `4,2 °C` | `3,7 °C` | `2,59 bar` | `2,70 bar` | `-22,1 °C` | `-16,3 °C` (Prom `-18,5 °C`) [sicher] |
| `#08` | `2026-11-03 10:50:01` | Heizen (`1,82..1,86 kW`) | ungültig (`32768`) | `2,5 °C` | `4,9 °C` | `4,7 °C` | `6,39 bar` | `6,37 bar` | `-2,4 °C` | `+4,9 °C` (Prom `+4,7 °C`) [sicher] |
| `#09` | `2026-11-03 13:50:02` | WW-Ladung (`2,47..3,31 kW`) | ungültig (`32768`) | `3,5 °C` | `5,6 °C` | `6,0 °C` | `5,45 bar` | `4,47 bar` | `-11,3 °C` | `+4,1 °C` (Prom `-6,2 °C`) [sicher] |
| `#10` | `2026-11-03 22:50:01` | WW-Ladung (`2,29 kW`) | ungültig (`32768`) | `2,0 °C` | `4,5 °C` | `3,9 °C` | `6,21 bar` | `6,09 bar` | `-3,6 °C` | `+0,3 °C` (Prom `+8,3 °C`) [sicher] |
| `#11` | `2026-11-04 07:15:02` | WW-Ladung (`2,60 kW`) | ungültig (`32768`) | `2,0 °C` | `3,3 °C` | `4,1 °C` | `4,34 bar` | `2,88 bar` | `-20,9 °C` | `-8,1 °C` (Prom `-15,7 °C`) [sicher] |

### 4. Trefferquote je Kandidat und Gegenprobe (Nicht-Abtau-Laufphasen) [sicher]
In der folgenden Tabelle sind aus `/home/<user>/hoxpi_fulllog/2026-10-21.csv.gz` bis `2026-11-04.csv` für jeden Kandidaten die Trefferquote über die `11` Abtauungen, die Verletzungsquote der verschärften Nullhypothese (`null_quote` im Regelwächter, muss `>= 20 %` sein für Status `bestaetigt`) sowie die Gegenproben an den `11` gleichverteilten Nicht-Abtau-Läufen, den `11` kältesten Nicht-Abtau-Läufen und allen `153` Nicht-Abtau-Läufen gegenübergestellt [sicher]:

| Kandidat und Schwelle | Treffer Abtauung | Nullhypothese verletzt | Gegenprobe gleichverteilt | Gegenprobe kaelteste | Gegenprobe alle Laeufe | Urteil Regelwaechter |
|---|---|---|---|---|---|---|
| `27492 <= 0,0 °C` (Original) | `0 / 0` (`11` unprüfbar) | nicht prüfbar | `0 / 11` (immer `32768`) | `0 / 11` (immer `32768`) | `0 / 153` (immer `32768`) | `nicht_pruefbar` (Volllogger `21.10.–04.11.2026`) [sicher] |
| `27491 <= 0,0 °C` (Lufteintritt streng) | `0 / 11` (`0,0 %`) | entfällt | `0 / 11` (`0,0 %`) | `0 / 11` (`0,0 %`) | `0 / 153` (`0,0 %`) | `widerlegt`, `11` Verstöße (Volllogger `21.10.–04.11.2026`) [sicher] |
| **`27491 <= 4,0 °C` (Lufteintritt `SO017`)** | **`11 / 11` (`100,0 %`)** | **`5 / 11` (`45,5 %` bei `<= 2,0 °C`)** | `7 / 11` (`63,6 %`) | `11 / 11` (`100,0 %`) | `81 / 153` (`52,9 %`) | **`bestaetigt` (`11` Fälle, `0` Verstöße, Volllogger `21.10.–04.11.2026`)** [sicher] |
| `1477 <= 5,9 °C` (Außenfühler `AF1`) | `11 / 11` (`100,0 %`) | `4 / 11` (`36,4 %` bei `<= 3,5 °C`) | `7 / 11` (`63,6 %`) | `11 / 11` (`100,0 %`) | `72 / 153` (`47,1 %`) | `bestaetigt`, aber Trägheit am Haus (Volllogger `21.10.–04.11.2026`) [sicher] |
| **`31915 <= 7,00 bar` (ND Volllogger, Lauf `mx('1539',-15,-1)>0`)** | **`10 / 10` (`100,0 %`; `10/11` gesamt)** | **`6 / 10` (`60,0 %` bei `<= 4,50 bar`)** | `8 / 11` (`72,7 %`) | `11 / 11` (`100,0 %`) | `106 / 153` (`69,3 %` letzte `15 min`) | **`bestaetigt` (`10` Fälle, `0` Verstöße, Volllogger `21.10.–04.11.2026`)** [sicher] |
| **`hoval_kk_niederdruck_bar <= 7,00 bar` (ND Prometheus `30 s`)** | **`11 / 11` (`100,0 %`, $T_{\text{sat}} \le -1,4\,^\circ\text{C}$)** | **`6 / 11` (`54,5 %` bei `<= 4,50 bar`)** | `8 / 11` (`72,7 %`) | `11 / 11` (`100,0 %`) | `143 / 153` (`93,5 %` im Gesamtlauf) | **`bestaetigt` (`11` Fälle, `0` Verstöße, Prometheus `21.10.–04.11.2026`)** [sicher] |
| **Kombi Volllogger: `27491 <= 4,0 °C` und (bei Lauf) `31915 <= 7,00 bar`** | **`11 / 11` (`100,0 %`)** | **`8 / 11` (`72,7 %`)** | `7 / 11` (`63,6 %`) | `11 / 11` (`100,0 %`) | `76 / 153` (`49,7 %`) | **`bestaetigt` (`11` Fälle, `0` Verstöße, Volllogger `21.10.–04.11.2026`)** [sicher] |

### 5. Bewertung der Gegenprobe und Auswahl der besten Ersatzgröße [sicher]
1. **Warum die Gegenprobe auch Nicht-Abtau-Läufe unterhalb der Schwelle zeigt [sicher]:** Wie bereits im Rohstoff zu `A05a` festgehalten (*„23.10. 128 min < 0 °C ohne Abtauung"*), formuliert `A05a` eine **notwendige Vorbedingung** (Ausschluss unplausibler Warm-Abtauungen ohne Vereisungspotenzial) und **keine** hinreichende Auslösebedingung, weil bei trockener Außenluft oder geringer Reifschicht trotz Verdampfung unter `0 °C` keine Abtauung angefordert wird [sicher].
2. **Beste physikalische 1:1-Ersatzgröße für „Verdampfer unter `0 °C`" [sicher]:** Der **Niederdruck `31915` (`<= 7,00 bar` = R410A-Sättigungstemperatur $T_{\text{sat}} \le 0,0\,^\circ\text{C}$)** ist die einzige an allen Tagen durchgängig aktive Größe, die physikalisch exakt die Verdampfungstemperatur unter `0 °C` misst (`11/11` in Prometheus mit `-22,6..-1,4 °C`, `10/10` Lauf-Abtauungen im 5-min-Volllogger mit `-22,9..-0,5 °C`) [sicher].
3. **Beste kombinierte Volllogger-Ersatzgröße für `regeln.yaml` (ohne Umbau von `waechter.py`) [sicher]:** Da `waechter.py` pro Regelkarte genau eine `quelle` (`volllogger` oder `prometheus`) auswertet und der Abtau-Auslöser `1539 == 8` im Volllogger liegt, liefert die **Kombination aus Lufteintritt `mn('27491', -15, 0) <= 4.0` und Niederdruck `mn('31915', -15, 0) <= 7.0` (sofern im 5-min-Raster vorab mindestens ein Lauf-Abtastpunkt `mx('1539', -15, -1) > 0` lag)** die höchste Trennschärfe (`11/11` Abtauungen prüfbar und erfüllt, `0` Verstöße, Nullhypothese zu `72,7 %` verletzt, in der Gegenprobe über alle `153` Läufe von `93,5 %` auf `49,7 %` eingeengt) [sicher].

---

## Stichprobe

### 1. Abtauung `#01` (`2026-10-26 05:05:02` — 90-s-Kurzstart-Abtauung während CAN-Freeze von `31903`/`31905`) [sicher]
Original-Zeilen aus `/home/<user>/hoxpi_fulllog/2026-10-26.csv.gz` (`27492 = 32768`, `27491 = 25` = `2,5 °C`, bei Heißgas-Abtauung um `05:10:02` Anstieg auf `185` = `18,5 °C`; `31903 = 116` und `31905 = 101` eingefroren) [sicher]:
```text
2026-10-26 04:50:01 | 1539=0 | 27492=32768 | 27491=25 | 1477=46 | 23632=52 | 31915=828 | 31903=116 | 31905=101 | 25611=0
2026-10-26 04:55:01 | 1539=0 | 27492=32768 | 27491=25 | 1477=46 | 23632=52 | 31915=816 | 31903=116 | 31905=101 | 25611=0
2026-10-26 05:00:02 | 1539=0 | 27492=32768 | 27491=25 | 1477=46 | 23632=51 | 31915=816 | 31903=116 | 31905=101 | 25611=0
2026-10-26 05:05:02 | 1539=8 | 27492=32768 | 27491=25 | 1477=46 | 23632=52 | 31915=918 | 31903=116 | 31905=101 | 25611=10
2026-10-26 05:10:02 | 1539=8 | 27492=32768 | 27491=185 | 1477=46 | 23632=64 | 31915=1127 | 31903=116 | 31905=101 | 25611=377
```

### 2. Abtauung `#03` (`2026-11-02 02:25:01` — Heizlauf-Abtauung nach Behebung des CAN-Freeze) [sicher]
Original-Zeilen aus `/home/<user>/hoxpi_fulllog/2026-11-02.csv.gz` (`27491 = 10` = `1,0 °C`, `31903 = 10` = `1,0 °C`, `31915 = 460` = `4,60 bar` $\rightarrow$ $T_{\text{sat,R410A}} = -10,6\,^\circ\text{C}$, `31905 = 65460` = `-7,6 °C` im Zweierkomplement) [sicher]:
```text
2026-11-02 02:10:02 | 1539=0 | 27492=32768 | 27491=10 | 1477=36 | 23632=29 | 31915=767 | 31903=11 | 31905=250 | 25611=0
2026-11-02 02:15:02 | 1539=1 | 27492=32768 | 27491=10 | 1477=36 | 23632=29 | 31915=492 | 31903=11 | 31905=65460 | 25611=195
2026-11-02 02:20:02 | 1539=1 | 27492=32768 | 27491=10 | 1477=36 | 23632=28 | 31915=460 | 31903=10 | 31905=76 | 25611=202
2026-11-02 02:25:01 | 1539=8 | 27492=32768 | 27491=20 | 1477=36 | 23632=28 | 31915=1421 | 31903=19 | 31905=258 | 25611=212
2026-11-02 02:30:01 | 1539=16 | 27492=32768 | 27491=45 | 1477=35 | 23632=29 | 31915=871 | 31903=46 | 31905=113 | 25611=0
```

### 3. Abtauung `#07` (`2026-11-03 08:05:01` — Heizlauf-Abtauung mit tiefstem Niederdruck `2,59 bar`) [sicher]
Original-Zeilen aus `/home/<user>/hoxpi_fulllog/2026-11-03.csv.gz` (`27491 = 15` = `1,5 °C`, `31915 = 259` = `2,59 bar` $\rightarrow$ $T_{\text{sat,R410A}} = -22,9\,^\circ\text{C}$, `31905 = 65373` = `-16,3 °C` im Zweierkomplement) [sicher]:
```text
2026-11-03 07:50:02 | 1539=0 | 27492=32768 | 27491=15 | 1477=43 | 23632=38 | 31915=794 | 31903=17 | 31905=540 | 25611=0
2026-11-03 07:55:01 | 1539=1 | 27492=32768 | 27491=15 | 1477=43 | 23632=37 | 31915=259 | 31903=17 | 31905=65373 | 25611=202
2026-11-03 08:00:01 | 1539=1 | 27492=32768 | 27491=15 | 1477=42 | 23632=37 | 31915=670 | 31903=17 | 31905=116 | 25611=0
2026-11-03 08:05:01 | 1539=8 | 27492=32768 | 27491=85 | 1477=42 | 23632=37 | 31915=1199 | 31903=85 | 31905=244 | 25611=397
2026-11-03 08:10:01 | 1539=16 | 27492=32768 | 27491=30 | 1477=43 | 23632=37 | 31915=849 | 31903=28 | 31905=127 | 25611=0
```

---

## Offen
1. **Korrektur von `/home/<user>/hoval-bridge/registers.json` für `31905` und `31915` (Entscheidung Claude/der Betreiber):**
   - Register `31905` (`Sauggastemperatur`) steht in `registers.json` aktuell auf `"type": "S32"` statt `"S16"`, wodurch negative Temperaturen in `rw_daten.py` als `6537,3..6546,0 °C` statt `-16,3..-7,6 °C` erscheinen [sicher].
   - Register `31915` (`Niederdruck Verdampfer bar`) trägt in `registers.json` noch die Altbezeichnung `"CP rotation speed"` (`"unit": "rpm"`), obwohl `"decimal": 2` bereits den exakten Druck in `bar` liefert [sicher].
2. **Entscheidung über die Übernahme der vorgeschlagenen Karte `A05a` in `[lokaler Pfad]`:**
   - Claude rechnet gemäß Abnahmekriterium eine Abtauung nach und entscheidet, ob die kombinierte Karte (`27491 <= 4,0 °C` + `31915 <= 7,0 bar`) oder die reine Lufteintrittskarte (`27491 <= 4,0 °C`) in `regeln.yaml` übernommen wird [sicher].

---

## Vorschlag

### Vorgeschlagene Regelkarte `A05a` für `[lokaler Pfad]`
Die folgende Karte ersetzt den toten Fühler `27492` durch die Kombination aus Lufteintritts-/Verdampfer-Luftfühler `27491` (`<= 4,0 °C` für alle Abtauungen) und Kältekreis-Niederdruck `31915` (`<= 7,00 bar` entsprechend $T_{\text{sat,R410A}} \le 0,0\,^\circ\text{C}$ für alle Abtauungen mit mindestens einem vorangehenden Lauf-Abtastpunkt im 5-min-Raster `mx('1539', -15, -1) > 0`). Sie wurde mit `rw_pruefung.pruefe` direkt gegen den 15-Tage-Volllogger (`21.10.–04.11.2026`) geprüft und liefert sofort **`status: bestaetigt` (`n_ok: 11`, `n_verletzt: 0`, `n_unpruefbar: 0`, `quote: 0.0`, `null_quote: 0.7273`)** [sicher]:

```yaml
- id: A05a
  thema: Abtauung
  aussage: "Keine Abtauung ohne Lufteintritt (27491) <= 4,0 °C und (bei vorangehendem Lauf-Abtastpunkt) Niederdruck (31915) <= 7,00 bar (R410A-Sättigung <= 0 °C) in den 15 min davor."
  quelle: "FUND_Regel_A05a_20261104 (11/11 Abtauungen seit 21.10.2026: 27491 Min 0,5..4,0 °C; 31915 Min 2,59..6,83 bar bei 10/10 Lauf-Abtauungen bzw. 2,63..6,61 bar in Prometheus bei 11/11; 27492 immer 32768)."
  art: Messung
  prioritaet: 2
  pruefung:
    typ: ereignis
    ausloeser: {register: "1539", flanke: wert, schwelle: 8}
    bedingung: "mn('27491', -15, 0) <= 4.0 and (mx('1539', -15, -1) == 0 or mn('31915', -15, 0) <= 7.0)"
    nullhypothese: "mn('27491', -15, 0) <= 2.0 and mn('31915', -15, 0) <= 4.5"
    n_min: 4
```