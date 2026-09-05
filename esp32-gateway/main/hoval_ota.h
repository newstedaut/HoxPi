/* hoval_ota.h — Firmware-Update ueber HTTP(S) (esp_https_ota) mit Rollback-Schutz
 *
 *   POST /ota  {"url":"https://host/hoxpi_esp32.bin"}  (X-Token)  -> hota_start(): Task laedt das Image in die
 *              inaktive OTA-Partition, prueft es (esp_https_ota), setzt sie als Boot-Partition und startet neu.
 *   GET  /ota  Zustand: laufende Partition, App-Version, pending_verify, letzter Lauf (Fortschritt/Fehler).
 *
 * Rollback (CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE): nach dem Neustart in ein neues Image bleibt es "pending
 * verify", bis hota_watch() den ersten dekodierten CAN-Datenpunkt sieht -> esp_ota_mark_app_valid_cancel_rollback().
 * Kommt innerhalb HOXPI_OTA_VALID_AFTER_S kein Datenpunkt (CAN tot, Absturz vor Eintrag), wird das Image als
 * ungueltig markiert und der Bootloader startet die vorige Firmware. Ein Gateway, das den Hoval-Bus nicht liest,
 * ist wertlos - deshalb ist "CAN dekodiert" das Gueltigkeitskriterium, nicht "bootet".
 *
 * Nur die Bibliothek ist host-getestet (URL-Pruefung/JSON in hoval_json.c); die IDF-Aufrufe hier sind
 * gegen Stub-Header syntaxgeprueft (05.09.2026, kein Board).
 */
#ifndef HOVAL_OTA_H
#define HOVAL_OTA_H
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

#define HOTA_URL_MAX 200

typedef enum { HOTA_IDLE = 0, HOTA_RUNNING, HOTA_OK, HOTA_FAILED } hota_state_t;

typedef struct {
    bool         enabled;              /* CONFIG_HOXPI_OTA_ENABLE */
    const char  *running;              /* Label der laufenden Partition ("ota_0", "factory") */
    const char  *boot;                 /* Label der naechsten Boot-Partition */
    const char  *app_version;          /* esp_app_desc_t.version (PROJECT_VER / git describe) */
    const char  *app_date;             /* Kompilierdatum */
    bool         pending_verify;       /* neues Image, noch nicht bestaetigt (Rollback moeglich) */
    hota_state_t state;                /* letzter/laufender Update-Versuch */
    char         url[HOTA_URL_MAX];    /* URL des letzten Versuchs (leer = keiner seit Start) */
    uint32_t     bytes;                /* geladene Bytes */
    int32_t      total;                /* Gesamtlaenge laut Content-Length, -1 = unbekannt */
    const char  *error;                /* Fehlertext (state FAILED), sonst "" */
    uint32_t     started_s, finished_s;/* Laufzeit-Sekunden (uptime) */
} hota_info_t;

bool hota_enabled(void);
/* Update starten: prueft URL-Schema (https, http nur mit HOXPI_OTA_ALLOW_HTTP), legt den Task an.
 * false + err bei laufendem Update, ungueltiger URL oder Task-Fehler. */
bool hota_start(const char *url, char *err, size_t errcap);
/* Zustand fuer /ota und /status */
void hota_info(hota_info_t *out);
/* Nach dem Start aufrufen: Task, der das Image bestaetigt (erster dekodierter Datenpunkt) oder zurueckrollt. */
void hota_watch(void);
/* Rollback-Situation beim Start ins Log schreiben (welche Partition, pending?) */
void hota_log_boot(void);

#endif
