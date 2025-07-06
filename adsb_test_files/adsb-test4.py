import pyModeS as pms
import math
import numpy as np

msg = "8D4840D6202CC371C32CE0576098"
df = pms.df(msg)
tc = pms.typecode(msg)

print(f"DF: {df}, TC: {tc}")

if (df != 17) or (tc < 1) or (tc > 28):
    print("Invalid message")
    quit()
else:
    print("Valid message")

pms.adsb.icao(msg)  # ICAO address
print(f"ICAO: {pms.adsb.icao(msg)}")
print(f"CallSign: {pms.adsb.callsign(msg)}")


#-----------------------------------------------

generator = 1111111111111010000001001
#msg = ("8D4840D6202CC371C32CE0576098") # 112 bits
msg = ("33C596B33AE074CA9646F8EFF336")
msg_stock = msg # save original message
msg = int(msg, 16) # convert to int
msg = bin(msg)[2:] # convert to binary string
for i in range(88): # 112 bits - 24 parity bits
    if msg[i] is 1:
        msg[i:i+24] = msg[i:i+24] ^ generator
crc = msg[-24:] # last 24 bits of result
print(f"CRC: {crc}") # CRC value
if crc == 0:
    print("CRC is valid")
else:
    print("CRC is invalid")
msg = ("8D4840D6202CC371C32CE0576098") # 112 bits
msg = ("33C596B33AE074CA9646F8EFF336")
decoder = {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h",
    "9": "i",
    "10": "j",
    "11": "k",
    "12": "l",
    "13": "m",
    "14": "n",
    "15": "o",
    "16": "p",
    "17": "q",
    "18": "r",
    "19": "s",
    "20": "t",
    "21": "u",
    "22": "v",
    "23": "w",
    "24": "x",
    "25": "y",
    "26": "z",
    "32": "_",
    "48": "0",
    "49": "1",
    "50": "2",
    "51": "3",
    "52": "4",
    "53": "5",
    "54": "6",
    "55": "7",
    "56": "8",
    "57": "9", 
}

