import os
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy import signal

# 1. DOSYA YOLLARI
# Masaüstündeki ödev klasörünün yollarını belirtiyoruz
clean_dir = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\original"
noisy_dir = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\noisy"
output_dir = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\temizlenmis"
rapor_yolu = r"C:\Users\VICTUS\Desktop\6.DÖNEM\İşaretVeSistemler\ödev\analiz_raporu.txt"

# Eğer "temizlenmis" diye bir klasör yoksa Python bizim için oluşturacak
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. METRİK HESAPLAMA FONKSİYONLARI (Rapordaki nicel analizler)
def calculate_mse(clean, filtered):
    return np.mean((clean - filtered) ** 2)

def calculate_snr(clean, filtered):
    noise_power = np.sum((clean - filtered) ** 2)
    if noise_power == 0:
        return float('inf') # Hata sıfırsa SNR sonsuzdur (mükemmel)
    signal_power = np.sum(clean ** 2)
    return 10 * np.log10(signal_power / noise_power)

# 3. RAPOR DOSYASINI HAZIRLAMA
with open(rapor_yolu, "w", encoding="utf-8") as rapor:
    rapor.write("Dosya Adı\t|\tGürültü Frekansı (Hz)\t|\tSNR (dB)\t|\tMSE\n")
    rapor.write("-" * 80 + "\n")

    # 4. 650 DOSYA İÇİN DÖNGÜYÜ BAŞLATMA
    dosya_listesi = [f for f in os.listdir(noisy_dir) if f.endswith('.wav')]
    toplam_dosya = len(dosya_listesi)

    print(f"Toplam {toplam_dosya} dosya tespit edildi. Temizleme operasyonu başlıyor...")

    for index, filename in enumerate(dosya_listesi):
        clean_path = os.path.join(clean_dir, filename)
        noisy_path = os.path.join(noisy_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Temiz dosya eksikse atla
        if not os.path.exists(clean_path):
            continue

        fs_clean, data_clean = wavfile.read(clean_path)
        fs_noisy, data_noisy = wavfile.read(noisy_path)

        # Mono çevirimi (Garantiye almak için)
        if len(data_clean.shape) > 1: data_clean = data_clean.mean(axis=1)
        if len(data_noisy.shape) > 1: data_noisy = data_noisy.mean(axis=1)

        # Boyut eşitleme (Eğer iki dosyanın milisaniyelik uzunluk farkı varsa patlamaması için)
        min_len = min(len(data_clean), len(data_noisy))
        data_clean = data_clean[:min_len]
        data_noisy = data_noisy[:min_len]

        # ---------------- GÜRÜLTÜ FREKANSINI DİNAMİK TESPİT ETME ---------------- #
        N = len(data_noisy)
        yf_clean = fft(data_clean)
        yf_noisy = fft(data_noisy)
        xf = fftfreq(N, 1 / fs_noisy)[:N//2]

        amp_clean = np.abs(yf_clean[0:N//2])
        amp_noisy = np.abs(yf_noisy[0:N//2])

        # Gürültülü sinyalden temiz sinyali çıkararak gürültünün "kendisini" buluyoruz
        fark_spektrumu = amp_noisy - amp_clean
        
        # Farkın en yüksek olduğu (en şiddetli gürültünün olduğu) frekansın indeksini bul
        max_noise_index = np.argmax(fark_spektrumu)
        target_f0 = xf[max_noise_index]

        # Eğer bulunan gürültü frekansı 0 çıkarsa (DC bileşeni), filtre hatasını önlemek için 1 Hz'e çekiyoruz
        if target_f0 == 0: target_f0 = 1.0 

        # ---------------- DİNAMİK FİLTRE UYGULAMA ---------------- #
        Q = 5.0 # Filtre darlığı (Kalite faktörü)
        b, a = signal.iirnotch(target_f0, Q, fs_noisy)
        filtered_data = signal.filtfilt(b, a, data_noisy)

        # ---------------- METRİKLERİ HESAPLAMA VE KAYDETME ---------------- #
        # Sinyali float formunda hesaplıyoruz ki taşma (overflow) yapmasın
        mse_val = calculate_mse(data_clean.astype(float), filtered_data.astype(float))
        snr_val = calculate_snr(data_clean.astype(float), filtered_data.astype(float))

        # Filtrelenmiş sesi yeni klasöre kaydet (int16 formatına geri döndürerek)
        wavfile.write(output_path, fs_noisy, filtered_data.astype(np.int16))

        # Sonuçları rapora yaz
        rapor.write(f"{filename}\t\t|\t{target_f0:.2f} Hz\t\t\t|\t{snr_val:.2f}\t\t|\t{mse_val:.2f}\n")

        # Konsola süreci yazdır (Hangi dosyada olduğumuzu görmek için)
        print(f"[{index + 1}/{toplam_dosya}] {filename} temizlendi. Gürültü Hedefi: {target_f0:.2f} Hz | SNR: {snr_val:.2f}")

print("\nBÜTÜN İŞLEM TAMAMLANDI! Sonuçlar 'analiz_raporu.txt' dosyasına kaydedildi.")