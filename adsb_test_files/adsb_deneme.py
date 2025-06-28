import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import pathlib
amount = 1000
def path_one_dir_above(filename):
    # Get the current file's directory
    current_dir = pathlib.Path(__file__).parent
    # Go one directory up
    parent_dir = current_dir.parent
    # Return the full path to the file in the parent directory
    return parent_dir / filename
file1 = path_one_dir_above("adsb.2021.wav")
print(file1)
fs, data = wavfile.read(file1)
file= "adsb.2021.wav"

import numpy as np
from scipy.io import wavfile
import pyModeS as pms

def read_iq_from_wav(filename):
    sample_rate, data = wavfile.read(filename)
    # Assuming stereo: I = channel 0, Q = channel 1
    if data.ndim == 2:
        iq_samples = data[:,0].astype(np.float32) + 1j * data[:,1].astype(np.float32)
    else:
        raise ValueError("WAV file must be stereo with I and Q channels.")
    # Normalize to [-1, 1]
    iq_samples /= np.max(np.abs(iq_samples))
    return sample_rate, iq_samples

def detect_preamble(iq_samples, sample_rate):
    # 1 sample per microsecond, so pulse positions are integers
    pulse_positions = [0, 1, 3, 4, 5, 7]
    preamble_len = 8  # samples

    mag = np.abs(iq_samples)
    preamble_positions = []

    threshold = 0.5
    for i in range(len(mag) - preamble_len):
        window = mag[i:i + preamble_len]
        pulses = [window[p] for p in pulse_positions]

        if all(p > threshold for p in pulses):
            preamble_positions.append(i)

    return preamble_positions

def decode_message(iq_samples, start, sample_rate):
    # ADS-B bit period is 1 us, samples at 1 MHz, so 1 sample per bit
    # Message length: 112 bits = 112 us
    msg_len = 112

    if start + msg_len > len(iq_samples):
        return []

    bits = []
    mag = np.abs(iq_samples)
    for i in range(msg_len):
        # For each bit sample, decide 1 or 0 by magnitude threshold
        bit_sample = mag[start + i]
        bits.append(1 if bit_sample > 0.15 else 0)

    return bits

def bits_to_int(bits):
    bit_string = ''.join(str(b) for b in bits)
    return int(bit_string, 2)

def parity_check(bits):
    poly = 0xFFF409
    msg = 0
    for b in bits:
        msg = (msg << 1) | b
    data = msg >> 24
    received_crc = msg & 0xFFFFFF
    crc = 0
    for i in range(88):
        bit = ((data >> (87 - i)) & 1) ^ ((crc >> 23) & 1)
        crc = ((crc << 1) & 0xFFFFFF)
        if bit:
            crc ^= poly
    return crc == received_crc

def bits_to_hex(bits):
    bit_string = ''.join(str(b) for b in bits)
    return hex(int(bit_string, 2))[2:].zfill(28).upper()

def decode_adsb_with_pymodes(bits):
    if len(bits) < 112:
        return None

    hex_msg = bits_to_hex(bits)
    icao = pms.icao(hex_msg)
    msg_type = pms.typecode(hex_msg)

    print(f"ICAO: {icao}, Type: {msg_type}")

    if 1 <= msg_type <= 4:
        callsign = pms.callsign(hex_msg)
        print(f"Callsign: {callsign}")

    elif 9 <= msg_type <= 18:
        print("Position message")

    elif msg_type == 19:
        velocity = pms.velocity(hex_msg)
        print(f"Velocity: {velocity}")

    else:
        print("Other message type")

    return hex_msg

def main():
    filename = "D:\\adsb.2021.wav" # Replace with your file path
    sample_rate, iq_samples = read_iq_from_wav(filename)

    # Process only first 1 million samples (1 second at 1 MHz)
    iq_samples = iq_samples[:1_000_000]

    preambles = detect_preamble(iq_samples, sample_rate)

    print(f"Detected {len(preambles)} preambles")

    valid_messages = 0
    max_messages = 5000

    for start in preambles[:max_messages]:
        bits = decode_message(iq_samples, start, sample_rate)
        bits = decode_message(iq_samples, start, sample_rate)
        if len(bits) < 112:
            continue
        
        if not parity_check(bits):
            continue

        msg_int = bits_to_int(bits)


        valid_messages += 1
        print(f"\nValid message #{valid_messages} at sample {start}")

        decode_adsb_with_pymodes(bits)

    print(f"\nTotal valid ADS-B messages decoded: {valid_messages}")

if __name__ == "__main__":
    main()
