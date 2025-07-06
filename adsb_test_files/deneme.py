import pyModeS as pms
import pandas as pd
import bios
import json

#data = bios.read("adsb_messages.csv")#
data = bios.read("converted_single_line.csv")
data = data[0]

data_dict = {}  # Store messages per ICAO
x = 0

for j in data:
    if j == "":
        continue
    try:
        df = pms.df(j)
        icao = pms.adsb.icao(j)

        if icao is not None:
            x += 1
            if icao not in data_dict:
                data_dict[icao] = []

            data_dict[icao].append({"msg_num": x, "message": j})

            print(f"x: {x}, df: {df}, icao: {icao}, message: {j}")
        
    except Exception as e:
        pass  # Or: print("Error:", e)

# Save to JSON
with open("adsb_data.json", "w") as json_file:
    json.dump(data_dict, json_file, indent=4)
