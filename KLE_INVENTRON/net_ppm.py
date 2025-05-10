import json
import re
import serial
import time

# Load the JSON file
with open("ref_values.json", "r") as file:
    data = json.load(file)

# Initialize serial connection
esp = serial.Serial(port='COM12', baudrate=9600, timeout=1)
time.sleep(2)  # Give Arduino time to reset

# Counter to limit the number of outputs
read_count = 0
MAX_READS = 1

while read_count < MAX_READS:
    try:
        line = esp.readline().decode('utf-8', errors='ignore').strip()
        if line:
            # Try to extract float from line using regex
            match = re.search(r"([\d]+(?:\.[\d]+)?)", line)
            if match:
                lux_value = float(match.group(1))
                print(f"Average Lux: {lux_value}")

                # Lookup matching data range
                for entry in data:
                    lux_min = entry["lux_min"]
                    lux_max = entry["lux_max"] if entry["lux_max"] is not None else float('inf')

                    if lux_min <= lux_value <= lux_max:
                        expected_min = entry["nitrogen_level_ppm"]["min"]
                        expected_max = entry["nitrogen_level_ppm"]["max"]
                        fertility_level = entry["fertility_level"]
                        expected_avg_nitrogen_ppm = (expected_min + expected_max) / 2

                        print(f"Fertility Level: {fertility_level}")
                        print(f"Nitrogen Range: {expected_min} - {expected_max} ppm")
                        print(f"Expected Avg Nitrogen: {expected_avg_nitrogen_ppm} ppm")
                        print("=" * 40)
                        read_count += 1
                        break
                else:
                    print("Lux value is out of defined ranges.")
            else:
                print(f"Ignored line: {line}")
    except Exception as e:
        print("Error:", e)
