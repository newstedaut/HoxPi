/* regmap_example.h — BEISPIEL-Tabelle (20 allgemein bekannte Register), damit das Projekt ohne
 * Hovals Datenpunktliste kompiliert. Die vollstaendige Tabelle erzeugt tools/gen_esp32_regmap.py
 * lokal als regmap_gen.h (nicht im Repo). Format identisch. */
#include "hoval_proto.h"

const hp_reg_t hp_regs[] = {
/*   reg, unit,  fg,  fn,    dp, type, dec, flags,        min,        max   name */
    { 1477,    1,   0,   0,     0, 3, 1, HP_F_NO_RANGE,          0,          0}, /* AF1 - outdoor sensor 1 [°C] */
    { 1478,    1,   1,   0,  3050, 6, 0, HP_F_WRITABLE|HP_F_NO_RANGE,          0,          0}, /* Heating operation choice */
    { 1481,    1,   1,   0,  3051, 3, 1, HP_F_WRITABLE,        100,        300}, /* Normal room temp. heating oper. [°C] */
    { 1490,    1,   1,   0,  7036, 3, 1, HP_F_WRITABLE,        100,       1100}, /* Flow setpoint constant req. heating [°C] */
    { 1496,    1,   2,   0,  5050, 6, 0, HP_F_WRITABLE|HP_F_NO_RANGE,          0,          0}, /* Hot water operation choice */
    { 1497,    1,   2,   0,  5051, 3, 1, HP_F_WRITABLE,        100,        700}, /* Normal hot water temp. [°C] */
    { 1499,    1,   2,   0,  1004, 3, 1, HP_F_NO_RANGE,          0,          0}, /* Hot water setpoint [°C] */
    { 1500,    1,   2,   0,     4, 3, 1, HP_F_NO_RANGE,          0,          0}, /* Hot water actual SF [°C] */
    { 1501,    1,   1,   0,  2051, 0, 0, HP_F_NO_RANGE,          0,          0}, /* Status heating circuit control */
    { 1534,    1,  60, 254,    27, 0, 0, HP_F_NO_RANGE,          0,          0}, /* Error code from controller */
    { 1561,    1,  10,   1,  9075, 6, 0, HP_F_WRITABLE|HP_F_NO_RANGE,          0,          0}, /* Heat generator operation choice */
    {19482,    1,   1,   0,  7047, 3, 1, HP_F_WRITABLE,          0,        300}, /* Flow setpoint constant req. cooling [°C] */
    {23622,  520,  50,   0, 40650, 6, 0, HP_F_WRITABLE|HP_F_NO_RANGE,          0,          0}, /* Op. choice ventilation */
    {23632,  520,  50,   0,     0, 3, 1, 0,       -300,        500}, /* Outside air temp. [°C] */
    {25613,    1,  10,   1, 23009, 4, 3, HP_F_NO_RANGE,          0,          0}, /* Eletrical energy WEZ MWh_high [MWh] */
    {25614,    1,  10,   1, 23009, 4, 3, HP_F_LOW_HALF|HP_F_NO_RANGE,          0,          0}, /* Eletrical energy WEZ MWh_low [MWh] */
    {27486,    1,  60, 254,    51, 4, 3, HP_F_NO_RANGE,          0,          0}, /* Heat quantity cooling_high [MWh] */
    {27487,    1,  60, 254,    51, 4, 3, HP_F_LOW_HALF|HP_F_NO_RANGE,          0,          0}, /* Heat quantity cooling_high [MWh] */
    {27490,    1,  60, 254,    45, 0, 1, HP_F_NO_RANGE,          0,          0}, /* Coefficient of Performance */
    {27509,    1,   2,   0,  5077, 3, 1, HP_F_WRITABLE,          0,        800}, /* Smart-Grid (Offset) WW-Sollvalue [K] */
};
const uint16_t hp_regs_count = 20;

/* Modbus-Bereiche (Holding Register) fuer den esp-modbus-Slave */
const hp_area_t hp_areas[] = {
    { 1477,    85},
    {19482,     1},
    {23622,    11},
    {25613,     3},
    {27486,    24},
};
const uint16_t hp_areas_count = 5;

/* Schreib-Whitelist (Register, die Modbus-Clients schreiben duerfen) */
const uint16_t hp_whitelist[] = { 1478, 1479, 1481, 1482, 1496, 1497, 1498, 27509, 27528, 27529, 27530, 27545, 27546, 28839, 1561, 1510, 1511, 1490, 1491, 19482, 23755, 27510, 27511, 27531, 27532 };
const uint16_t hp_whitelist_count = 25;
