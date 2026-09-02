#pragma once
#include <stdint.h>
#include "esp_err.h"
typedef enum { SPI1_HOST, SPI2_HOST, SPI3_HOST } spi_host_device_t;
#define SPI_DMA_CH_AUTO 3
typedef struct { int mosi_io_num, miso_io_num, sclk_io_num, quadwp_io_num, quadhd_io_num; } spi_bus_config_t;
typedef struct { uint8_t command_bits, address_bits, mode; int clock_speed_hz, spics_io_num, queue_size; } spi_device_interface_config_t;
esp_err_t spi_bus_initialize(spi_host_device_t h, const spi_bus_config_t *c, int dma);
