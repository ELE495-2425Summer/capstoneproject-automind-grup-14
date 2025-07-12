import time
import json
import os
import math
import smbus
from gpiozero import Device, Motor, DistanceSensor
from openai import OpenAI

# OpenAI istemcisi
client = OpenAI(api_key="anahtar")

def sesli_bildirim(metin):
    ses_haritasi = {
        "İleri gidiyorum": "/home/bitirme/Desktop/bitirme_deneme/ileri_gidiyorum.mp3",
        "Geri gidiyorum": "/home/bitirme/Desktop/bitirme_deneme/geri_gidiyorum.mp3",
        "Sola dönüyorum": "/home/bitirme/Desktop/bitirme_deneme/sola_donuyorum.mp3",
        "Sağa dönüyorum": "/home/bitirme/Desktop/bitirme_deneme/saga_donuyorum.mp3",
        "Geri dönüyorum": "/home/bitirme/Desktop/bitirme_deneme/geri_donuyorum.mp3",
        "Engel algılandı": "/home/bitirme/Desktop/bitirme_deneme/engel_durma.mp3",
        "Komut bekliyorum": "/home/bitirme/Desktop/bitirme_deneme/bitis.mp3"
    }

    ses_dosyasi = ses_haritasi.get(metin)
    if ses_dosyasi and os.path.exists(ses_dosyasi):
        os.system(f"mpg123 '{ses_dosyasi}'")
    else:
        print(f"❌ Ses dosyası bulunamadı: {ses_dosyasi}")


def hareket_durumu_yaz(mesaj):
    with open("status.txt", "w", encoding="utf-8") as f:
        f.write(mesaj)

# Motorlar
motor_sol = Motor(forward=21, backward=20, enable=13, pwm=True)
motor_sag = Motor(forward=26, backward=19, enable=12, pwm=True)

# Sadece ortadaki sensörler
sensor_ileri_orta = DistanceSensor(echo=25, trigger=22, max_distance=1.75)
sensor_geri_orta = DistanceSensor(echo=6, trigger=5, max_distance=1.75)

# MPU-6050 ayarları
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43

bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def gyro_x_oku_raw():
    high = bus.read_byte_data(MPU6050_ADDR, GYRO_XOUT_H)
    low = bus.read_byte_data(MPU6050_ADDR, GYRO_XOUT_H + 1)
    value = (high << 8) | low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value / 131.0

def gyro_x_offset_hesapla(num_samples=500):
    toplam = 0
    for _ in range(num_samples):
        toplam += gyro_x_oku_raw()
        time.sleep(0.002)
    return toplam / num_samples

gyro_x_offset = gyro_x_offset_hesapla()

def gyro_x_oku():
    return gyro_x_oku_raw() - gyro_x_offset

def dur():
    motor_sol.stop()
    motor_sag.stop()
    print("■ Motorlar durdu")
    hareket_durumu_yaz("Araç durdu")
    time.sleep(0.5)

def mesafeye_gore_hareket(sensor, yon="ileri", mesafe_dur=40, sure=None):
    hareket_durumu_yaz(f"Araç {yon.capitalize()} gidiyor")
    print(f"➡️ {yon.capitalize()} git (mesafeye duyarlı hız)")

    start = time.time()

    while True:
        mesafe = sensor.distance * 100  # cm
        zaman_gecen = time.time() - start

        if sure is not None and zaman_gecen >= sure:
            print(f"⏱ Süre doldu ({sure}s), duruluyor.")
            break

        if mesafe <= mesafe_dur:
            print(f"🛑 Mesafe {mesafe:.1f} cm, DURULUYOR.")
            dur()
            sesli_bildirim("Engel algılandı")
            hareket_durumu_yaz("Araç durdu")
            break

        if mesafe <= 60:
            hiz = 0.3
        elif mesafe <= 80:
            hiz = 0.4
        elif mesafe <= 120:
            hiz = 0.5
        elif mesafe <= 160:
            hiz = 0.6
        else:
            hiz = 0.8

        if yon == 'ileri':
            motor_sol.backward(hiz)
            motor_sag.backward(hiz)
        else:
            motor_sol.forward(hiz)
            motor_sag.forward(hiz)

        print(f"Mesafe ({yon}): {mesafe:.1f} cm | Hız: {hiz:.2f} | Zaman: {zaman_gecen:.1f}s")

    dur()

