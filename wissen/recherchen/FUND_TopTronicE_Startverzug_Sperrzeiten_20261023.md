# FUND: TopTronic E / UltraSource – Startverzug nach Heizanforderung, Sperrzeiten (Recherche 23.10.2026 11:54)

Anlage: UltraSource B comfort C17, TTE-WEZ SW 2.15.006, HK1 „Heizen extern/konstant“ (Loxone).
Beobachtung: Verdichter startet oft ~20 min nach Anforderung, Mindeststillstand ~15 min.
Baut auf: FUND_TopTronicE_Heiz_Schaltdifferenz_Takten_20261023.md (33-053/054 dort belegt, hier nicht wiederholt), FUND_Zuschaltzeiten_Sperrzeiten_Takten_20261015.md, FUND_Navigator_Fachmann_Parameter_20261015.md.

## 0. Korrektur zu früheren Funden (wichtig)
- Das GP-Joule-PDF „Technische_Unterlagen_Steuerung_Hoval.pdf“ ist laut WebFetch (23.10.2026) die Anleitung **„Fernwärmemodul TTE-FW“**. Wärmepumpen-/WEZ-Parameter stehen dort NICHT drin.
  https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
  Daraus folgt: Die Werkswerte für 05-0xx, 06-0xx und 07-0xx in FUND_Zuschaltzeiten… (z. B. 05-081, 05-083, 07-003) gelten für TTE-FW. Am TTE-WEZ der UltraSource können sie anders sein. Gleiche Nummern über Module hinweg bedeuten nicht automatisch dieselbe Funktion (33-000…33-002 sind beim TTE-FW Fühler/VE-Konfiguration, beim WEZ liegen unter 33-05x die Schaltdifferenzen).
- FUND_Zuschaltzeiten… Abschnitt 3 („feste Mindeststillstandszeit 10–15 min, Restart-Delay, Modbus-Statuscode 16“) hat eine Sammelquelle ohne konkretes Dokument (idm-energie.at / hoval.at). **Nicht als Beleg verwenden.** Im Hoval-Datenpunkttext unten bedeutet 16 „Störung“, nicht Restart-Delay.
- Die 15-min-Mindeststehzeit aus der iDM-Navigator-2.0-Anleitung ist iDM, nicht Hoval. Sie passt aber zur Beobachtung, siehe 1.2.

## 1. BELEGT

### 1.1 Hoval-Datenpunkt „Zustand Wärmeerzeugerregelung“ (dp 18743) kennt eigene Sperr-/Verzögerungszustände
Quelle: Hoval-Datenpunkttexte, von des Betreibers Anlage per HoxPi ausgelesen (Projektdoku `Heizung/fetch_missing_en_out.txt`, 17.10.2026). Kein öffentliches Web-Dokument, aber es ist Hoval-Firmwaretext von genau dieser Anlage. Wortlaut (Auszug):
- „#2 = Vorlaufzeit Heizbetrieb“
- „#3 = Extern gesperrt“
- „#27 = Warmwasser Ladesperre“
- „#28 = Minimale Auszeit“ / „#29 = Minimale Einzeit“
- „#33 = Verzoegerung Folge WE“
- weitere: 0 Abgeschaltet, 1 Heizbetrieb, 17 Blockiert, 21 WFmax-, 22 WFsoll-Abschaltung, 26 Bivalenzabschaltung, 32 Nachlauf
Bedeutung: Die WEZ-Regelung führt nachweislich eine **Mindest-Auszeit** (= Mindeststillstand), eine **Mindest-Einzeit**, eine **Vorlaufzeit Heizbetrieb** und eine **WW-Ladesperre** als eigene Zustände. Wo der Startverzug herkommt, lässt sich also **messen statt raten**: Man liest dp 18743 in der Wartephase ab.
Ergänzend (gleiche Quelle): dp 1501 HK-Zustand „#23 = Heizbetrieb Extern/Konstantanforderung“; dp 17384 Puffer „#1 = Anforderung, Temp. tief, PLP aus (Entladeschutz)“ und „#3 = Anforderung UPE-Umschaltverzögerung“. dp 27549 nennt eine „bedingte Freigabe (09-011)“ des WEZ abhängig von der Außentemperatur.

