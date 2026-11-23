# MODELLTEST 22.11.2026 – welches Modell bringt uns am meisten? (der Betreiber: „alle modelle … testen … dann entsprechend alles umstellen“)

## Phase A – Antigravity (läuft seit 22.11. 11:41)
- 9 Modelle, per Rauchprobe bestätigt (`planModel` = gewünschtes Modell): Neon M/H, Hydrogen M/H, Argon M, Flash 3.8 M, Claude Opus 5.5 M, Claude Sonnet 5.5 M, GPT-OSS 120B M.
  Nicht über agentapi ansteuerbar: „Orchestrator (Neon/Argon)“ und „Gemini 4 Carbon“ (fallen auf Standardmodell M530 zurück) → nicht im Test.
- 3 Aufgaben mit von Claude nachgerechneter Wahrheit (`[lokaler Pfad]`, außerhalb von HoxPi-Doku):
  T1 WW-Ladungen 20.11. aus ww_hires (Rohwerte ×10, Lückenregel) · T2 Abtauungen 20.11. aus verdichter_catch · T3 Urteile aus einer Nachrechnungsdatei ablesen.
- Läufer `[lokaler Pfad]`: drei Spuren parallel (Gemini-Topf, Argon-Topf, Claude/GPT-Topf), in der Spur nacheinander,
  Kontingent vor/nach jedem Lauf, max. 40 min je Lauf, Claude/GPT-Spur stoppt bei < 3 %. Protokoll `runner.log`, Läufe `laeufe.csv`, Antworten `HoxPi-Doku\Modelltest\`.
- Auswertung `py -3 -X utf8 [lokaler Pfad]` → `HoxPi-Doku\MODELLTEST_ERGEBNIS_20261122.md` (Punkte /300, Zeit, Kosten, Punkte je %-Punkt).

## Umstellen nach Phase A (Orchestrator, sobald `runner.log` „Modelltest komplett“ zeigt)
1. Auswertung laufen lassen, 2 Antworten stichprobenhaft selbst gegen die Wahrheit lesen.
2. Rollen neu vergeben (Regel: Qualität zuerst – nur Modelle mit ≥ 240/300; darunter nach Punkten je %-Punkt; Töpfe nicht doppelt belasten):
   - **Labor (Dauerarbeit MD-Pakete):** bestes Modell aus dem größten Topf (Gemini oder Argon).
   - **Failsafe:** bestes Modell aus einem *anderen* Topf als das Labor.
   - **Gegenprüfungen/Nachrechnungen:** bestes Modell eines anderen Herstellers/Topfs als der Ersteller (Claude/GPT-Topf, solange > 15 %).
   - **Ersatzweg 2b:** Reihenfolge der übrigen Modelle nach Punkten.
3. Umsetzen: Labor = neue Konversation mit dem Siegermodell registrieren (`cc_argon_senden.py --registrieren`), Failsafe-Modell in der Automation (Bildschirmweg),
   `ARGON_FAILSAFE.md`, SKILL.md 2/2b/3c nachführen; Rückweg je Punkt notieren. Ergebnis + Umstellung als `## 🎛 ORCHESTRATOR` ins Journal.
4. Wiederholung: monatlich oder wenn Antigravity neue Modelle zeigt (`ag_modelle.py`).

## Phase A – Stand 11:47
Claude/GPT-Topf nach Opus (T1–T3) und Sonnet (T3) auf 0 % (Reset 25.11. 12:56) → Spur 3p beendet. **Nach dem Reset die Spur nachholen:**
`py -3 -X utf8 [lokaler Pfad] 3p` (überspringt Fertiges; Sonnet T1/T2, GPT-OSS T1–T3). Bis dahin ist der Ersatzweg 2b ohne Claude/GPT.

## Phase B – Jarvis (der Betreiber 22.11.: „ja gern teste jarvis durch … auch gratis online modelle … auf ein online modell switchen sobald jemand am pc ist“)
- Test `[lokaler Pfad]`: echte Jarvis-Aufgabe über `hermes chat --oneshot` (8 Register lesen, feste Tabelle), 2× je Kandidat,
  Wahrheit über den HoxPi-MCP (8808) direkt vor/nach dem Lauf. Punkte /100: 8×10 richtige Werte, 10 Tabellenkopf, 10 keine Zusatzzeilen. Ergebnisse `jarvis_laeufe.csv`, Antworten `jarvis_antworten.txt`.
