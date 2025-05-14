"""Data models"""

import json
from dataclasses import dataclass

@dataclass
class EcoTrackerData:
    """EcoTracker Data model"""
    power: float
    power_phase1: float
    power_phase2: float
    power_phase3: float
    power_avg: float
    energy_counter_out: float
    energy_counter_in: float
    energy_counter_in_t1: float
    energy_counter_in_t2: float
    serial: str
    firmware_version: str
    rssi: int

    def __init__(self, power: float, power_phase1: float, power_phase2: float, power_phase3: float, power_avg: float, energy_counter_out: float, energy_counter_in: float, energy_counter_in_t1: float, energy_counter_in_t2: float, serial: str, firmware_version: str, rssi: int):
        self.power = power
        self.power_phase1 = power_phase1
        self.power_phase2 = power_phase2
        self.power_phase3 = power_phase3
        self.power_avg = power_avg
        self.energy_counter_out = energy_counter_out
        self.energy_counter_in = energy_counter_in
        self.energy_counter_in_t1 = energy_counter_in_t1
        self.serial = serial
        self.firmware_version = firmware_version
        self.rssi = rssi

    @classmethod
    def from_json(cls, json_str: str) -> 'EcoTrackerData':
        """Create the EcoTrackerData from a JSON string."""
        data = json.loads(json_str)
        return cls(
            power=data.get("power", 0.0),
            power_phase1=data.get("powerPhase1", 0.0),
            power_phase2=data.get("powerPhase2", 0.0),
            power_phase3=data.get("powerPhase3", 0.0),
            power_avg=data.get("powerAvg", 0.0),
            energy_counter_out=data.get("energyCounterOut", 0.0),
            energy_counter_in=data.get("energyCounterIn", 0.0),
            energy_counter_in_t1=data.get("energyCounterInT1", 0.0),
            energy_counter_in_t2=data.get("energyCounterInT2", 0.0),
            serial=data.get("serial", ""),
            firmware_version=data.get("firmwareVersion", ""),
            rssi=data.get("rssi", 0),
        )