### 1.2 Nutzerbeleg 15-min-Zwangspause beim Verdichter (UltraSource)
- Marty (energiesparhaus.at, 31.01.2024, #57) fragt, ob jemand von WW auf Heizen umschalten konnte „ohne die 15min Zwangspause beim Verdichter?“
  https://www.energiesparhaus.at/forum/56645_3
  Im Thread keine Antwort, keine Parameternummer. Damit ist die beobachtete ~15-min-Pause **nach WW-Ladung** bei einer zweiten UltraSource bestätigt.
- MSC1 (10.12.2022): „Mindest Verdichter Stehzeit … (auch einstellbar)“. Die Startbedingung ist UND-verknüpft: Stehzeit abgelaufen UND VL-Ist um Einschaltdiff. unter VL-Soll. https://www.energiesparhaus.at/forum/70426 (bereits im Vorfund, hier nur als UND-Logik präzisiert)

### 1.3 Zeitparameter WW, Forenabschriften UltraSource (Fachmannebene, keine Werkswert-Belege)
- „Warmwasser Ladevorgang "05-002" = 0,1h“ und „Pumpenachlauf "05-003" = 0,5min“ (Domi90, 29.11.2023) https://www.energiesparhaus.at/forum/56645_2
  05-003 ist Nachlauf, kein Vorlauf. Die Funktion von 05-002 ist nicht beschrieben, siehe 2.
- Abtauung: „Max. Abtauzeit "33-283" = 15min“ (ffischer, 11.02.2020) https://www.energiesparhaus.at/forum/56645_2

## 2. WAHRSCHEINLICH (abgeleitet, nicht belegt)
- **~15 min Mindeststillstand = Zustand 28 „Minimale Auszeit“.** Das ist sehr wahrscheinlich eine Verdichter-Schutzzeit im WEZ- bzw. Kältekreisregler (Hoval-Display „Zwangspause“). Sie gilt auch nach einer WW-Ladung, weil das Umschalten WW→Heizen für den Verdichter Stopp und Neustart bedeutet. Die Parameternummer ist öffentlich nicht zu finden. Sie liegt vermutlich im 33-xxx-Block (WEZ/Wärmepumpe) oder ist im Kältekreis fest hinterlegt.
- **~20 min bis Start = Summe mehrerer Bedingungen**, keine einzelne Verzögerung. Plausibel ist eine Kombination aus:
  a) laufender Mindest-Auszeit seit dem letzten Stopp (28),
  b) VL-Ist noch nicht um 33-054 unter VL-Soll. Bei HK „extern/konstant“ zählt der Konstant-Sollwert plus 07-001 Überhöhung. Hat das Wasser im Puffer bzw. im Kreis noch Wärme, dauert das Abkühlen bis zur Schwelle,
  c) Vorlaufzeit Heizbetrieb (2), also die Pumpe läuft vor dem Verdichter. Typisch sind Sekunden bis wenige Minuten, nicht 20 min,
  d) WW-Ladesperre (27) oder Puffer-Entladeschutz (dp 17384 = 1).
- **Wenn 18743 in der Wartezeit = 1 (Heizbetrieb) zeigt und das FA-Status-Feld nicht 4 ist**, wartet höchstwahrscheinlich der Kältekreis bzw. FA-Automat, etwa auf eine Schutzzeit oder auf 33-054. In diesem Fall ist die TTE-Ebene nicht die Bremse.
- 05-002 „Warmwasser Ladevorgang 0,1h“ (6 min) kann eine Mindest-Ladezeit oder eine Sperre sein. Das ist nur eine Vermutung.
- 09-011 „bedingte Freigabe“ des WEZ nach Außentemperatur (dp 27549) ist bei Bivalenz/Heizstab relevant, für den Startverzug wahrscheinlich nicht.

