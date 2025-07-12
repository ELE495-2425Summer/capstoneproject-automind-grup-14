import openai # OpenAI kütüphanesi çağrılır
import os # İşletim sistemi ile ilgili işlemler için os modülü çağrılır
import subprocess

api_anahtar = "anahtar" # OpenAI API anahtarı tanımlanır
openai.api_key = api_anahtar # API anahtarı global olarak ayarlanır
openAI_TTS = openai.OpenAI(api_key = api_anahtar) # TTS (Text-To-Speech) işlemleri için istemci nesnesi oluşturulur

def TTS_api(metin): # Metni ses dosyasına çeviren fonksiyon
    chatgpt_cevap_sesli = openAI_TTS.audio.speech.create    ( # OpenAI TTS servisine gönderilir
                                                                model = "tts-1", # Kullanılacak TTS modeli seçilir
                                                                voice = "nova", # Seslendirme seçilir
                                                                input = metin # Seslendirilecek metin seçilir
                                                            )
    
    with open("chatgpt_cevap_sesli.mp3", "wb") as f: # Ses dosyası kaydedilir
        f.write(chatgpt_cevap_sesli.content) # İçerik dosyaya yazılır
    
    os.system("mpg123 chatgpt_cevap_sesli.mp3") # mp3 dosyası oynatılır

if __name__ == "__main__": # Dosya doğrudan çalıştırıldığında

    with open("text_to_speech.txt", "r", encoding = "utf-8") as f: # ChatGPT cevabı dosyadan okunur
        chatgpt_cevap = f.read() # Dosya içeriğindeki metin alınır
    
    TTS_api(chatgpt_cevap) # Metin, ses dosyasına çeviren fonksiyona gönderilir

    try: 
        with open('motor_surucu.py', 'r') as file:
            code = file.read()

        exec(code)

        print("motor_surucu.py başlatıldı")
    except Exception as e:
        print(f"motor_surucu.py başlatılamadı: {e}")