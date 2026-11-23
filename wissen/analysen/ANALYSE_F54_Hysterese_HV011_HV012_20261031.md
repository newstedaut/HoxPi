# F54 Teilschritt: Ist die Stopp-Hysterese "+6 K" fest oder ein Parameter? (OR 31.10.2026 13:00, nur lesend)

**Frage (aus Loop-Stundenbericht 31.10. 10:20, Naechster Schritt):** Heizlauf endet bei WP-Vorlauf 1525 ~ 1520 + 6 K, Start bei 1525 ~ 1490 + 0,5 K. Haengt das an Hoval-Parametern?

## Ergebnis
1. **Die Schwellen sind Kaelteregler-Parameter, keine Hoval-TopTronic-Parameter** (wahrscheinlich, nahe sicher):
   - 33-053 / HV011 (pCO-DB 0x811D) **Ausschaltdifferenz Heizen = 3,0 K** (sicher, X26 passiv 23.10., 199/199 Lesungen, `ANALYSE_Einschaltverzoegerung_Parameter_20261023.md`).
   - 33-054 / HV012 (0x811E) **Einschaltdifferenz Heizen = 1,0 K** (sicher; seit 09.09.2026 18:25, vorher 3,0 K, `CAN_Opcode_0x72_Servicekanal_Analyse.md`).
   - 33-055 / HKA59 = 15 min Freigabeverzoegerung (sicher, F5).
   - Soll des Kaeltereglers = X26 M0 = 1520 = 1490 + 3 K (07-001) (sicher, F34).
   - Offizielle Hoval-Datenpunktliste `WEZ_Register_offiziell_UnitId1.csv`: kein Schaltdifferenz-Register fuer den Waermeerzeuger (nur SG-Hysteresen) - sicher.
2. **Der Kaelteregler schaltet am Ruecklauf, nicht am Vorlauf** (wahrscheinlich): Volllogger 29.-31.10. (Skript `HoxPi-Doku\cc_hv011_20261031_1300.py`, am Pi nur /tmp, 5-min-Raster, letzter Wert vor dem Wechsel, 1501 = 23):
   - **STOPP (21 Faelle):** RL 1535 - 1520 = **+2,0 ... +3,0 K** (19/21; je einmal +1,0 am 30.10. 09:35 - derselbe Ausreisser wie im Loop, +4,5 K VL - und +1,5 am 31.10. 11:25), **nie > +3,0** -> passt zu AUS bei RL >= 1520 + HV011 (3,0 K). VL 1525 liegt dabei +5,5...+6,5 K ueber 1520 = RL-Schwelle + Spreizung ~3,5 K. Die "+6 K" sind also 3 K HV011 + Spreizung, kein eigener Parameter.
   - **START (23 Faelle):** RL - 1520 = **-1,5 ... -2,5 K** im Regelfall (16/23), nie > -1,5 -> passt zu EIN erst nach RL <= 1520 - HV012 (1,0 K) **plus** 15 min HKA59, in denen der RL weiter faellt. Tiefere Werte (-3 ... -7 K) = Starts nach Loxone-Pause (1490 vorher 0) bzw. nach Nacht.
   - Spalte 18742 (RL Waermeerzeuger) = 1535 auf +-0,5 K (sicher).
   - Stichprobe von Hand: 31.10. 10:25 STOPP 1520 = 32,5, RL 1535 +2,5 (= 35,0), VL +6,5 (= 39,0) - deckt sich mit Loop-Live-Wert 39,0 bei Soll 32,5.

## Was bringt uns das
- Zwilling (`wez_zwilling.py`): Taktregel = AUS bei RL >= 1520 + 3,0; EIN, wenn RL 15 min lang <= 1520 - 1,0 (und Loxone-Anforderung 1490 > 0). Statt fester "+6 K VL".
- Hebel (nur zur Entscheidung durch der Betreiber, nichts geaendert): HV011 groesser = laengere Laeufe/weniger Starts, aber hoeherer Vorlauf (COP); HV012 wurde am 09.09. schon von 3,0 auf 1,0 K gesenkt. Rueckweg und Schreibweg betreffen den Kaelteregler - **Orchestrator schreibt dort nie**.
- Offener Rest F54: Nacht-Zeitreihe demandHeat (Loop).