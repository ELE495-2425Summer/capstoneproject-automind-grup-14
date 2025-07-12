import serial
import time
import sys
import os

def sesli_bildirim(isim):
    ses_haritasi = {
        "Omer": "/home/bitirme/Desktop/bitirme_deneme/hosgeldin_omer.mp3",
        "Enis": "/home/bitirme/Desktop/bitirme_deneme/hosgeldin_enis.mp3",
        "Alperen": "/home/bitirme/Desktop/bitirme_deneme/hosgeldin_alperen.mp3",
        "Emre": "/home/bitirme/Desktop/bitirme_deneme/hosgeldin_emre.mp3",
        "Bora": "/home/bitirme/Desktop/bitirme_deneme/hosgeldin_bora.mp3",
        "Gecersiz Kart": "/home/bitirme/Desktop/bitirme_deneme/gecersiz_kart.mp3"

    }

    ses_dosyasi = ses_haritasi.get(isim)
    if ses_dosyasi and os.path.exists(ses_dosyasi):
        os.system(f"mpg123 '{ses_dosyasi}'")
    else:
        print(f"❌ Ses dosyası bulunamadı: {ses_dosyasi}")

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()

sys.stdout = Tee(sys.stdout, open("server_log.txt", "a", encoding="utf-8"))
sys.stderr = Tee(sys.stderr, open("server_log.txt", "a", encoding="utf-8"))

# UID → isim eşleştirme
uid_to_isim = {
    "UID: C2 46 51 4B 9E": "Omer",
    "UID: 51 6D 57 6A 01": "Alperen",
    "UID: 7A FC 81 DF D8": "Bora",
    "UID: 51 F3 A9 6A 61": "Enis",
    "UID: F1 65 76 6A 88": "Emre"
}

# Seri port ayarları
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
print("📡 Kart bekleniyor...")

while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("UID:"):
            print("📥 Kart okundu:", line)
            if line in uid_to_isim:
                isim = uid_to_isim[line]
                print(f"✅ Yetkili kart! Araç çalıştı. Hoş geldin {isim}")
                sesli_bildirim(isim)
                with open("durum.txt", "w") as f:
                    f.write("ARAC_CALISTI")
            else:
                sesli_bildirim("Gecersiz Kart")
                print("❌ Yetkisiz kart! Erişim reddedildi.")
                with open("durum.txt", "w") as f:
                    f.write("ARAC_KAPALI")
            break
    time.sleep(0.1)
