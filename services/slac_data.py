import asyncio
import os

SLACData = {
    "mode": None,
    "pev_mac": None, #pretend EV mac adress
    "u_inlet": None, # 
    "evse_present_voltage": None,
    "pev_state": None,
    "evse_state": None,
    "soc": None,
    "target_u_and_i": None,
    "power_supply_u_present": None,
    "power_supply_u_target": None
}

class SlacData:
    def __init__(self):
        pass
    # functions for updating Data
    def update(self, key, value):
        print(f"[SlacData] Updating {key} with value {value}")
        SLACData[key] = value

    def get(key):
        return SLACData.get(key)
