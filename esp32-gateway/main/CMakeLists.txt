# Registerkarte: die generierte regmap_gen.h (aus Hovals Datenpunktliste, nicht im Repo) hat Vorrang,
# sonst wird die kleine Beispieltabelle regmap_example.h eingebunden (Projekt bleibt kompilierbar).
if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/regmap_gen.h")
    set(HOXPI_REGMAP "regmap_gen.h")
    message(STATUS "HoxPi: Registerkarte regmap_gen.h (vollstaendig)")
else()
    set(HOXPI_REGMAP "regmap_example.h")
    message(WARNING "HoxPi: regmap_gen.h fehlt - nur Beispieltabelle (tools/gen_esp32_regmap.py ausfuehren)")
endif()

idf_component_register(
    SRCS "main.c" "hoval_proto.c" "hoval_can.c" "hoval_modbus.c" "hoval_cfg.c" "hoval_cfg_nvs.c" "hoval_json.c" "hoval_http.c" "hoval_ha.c" "hoval_mqtt.c" "regmap.c"
    INCLUDE_DIRS "."
    REQUIRES driver esp_eth esp_netif esp_event nvs_flash esp_timer esp_http_server mqtt esp-modbus)
target_compile_definitions(${COMPONENT_LIB} PRIVATE HP_REGMAP_HEADER="${HOXPI_REGMAP}")
