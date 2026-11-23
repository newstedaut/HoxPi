# FUND: Verdichterstarts, Mindestlaufzeit, Ölrückführung – sind 15–25-min-Läufe schädlich?

**Datum:** 23.10.2026 · **Claude Orchestrator, Recherche** (nur öffentliche Webquellen ohne Login, WebFetch am 23.10.2026)
Kennzeichnung: **[BELEGT]** = URL + Wortlaut/Zahl selbst abgerufen · **[WAHRSCHEINLICH]** = abgeleitet · **[NICHT GEFUNDEN]**
Nicht wiederholt (steht schon in FUND_C17_… / FUND_Zuschaltzeiten_…): C17-Datenblatt-Minima, >12 m → 40 % Mindestdrehzahl, 15-min-Mindeststehzeit (V99), OptiPower/BFE, Hoval-Puffer-Text „Mindestlaufzeiten berücksichtigt“.
Kältemittel: R410A (Hoval-Datenblatt, bereits belegt). Verdichterbauart (Rollkolben/Scroll) des C17: **[NICHT GEFUNDEN]** – nicht behaupten.
Achtung: Der „Ölrückführzyklus 2–5 min“-Absatz in FUND_Zuschaltzeiten_… §1 hat keine URL → als **unbelegt** behandeln.

---

## 1. Starts pro Jahr – Feldtest [BELEGT]

**Fraunhofer ISE, WP-QS im Bestand, Schlussbericht (Kurzfassung S. 9)** – https://www.ise.fraunhofer.de/content/dam/ise/de/documents/projekte/WP-QS_Schlussbericht.pdf
- „eine große Streuung von 550 bis 15.800 Verdichterstarts pro Jahr“
- „90 % der Anlagen weisen weniger als 5.500 Starts je Jahr auf“; „etwa ein Drittel liegt bei maximal 2.000“
- „Gleichwohl werden sehr geringe Betriebsstarts von unter 2.000 nur von knapp dimensionierten Wärmepumpen erreicht.“ (Satz < 15 Wörter gekürzt zitiert)
- Anlagen mit > doppelter Heizlast bei −7 °C konnten trotzdem „mit weniger als 4.000 Starts im Jahr betrieben werden“
- „Sehr kurze Betriebsphasen von nur wenigen Minuten können mitunter direkte Schäden verursachen.“
- Ursachen hoher Schalthäufigkeit laut Bericht: Regelung auf Vorlauftemperatur, geringe Hysterese, schlecht genutzter Modulationsbereich, kleine parallele Speicher. Eine Minutenangabe für „zu kurz“ nennt die Kurzfassung **nicht**; Kap. 6.3 (S. 98) per WebFetch nicht erreichbar.
- Pressemitteilung (77 WP, davon 61 L/W, 4 Jahre): „Schalthäufigkeiten lagen bei einigen Anlagen im sehr hohen Bereich“ – https://www.ise.fraunhofer.de/content/dam/ise/de/documents/presseinformationen/2025/3025_ISE_PI_Waermepumpen-heizen-auch-im-Altbau-klimafreundlich.pdf

**Lebensdauer in Starts (Hersteller-Wissensseite)** – alpha innotec: „Typical heat pumps are designed for 200,000 to 300,000 starts.“ – https://www.alpha-innotec.com/en/knowledge-base/heat-pump-knowledge-center/service-life-of-a-heat-pump [BELEGT, ohne Prüfnorm/Quelle]
- Gegenposition (Ratgeber, ohne Quelle): „rund 100.000 Schaltzyklen“ als Richtwert – https://42watt.de/magazin/lebensdauer-waermepumpe [nur zweite Hand, nicht belastbar]

## 2. Mindestlaufzeit / Starts pro Stunde – Verdichterhersteller [BELEGT]

**Copeland Variable-Speed-Scroll für Wärmepumpen ZHW015–030 (Application Guidelines)** – https://climate.emerson.com/documents/copeland-scroll-variable-speed-heat-pump-compressors-zhw015-zhw030-en-gb-4223802.pdf
- §5.12: „The most critical consideration is the minimum run time required to return oil“ – **kein fester Minutenwert**, Ermittlung per Schauglas-Test in der Anlage
- Test soll in der Anlage „with the longest connecting lines“ erfolgen (= lange Kältemittelleitung ist der Auslegungsfall)
- „Emerson recommends a maximum of 10 starts per hour.“
- „There is no minimum off time because scroll compressors start unloaded“
- §2.4.6: Ölrückholung nötig bei „continuous operation of over two hours below 1800 rpm“ → „ramp up … to 3600 rpm for 5 minutes“
- Start: „start with a speed of 3000 rpm“, Drehzahl mind. 30 s halten
- Gleiche Aussagen (10 Starts/h, Mindestlaufzeit = Ölrückführung) auch in Copeland XHV-VS-Guideline: https://media.copeland.com/<UUID>/C060239_1218_E_AGL_HPScroll_XHV_VS_FULL.pdf

