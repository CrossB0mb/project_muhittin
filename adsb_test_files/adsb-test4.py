#import pyModeS as pms
import math
import numpy as np
import bios

msg = "8D4840D6202CC371C32CE0576098"
#df = pms.df(msg)
#tc = pms.typecode(msg)
#
#print(f"DF: {df}, TC: {tc}")
#
#if (df != 17) or (tc < 1) or (tc > 28):
#    print("Invalid message")
#    quit()
#else:
#    print("Valid message")
#
#pms.adsb.icao(msg)  # ICAO address
#print(f"ICAO: {pms.adsb.icao(msg)}")
#print(f"CallSign: {pms.adsb.callsign(msg)}")
#

#-----------------------------------------------

generator = 1111111111111010000001001
msg = ("8D4840D6202CC371C32CE0576098") # 112 bits
info = [["icao", "decoded_callsign_str", "downlink_format", "emitter_category", "type_code", "surveillance_status", "nic_supplement_b"]]
msg_stock = msg # save original message

def crc_check(msg, generator):
    msg = int(msg, 16) # convert to int
    msg = bin(msg)[2:] # convert to binary string
    for i in range(88): # 112 bits - 24 parity bits
        if msg[i] is 1:
            msg[i:i+24] = msg[i:i+24] ^ generator
    crc = msg[-24:] # last 24 bits of result
    print(f"CRC: {crc}") # CRC value
    if crc == 0:
        control = 1
        print("CRC is valid")
    else:
        control = 0
        print("CRC is invalid")
    msg = ("8D4840D6202CC371C32CE0576098") # 112 bits
    msg = ("33C596B33AE074CA9646F8EFF336")
    return control
crc_check(msg, generator) # call function
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
    
    
    info.append([icao, decoded_callsign_str, int(downlink_format, 2), emitter_category, int(type_code, 2), surveillance_status, nic_supplement_b])
    #print(info) # print list
    return info # return list

def decoding_until_callsign2(msg):
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
    
    
    info.append([icao, decoded_callsign_str, int(downlink_format, 2), emitter_category, int(type_code, 2), surveillance_status, nic_supplement_b])
    #print(info) # print list
    return [icao, decoded_callsign_str, int(downlink_format, 2), emitter_category, int(type_code, 2), surveillance_status, nic_supplement_b] # return list


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
        print(len(hex_msg))
        print(hex_msg)
        raise ValueError("ADS-B message must be 28 hex characters (112 bits).")
    
    binary_msg = hex_to_bin(hex_msg)
    
    lat_cpr_bits = binary_msg[54:71]  # bits 55–71 (Python index 54–71)
    lon_cpr_bits = binary_msg[71:88]  # bits 72–88 (Python index 71–88)

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


messages = ["8D40621D58C382D690C8AC2863A7", "8D40621D58C386435CC412692AD6"] # list of messages
msg1 = messages[0] # first message
msg2 = messages[1] # second message
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


def NL_lat(lat): 
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
    return NL_lat_numpy
NL_lat_numpy = NL_lat(lat)  # Calculate NL value based on latitude

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

#TODO: calculate latitude index j
def calculate_latitude_index_j(lat_cpr_even, lat_cpr_odd):
   
    j = np.floor(((59 * lat_cpr_even) - (60 * lat_cpr_odd)) + (1/2))
    return j
latitude_index_j = calculate_latitude_index_j(cpr_data[1][0], cpr_data[1][2])

def calculate_latitude(lat_index_j, lat_cpr_even, lat_cpr_odd, NZ, Te, To):
    DLatEven = (360 / (4* NZ))
    DLatOdd = (360 / ((4 * NZ)-1))

    LatEven = DLatEven * (np.mod(lat_index_j,60) + lat_cpr_even)
    LatOdd = DLatOdd * (np.mod(lat_index_j,59) + lat_cpr_odd)
    if LatEven >= 270:
        LatEven -= 360
    if LatOdd >= 270:
        LatOdd -= 360

    if Te >= To:
        Lat = LatEven
    else:
        Lat = LatOdd
    return Lat, LatEven, LatOdd
latitude =[]


#! Te and To need to be set via msg. So it can be dynamic.
Te = 2  # Even frame time
To = 1  # Odd frame time


