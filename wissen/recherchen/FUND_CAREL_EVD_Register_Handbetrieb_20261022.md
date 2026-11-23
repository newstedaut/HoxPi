# FUND: CAREL EVD (X4-Slave 99) – Registerbedeutung laut öffentlichem Handbuch (Web-Recherche, 22.10.2026)
Quelle: CAREL EVD ice Handbuch +0300038EN rel. 1.2, Tab. 8.b S. 22–23
https://www.carel.com/documents/10191/0/+0300038EN/<UUID>?version=1.2

## Belegt (Handbuch)
- Reg 134 = Man_posit_steps (manuelle Ventilposition in Schritten, 0–999, R/W)
- Reg 131 = EEV_Positions_steps (Ist-Position) – passt zu unserer Messung 0…480
- Coil 10 = Manual_posit_enable (Handpositionierung ein); laut Handbuch hat Handbetrieb Vorrang vor Regelung und Schutzfunktionen des Treibers, wird nach Stromausfall nicht gespeichert
- Reg 6 = S2_Value (Sauggasfühler NTC)
- Adressierung: unsere Busadressen entsprechen der Modbus-Spalte direkt (131 = Ist-Schritte bestätigt das)

## Wahrscheinlich
- Coil 10 dauerhaft FF00 → der Master (Kälteregler) positioniert das Ventil selbst in Schritten und setzt den Handbetrieb nach jedem Neustart neu; die treibereigene Überhitzungsregelung läuft nicht.
- 335 = Schritte (≈ 70 % von 480), keine Promille; Startposition kommt vom Master.
- Reg 6 konstant 141–147 → S2 vermutlich nicht angeschlossen/genutzt.

## Korrekturbedarf an unserer Doku (nur Hinweis, noch nicht geändert)
- „Reg 134 = EEV-Soll" → genauer: manuelle Sollposition, vom Master geschrieben
- „Reg 6 = Lufttemperatur Außeneinheit" → laut Handbuch Sauggasfühler S2; zweifelhaft

## Nicht gefunden
- Skalierung der Analogwerte, Statuscodes, R410A-spezifische Sollwerte; ob EVD ice oder evolution verbaut ist (Registerlage passt zu ice).

## Weitere Quellen
- EVD evolution +0300005EN rel. 3.3: https://users-phys.au.dk/~srf/SONG/0300005EN.pdf
- https://iot.carel.com/product/evd-ice