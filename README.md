Sakarya Uygulamalı Bilimler Üniversitesi İşaretler ve Sistemler dersi ödevi
# 🎧 Dinamik Ses Sinyali Filtreleme ve Analiz (Dynamic Audio Noise Filtering)

Bu proje, İşaret ve Sistemler (Signals and Systems) dersi kapsamında geliştirilmiş, makine öğrenmesi veya hazır gürültü azaltma algoritmaları **kullanılmadan**, tamamen Klasik Dijital Sinyal İşleme (DSP) teknikleriyle ses dosyalarındaki gürültüleri tespit edip temizleyen bir otomasyon aracıdır.

## 🚀 Projenin Amacı
Gürültülü (noisy) ve temiz (original) ses dosyaları eşleştirilerek, gürültünün frekans spektrumundaki konumu dinamik olarak tespit edilir. Ardından bu gürültüye özel tasarlanan dijital IIR filtreler uygulanarak sinyal temizlenir ve sistemin başarı oranı **SNR (Sinyal-Gürültü Oranı)** ve **MSE (Ortalama Karesel Hata)** metrikleriyle nicel olarak raporlanır.

## ✨ Özellikler
* **Dinamik Gürültü Tespiti:** Sabit bir filtre kullanmak yerine, her bir ses dosyasının FFT (Hızlı Fourier Dönüşümü) analizi yapılarak gürültünün merkez frekansı (f0) otonom olarak bulunur.
* **Sıfır Faz Kayması:** `scipy.signal.filtfilt` metodu kullanılarak sinyalde faz bozulması (phase shift) engellenir.
* **Toplu Dosya İşleme:** Verisetindeki yüzlerce (örn. 650 adet) ses dosyası tek bir döngü ile saniyeler içinde analiz edilip temizlenir.
* **Otomatik Raporlama:** Temizlenen her dosya için elde edilen matematiksel başarı değerleri (SNR ve MSE) otomatik olarak bir metin belgesine aktarılır.

## 🛠️ Kullanılan Teknolojiler
* **Dil:** Python 3.x
* **Kütüphaneler:** * `numpy` (Matematiksel dizi ve matris işlemleri)
  * `scipy` (Filtre tasarımı, FFT ve .wav dosya I/O işlemleri)
  * `matplotlib` (Frekans spektrumu görselleştirme)

## 📂 Proje Dizin Yapısı
```text
📦 Proje Klasörü
┣ 📂 original/            # Temiz (referans) ses dosyaları
┣ 📂 noisy/               # Gürültülü ses dosyaları (Girdi)
┣ 📂 temizlenmis/         # Filtreden geçen ses dosyaları (Çıktı)
┣ 📜 analiz.py            # Tekil dosya frekans analiz ve görselleştirme aracı
┣ 📜 filtre.py            # Çentik/Bant Durduran filtre test aracı
┣ 📜 otomasyon.py         # Tüm veri setini işleyen ana betik
┗ 📜 analiz_raporu.txt    # SNR ve MSE nicel sonuç tablosu

Verisetini indirmek için linke gidiniz (subu uzantılı mail adresinizi kullanmalısınız.): https:
//drive.google.com/drive/folders/18VmT5jot30cPlzRlJGkl-pywglfglwaO?usp=drive_
link
