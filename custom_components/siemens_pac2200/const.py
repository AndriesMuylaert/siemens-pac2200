"""Constants for Siemens PAC2200 integration."""

DOMAIN = "siemens_pac2200"
DEFAULT_PORT = 502
DEFAULT_SLAVE = 1
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_DELAY = 2

CONF_SLAVE = "slave"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_DELAY = "delay"

# (name, unique_id_suffix, address, unit, device_class, state_class)
SENSOR_DEFINITIONS = [
    # Per-phase voltages L-N
    ("Grid Voltage VL1-N",        "VL1N",   1,  "V",   "voltage",        "measurement"),
    ("Grid Voltage VL2-N",        "VL2N",   3,  "V",   "voltage",        "measurement"),
    ("Grid Voltage VL3-N",        "VL3N",   5,  "V",   "voltage",        "measurement"),
    # Per-phase voltages L-L
    ("Grid Voltage VL1-L2",       "VL1L2",  7,  "V",   "voltage",        "measurement"),
    ("Grid Voltage VL2-L3",       "VL2L3",  9,  "V",   "voltage",        "measurement"),
    ("Grid Voltage VL3-L1",       "VL3L1",  11, "V",   "voltage",        "measurement"),
    # Currents
    ("Grid Current L1",           "IL1",    13, "A",   "current",        "measurement"),
    ("Grid Current L2",           "IL2",    15, "A",   "current",        "measurement"),
    ("Grid Current L3",           "IL3",    17, "A",   "current",        "measurement"),
    # Apparent power
    ("Grid Apparent Power L1",    "SAL1",   19, "VA",  "apparent_power", "measurement"),
    ("Grid Apparent Power L2",    "SAL2",   21, "VA",  "apparent_power", "measurement"),
    ("Grid Apparent Power L3",    "SAL3",   23, "VA",  "apparent_power", "measurement"),
    # Active power
    ("Grid Active Power L1",      "PAL1",   25, "W",   "power",          "measurement"),
    ("Grid Active Power L2",      "PAL2",   27, "W",   "power",          "measurement"),
    ("Grid Active Power L3",      "PAL3",   29, "W",   "power",          "measurement"),
    # Reactive power
    ("Grid Reactive Power L1",    "QAL1",   31, "var", "reactive_power", "measurement"),
    ("Grid Reactive Power L2",    "QAL2",   33, "var", "reactive_power", "measurement"),
    ("Grid Reactive Power L3",    "QAL3",   35, "var", "reactive_power", "measurement"),
    # Power factor
    ("Grid Power Factor L1",      "PFL1",   37, None,  "power_factor",   "measurement"),
    ("Grid Power Factor L2",      "PFL2",   39, None,  "power_factor",   "measurement"),
    ("Grid Power Factor L3",      "PFL3",   41, None,  "power_factor",   "measurement"),
    # Totals / averages
    ("Grid Frequency",            "FREQ",   55, "Hz",  "frequency",      "measurement"),
    ("Grid Average Voltage L-N",  "VAVGLN", 57, "V",   "voltage",        "measurement"),
    ("Grid Average Voltage L-L",  "VAVGLL", 59, "V",   "voltage",        "measurement"),
    ("Grid Average Current",      "IAVG",   61, "A",   "current",        "measurement"),
    ("Grid Total Apparent Power", "STOT",   63, "VA",  "apparent_power", "measurement"),
    ("Grid Total Active Power",   "PTOT",   65, "W",   "power",          "measurement"),
    ("Grid Total Reactive Power", "QTOT",   67, "var", "reactive_power", "measurement"),
    ("Grid Total Power Factor",   "PFTOT",  69, None,  "power_factor",   "measurement"),
]
