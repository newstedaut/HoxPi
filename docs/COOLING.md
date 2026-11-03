# Cooling with the official template — the missing base setting / Kühlen mit dem Original-Template

*Deutsch weiter unten.* Field notes from an UltraSource B comfort C17 with TopTronic® E (WEZ + FE module), floor heating, Loxone Miniserver. Discussion: [loxforum thread](https://www.loxforum.com/forum/hardware-zubeh%C3%B6r-sensorik/490650-hoval-template-k%C3%BChlung-l%C3%A4uft-nicht-%E2%80%94-die-fehlende-grundeinstellung-an-der-tte).

## English

**Symptom:** the official Hoval® "Heating & Cooling" template writes the cooling setpoint, but the heat pump never starts cooling.

**Cause:** Hoval's Modbus guideline marks 1490 *flow setpoint heating* and 19482 *flow setpoint cooling* with an asterisk: the Hoval service has to make on-site base settings before these datapoints take effect. Without them the template is correct, but the controller does not listen.

What it was on our unit:

| Parameter (panel) | Datapoint | Meaning | Note |
|---|---|---|---|
| 30-066 | 30066 | input assignment heating/cooling switchover | the direction comes from this input |
| 07-044 | 7044 | minimum flow temperature cooling | hard lower clamp of every cooling setpoint (ours was 19 °C → nothing to do) |
| 01-002 | — | resulting flow setpoint of the circuit | the only place where you see what survives all internal limits |

Two traps:

1. **07-044 clamps silently.** Write 16 °C, the circuit computes 19 °C. Hoval recommends 18 °C; lower only with vapour-tight insulated pipes and central + local dew-point monitoring.
2. **Control strategy 3 (constant) uses ONE setpoint channel.** The cooling channel 19482 stays inert; the setpoint has to come via 1490 and the switchover input decides the direction. Under strategy 4, 19482 works as expected (measured with a full test matrix).

**With HoxPi:** the parameter number without the dash is the CAN datapoint (07-044 = 7044, 30-066 = 30066), so the settings that are visible in the panel's service menu can be read over CAN — the official Modbus list is only a subset. HoxPi's *relay-free template mode* (channel exclusion + keepalive on inputs 30-046/057/066, see README) lets the unmodified template switch heating/cooling without a wire bridge. Changing service parameters is your own responsibility; note the old value first.

**Still open:** why 19482 stays inert under strategy 3 even with input 30-057 assigned. If you have the Hoval KDT/CST documentation for the heating-circuit/DHW controller module, please open an issue.

## Deutsch

**Symptom:** Das offizielle Hoval®-Template „Heating & Cooling“ schreibt den Kühl-Sollwert, die Wärmepumpe geht aber nie in den Kühlbetrieb.

**Ursache:** Hovals Modbus-Guideline markiert 1490 *Vorlauf Soll Heizen* und 19482 *Vorlauf Soll Kühlen* mit einem Sternchen: Der Hoval-Service muss vor Ort Grundeinstellungen vornehmen, bevor diese Datenpunkte wirken. Ohne diese Einstellungen ist das Template korrekt, die Anlage hört nur nicht zu.

Bei unserer Anlage war es:

| Parameter (Bedienteil) | Datenpunkt | Bedeutung | Hinweis |
|---|---|---|---|
| 30-066 | 30066 | Zuordnung Eingang Umschaltung Heizen/Kühlen | aus diesem Eingang kommt die Richtung |
| 07-044 | 7044 | Vorlaufminimaltemperatur Kühlen | begrenzt jeden Kühl-Sollwert hart nach unten (bei uns 19 °C, also nichts zu tun) |
| 01-002 | — | resultierender Vorlauf-Sollwert des Kreises | nur hier sieht man, was nach allen internen Begrenzungen übrig bleibt |

Zwei Stolpersteine:

1. **07-044 begrenzt still.** Man schreibt 16 °C, der Kreis rechnet 19 °C. Hoval empfiehlt 18 °C; weniger nur mit dampfdiffusionsdicht isolierten Leitungen und zentraler plus dezentraler Taupunktüberwachung.
2. **Regelstrategie 3 (Konstant) nutzt EINEN Sollwertkanal.** Der Kühlkanal 19482 bleibt wirkungslos; der Sollwert muss über 1490 kommen, die Richtung entscheidet der Umschalteingang. Bei Regelstrategie 4 funktioniert 19482 wie erwartet (mit einer vollständigen Testreihe gemessen).

**Mit HoxPi:** Die Parameternummer ohne Bindestrich ist der CAN-Datenpunkt (07-044 = 7044, 30-066 = 30066). Damit ist über CAN lesbar, was im Servicemenü des Bedienteils sichtbar ist; die offizielle Modbus-Liste ist nur eine Teilmenge. Der *relais-freie Template-Betrieb* von HoxPi (Kanal-Exklusion plus Keepalive auf den Eingängen 30-046/057/066, siehe README) lässt das unveränderte Template ohne Drahtbrücke zwischen Heizen und Kühlen umschalten. Serviceparameter änderst du auf eigene Verantwortung; alten Wert vorher notieren.

**Noch offen:** Warum 19482 bei Regelstrategie 3 auch mit zugeordnetem Eingang 30-057 wirkungslos bleibt. Wer die Hoval-KDT- oder CST-Anleitung zum Reglermodul Heizkreis/Warmwasser hat: bitte ein Issue eröffnen.
