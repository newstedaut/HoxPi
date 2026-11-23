# FUND: W:61 / WEZ-Status 98 – Startphase nach Kühlbetrieb (Web-Recherche, 22.10.2026)
Recherche-Agent im Auftrag des Orchestrators. Nur öffentliche Quellen, nichts heruntergeladen.

## Belegt
- Status 98 = „Kaltstart" (97 = „Ölvorwärmung", 16 = „Wiederanlauf", 18 = „Vorlaufzeit", 8 = „Abtauen") steht in ein anderer HoxPi-Nutzer/esp_canbus `hoval_data_processing/generate_presets.py` (Commit 645c674, 09.10.2026) — **aber dort ausdrücklich „ported from the independent HoxPi project"** → kein unabhängiger Beleg, Zirkelschluss.
- Kurbelwannenheizung: verhindert Kältemittelverlagerung in den Verdichter im Stillstand (Ölverdünnung, Schäumen, Flüssigkeitsschlag beim Start). https://hvacrschool.com/field-guide-to-crankcase-heaters/
- Hoval UltraSource: Forenfall mit ND-Fehler beim Anlauf bzw. Wechsel WW→Heizen, behoben durch EEV-Geschwindigkeit (nicht W:61, zeigt aber heikle Startphase). https://www.energiesparhaus.at/forum/57498

## Wahrscheinlich (Fachwissen, für Hoval nicht belegt)
- 98 ohne Verdichter nach Kühlbetrieb = temperaturabhängige Startfreigabe gegen Kältemittelverlagerung (Ölsumpf gegen Verdampfungstemperatur o. ä.); 5–15 min und nur 4/65 Wechsel sprechen gegen eine feste Zeit.
- 4-Wege-Umschaltung/Druckausgleich erklärt eher kurze feste Wartezeiten (1–3 min).
- Mindeststillstand hat eigenen Code (16) → 98 ist etwas anderes.
- W:61 erst ab Kälteregler V1.18 → neu eingeführte/neu angezeigte Startschutz-Logik (Vermutung).

## Nicht gefunden
- Öffentliche Hoval-Warncodeliste (W:xx), iDM-Navigator-Fehlerliste, „W:61" wörtlich in Foren, Release-Notes Hoval/HAICO 2024/2025 (V1.18).

## Nächster Schritt (nur lesen)
1. `Hoval_Modbus_Guideline_offiziell.xlsx` (Vault): Optionsliste des WEZ-Status prüfen — stehen 97/98 dort als Ölvorwärmung/Kaltstart?
2. Volllogger: Außentemperatur, Verdampfer/ND an den 4 Ereignissen vs. den 61 Wechseln ohne Ereignis → Temperaturbedingung eingrenzen.

## Quellen
- https://github.com/ein anderer HoxPi-Nutzer/esp_canbus
- https://hvacrschool.com/field-guide-to-crankcase-heaters/
- https://www.energiesparhaus.at/forum/57498 · /forum/74102 · /forum-hoval-ultrasource-b-comfort-11-optimierung-kuehlt-nicht/85791 · /forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2
- https://cdn.swiss-arc.ch/m10/95/41114595/etc/80/41843080.pdf
- https://danfoss.com/de-de/service-and-support/case-studies/dcs/components-for-heat-pumps-part-5-four-way-reversing-valves