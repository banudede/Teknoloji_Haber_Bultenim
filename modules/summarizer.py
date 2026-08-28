
"""
Ne İşe Yarar: Haber listesini alır, Gemini AI modeline akıllı 
bir talimat (prompt) gönderir ve e-postaya yapıştırmaya hazır, şık bir HTML bülteni üretir.
"""

import os   # Dosya ve sistem yollarını bulma paketi
import sys  # Proje klasörlerini tanımlama paketi

# Ana proje klasörünü Python'ın arama listesine ekliyoruz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv  # .env dosyasındaki gizli şifreleri okuma paketi
from google import genai       # Google Gemini yapay zeka kütüphanesi

# .env dosyasındaki API anahtarını hafızaya yüklüyoruz
load_dotenv(override=False)

# Gemini istemcisini (AI bağlantısını) API anahtarımızla başlatıyoruz
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_newsletter_html(news_list):
    """
    Toplanan haber listesini alıp Gemini API ile Türkçe ve şık bir HTML bültenine dönüştürür.
    (Haberleri yapay zekaya verip harika bir gazete sayfası tasarlatma işi yapar)
    """
    print("Haberler Gemini API ile Türkçe bülten haline getiriliyor...")

    # Yapay zekaya haberleri nasıl işlemesi gerektiğini söyleriz (Prompt / Talimat metni)
    prompt_instruction = """
Sen uzman bir teknoloji editörüsün. Sana verilen teknoloji haberlerini incele ve profesyonel, 
akademik bir titizlikte, sade, son derece anlaşılır Türkçe bir e-posta bülteni (HTML formatında) hazırla.

Şu kurallara KESİNLİKLE uy:
1. Çıktı SADECE geçerli bir HTML kütüphanesi/gövdesi olmalı. ```html veya başka açıklama metinleri EKLEME.
2. Bültenin en üstünde (Header) ana başlık olarak SADECE "Teknoloji Haber Bültenim" yaz. Bu ana başlığın altına veya üstüne KESİNLİKLE rastgele slogan, alt başlık veya ekstra açıklama ekleme.
3. Her haber için şık bir kart tasarımı oluştur.
4. Paragraflar arasında göz yormayan, ferah boşluklar (padding/margin) bırak.
5. Haberlerin kendi orijinal başlıklarını net ve dikkat çekici Türkçe başlıklar olarak koru.
6. Her haberin altında kaynağın adı ve orijinal habere giden şık bir tıklanabilir link (Devamını Oku) bulunsun.
7. Tasarımda modern ve temiz renkler (koyu mavi, gri, beyaz tonları) kullan.

Sana verilen haber verileri:
"""
    # Haber listesini yapay zekanın anlayacağı metin formatına çeviriyoruz
    for index, item in enumerate(news_list, 1):
        prompt_instruction += f"\n--- HABER {index} ---\n"
        prompt_instruction += f"Orijinal Başlık: {item['title']}\n"
        prompt_instruction += f"Kaynak: {item['source']}\n"
        prompt_instruction += f"Özet/İçerik: {item['description']}\n"
        prompt_instruction += f"Link: {item['link']}\n"

    try:
        # Gemini modeline isteğimizi gönderiyoruz (yeni SDK ile uyumlu gemini-2.0-flash)
        response = gemini_client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt_instruction,
        )
        
        # Yapay zekanın ürettiği HTML kodunu alıyoruz
        html_content = response.text.strip()
        
        # Eğer yapay zeka kod bloğu işaretleri koyduysa temizliyoruz
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        if html_content.startswith("```"):
            html_content = html_content[3:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]

        return html_content.strip()

    except Exception as error:
        print(f"Gemini API ile bülten oluşturulurken hata oluştu: {error}")
        return None


# Modülü kendi içinde tek başına test etmek için kontrol bloğu
if __name__ == "__main__":
    from modules.scraper import fetch_latest_news
    
    sample_news = fetch_latest_news()
    if sample_news:
        html_result = generate_newsletter_html(sample_news[:2])  # Test için sadece 2 haber gönderiyoruz
        print("\n--- ÜRETİLEN HTML ÖRNEĞİ (İLK 300 KARAKTER) ---")
        print(html_result[:300] if html_result else "HTML üretilemedi!")
