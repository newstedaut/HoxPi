# Host-Test fuer die Protokollbibliothek (kein ESP-IDF noetig):
#   make test            baut test_proto mit regmap_example.h, fuehrt es aus und vergleicht
#                        die Frame-/Dekodier-Ausgabe mit der Python-Referenz (bridge/hoval_bridge.py);
#                        dazu test_cfg (Laufzeit-Konfiguration: Whitelist-Text, Grenzen, Override)
#   make REGMAP=../main/regmap_gen.h test    dasselbe mit der echten, generierten Tabelle
#   make syntax          Syntaxpruefung der ESP-IDF-Module gegen Stub-Header (idf_stubs/)
CC      ?= gcc
CFLAGS  ?= -std=c11 -Wall -Wextra -Werror -O1 -g -I../main
REGMAP  ?= ../main/regmap_example.h
PYTHON  ?= python3

all: test

test_proto: test_proto.c ../main/hoval_proto.c ../main/hoval_proto.h $(REGMAP)
	$(CC) $(CFLAGS) -DHP_REGMAP_HEADER='"$(REGMAP)"' -o $@ test_proto.c ../main/hoval_proto.c regmap_tu.c

test_cfg: test_cfg.c ../main/hoval_cfg.c ../main/hoval_cfg.h ../main/hoval_proto.c $(REGMAP)
	$(CC) $(CFLAGS) -DHP_REGMAP_HEADER='"$(REGMAP)"' -o $@ test_cfg.c ../main/hoval_cfg.c ../main/hoval_proto.c regmap_tu.c

test: test_proto test_cfg
	./test_cfg
	./test_proto > out_c.txt
	$(PYTHON) ref_proto.py > out_py.txt
	@sed -n '1,/^CHK U16/p' out_c.txt > out_c_cmp.txt
	@diff -u out_py.txt out_c_cmp.txt && echo "REFERENZ-VERGLEICH OK ($$(wc -l < out_py.txt) Zeilen identisch mit hoval_bridge.py)"
	@grep -E "^(REASM|TABLE)" out_c.txt

syntax:
	$(CC) -std=gnu11 -Wall -Wextra -fsyntax-only -I../main -Iidf_stubs ../main/hoval_can.c ../main/hoval_modbus.c ../main/hoval_cfg_nvs.c ../main/main.c
	@echo "SYNTAX OK (gegen idf_stubs)"

clean:
	rm -f test_proto test_cfg out_*.txt
