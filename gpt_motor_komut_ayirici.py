import subprocess
# Dosya adları
input_file = "chatgpt_cevap.txt"
text_file = "text_to_speech.txt"
json_file = "motor_commands.txt"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# '***' işaretine göre ayır
parts = content.split('***')

if len(parts) < 2:
    print("Ayırma için *** işareti bulunamadı.")
else:
    # İlk kısmı temizle ve dosyaya yaz
    text_part = parts[0].strip()
    with open(text_file, "w", encoding="utf-8") as f_text:
        f_text.write(text_part)
    
    # İkinci kısım JSON komutları (string halinde)
    json_part = parts[1].strip()

    # Bazı durumlarda JSON formatı tırnakları ' yerine " olabilir. 
    # Eğer gerekirse düzelt:
    json_part = json_part.replace("'", "\"")

    with open(json_file, "w", encoding="utf-8") as f_json:
        f_json.write(json_part)

    print(f"Metin '{text_file}' dosyasına, JSON komutları '{json_file}' dosyasına yazıldı.")

    try: 
        subprocess.Popen(['python', 'openai_tts.py'])
        print("openai_tts.py başlatıldı")
    except Exception as e:
        print(f"openai_tts.py başlatılamadı: {e}")