**Danfoss Performer Scroll (Festdrehzahl, Parallelverbund)** – https://assets.danfoss.com/documents/89978/AB230086439211en-000801.pdf
- „minimum compressor running time of 2 minutes“; „no more than 12 starts per hour“; Anti-Short-Cycle „A three-minute (180-sec) time-out is recommended.“
- Leitungen „exceeding 20 m or with many oil traps“ → evtl. Ölnachfüllung

**iDM Wissensseite On/Off-Regelung** (Herstellerseite, gilt für Ein/Aus-Betrieb) – https://www.idm-energie.at/en/heat-pump-control/on-off-control/
- Mindestlaufzeit typisch 2–5 min, Mindeststillstand 3–10 min, akzeptabel 4–6 Starts/h (Wohn-WP)

**Labortest UK/DECC (EA Technology 2012, Festdrehzahl-WP)** – https://assets.publishing.service.gov.uk/media/5a78e0d9e5274a2acd18a7c6/7389-effects-cycling-heat-pump-performance.pdf
- „short cycling (run times of less than 6 minutes) have a detrimental effect“
- Empfehlung: „minimum run time of circa 6 minutes“; L/W-WP bei ~8 min nahe Katalog-COP
- Mindestlaufzeit auch nötig „to ensure the establishment of good oil circulation“
- Inverter nicht untersucht.

**Inverter vs. Ein/Aus – Simulationsstudie** – Dongellini & Morini 2019, Energy Conv. Mgmt. 196, DOI 10.1016/j.enconman.2019.06.022, Abstract: https://cris.unibo.it/handle/11585/699402
- Taktverluste relevant „only for single-stage units“, dort SPF bis −12 %; Inverter vermeiden Takten großteils (bei passender Dimensionierung).

## 3. Ölrückführung bei Inverter-Split / langen Leitungen [BELEGT, andere Hersteller]

- **Daikin Multi-Split RMXS (Bedienungsanleitung):** „Oil return operation will be performed once every 8 hours“, Heizen dann 5–10 min nicht möglich – https://daikinac.com/docs/default-source/rmxs-series-8-zone-multi-split/om-rmxs48lvju.pdf
- **Fujitsu General VRF (Technical Reference):** Heiz-Ölrückholung, wenn kumulierte Verdichterlaufzeit seit letzter Rückholung „exceeds 8 hours“, erste nach 1 h, Dauer ~4 min – https://assist.fujitsugeneral.com.au/support/solutions/articles/6000233054-vii-oil-recovery-preheat-defrost-control
- **Daikin Altherma 3 ERLA (Installationsanleitung):** Leitung max. 20 m, min. 3 m, „Keep field piping as short as possible.“ Zu Mindestlaufzeit/Ölrückführung **nichts** – https://www.daikin.nl/content/dam/document-library/installation-manuals/heat/air-to-water-heat-pump-low-temperature/erla-dv/ERLA-DV_Installation%20manual_4PEN596797-1B_English.pdf
- Fazit der Quellen [WAHRSCHEINLICH]: Neben einer kurzen Mindestlaufzeit je Start (Danfoss 2 min; Copeland anlagenspezifisch per Test) wird Ölrückführung über **kumulierte Laufzeit-Zähler** (Stunden) und **Mindestdrehzahl** gelöst. Kritischer Fall laut Copeland: lange Laufzeit bei sehr niedriger Drehzahl – nicht ein 20-min-Lauf.

## 4. Faustregeln aus Ratgebern / Foren [nur zweite Hand]
- 42watt (zitiert BWP, Fraunhofer, Copeland, Danfoss): BWP-Ziel „mindestens 10 bis 20 Minuten pro Start“ – Originalquelle BWP **nicht** selbst geprüft – https://42watt.de/magazin/taktung-warmepumpe
- Mitsubishi Ecodan „Compressor On Guard“ 20 min Mindestlaufzeit: nur Forenaussage nach Telefonat, „definitely isn't in the manual“ – https://renewableheatinghub.co.uk/forums/renewable-heating-air-source-heap-pumps-ashps/ecodan-minimum-run-time-flow-cop → **unbelegt**
- Panasonic Aquarea: öffentliche Angaben zu Mindestlaufzeit/Ölrückholung **[NICHT GEFUNDEN]**

