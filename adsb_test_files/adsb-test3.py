import random
import time

def generate_adsb_message():
    # Generate a random ICAO address
    icao_address = ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
    
    # Random position and altitude
    latitude = random.uniform(30.0, 50.0)
    longitude = random.uniform(-130.0, -60.0)
    altitude = random.randint(10000, 45000)  # in feet

    # Current time in UTC
    current_time = time.strftime("%Y/%m/%d,%H:%M:%S")
    
    # Generate a simulated message
    message = f"MSG,3,111,11111,{icao_address},111111,{current_time},{current_time},,{altitude},,,{latitude},{longitude},,,0,,0"
    return message

# Generate a message and print
print(generate_adsb_message())
import pyModeS as pms

# Even and Odd CPR messages
msg1 = "8D40621D58C382D690C8AC2863A7"
msg2 = "8D40621D58C386435CC412692AD6"  # << last digit changed to fix odd bit
print(pms.adsb.decode(msg1))  # Decode the first message
print(pms.adsb.decode(msg2))  # Decode the second message

even_msg = ""
odd_msg = ""

def get_odd_flag(msg):
    # Extract the 7th byte (message[12:14]) and examine its 6th bit (bit 53)
    byte7 = int(msg[12:14], 16)  # This grabs the 7th byte of the message
    bit53 = (byte7 >> 3) & 1  # Extract the 6th bit (bit 53 in the CPR format)
    print(f"Message: {msg} - Byte 7: {byte7} - Bit 53: {bit53}")
    return bit53


messages = [msg1, msg2]
for msg in messages:
    flag = get_odd_flag(msg)
    if flag == 0:
        print(f"{msg} is an EVEN CPR message")
    else:
        print(f"{msg} is an ODD CPR message")

icao = pms.adsb.icao(even_msg)

# Simulated timestamps for CPR decoding (must be within 10 seconds)
t_even = 100.0
t_odd = 105.0
print(len(even_msg), len(odd_msg))  # Should be 28

# Decode position from CPR
lat, lon = pms.adsb.airborne_position(even_msg, odd_msg, t_even, t_odd)

# Decode altitude
alt = pms.adsb.altitude(even_msg)

# Print result
print("ICAO:", icao)
print("Altitude:", alt, "feet")
print("Latitude:", lat)
print("Longitude:", lon)
