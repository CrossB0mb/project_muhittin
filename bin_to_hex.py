# Read the .bin file and print raw hex data

file_path = "output.bin"

import csv

output_csv = "adsb_hex_output.csv"

with open(file_path, "rb") as f:
    data = f.read()

# Number of bytes per CSV row
bytes_per_row = 16

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Loop through data in chunks of 16 bytes
    for i in range(0, len(data), bytes_per_row):
        chunk = data[i:i+bytes_per_row]
        # Convert each byte to two-digit uppercase hex
        hex_chunk = [f"{b:02X}" for b in chunk]
        writer.writerow(hex_chunk)
        print(f"Row {i // bytes_per_row + 1}: {' '.join(hex_chunk)}")

print(f"Hex data saved to {output_csv}")