## 5. Hoval [NICHT GEFUNDEN / bekannt]
- Öffentliche Hoval-Angaben zu max. Starts, Mindestlaufzeit je Start, Ölrückholzyklus: **[NICHT GEFUNDEN]**.
- Bekannt (frühere Funde): >12 m Leitung → Mindestdrehzahl 40 %; Mindeststehzeit 15 min an der eigenen Anlage gemessen (V99); Puffer-Mindestgröße „Mindestlaufzeiten berücksichtigt“ (Technikhandbuch S. 37, gp-joule – heute erneut client_error, Literwert C17 hier nicht neu geprüft).
- [WAHRSCHEINLICH] Die 40-%-Regel bei langen Leitungen ist genau die Ölrückführ-Maßnahme (Gasgeschwindigkeit), analog Copeland „below 1800 rpm“ → Hoval löst das über Drehzahl, nicht über Laufzeit. Nicht belegt.

---

## 6. Bewertung für die C17 [WAHRSCHEINLICH, eigene Rechnung]

Annahmen: C17-Minimum ~8 kW (gemessen), 15 min Mindeststehzeit, Lauf 15–25 min.
- **Lauflänge:** 15–25 min liegt klar über allen belegten kritischen Grenzen (2 min Danfoss, ~6–8 min UK-Labor, Takt-Grenze 6/10/12 pro h). Für Ölrückführung je Start nicht kritisch.
- **Starts:** Läufe 20 min + 15 min Pause ergeben max. ~1,7 Starts/h – unter 10–12/h (Copeland/Danfoss), aber über der Ratgeber-Komfortzone < 1/h.
- **Jahresstarts:** z. B. 20 Starts/Tag × 200 Heiztage = 4.000/Jahr → im Fraunhofer-Feld (90 % < 5.500). Bei 25 Jahren = 100.000 Starts – Hälfte der 200–300 Tsd. laut alpha innotec. → **Kein akuter Schaden, aber Verschleiß-Mehrbelastung**; eigene Startzahl aus HoxPi-Daten auszählen statt schätzen.
- **Effizienz:** Anlaufverlust je Start ist fix (Größenordnung wenige Minuten Einschwingen). Anteil sinkt ~1/Laufzeit: 20 → 40 min halbiert ihn, 40 → 60 min nur noch −1/3. Zahl für Inverter-Split **[NICHT GEFUNDEN]**.
- **40 vs. 60 min Mindestlaufzeit:** Starts/Tag ∝ 1/Lauflänge (bei gleicher Wärmemenge). 20 → 40 min = −50 % Starts (lohnt), 40 → 60 min = nochmal −33 % (abnehmender Nutzen). Preis: bei 8 kW Leistung und z. B. 3 kW Bedarf müssen pro 60-min-Lauf ~5 kWh zusätzlich gespeichert werden → höhere Vorlauf-/Puffer-/Raumüberhöhung → schlechterer COP und Ofen-/Raumregler-Konflikt. Puffer 283 l bei 5 K ≈ 1,6 kWh, Rest muss Estrich aufnehmen.
- **Empfehlung:** 40 min als Ziel ist sinnvoll; 60 min nur, wenn FBH-Kreise offen bleiben und Vorlauf-Überhöhung ≤ ~2–3 K bleibt. Nicht „um jeden Preis“ verlängern – Lebensdauergewinn 40→60 min ist klein.

## Was bringt uns das
- 15–25-min-Läufe sind **nicht schädlich** im Sinne von Öl-/Mechanikschaden; alle belegten Grenzen liegen bei 2–10 min bzw. 10–12 Starts/h.
- Das echte Thema ist die **Jahres-Startzahl** (Ziel < 4.000, gut < 2.000) – also Startzähler aus HoxPi auswerten (Starts/Tag vs. Außentemperatur).
- Verlängerung auf ~40 min bringt am meisten; 60 min nur mit Speicherreserve, Nutzen sinkt.
- Ölrückführung bei langen Leitungen löst die Hoval vermutlich über die 40-%-Mindestdrehzahl; Kältemittelleitungslänge weiter klären.
- Offen: Verdichterbauart/-hersteller C17, Hoval-Vorgabe max. Starts, Fraunhofer Kap. 6.3 (S. 98) im Volltext.