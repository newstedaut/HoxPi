/* hoval_can.h — TWAI (ESP32-CAN) @ 50 kbit/s: Empfang + Reassembly + Poll-Scheduler + SET senden */
#ifndef HOVAL_CAN_H
#define HOVAL_CAN_H
#include <stdint.h>
#include <stdbool.h>
#include "hoval_proto.h"

/* Register-Speicher (wird von hoval_modbus.c bereitgestellt): Wort schreiben / lesen */
typedef void (*hc_store_cb_t)(uint16_t reg, uint16_t word);

typedef struct {
    uint32_t rx_frames, rx_msgs, decoded, tx_frames, tx_errors, bus_off;
    uint32_t last_rx_ms;          /* letzter dekodierter Datenpunkt (fuer Stale-Erkennung) */
} hc_stats_t;

/* Treiber installieren + Tasks starten. store: Ziel fuer dekodierte Woerter. */
bool hc_start(hc_store_cb_t store);
/* Wurde reg schon einmal vom CAN gelesen? (Kalt-Cache-Schutz beim Schreiben) */
bool hc_seen(uint16_t reg);
/* SET-Frame senden (Wert = Rohwert wie im Modbus-Wort). true wenn in die TX-Queue gelegt. */
bool hc_send_set(const hp_reg_t *r, int32_t value);
const hc_stats_t *hc_stats(void);

#endif
