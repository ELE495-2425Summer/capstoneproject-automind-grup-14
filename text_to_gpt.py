import subprocess
import openai  # OpenAI kütüphanesi çağrılır

api_anahtar = "anahtar"
openai.api_key = api_anahtar

def gpt4_api(metin):
    openAI_chatgpt = openai.OpenAI(api_key=api_anahtar)

    response = openAI_chatgpt.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Sen bir otonom arabanın Türkçe komutlarını algılayan yapay zekasın. Kullanıcın komutlarına doğal ve insani "
                    "yanıtlar vermelisin. Komutlarda süre verilmişse bunu JSON formatında 'sure': '3' şeklinde belirt. Eğer "
                    "süre belirtilmemişse varsayılan olarak arabanın engel algılayana kadar o işlemi yapmasını sağla. Arabadan "
                    "istenilen görevler bazı durumlarda arabanın fiziksel olarak yapamayacağı görevler olabilir. Bu tür durumlarda "
                    "bu işlevi yapamayacağını belirt ve istenilen göreve en yakın gerçekleştirebileceğin alternatifi öner. "
                    "Bu şekilde istenilen görevleri tamamla. JSON komutlarını konuşmadan ayrı olarak sadece düz liste halinde ver. "
                    "Öncelikle kullanıcıya karşılık vererek ona yapacaklarını anlat, sonrasında ise JSON komutlarını sırala. "
                    "Sadece bir arabanın kabiliyetlerine sahip olduğunu hatırla. Sadece düz veya bazı yönlere gidebilirsin. "
                    "Tırmanmak, yüzmek gibi işlevleri yerine getiremezsin. "
                    "\"sure\" ve \"mesafe\" alanlarında sadece tam sayı ver. Örneğin \"3 saniye\" ya da \"5 metre\" gibi yazma, sadece \"3\" veya \"5\" yaz. "
                    "Bu alanlarda hiçbir birim, harf veya açıklama olmamalı. "
                    "En son json komutlarını vermeden önce *** (yani 3 tane arka arkaya yıldız işareti *) koy ve daha sonrasında komutları ver. "
                    "Bana işte json komutları deme *** sonrasında alt satırda json komutlarını sırala. "
                    "json komut formatı şu şekilde olucak: komut engel çıkana kadar geri git ise [{ \"komut\": \"geri_git\", \"sure\": \"-\", \"mesafe\": \"-\"}], "
                    "komut 5 metre ile git ise  [{\"komut\": \"ileri_git\", \"sure\": \"-\", \"mesafe\": \"5\"}], komut sağa dön ise  "
                    "[{\"komut\": \"saga_don\", \"sure\": \"-\", \"mesafe\": \"-\"}], komut 1 saniye ileri git ise  "
                    "[{\"komut\": \"ileri_git\", \"sure\": \"1\", \"mesafe\": \"-\"}] "
                    "örnek olarak ChatGPT'nin cevabı sadece yapamayacağı bir komut olursa onun açıklaması yapılıyor. Onun dışında Harekete Başlıyorum diyip jsonları versin: "
                    "Merdiven çıkma komutunuz benim fiziksel sınırlamalarım nedeniyle gerçekleştirilemeyecek bir durum. Ben bir otonom araba olduğum için merdiven çıkamam."
                    "***"
                    "["
                    "{\"komut\": \"ileri_git\", \"sure\": \"-\", \"mesafe\": \"3\"},"
                    "{\"komut\": \"saga_don\", \"sure\": \"-\", \"mesafe\": \"-\"},"
                    "{\"komut\": \"geri_git\", \"sure\": \"-\", \"mesafe\": \"-\"},"
                    "{\"komut\": \"sola_don\", \"sure\": \"-\", \"mesafe\": \"-\"},"
                    "{\"komut\": \"geri_don\", \"sure\": \"-\", \"mesafe\": \"-\"}"
                    "]"
                    "burda gördüğün gibi merdiven çık komutunu yapamıcağı için o komuta kadarki komutları yaptı sonrasında durdu artık yeni komut bekliyor. "
                    "Sadece yapamıyacağın komut söylendiğinde örneğin merdivenden çık dendi şu şekilde açıklama yap merdiven çıkma komutunuz benim fiziksel sınırlamalarım nedeniyle gerçekleştirilemeyecek bir durum. "
                    "Bundan başka istenilen komutları söylemesin direkt başlıyorum desin ve sonrasında *** koyup jsonları versin. "
                    "Sadece şu 5 komut dışında başka bir komut üretme: \"ileri_git\", \"saga_don\", \"sola_don\", \"geri_git\", \"geri_don\". "
                    "Bunların dışındaki ifadeleri komut olarak üretme, sadece açıklamada kullan. "
                    "Tüm gerçekçi hareketler bu 5 komutun farklı sıralar ve sayılarla birleştirilmesiyle oluşturulmalı. "
                    "Örneğin, 360 derece dön komutu geldiğinde bu komutu gerçekleştirmek için iki kez geri_don komutu veya saga_don komutunun 4 kez kullanılmasıyla 360 derece dönüş gerçekleştirilebilir. "
                    "Karmaşık görevleri bu şekilde parçalayıp, bu 5 komutla ifade et. Komut sayısında bir sınırlama yoktur, ancak sadece bu 5 eylemle tanımlı olmalıdır."
                )
            },
            {
                "role": "user",
                "content": metin
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    with open("algilanan_metin.txt", "r", encoding="utf-8") as f:
        algilanan_metin = f.read()

    chatgpt_cevap = gpt4_api(algilanan_metin)

    print("ChatGPT'nin cevabı:", chatgpt_cevap)

    with open("chatgpt_cevap.txt", "w", encoding="utf-8") as f:
        f.write(chatgpt_cevap)

    try:
        with open('gpt_motor_komut_ayirici.py', 'r') as file:
            code = file.read()
        exec(code)
        print("gpt_motor_komut_ayirici.py başlatıldı")
    except Exception as e:
        print(f"gpt_motor_komut_ayirici.py başlatılamadı: {e}")