- Tagteil (läuft seit 11:51, `mt_jarvis_tag.ps1`): Qwen lokal + 7 Gratis-Modelle über OpenRouter (`:free`): Nemotron 3 Ultra 550B, Nemotron 3.5 Super VL, Gemma 4 31B, Gemma 4 26B, Ling 3.2 Flash, ERNIE 5.5 Flash, openrouter/free.
- Nachtteil (geplante Aufgabe `HoxPi_Jarvis_Modelltest_Nacht`, einmalig ab 23.11. 00:30, nur bei ≥ 10 min ohne Eingabe, Fenster bis 05:30): Gemma 4 26B lokal und GPT-OSS 20B lokal, danach **immer** Qwen zurück (`modell_vor_modelltest.json`). Protokoll `jarvis_nacht.log`.
- **⚠ Kosten (sicher, 22.11.):** Jarvis’ Cloud-Rückfall in `[lokaler Pfad]` (`fallback_providers`) zeigt auf **kostenpflichtige** OpenRouter-Modelle
  (Claude Sonnet 5.5, Kimi K3.1 Pro). Der OpenRouter-Schlüssel meldet „$80.38 used“ und ist gesperrt (Limit 0 $) – seit 21.11. 16:37 scheitert jeder Rückfall mit HTTP 403.
- **Umbau nach dem Test (der Betreiber hat „alles versuchen“ freigegeben; je Schritt Backup + Rückweg):**
  1. `fallback_providers` auf die 2 besten Gratis-Modelle (`:free`) umstellen – nie wieder ein bezahltes Modell. Schlüssel-Limit 0 $ lassen (Schutz).
  2. Hybridbetrieb im Wachhund (v4): der Betreiber am PC (Eingabe < 10 min) → lokales Modell entladen, Jarvis-Läufe (`jarvis_takt.py`) mit dem besten Gratis-Online-Modell;
  3. OpenRouter-Gratisgrenzen beachten (Minuten-/Tageslimit je Konto): Läufe je Stunde zählen, bei 429 auf das zweitbeste Gratis-Modell, sonst warten.
- Lokale Modelle in `[lokaler Pfad]`: Qwen3.6-35B-A3B (aktiv), gemma-4-26B-A4B, gpt-oss-20b.
- Test: derselbe feste Jarvis-Einzelauftrag (Register + Loxone-Zustände, Tabelle mit festem Kopf) je Modell, Wahrheit = Claude liest dieselben Werte in derselben Minute;
  gemessen: richtig/falsch je Wert, Format, Deutungen (verboten), Dauer, Token/s.
  → nur in einem Fenster, das der Betreiber freigibt (oder wenn der PC ≥ 10 min ohne Eingabe ist und der Betreiber „nachts erlaubt“ gesagt hat).

## Nebenbefund 22.11. 11:39 – Wachhund v3
Jarvis stand seit 21.11. 16:36 still: „Spielmodus“ wurde von `dwm` (Windows-Fensterverwaltung, 2,2 GB Grafikspeicher bei der breiten Bildschirmfläche) ausgelöst und nie
wieder freigegeben (Schwelle 1,8 GB). v3: Windows-/Büroprozesse zählen nicht; Spielmodus nur, wenn der Betreiber am PC ist (Eingabe < 10 min); nach 10 min ohne Eingabe lädt
Jarvis wieder. Datei `[lokaler Pfad]`, Rückweg `jarvis_wachhund_v2_bak_20261122.ps1` + Aufgabe `Jarvis_Wachhund` neu starten.

## Stand 22.11. 13:20 (Orchestrator) - Entscheidung Umstellen
- Phase A Gemini/Argon komplett, Auswertung `HoxPi-Doku\MODELLTEST_ERGEBNIS_20261122.md`: alle 6 Gemini/Argon-Modelle 300/300 (Test trennt nicht), Opus 100 und Sonnet 0 nur wegen leerem Claude/GPT-Topf (Laeufe ohne Antwortdatei, kein Qualitaetsurteil).
- Stichprobe selbst: hydrogen-m T2 = Wahrheit (<MAC>, <MAC>) [sicher]; opus-m T1/T2 ohne Antwortdatei (laeufe.csv False) [sicher].
- **Entscheidung: vorerst keine Umstellung.** Gruende: Gleichstand 300/300 liefert keine Rangfolge; Failsafe auf Neon M ist des Betreibers Wahl von heute 11:12; 3p-Spur fehlt bis Reset 25.11. 12:56. Labor bleibt Argon (Topf 32 %, Reset 29.11.), solange Argon-Woche > 15 %; faellt sie darunter, Labor auf hydrogen-m (schnellster Gemini, 3,9 min).
- Naechster Schritt: nach 25.11. 12:56 `mt_runner.py 3p`, danach schwerere Aufgaben (T4/T5 mit Abgrenzungsfragen wie in den Stau-Abweichungen), dann Rollen nach Plan vergeben. Bis dahin meldet der Orchestrator „Modelltest komplett“ nicht erneut als offen.