latitude.append(calculate_latitude(latitude_index_j, cpr_data[1][0], cpr_data[1][2], NZ, Te, To))
Lat, LatEven, LatOdd = calculate_latitude(latitude_index_j, cpr_data[1][0], cpr_data[1][2], NZ, Te, To)

print(f"Latitude: {Lat}, LatEven: {LatEven}, LatOdd: {LatOdd}")


def NL_func(lat):
    import math
    if abs(lat) < 10**-6:
        return 59
    a = 1 - np.cos(np.pi / 30)
    b = 1 - np.cos(np.pi / 180 * abs(lat))**2
    if b == 0:
        return 1
    nl = 2 * np.pi / np.arccos(1 - a / b)
    return int(np.floor(nl))

def calculate_longitude(lon_cpr_even, lon_cpr_odd, NZ, Te, To):
    if Te >= To:
        ni = max((NL_lat(LatEven)), 1)
        DLon = 360/ni
        m = np.floor((lon_cpr_even * (NL_lat(LatEven) - 1) - lon_cpr_odd * NL_lat(LatEven) + 1/2))
        Lon = DLon * (np.mod(m, ni) + lon_cpr_even)
    elif Te < To:
        ni = max(NL_lat(LatOdd), 1)
        DLon = 360/ni
        m = np.floor((lon_cpr_even * (NL_lat(LatOdd) - 1) - lon_cpr_odd * NL_lat(LatOdd) + 1/2))
        Lon = DLon * (np.mod(m, ni) + lon_cpr_odd)

    if Lon >= 180:
        Lon -= 360
    return Lon
Lon = calculate_longitude(cpr_data[1][1], cpr_data[1][3], NZ, Te, To)
print(f"Longitude: {Lon}")

def extract_altitude_from_adsb(hex_msg):
    """
    ADS-B mesajından altitude (ft) bilgisini çözer (sadece Q-bit = 1 için).
    """
    if len(hex_msg) != 28:
        raise ValueError("ADS-B message must be 28 hex characters (112 bits).")

    binary_msg = bin(int(hex_msg, 16))[2:].zfill(112)

    # ALTITUDE alanı: bit 41–52 → index 40:52 (12 bit)
    alt_bits = binary_msg[40:52+1]

    q_bit = alt_bits[7]  # Q-bit = 8. bit (index 7)

    if q_bit == '1':
        # Q-bit'i çıkar → ilk 7 bit + son 4 bit = 11 bit
        n_bits = alt_bits[:7] + alt_bits[8:]
        #delete last bit
        n_bits = n_bits[:-1]
        print("n_bits:", n_bits)  # print n_bits for debugging
        N = int(n_bits, 2)
        print("N:", N)
        altitude = N * 25 - 1000
        return altitude
    else:
        return None


messages = bios.read("messages.csv")
print("Messages from CSV:", messages)

messages = messages[0]

lat_counter = 0   
cpr_data = [["lat_cpr_even", "lon_cpr_even", "lat_cpr_odd", "lon_cpr_odd"]]
info = [["icao", "decoded_callsign_str", "downlink_format", "emitter_category", "type_code", "surveillance_status", "nic_supplement_b"]]
latitude =[]
Te = 2  # Even frame time
To = 1  # Odd frame time
data_info = [["ICAO","Latitude","Longitude","Altitude","Callsign"]]
for msg in messages:
    crc_check(msg, generator)  # CRC kontrolü
    decoding_until_callsign(msg)  # Çağrı işareti ve diğer bilgileri çöz
    icao, decoded_callsign_str, downlink_format, emitter_category, type_code, surveillance_status, nic_supplement_b = decoding_until_callsign2(msg)
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
        latitude_index_j = calculate_latitude_index_j(cpr_data[1][0], cpr_data[1][2])
        latitude.append(calculate_latitude(latitude_index_j, cpr_data[1][0], cpr_data[1][2], NZ, Te, To))
        Lat, LatEven, LatOdd = calculate_latitude(latitude_index_j, cpr_data[1][0], cpr_data[1][2], NZ, Te, To)
        Lon = calculate_longitude(cpr_data[1][1], cpr_data[1][3], NZ, Te, To)
        print(f"Longitude: {Lon}")
        altitude = extract_altitude_from_adsb(msg)
        data_info.append([icao, Lat, Lon, altitude, decoded_callsign_str])
        #write_to_csv(data_info, "adsb_data_info")  # Write to CSV file