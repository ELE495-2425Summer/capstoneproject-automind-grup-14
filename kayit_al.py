import sounddevice as sd
import wave
import os
import numpy as np
import time
import subprocess

# Sabit ayarlar
fs = 16000  # 16 kHz örnekleme frekansı
kayit = []
dosya_yolu = "/home/bitirme/Desktop/bitirme_deneme/Giris_Sesi_Bitirme.wav"
BASLA_DOSYASI = "flask_basla.txt"
BITIR_DOSYASI = "flask_bitir.txt"
kayit_suresi = 10  # Kayıt süresi (saniye)

print("🎙️ Kayıt sistemi hazır. 'basla' sinyali bekleniyor...")

# 'basla' sinyalini bekle
while True:
    if os.path.exists(BASLA_DOSYASI):
        with open(BASLA_DOSYASI, "r") as f:
            if "basla" in f.read():
                break
    time.sleep(0.1)

print("🔴 Kayıt başladı. 'bitir' sinyali bekleniyor...")

# Callback fonksiyonu ile veri kaydetme
def kayit_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    kayit.append(indata.copy())  # Veri kaydedilir

# Ses kaydını başlat
with sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=kayit_callback):
    while True:
        if os.path.exists(BITIR_DOSYASI):
            with open(BITIR_DOSYASI, "r") as f:
                if "bitir" in f.read():
                    break
        time.sleep(0.2)

print("🛑 Kayıt durduruluyor ve WAV dosyasına kaydediliyor...")

# Kaydın tamamlanmasını bekleyin ve veriyi birleştirin
kayit_np = np.concatenate(kayit)

# Dosya dizinini oluştur
os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)

# WAV dosyasına kaydet
with wave.open(dosya_yolu, 'wb') as dosya:
    dosya.setnchannels(1)  # Mono kanal
    dosya.setsampwidth(2)  # 16-bit PCM
    dosya.setframerate(fs)
    dosya.writeframes(kayit_np.tobytes())

print(f"✅ Ses başarıyla kaydedildi → {dosya_yolu}")

# kimlik_tanima.py dosyasını çalıştır
try:
    subprocess.run(["python3", "kimlik_tanima.py"], check=True)
    print("✅ kimlik_tanima.py başarıyla çalıştı.")
except subprocess.CalledProcessError as e:
    print(f"❌ kimlik_tanima.py çalıştırılamadı: {e}")
