Minimale Stub-Header, damit `make syntax` die ESP-IDF-Module (hoval_can.c, hoval_modbus.c, main.c)
auf dem Host mit `gcc -fsyntax-only` pruefen kann. Sie bilden NUR die hier benutzten Symbole der
ESP-IDF-5.x-/esp-modbus-1.x-API nach und ersetzen keinen echten Build mit idf.py.