## 3. NICHT GEFUNDEN (öffentlich, ohne Login)
- Parameternummer, Werkswert, Bereich und Ebene von Mindest-Auszeit, Mindest-Einzeit und Vorlaufzeit Heizbetrieb am TTE-WEZ bzw. an der UltraSource.
- Eine TopTronic-E-WEZ- bzw. UltraSource-Fachmannanleitung mit Parametertabelle. Öffentlich gibt es nur Kataloge und Technikhandbücher ohne Regelungsparameter. Belaria-Parameter gelten laut Forum nicht für die UltraSource (energiesparhaus 69911, 04.11.2022: „Stimmt, ist von der Belaria.“ https://www.energiesparhaus.at/forum-hoval-ultrasource-mit-toptronic-e-raumeinfluss-einstellbar/69911).
- Werkswerte und Bereiche für 33-053 und 33-054 (wie im Vorfund).
- Eine eigene „Sperrzeit nach WW-Ladung“ als Parameter. Belegt ist nur die 15-min-Zwangspause als Nutzerbeobachtung.
- Hinweise, ob „Heizen extern/konstant“ eine eigene Zuschaltverzögerung hat.

## 4. Was das bringt
- Den Startverzug muss man nicht mehr per Webrecherche klären, sondern per Zustandslog. Dafür in der Wartezeit alle 1 min mitschreiben: dp 18743 (Zustand WEZ-Regelung), 18723 (FA-Status), 18724/18744 (WEZ-Soll), 18725 (WEZ-Ist), 18742 (RL) und 1501 (HK-Zustand). Das geht über HoxPi, nur lesen. Die Zustandsfolge zeigt dann direkt, ob es an 28 (Mindest-Auszeit), 27 (WW-Sperre), 2 (Vorlaufzeit) oder an der Temperaturschwelle (33-054) liegt.
- Nur die Temperaturschwelle lässt sich sinnvoll beeinflussen: 33-054 kleiner bedeutet früherer Start, aber mehr Takte. Die Mindest-Auszeit ist Verdichterschutz und soll nicht verkürzt werden.

## 5. Was der Betreiber am Bedienteil ablesen soll (nur lesen, nichts verstellen)
1. Info › Wärmeerzeuger › UltraSource während einer Wartephase (Anforderung von Loxone aktiv, Verdichter aus): „Status Wärmeerzeugerregelung“ und „FA-Status“ alle 2–3 min fotografieren, mit Uhrzeit. Erwartet wird ein Wert aus 2 / 27 / 28 / 1.
2. Dabei auch WEZ-Soll Heizen, WEZ-Ist und RL WEZ notieren. Startet sie bei WEZ-Ist ≈ Soll − 33-054?
3. Info › Heizkreis HK1: Zustand sollte „Heizbetrieb Extern/Konstantanforderung“ (23) sein. Vorlauf-Soll Konstant ablesen.
4. Fachmannebene, nur ansehen: im WEZ-Menü 33-xxx nach Einträgen mit „Auszeit“, „Einzeit“, „Stehzeit“, „Vorlaufzeit“, „Sperr“ oder „Verzög“ suchen. Nummer, Wert, Einheit, min/max notieren.
5. 05-002 (Warmwasser Ladevorgang): Klartext und Hilfetext abschreiben.
6. 09-011 (bedingte Freigabe) und den zugehörigen Außentemperatur-Wert ablesen.
7. Fällt ein Startverzug von ~20 min mit einer WW-Ladung kurz davor zusammen? Zeitpunkt des WW-Ladeendes notieren.

Quellen-Check (23.10.2026, WebFetch): energiesparhaus 56645_3 (Marty #57, „15min Zwangspause“) ✓, 56645_2 ✓, 70426 ✓, 69911 ✓, GP-Joule-PDF = TTE-FW ✓. dp-18743-Text aus Projektdoku `Heizung/fetch_missing_en_out.txt` (lokal, nicht öffentlich).