def write_to_csv(data, filename):
    import csv
    with open(f"{filename}.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)




def decoding_until_callsign(msg):
    #* decoding dc ec tc etc.
    
    msg = int(msg, 16) # convert to int
    msg = bin(msg)[2:] # convert to binary string
    print("msg: ", msg) # remaining bits
    downlink_format = msg[:5]
    print("downlink_format: ", downlink_format) # first 5 bits
    msg = msg[5:] # remove first 5 bits
    emitter_category = msg[:3] # first 3 bits  #! EC = 0 ise TC verisi yok sinyalde.
    print("emitter_category: ", emitter_category) # first 3 bits
    msg = msg[3:] # remove first 3 bits
    #print("msg: ", msg) # remaining bits
    msg_int = int(msg, 16) # convert to int
    #print("msg_int: ", msg_int) # convert to int
    icao = msg[:24] # first 24 bits
    print("icao: ", icao) # first 24 bits
    msg = msg[24:] # remove first 24 bits
    #print("msg: ", (msg)) # remaining bits
    type_code = msg[:5] # first 5 bits
    print("type_code: ", type_code) # first 5 bits
    msg = msg[5:] # remove first 5 bits
    surveillance_status = msg[:2] # first 3 bits
    print("surveillance_status: ", surveillance_status) # first 3 bits
    msg = msg[2:] # remove first 3 bits
    nic_supplement_b = msg[:1] # first 1 bit
    print("nic_supplement_b: ", nic_supplement_b) # first 1 bit
    msg = msg[1:] # remove first 1 bit
    #print("msg: ", msg) # remaining bits
    # last 24 bits
    parity = msg[-24:] # last 24 bits
    #print("parity: ", parity) # last 24 bits
    msg = msg[:-24] # remove last 24 bits
    #print("msg: ", msg) # remaining bits
    decoded_callsign = []


    #* decoding callsign
    while msg != "":
        msg_part = msg[:6] # first 6 bits
        print(msg_part) # print first 6 bits
        msg = msg[6:] # remove first 6 bits
        decoder_part = int(msg_part, 2) # convert to int
        #decoder{decoder_part} # get value from dictionary}
        print(decoder_part)
        decoded_callsign.append(decoder_part) # append to list

    print("decoded_callsign: ", decoded_callsign) # print list
    decoded_callsign_str = ""
    for part in decoded_callsign:
        print(part)
        try:
            print(decoder[str(part)],)
            decoded_callsign_str += decoder[str(part)] # append to string
        except:
            pass
    print("decoded_callsign_str:", decoded_callsign_str) # print string
    #! icao = int(icao, 2) # convert to int
    print("icao: ", icao) # convert to int
    
    info = [["icao", "decoded_callsign_str", "downlink_format", "emitter_category", "type_code", "surveillance_status", "nic_supplement_b"]]
    info.append([icao, decoded_callsign_str, int(downlink_format, 2), emitter_category, int(type_code, 2), surveillance_status, nic_supplement_b])
    #print(info) # print list
    return info # return list

def hex_to_bin(hex_str):
    """
    Hexadecimal string'i 112-bitlik binary string'e çevirir.
    """
    bin_str = bin(int(hex_str, 16))[2:].zfill(112)
    return bin_str

def extract_cpr_from_adsb(hex_msg):
    """
    ADS-B hexadecimal mesajından LAT-CPR ve LON-CPR değerlerini çıkarır.
    
    :param hex_msg: ADS-B mesajı (28 karakterlik hex string, örn: '8D4840D6202CC371C32CE0576098')
    :return: lat_cpr (int), lon_cpr (int), frame_flag (0=even, 1=odd)
    """
    if len(hex_msg) != 28:
        raise ValueError("ADS-B message must be 28 hex characters (112 bits).")
    
    binary_msg = hex_to_bin(hex_msg)
    
    lat_cpr_bits = binary_msg[54:72]  # bits 55–71 (Python index 54–71)
    lon_cpr_bits = binary_msg[72:89]  # bits 72–88 (Python index 71–88)

    frame_flag = int(binary_msg[53])  # bit 54: CPR frame flag (even/odd)

    lat_cpr = int(lat_cpr_bits, 2)
    lon_cpr = int(lon_cpr_bits, 2)

    return lat_cpr, lon_cpr, frame_flag


aircraft_info = decoding_until_callsign(msg) # call function

def even_odd_finder(given_msg):
    bit54 = given_msg
    bit54 = int(bit54, 16) # convert to int
    bit54 = bin(bit54)[2:] # convert to binary string
    bit54 = bit54[53] # 54th bit of original message
    print("bit54: ", bit54) # print 54th bit of original message


msg1 = "8D40621D58C382D690C8AC2863A7"
msg2 = "8D40621D58C386435CC412692AD6"
even_odd_finder(msg1) # call function
x= decoding_until_callsign(msg1) # call function
print("msg1: ", msg1) # print original message
print("-----------------------------------------------------------------------------")
even_odd_finder(msg2) # call function
y = decoding_until_callsign(msg2) # call function
print("msg2: ", msg2) # print original message
z = x
z.append(y[1]) # append y[1] to x[1]
if x[1][0] == y[1][0]:
    print("Same ICAO")
    print(z)
    write_to_csv(z, "aircraft_info") # write to csv file
else:
    print("Different ICAO")

#TODO: 3.2 CPR parameters and functions

NZ = 15
lat = -87 #! lat data need to be set via msg. So it can be dynamic.


NL_lat_numpy = np.floor((2 * np.pi) / (
    np.arccos(1 - ((1 - np.cos(np.pi / (2 * NZ))) /
    (np.cos((np.pi / 180) * lat) ** 2)))
))

# NL value fixation based on latitude limitations
if lat < -87:
    NL_lat_numpy = 1
elif lat == -87:
    NL_lat_numpy = 2
elif lat == 0:
    NL_lat_numpy = 59
elif lat == 87:
    NL_lat_numpy = 2
elif lat > 87:
    NL_lat_numpy = 1
print(f"NL_lat: {NL_lat_numpy}")

cpr_constant = 131072
messages = [
    "8D40621D58C382D690C8AC2863A7",  # Example message 1
    "8D40621D58C386435CC412692AD6"   # Example message 2
]

lat_counter = 0   
cpr_data = [["lat_cpr_even", "lon_cpr_even", "lat_cpr_odd", "lon_cpr_odd"]]
for msg in messages:
    lat_cpr, lon_cpr, frame_flag = extract_cpr_from_adsb(msg)
    print(f"LAT-CPR: {lat_cpr}, LON-CPR: {lon_cpr}, Frame Flag: ","Odd" if frame_flag else "Even")
    if frame_flag == 0:
        lat_cpr_even = lat_cpr / cpr_constant
        lon_cpr_even = lon_cpr / cpr_constant
    elif frame_flag == 1:
        lat_cpr_odd = lat_cpr / cpr_constant
        lon_cpr_odd = lon_cpr / cpr_constant
    else:
        print("Invalid frame flag", frame_flag)
        continue
    lat_counter += 1
    if lat_counter == 2:
        cpr_data.append([lat_cpr_even, lon_cpr_even, lat_cpr_odd, lon_cpr_odd])
        lat_counter = 0
    
print("cpr_data: ", cpr_data) # print cpr data

