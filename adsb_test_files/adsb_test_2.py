import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
amount = 1000
#fs, data = wavfile.read("D:\\adsb.2021-11-26T15_03_30_573.wav")
fs, data = wavfile.read("D:\\adsb.2021.wav")

if data.ndim != 2 or data.shape[1] != 2:
    raise ValueError("WAV dosyası stereo değil. IQ verisi stereo olmalıdır.")

I = data[:, 0].astype(np.float32)
Q = data[:, 1].astype(np.float32)
iq = I + 1j * Q


magnitude = np.abs(iq)
magnitude /= np.max(magnitude)


from scipy.signal import find_peaks

# 0.5 eşik değerini geçince ADS-B mesajı olabilir
threshold = 0.3
peaks, _ = find_peaks(magnitude, height=threshold, distance=int(fs * 0.0001))  # min 100 µs aralıklı

print(f"Bulunan olası mesaj sayısı: {len(peaks)}")


def ppm_decode_from_index(magnitude, start_idx, fs, msg_bits=112):
    bit_len = int(fs / 1_000_000)  # 1 µs kaç örnek
    msg = []

    for i in range(msg_bits):
        b_start = start_idx + i * bit_len
        b_end = b_start + bit_len
        if b_end > len(magnitude):
            return None  # Dosya sonuna gelmiş olabilir

        first_half = magnitude[b_start : b_start + bit_len // 2]
        second_half = magnitude[b_start + bit_len // 2 : b_end]

        bit = 1 if np.mean(first_half) > np.mean(second_half) else 0
        msg.append(bit)

    return msg


all_messages = []
counter = 0
for idx in peaks:
    counter += 1
    bits = ppm_decode_from_index(magnitude, idx, fs)
    if bits and len(bits) == 112:
        all_messages.append(bits)
        print(bits)
    if counter >= amount:  # İlk 10 mesajı göster
        break

import pyModeS as pms

for i, bits in enumerate(all_messages[:amount]):  # ilk 5 mesajı göster
    binstr = ''.join(map(str, bits))
    hexmsg = f"{int(binstr, 2):028X}"
    try:
        df = pms.df(hexmsg)
        icao = pms.icao(hexmsg)
        deneme = pms.typecode(hexmsg)
        if (df == 17 or df == 4 or df == 18):
            if icao != None:
                print(f"{i+1}. Mesaj: DF={df}, ICAO={icao}, HEX={hexmsg}, Type={deneme}")
    except:
        print(f"{i+1}. Mesaj çözülemedi: {hexmsg}")
