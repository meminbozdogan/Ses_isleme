import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq

# 1. Dosya Yolları (Windows formatına uygun şekilde r ile eklendi)
clean_audio_path = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\original\1.wav" 
noisy_audio_path = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\noisy\1.wav"

# 2. Ses dosyalarını okuma (Örnekleme frekansı ve veri)
fs_clean, data_clean = wavfile.read(clean_audio_path)
fs_noisy, data_noisy = wavfile.read(noisy_audio_path)

# Sinyaller stereo (çift kanal) ise tek kanala (mono) çevirme işlemi
if len(data_clean.shape) > 1:
    data_clean = data_clean.mean(axis=1)
if len(data_noisy.shape) > 1:
    data_noisy = data_noisy.mean(axis=1)

# 3. Fourier Dönüşümü (FFT) Hesaplama
N = len(data_noisy)

# Zaman aralığını frekans eksenine çevirme
yf_clean = fft(data_clean)
yf_noisy = fft(data_noisy)
xf = fftfreq(N, 1 / fs_noisy)[:N//2]

# Genlikleri hesaplama (Sadece pozitif frekanslar)
amp_clean = 2.0 / N * np.abs(yf_clean[0:N//2])
amp_noisy = 2.0 / N * np.abs(yf_noisy[0:N//2])

# 4. Görselleştirme (Raporunda kullanabileceğin formatta)
plt.figure(figsize=(12, 6))

# Gürültülü sinyali kırmızı, temiz sinyali mavi çizdiriyoruz
plt.plot(xf, amp_noisy, color='red', alpha=0.7, label='Gürültülü Sinyal (Noisy)')
plt.plot(xf, amp_clean, color='blue', alpha=0.7, label='Temiz Sinyal (Original)')

plt.title('Ses Sinyallerinin Frekans Spektrumu Karşılaştırması')
plt.xlabel('Frekans (Hz)')
plt.ylabel('Genlik')
plt.legend()
plt.grid()

# Grafiği Nyquist frekansına (fs/2) kadar sınırlandırma
plt.xlim(0, fs_noisy / 2) 
plt.show()