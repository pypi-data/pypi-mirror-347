"""Data models"""

import json
from typing import Optional
from dataclasses import dataclass

@dataclass
class EcoTrackerData:
    """EcoTracker Data model"""
    power: Optional[float]
    power_phase1: Optional[float]
    power_phase2: Optional[float]
    power_phase3: Optional[float]
    power_avg: Optional[float]
    energy_counter_out: Optional[float]
    energy_counter_in: Optional[float]
    energy_counter_in_t1: Optional[float]
    energy_counter_in_t2: Optional[float]
    serial: str
    firmware_version: str
    rssi: int

    def __init__(self, power: Optional[float], power_phase1: Optional[float], power_phase2: Optional[float], power_phase3: Optional[float], power_avg: Optional[float], energy_counter_out: Optional[float], energy_counter_in: Optional[float], energy_counter_in_t1: Optional[float], energy_counter_in_t2: Optional[float], serial: str, firmware_version: str, rssi: int):
        self.power = power
        self.power_phase1 = power_phase1
        self.power_phase2 = power_phase2
        self.power_phase3 = power_phase3
        self.power_avg = power_avg
        self.energy_counter_out = energy_counter_out
        self.energy_counter_in = energy_counter_in
        self.energy_counter_in_t1 = energy_counter_in_t1
        self.energy_counter_in_t2 = energy_counter_in_t2
        self.serial = serial
        self.firmware_version = firmware_version
        self.rssi = rssi

    @classmethod
    def from_json(cls, json_str: str) -> 'EcoTrackerData':
        """Create the EcoTrackerData from a JSON string."""
        data = json.loads(json_str)
        return cls(
            power=data.get("power"),
            power_phase1=data.get("powerPhase1"),
            power_phase2=data.get("powerPhase2"),
            power_phase3=data.get("powerPhase3"),
            power_avg=data.get("powerAvg"),
            energy_counter_out=data.get("energyCounterOut"),
            energy_counter_in=data.get("energyCounterIn"),
            energy_counter_in_t1=data.get("energyCounterInT1"),
            energy_counter_in_t2=data.get("energyCounterInT2"),
            serial=data.get("serial", ""),
            firmware_version=data.get("firmwareVersion", ""),
            rssi=data.get("rssi", 0),
        )

    def to_json(self) -> str:
        """Serialize the EcoTrackerData instance to a JSON string."""
        return json.dumps({
            "power": self.power,
            "powerPhase1": self.power_phase1,
            "powerPhase2": self.power_phase2,
            "powerPhase3": self.power_phase3,
            "powerAvg": self.power_avg,
            "energyCounterOut": self.energy_counter_out,
            "energyCounterIn": self.energy_counter_in,
            "energyCounterInT1": self.energy_counter_in_t1,
            "energyCounterInT2": self.energy_counter_in_t2,
            "serial": self.serial,
            "firmwareVersion": self.firmware_version,
            "rssi": self.rssi,
        })