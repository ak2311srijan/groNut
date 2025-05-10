import json

# Load the JSON file
with open("ref_values.json", "r") as file:
    data = json.load(file)

# Sensor input (BH1750 lux value)
import serial
import time

#entering lux value
lux_value=float(input("ENTER VALUE"))

# Find the range that matches the lux value
for entry in data:
    lux_min = entry["lux_min"]
    lux_max = entry["lux_max"] if entry["lux_max"] is not None else float('inf')

    if lux_min <= lux_value <= lux_max:
        expected_min = entry["nitrogen_level_ppm"]["min"]
        expected_max = entry["nitrogen_level_ppm"]["max"]
        fertility_level = entry["fertility_level"]
        break
else:
    raise ValueError("Lux value is out of defined ranges in JSON.")

# Calculate the expected average nitrogen concentration
expected_avg_nitrogen_ppm = (expected_min + expected_max) / 2

# Output results
print(f"Lux Value: {lux_value}")
print(f"Fertility Level: {fertility_level}")
print(f"Nitrogen Range: {expected_min} - {expected_max} ppm")
print(f"Expected Average Nitrogen Concentration: {expected_avg_nitrogen_ppm} ppm")
