/* hoval_modbus.h — Modbus-TCP-Slave (esp-modbus) mit Hoval-Registerkarte, Port 502, FC3/FC6/FC16 */
#ifndef HOVAL_MODBUS_H
#define HOVAL_MODBUS_H
#include <stdint.h>
#include <stdbool.h>

/* Registerwort setzen (Aufruf aus dem CAN-RX-Task) — unbekannte Register werden ignoriert */
void hm_store(uint16_t reg, uint16_t word);
/* Aktuelles Wort lesen; false wenn reg in keinem Bereich liegt */
bool hm_read(uint16_t reg, uint16_t *word);
/* Slave starten (netif = Ethernet-Interface, darf NULL sein = alle). enable_write: Schreibpfad frei */
bool hm_start(void *netif, bool enable_write);

#endif
