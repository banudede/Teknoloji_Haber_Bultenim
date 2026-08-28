"""
Ne İşe Yarar: Projenin şefi/orkestra şefidir.Sırasıyla haberleri toplar, 
Gemini'a gönderip bülten oluşturur ve e-posta olarak kutuna atar.
"""

import sys  # Sistem işlevleri paketi
import os   # Dosya ve dizin yönetimi paketi

# Modüllerimizi içe aktarıyoruz (diğer dosyalardan fonksiyonları çağırıyoruz)
from modules.scraper import fetch_latest_news
from modules.summarizer import generate_newsletter_html
from modules.mailer import send_newsletter

def run_pipeline():
    """
    Tüm bülten sürecini baştan sona çalıştıran ana orkestra fonksiyonu.
    (Haberleri topla -> Gemini ile özetle -> E-posta at)
    """
    print("=== GÜNLÜK TEKNOLOJİ HABER BÜLTENİ OTOMASYONU BAŞLADI ===")

    # 1. Adım: Haber kaynaklarından güncel verileri topla
    news_items = fetch_latest_news()
    if not news_items:
        print("Hata: Hiç haber toplanamadı. Süreç durduruluyor.")
        return

    # 2. Adım: Gemini API ile haberleri Türkçe HTML bülten haline getir
    html_newsletter = generate_newsletter_html(news_items)
    if not html_newsletter:
        print("Hata: Yapay zeka bülteni oluşturamadı. Süreç durduruluyor.")
        return

    # 3. Adım: Bülteni Gmail üzerinden alıcıya postala
    is_sent = send_newsletter(html_newsletter)
    if is_sent:
        print("=== BÜLTEN BAŞARIYLA TAMAMLANTI VE GÖNDERİLDİ ===")
    else:
        print("Hata: Bülten e-posta ile gönderilemedi.")

if __name__ == "__main__":
    run_pipeline()
