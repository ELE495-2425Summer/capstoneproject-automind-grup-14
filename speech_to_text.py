import openai # OpenAI kütüphanesi çağrılır
from openai import OpenAI # OpenAI istemci sınıfı içe aktarılır
import os # İşletim sistemi ile ilgili işlemler için os modülü çağrılır
import subprocess

api_anahtar = "anahtar" # OpenAI API anahtarı tanımlanır
openAI_STT = OpenAI(api_key = api_anahtar) # STT (Speech-To-Text) işlemleri için istemci nesnesi oluşturulur

with open("Giris_Sesi_Bitirme.wav", "rb") as audio_file: # Ses kaydı dosyası okunur
    metin = openAI_STT.audio.transcriptions.create ( # OpenAI STT servisine gönderilir
                                                    model = "whisper-1", # Kullanılacak STT modeli seçilir
                                                    file = audio_file, # Kullanılacak ses dosyası seçilir
                                                    language = "tr" # Dil Türkçe olarak seçilir
                                                )

print("Algılanan metin:", metin.text) # Algılanan metin ekrana yazdırılır

with open("algilanan_metin.txt", "w", encoding = "utf-8") as f: # Algılanan metin dosyaya yazılır
    f.write(metin.text)

try: 
    #with open('text_to_gpt.py', 'r') as file:
        #code = file.read()

    #exec(code)
    subprocess.Popen(['python', 'text_to_gpt.py'])
    print("text_to_gpt.py başlatıldı")
except Exception as e:
    print(f"text_to_gpt.py başlatılamadı: {e}")
    