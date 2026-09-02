# HoxPi-ESP32 — Hoval-CAN -> Modbus-TCP-Gateway (ESP-IDF >= 5.3)
#   idf.py set-target esp32      (Olimex ESP32-EVB, RMII-Ethernet)   oder
#   idf.py set-target esp32s3    (Waveshare ESP32-S3-POE-ETH, W5500)
#   idf.py menuconfig  -> "HoxPi Gateway"  (Board, Pins, Poll, Schreiben)
#   python3 ../tools/gen_esp32_regmap.py registers.json -o main/regmap_gen.h   (lokal, nicht im Repo)
#   idf.py build flash monitor
cmake_minimum_required(VERSION 3.16)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(hoxpi_esp32)
