#pragma once
#include "freertos/FreeRTOS.h"
typedef void *TaskHandle_t; typedef void (*TaskFunction_t)(void *);
BaseType_t xTaskCreate(TaskFunction_t f, const char *n, uint32_t stack, void *p, UBaseType_t prio, TaskHandle_t *h);
void vTaskDelay(TickType_t t);
void vTaskDelete(TaskHandle_t h);
