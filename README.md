# Siemens PAC2200 – Home Assistant Integration

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration)
[![Default](https://img.shields.io/badge/Default-Integration-blue.svg?style=for-the-badge&logo=homeassistant&logoColor=white)](https://www.home-assistant.io)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Andries%20Muylaert-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/AndriesMuylaert)

> **This integration was fully generated with [Claude](https://claude.ai) by Anthropic.**

A HACS custom integration for the **Siemens SENTRON PAC2200** power meter using Modbus TCP.

## Features

| Measurement | HA Platform | Unit | Description |
|---|---|---|---|
| **Voltage L-N** | `sensor` | V | Per-phase voltages VL1-N, VL2-N, VL3-N |
| **Voltage L-L** | `sensor` | V | Line-to-line voltages VL1-L2, VL2-L3, VL3-L1 |
| **Current** | `sensor` | A | Per-phase currents L1, L2, L3 |
| **Active Power** | `sensor` | W | Per-phase and total active power |
| **Reactive Power** | `sensor` | var | Per-phase and total reactive power |
| **Apparent Power** | `sensor` | VA | Per-phase and total apparent power |
| **Power Factor** | `sensor` | – | Per-phase and total power factor |
| **Frequency** | `sensor` | Hz | Grid frequency |
| **Average Voltage** | `sensor` | V | Average L-N and L-L voltages |
| **Average Current** | `sensor` | A | Average current across all phases |

29 sensor entities in total, all updated at a configurable scan interval.

## Requirements

- Home Assistant **Core 2026.3+**
- Siemens SENTRON **PAC2200** with Modbus TCP enabled
- Python package: `pymodbus>=3.6.9` (uses HA's already-installed version, currently 3.11.2)

## Installation via HACS

1. Open HACS → **Integrations** → ⋮ menu → *Custom repositories*
2. Add `https://github.com/AndriesMuylaert/siemens-pac2200` as **Integration**
3. Search for *Siemens PAC2200* and install
4. Restart Home Assistant

## Configuration

Go to **Settings → Devices & Services → Add Integration** and search for *Siemens PAC2200*.

| Setting | Default | Range | Description |
|---|---|---|---|
| Modbus IP Address | *(empty)* | any IPv4 | IP address of the PAC2200 |
| Modbus Port | `502` | 1–65535 | TCP port (PAC2200 default: 502) |
| Slave ID | `1` | 1–247 | Modbus slave/unit ID |
| Connection Delay | `2` s | 0–30 s | Wait after connecting before first read |
| Scan Interval | `10` s | 5–3600 s | Poll frequency |

All settings except IP address and port can be changed later via **Configure** in the integration card.

## Modbus Register Map

All registers are **Holding Registers** with data type **float32** (2 registers each), communicated over **Modbus TCP** (framer: socket).

| Sensor | Address | Unit | Device Class |
|---|---|---|---|
| Voltage VL1-N | 1 | V | voltage |
| Voltage VL2-N | 3 | V | voltage |
| Voltage VL3-N | 5 | V | voltage |
| Voltage VL1-L2 | 7 | V | voltage |
| Voltage VL2-L3 | 9 | V | voltage |
| Voltage VL3-L1 | 11 | V | voltage |
| Current L1 | 13 | A | current |
| Current L2 | 15 | A | current |
| Current L3 | 17 | A | current |
| Apparent Power L1 | 19 | VA | apparent_power |
| Apparent Power L2 | 21 | VA | apparent_power |
| Apparent Power L3 | 23 | VA | apparent_power |
| Active Power L1 | 25 | W | power |
| Active Power L2 | 27 | W | power |
| Active Power L3 | 29 | W | power |
| Reactive Power L1 | 31 | var | reactive_power |
| Reactive Power L2 | 33 | var | reactive_power |
| Reactive Power L3 | 35 | var | reactive_power |
| Power Factor L1 | 37 | – | power_factor |
| Power Factor L2 | 39 | – | power_factor |
| Power Factor L3 | 41 | – | power_factor |
| Frequency | 55 | Hz | frequency |
| Average Voltage L-N | 57 | V | voltage |
| Average Voltage L-L | 59 | V | voltage |
| Average Current | 61 | A | current |
| Total Apparent Power | 63 | VA | apparent_power |
| Total Active Power | 65 | W | power |
| Total Reactive Power | 67 | var | reactive_power |
| Total Power Factor | 69 | – | power_factor |

## PAC2200 Modbus Setup

1. On the PAC2200 front panel or via its web interface: enable **Modbus TCP** under the communication settings
2. Note the IP address and port (default **502**)
3. Set the slave ID if needed (default **1**)

## HACS Icon Note

The icon displayed in HACS is fetched directly from GitHub. It will appear once the repository is pushed to GitHub — local installations will show "icon not available" in HACS until then.

## Credits

**Author:** [Andries Muylaert](https://github.com/AndriesMuylaert)

**Generated with:** [Claude](https://claude.ai) by [Anthropic](https://www.anthropic.com)

---

*© Andries Muylaert – MIT License*
