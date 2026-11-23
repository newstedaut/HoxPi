# FUND_Heiz_Hysterese_RL_20261101 (Katalog F65, Recherche-Subagent OR 01.11.2026 19:54, gegengelesen Claude)

**Frage (F65):** Wie heisst in oeffentlichen iDM-/Hoval-Unterlagen der Parameter, nach dem der Verdichter im Heizbetrieb abschaltet (RL > Soll + 3,0 K, MD-16) und wieder einschaltet (RL <= Soll - 1,5 K, dann 15 min 33-055)? Werkswert, Bereich, Ebene, Bezugsfuehler, Erfahrungen?

## Belegt (Forenaussagen von Hoval-UltraSource-Besitzern, kein Herstellerdokument)
- Hoval-Bezeichnungen im Menue "WFA 200 Konfiguration" (mehrfach gleich zitiert):
  - `33-053` "Ausschaltdiff. DK/WPF Heizen (CRF/WPF)"
  - `33-054` "Einschaltdiff. DK/WPF Heizen (CVF/WPF)"
  - Kuehlen: `33-061` "Ausschaltdiff. DK Kuehlen (CVF)", `33-062` "Einschaltdiff. DK Kuehlen (CRF)"
  - Quellen: https://www.energiesparhaus.at/forum/56645 (#3 ffischer, 16.02.2020); https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2 (#37 Domi90, 29.11.2023)
- Bezug Ruecklauf beim Abschalten: ffischer #3 (Abschalten bei 27 C RL, Ein bei 23,5 C RL; mit 33-053 = 1,0 / 33-054 = 2,5 genau Soll +1,0 / -2,5). #6 "Solltemperatur im Ruecklauf +1", #11 "Ruecklaufgesteuert". (https://www.energiesparhaus.at/forum/56645)
- Feldwerte (kein Werkswert genannt): ffischer 1,0/2,5; MSC1 1,0/2,0, spaeter 0,2/2,5; Domi90 2,0/3,0; Optihome 2,0 -> 3,0/3,0 (#44, 56645_3).
- Erfahrungen: kleinere Hysterese = mehr Starts, AZ "nicht merklich besser" (ffischer #11); hohe obere Schwelle bei Modulation bringt zu viel Leistung (MSC1); Vorschlag Einschaltdiff. 4 K ohne gepostetes Ergebnis (Akani #40 / Domi90 #41); "15min Zwangspause" nach WW -> Heizen erwaehnt, ohne Loesung (Marty #57, 56645_3).
- Verwandt, nicht dasselbe: `29-066`/`29-069` "Differenzst. 1 Einschaltdiff./Ausschaltdiff." (8,0/4,0 K), haelt laut Installateur die Spreizung 4 K; Aenderung verschlechterte AZ (#6, /forum/56645).
- iDM: aeltere Navigator-Generation "Hyster. Heizungspuffer: 4" (https://www.energiesparhaus.at/forum-hysterese-einstellung/24918); iDM Terra SWM Werkswert "mWn 3", Empfehlung 5 (https://www.energiesparhaus.at/forum/75316_2).
- iDM AERO SLM 3-11/6-17 Montageanleitung S. 24: nur allgemein "Schalthysterese", kein Wert (https://www.manualslib.de/manual/1242658/Idm-Aero-Slm-3-11.html, Teilvorschau).

## Wahrscheinlich
- Stopp RL > Soll + 3,0 K = **33-053 = 3,0 K**, Wiedereinschalten RL <= Soll - 1,5 K = **33-054 = 1,5 K** (Muster wie bei ffischer). Ob "HV011" dazu passt: Vermutung.
- Fuehlerkuerzel CRF/CVF bei 33-054 widerspricht den RL-Messungen der Foren -> Beschriftung wahrscheinlich ungenau.
- Ebene: Fachmann/Service.

## Nicht gefunden
- Werkswert/Bereich 33-053/054 in einem Hoval- oder iDM-Dokument; 33-055 oeffentlich; iDM-Modbus-Register; Vorher/Nachher auf haustechnikdialog/photovoltaikforum.

## Claude-Gegenprobe 01.11.2026 ~20:10
- HoxPi `search_registers` "Ausschaltdiff", "Schaltdifferenz", "33-053": keine Treffer -> nicht ueber die HoxPi-Registerliste lesbar [sicher]. Lesbar wahrscheinlich wie 33-055 passiv aus der X26-pCO-DB (Weg wie OR 23.10. 20:10) oder am Bedienteil Fachmann-Ebene.
- Zahlen 3,0/1,5 K decken sich mit MD-16 (70 Laeufe, Median nach Stopp +3,0 K) und F5 (Ein bei Soll - 1,5 K) [sicher als Messung; Zuordnung zum Parameter wahrscheinlich].

## Was bringt uns das
Die Stopp-Regel ist sehr wahrscheinlich Hovals "Ausschaltdiff. DK/WPF Heizen" 33-053 am Ruecklauf. Laengere Laeufe gingen ueber 33-053 hoeher, laengere Pausen ueber 33-054; nur lesend pruefen, Aenderung nur mit des Betreibers Freigabe und Rueckweg. Foren: weniger Starts, kaum AZ-Gewinn.

## Gelesene URLs
- https://www.energiesparhaus.at/forum/56645
- https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2
- https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_3
- https://www.energiesparhaus.at/forum-hoval-ultrasource-b-comfort-11-optimierung-kuehlt-nicht/85791_1
- https://www.energiesparhaus.at/forum-ueberdimensionierte-luft-wasser-wp-zuegeln/80465_2
- https://www.energiesparhaus.at/forum-hysterese-einstellung/24918
- https://www.energiesparhaus.at/forum-idm-waermepumpe-abschaltlogik/75497
- https://www.energiesparhaus.at/forum/75316_2
- https://www.manualslib.de/manual/1242658/Idm-Aero-Slm-3-11.html