def metreyi_saniyeye_cevir(metre):
    return float(metre) * 1.0

def ileri_git(sure=None):
    sesli_bildirim("İleri gidiyorum")
    mesafeye_gore_hareket(sensor_ileri_orta, yon="ileri", mesafe_dur=45, sure=sure)

def geri_git(sure=None):
    sesli_bildirim("Geri gidiyorum")
    mesafeye_gore_hareket(sensor_geri_orta, yon="geri", mesafe_dur=45, sure=sure)

def sola_don(hiz=0.6):
    sesli_bildirim("Sola dönüyorum")
    print("⟲ Sola dön")
    hareket_durumu_yaz("Araç Sola dönüyor")

    hedef_acisal_aci = 76.0
    toplam_acisal_aci = 0.0
    prev_time = time.perf_counter()

    motor_sol.forward(hiz)
    motor_sag.backward(hiz)

    while toplam_acisal_aci < hedef_acisal_aci:
        gyro_x = gyro_x_oku()
        simdi = time.perf_counter()
        dt = simdi - prev_time
        toplam_acisal_aci += gyro_x * dt
        prev_time = simdi
        print(f"Sola: gyro_x={gyro_x:.2f}  açı={toplam_acisal_aci:.2f}")

    dur()

def saga_don(hiz=0.6):
    sesli_bildirim("Sağa dönüyorum")
    print("⟳ Sağa dön")
    hareket_durumu_yaz("Araç Sağa dönüyor")

    hedef_acisal_aci = 76.0
    toplam_acisal_aci = 0.0
    prev_time = time.perf_counter()

    motor_sol.backward(hiz)
    motor_sag.forward(hiz)

    while toplam_acisal_aci < hedef_acisal_aci:
        gyro_x = -gyro_x_oku()
        simdi = time.perf_counter()
        dt = simdi - prev_time
        toplam_acisal_aci += gyro_x * dt
        prev_time = simdi
        print(f"Sağa: gyro_x={gyro_x:.2f}  açı={toplam_acisal_aci:.2f}")

    dur()

def geri_don(hiz=0.6):
    sesli_bildirim("Geri dönüyorum")
    print("⟳ Geri dön")
    hareket_durumu_yaz("Araç geri dönüyor")

    hedef_acisal_aci = 164.0
    toplam_acisal_aci = 0.0
    prev_time = time.perf_counter()

    motor_sol.backward(hiz)
    motor_sag.forward(hiz)

    while toplam_acisal_aci < hedef_acisal_aci:
        gyro_x = -gyro_x_oku()
        simdi = time.perf_counter()
        dt = simdi - prev_time
        toplam_acisal_aci += gyro_x * dt
        prev_time = simdi
        print(f"Geri dön: gyro_x={gyro_x:.2f}  açı={toplam_acisal_aci:.2f}")

    dur()

def komut_isle(json_dosya):
    with open(json_dosya, "r", encoding="utf-8") as f:
        komutlar = json.load(f)
    for k in komutlar:
        komut = k.get('komut')
        sure = k.get('sure')
        mesafe = k.get('mesafe')

        sure = None if sure == '-' else float(sure)
        mesafe = None if mesafe == '-' else float(mesafe)

        if sure is None and mesafe is not None:
            sure = metreyi_saniyeye_cevir(mesafe)

        if komut == 'ileri_git':
            ileri_git(sure=sure)
        elif komut == 'geri_git':
            geri_git(sure=sure)
        elif komut == 'sola_don':
            sola_don()
        elif komut == 'saga_don':
            saga_don()
        elif komut == 'geri_don':
            geri_don()
    dur()
    sesli_bildirim("Komut bekliyorum")

if __name__ == "__main__":
    komut_isle("motor_commands.txt")
