import os
import numpy as np
import torchaudio
from speechbrain.inference import EncoderClassifier
from scipy.spatial.distance import cosine
import sys

def sesli_bildirim(metin):
    ses_haritasi = {
        "omer": "/home/bitirme/Desktop/bitirme_deneme/merhaba_omer.mp3",
        "enis": "/home/bitirme/Desktop/bitirme_deneme/merhaba_enis.mp3",
        "alperen": "/home/bitirme/Desktop/bitirme_deneme/merhaba_alperen.mp3",
        "bora": "/home/bitirme/Desktop/bitirme_deneme/merhaba_bora.mp3",
        "emre": "/home/bitirme/Desktop/bitirme_deneme/merhaba_emre.mp3",
        "kisi_taninmadi": "/home/bitirme/Desktop/bitirme_deneme/kisi_taninmadi.mp3"
    }

    ses_dosyasi = ses_haritasi.get(metin)
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


# Global olarak modeli bir kez yükle
print("🔁 Ses kimlik doğrulama başlatılıyor...")

MODEL_PATH = "model_cache"  # Cache klasörü belirtebilirsiniz
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=MODEL_PATH,
    run_opts={"device": "cpu"}
)
print("✅ Model yüklendi.")

# Ses doğrulama fonksiyonu
def sesi_dogrula(dosya_yolu, centroid_dosyasi="centroids.npy", SIM_THRESH=0.55):
    if not os.path.exists(dosya_yolu):
        raise FileNotFoundError(f"❌ Ses dosyası bulunamadı: {dosya_yolu}")
    if not os.path.exists(centroid_dosyasi):
        raise FileNotFoundError(f"❌ 'centroids.npy' dosyası bulunamadı!")

    print("📂 Ses yükleniyor...")
    signal_data, fs_in = torchaudio.load(dosya_yolu)
    if fs_in != 16000:
        signal_data = torchaudio.functional.resample(signal_data, fs_in, 16000)

    print("🧠 Embed çıkarılıyor...")
    emb = classifier.encode_batch(signal_data).squeeze().numpy()

    print("📁 Merkez vektörler yükleniyor...")
    centroids = np.load(centroid_dosyasi, allow_pickle=True).item()

    best_name, best_sim = None, 0.0
    print("📊 Benzerlik oranları:")
    for name, cen in centroids.items():
        sim = 1 - cosine(emb, cen)
        print(f"  {name:<10}: {sim*100:5.1f} %")
        if sim > best_sim:
            best_name, best_sim = name, sim

    print("\n🧾 Sonuç:")
    if best_sim >= SIM_THRESH:
        print(f"✅ Tanındı: {best_name} ({best_sim*100:.1f} %)")
        sesli_bildirim(best_name)
        # Threshold geçtiyse speech_to_text.py dosyasını çalıştır
        try:
            with open('speech_to_text.py', 'r') as file:
                code = file.read()

            exec(code)
            print("speech_to_text.py başlatıldı")
        except Exception as e:
            print(f"speech_to_text.py başlatılamadı: {e}")
            
        return best_name, best_sim
    else:
        sesli_bildirim("kisi_taninmadi")
        print(f"❌ Tanınmadı. En yüksek benzerlik: {best_sim*100:.1f} %")
        return None, best_sim

# Örnek kullanım
dosya_yolu = "/home/bitirme/Desktop/bitirme_deneme/Giris_Sesi_Bitirme.wav"
sesi_dogrula(dosya_yolu)
