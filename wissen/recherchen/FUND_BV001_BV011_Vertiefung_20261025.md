# FUND BV001/BV011 Bivalenz-Enum (Vertiefung) 25.10.2026

Katalog: F30. Recherche-Agent (Orchestrator 25.10.2026 07:54, MEHR Stufe 2), 14 Suchanfragen DE/EN/IT. Vorlauf: `[lokaler Pfad]`.
Stichprobe Claude: Xerolux `const.py` per WebFetch wörtlich nachgelesen – Enum stimmt (0 Off / 1 Bivalence 1 Active / 2 Bivalence 2 Active / 3 Bivalence 1+2 Active).

## Kurz
- BV001 (0..4) und BV011 (0..3) sind öffentlich **nicht auffindbar** (sicher für die 14 Suchen + 5 geöffnete Dokumente).
- Neu und **sicher**: BV0xx = 2. Wärmeerzeuger, BV1xx = 3. Wärmeerzeuger (iDM-Modbus-Liste Reg 1120–1123).

## Belegt
1. iDM-Modbus-TCP-Parameterliste (Stand 25.08.2017, Navigator mod20.3-0), https://www.loxforum.com/filedata/fetch?id=124252
   - Reg 1120 „2. Wärmeerzeuger - Bivalenzpunkt 1 BV002“ (−30..40 °C, Werk 0 °C), Reg 1121 „… Bivalenzpunkt 2 BV003“ (Werk −10 °C)
   - Reg 1122/1123 = „3. Wärmeerzeuger - Bivalenzpunkt 1/2 BV102/BV103“. BV001/BV011 nicht in der Liste.
2. Community-Bibliothek idm-heatpump-api (Xerolux): Reg 1124 `bivalence_state`, UCHAR, Enum 0..3 (s. o.).
   https://raw.githubusercontent.com/Xerolux/idm-heatpump-api/main/idm_heatpump/const.py , `registers.py` im selben Ordner. Statusregister, kein Einstellparameter, kein BV-Kürzel.
3. iDM: Strategien Alternativ / Parallel / Teilparallel, https://www.idm-energie.at/en/heat-pump-installation/bivalent-systems/
4. iDM-Referenzhandbuch 2020: „Bivalenzpunkt 1: +2°C => WP & Gas parallel“, „Bivalenzpunkt 2: -11°C => nur Gas“
   https://www.idm-energie.at/wp-content/uploads/2021/01/Referenzhandbuch_2020_DRUCKBOeGEN_net.pdf → BP1 = Beginn Parallel, BP2 = Übergang „nur 2. WE“.
5. Forum (nur Nutzer-Vermutung): Navigator 2.0 zeigt den E-Heizstab evtl. als 2. Wärmeerzeuger, https://www.energiesparhaus.at/forum/55318_1

## Wahrscheinlich
- BV001 ist eine Einstellung (Modus/Betriebsart) des 2. Wärmeerzeugers; bei uns ist der 2. WE am ehesten der WP-Heizstab ~6 kW.

## Vermutung
- BV001 0..4 = Strategie-Auswahl (z. B. 0 Aus, 1 Parallel, 2 Alternativ, 3 Parallel-Alternativ, 4 neuere Option nach V1.11). Ebenso möglich: Erzeugertyp/Freigabe. Nicht belegt.
- BV011 0..3 passt im Wertebereich zum Muster Aus / Stufe 1 / Stufe 2 / 1+2 (Reg 1124). Einzige Stütze ist der gleiche Bereich.

## Nicht gefunden
Suchen u. a.: „iDM Navigator Bivalenz Betriebsart Parameter Fachmann“, „"BV001" iDM“, „Betriebsart Zusatzwärmeerzeuger iDM“, „iDM 2. Wärmeerzeuger Betriebsart Parallel Alternativ“, „Navigator 2.0 Modbus 1124“, „Bivalenzbetrieb Heizstab Kessel“, „Navigator 10 Installationsanleitung Bivalenz“, IT „bivalenza secondo generatore“, HA/kodebach/ioBroker/openHAB/FHEM, Hoval UltraSource Bivalenz, AERO SLM Montageanleitung.
Geöffnet ohne Treffer: AERO SLM 3-11/6-17 Montageanleitung 812179 Rev.7 (siblik.com), Terra SW Max (manualslib), Navigator-2021-Prospekt, KNX-Forum Navigator 2.0, ioBroker-Thread 22497.

## Folgerung für uns
- F30 „fertig, wenn“ erfüllt: Bedeutung 3/4 belegt „öffentlich nicht auffindbar“. V103d (bei Frost WP-Lauf und Stab-Einsatz mit AT notieren) bleibt unverändert – keine Anpassung nötig.
- Code-Befund (OR 25.10. 07:10): Heizstab-Freigabe läuft bei uns sehr wahrscheinlich über den Gradminuten-Zweig, nicht über die AT-Schwelle – die Unklarheit um BV001 = 4 ist damit für den Winter zweitrangig.
- Live-Messweg statt Doku: Reg 1124 ist nicht in der HoxPi-Registerkarte (`read_register 1124` 25.10. 08:0x: „nicht bekannt“, sicher; iDM-eigene Adresse); Bivalenz-Status nur über X26-pCO-DB Seite 0x87 bzw. Stab-Strom beobachtbar.