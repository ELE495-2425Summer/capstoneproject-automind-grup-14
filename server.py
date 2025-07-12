from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import logging
import time
import logging
import sys

log = logging.getLogger('werkzeug')
log.disabled = True


app = Flask(__name__)
CORS(app)

logging.basicConfig(
    filename='server_log.txt',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    encoding='utf-8'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASLA_DOSYASI = os.path.join(BASE_DIR, "flask_basla.txt")
BITIR_DOSYASI = os.path.join(BASE_DIR, "flask_bitir.txt")
mic_process = None

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global mic_process

    # Durum dosyasını kontrol et
    DURUM_DOSYASI = os.path.join(BASE_DIR, "durum.txt")
    if os.path.exists(DURUM_DOSYASI):
        with open(DURUM_DOSYASI, "r", encoding="utf-8") as f:
            durum = f.read().strip()
        if durum == "ARAC_KAPALI":
            sesli_bildirim("Araci calistirin")
            logging.warning("Kayıt başlatılamadı: Araç kapalı.")
            return jsonify({"message": "Araç kapalıyken kayıt başlatılamaz."}), 403

    if mic_process is not None and mic_process.poll() is None:
        return jsonify({"message": "Zaten çalışıyor."}), 400

    try:
        # Başla ve bitir dosyalarını temizle
        for path in [BASLA_DOSYASI, BITIR_DOSYASI]:
            if os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("")

        # Scripti başlat (ilk başta bekleme modunda olur)
        mic_process = subprocess.Popen(['python3', 'kayit_al.py'])

        # Kayda başla sinyali gönder
        time.sleep(0.1)
        with open(BASLA_DOSYASI, "w", encoding="utf-8") as f:
            f.write("basla")

        logging.info("Kayıt başlatıldı.")
        return jsonify({"message": "Ses kaydı başlatıldı."}), 200
    except Exception as e:
        logging.error(f"Başlatılamadı: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global mic_process
    try:
        # Bitir sinyali gönder
        with open(BITIR_DOSYASI, "w", encoding="utf-8") as f:
            f.write("bitir")

        logging.info("Bitir sinyali gönderildi.")

        # Kapanmasını bekle
        if mic_process is not None:
            for _ in range(20):  # 20 x 0.2s = 4 saniye bekleme
                if mic_process.poll() is not None:
                    break
                time.sleep(0.2)
            if mic_process.poll() is None:
                mic_process.terminate()
                logging.warning("Kayıt scripti zamanında kapanmadı, zorla kapatıldı.")
            mic_process = None

        return jsonify({"message": "Kayıt durduruldu."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_transcription', methods=['GET'])
def get_transcription():
    path = "chatgpt_cevap.txt"
    if not os.path.exists(path) or os.path.getsize(path) < 10:
        return jsonify({"transcription": "(Hazırlanıyor...)", "hazir": False}), 202

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return jsonify({"transcription": text, "hazir": True}), 200

@app.route('/get_status', methods=['GET'])
def get_status():
    try:
        with open("status.txt", "r", encoding="utf-8") as f:
            durum = f.read().strip()
        return jsonify({"durum": durum}), 200
    except FileNotFoundError:
        return jsonify({"durum": "Bilinmiyor"}), 200

@app.route('/get_log', methods=['GET'])
def get_log():
    try:
        with open("server_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        return jsonify({"log": ''.join(lines[-20:])}), 200
    except FileNotFoundError:
        return jsonify({"log": "Log dosyası bulunamadı."}), 200

@app.route('/clear_log', methods=['POST'])
def clear_log():
    try:
        open("server_log.txt", "w", encoding="utf-8").close()
        return jsonify({"success": True, "message": "Log dosyası temizlendi."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/arac_ac', methods=['GET'])
def araci_ac():
    try:
        subprocess.run(["python3", "uid_kontrol.py"], check=True)
        logging.info("Ara� a�ma i�lemi ba�lat�ld� (uid_kontrol.py).")
        return "UID kontrol� yap�ld�", 200
    except subprocess.CalledProcessError as e:
        logging.error(f"UID kontrol �al��t�r�lamad�: {e}")
        return "UID kontrol hatas�", 500

@app.route('/arac_kapat', methods=['GET'])
def araci_kapat():
    try:
        with open("durum.txt", "w") as f:
            f.write("ARAC_KAPALI")
        logging.info("Ara� kapat�ld� (durum.txt g�ncellendi).")
        return "Ara� kapat�ld�", 200
    except Exception as e:
        logging.error(f"durum.txt yaz�lamad�: {e}")
        return "Hata olu�tu", 500    
    
@app.route('/get_arac_durumu', methods=['GET'])
def get_arac_durumu():
    try:
        with open("durum.txt", "r") as f:
            durum = f.read().strip().upper()
        if durum == "ARAC_CALISTI":
            return jsonify({"arac_durumu": "calisti"}), 200
        elif durum == "ARAC_KAPALI":
            return jsonify({"arac_durumu": "kapali"}), 200
        else:
            return jsonify({"arac_durumu": "bilinmiyor"}), 200
    except FileNotFoundError:
        return jsonify({"arac_durumu": "bilinmiyor"}), 200    
    
@app.route('/run_command', methods=['POST'])
def run_command():
    try:
        komut = request.json.get("komut")
        if not komut:
            return jsonify({"error": "Komut belirtilmedi."}), 400
        
        result = subprocess.check_output(komut, shell=True, text=True, stderr=subprocess.STDOUT)
        return jsonify({"output": result}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"output": e.output, "error": str(e)}), 500


def sesli_bildirim(metin):
    ses_haritasi = {
        "Araci calistirin": "/home/bitirme/Desktop/bitirme_deneme/arac_calistir.mp3"
    }

    ses_dosyasi = ses_haritasi.get(metin)
    if ses_dosyasi and os.path.exists(ses_dosyasi):
        os.system(f"mpg123 '{ses_dosyasi}'")
    else:
        print(f"❌ Ses dosyası bulunamadı: {ses_dosyasi}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
