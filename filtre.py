import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy import signal

# 1. Dosya Yolları
clean_audio_path = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\original\1.wav" 
noisy_audio_path = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\noisy\1.wav"

# 2. Dosyaları Okuma ve Mono'ya Çevirme
fs_clean, data_clean = wavfile.read(clean_audio_path)
fs_noisy, data_noisy = wavfile.read(noisy_audio_path)

if len(data_clean.shape) > 1:
    data_clean = data_clean.mean(axis=1)
if len(data_noisy.shape) > 1:
    data_noisy = data_noisy.mean(axis=1)

# ---------------- YENİ BANT DURDURAN FİLTRE ---------------- #

# 3. Butterworth Bant Durduran Filtre Tasarımı
lowcut = 420.0  # Kesmeye başlayacağımız alt frekans
highcut = 560.0 # Kesmeyi bitireceğimiz üst frekans
order = 4       # Filtrenin keskinlik derecesi (Artarsa daha dik keser)

# Filtre katsayılarını hesaplama (Bandstop = Bant durduran)
b, a = signal.butter(order, [lowcut, highcut], btype='bandstop', fs=fs_noisy)

# Filtreyi gürültülü sinyale uygulama (Sıfır faz kayması için filtfilt)
filtered_data = signal.filtfilt(b, a, data_noisy)

# Sonucu kaydet
wavfile.write("filtrelenmis_ses_2_bandstop.wav", fs_noisy, filtered_data.astype(np.int16))

# ------------------------------------------------------------- #

# 4. FFT ile Sonuçları Görme
N = len(data_noisy)
xf = fftfreq(N, 1 / fs_noisy)[:N//2]

# Genlikleri Hesaplama
amp_clean = 2.0 / N * np.abs(fft(data_clean)[0:N//2])
amp_noisy = 2.0 / N * np.abs(fft(data_noisy)[0:N//2])
amp_filtered = 2.0 / N * np.abs(fft(filtered_data)[0:N//2])

# 5. Görselleştirme
plt.figure(figsize=(14, 7))

plt.plot(xf, amp_noisy, color='red', alpha=0.5, label='Gürültülü (Noisy)')
plt.plot(xf, amp_clean, color='blue', alpha=0.5, label='Temiz (Original)')
plt.plot(xf, amp_filtered, color='green', alpha=0.8, linewidth=1.2, label='Filtrelenmiş (Filtered)')

plt.title('Bant Durduran Filtre Öncesi ve Sonrası Spektrum')
plt.xlabel('Frekans (Hz)')
plt.ylabel('Genlik')
plt.xlim(0, 1000) # Değişimi görmek için 0-1000 Hz arasına odaklandık
plt.legend()
plt.grid()
plt.show()