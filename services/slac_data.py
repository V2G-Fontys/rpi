import asyncio
import os

class SlacData:
    def __init__(self):
        with open("/home/baskoeten/rpi/services/slacData.txt", "w") as file:
            pass 
    # functions for updating Data
    def update(self, key, value):
        print(f"[SlacData] Updating {key} with value {value}")
        print("ID:", id(self))
        with open("/home/baskoeten/rpi/services/slacData.txt", "w") as file:
            file.write(f"{key}\n")
            file.write(f"{value}\n")
            
            
    def get(self, key):
        print("ID:", id(self))
        with open("/home/baskoeten/rpi/services/slacData.txt", "r") as file:
            lines = file.readlines()
            if lines:
                print(lines[0].strip() + " | " + key)
                
                if lines[0].strip() == key:
                    return lines[1].strip()
                else:
                    print(f"[SlacData] Slac Data not found for")
                    return ""
        
slacData = SlacData()

def get_slac():
    return slacData
