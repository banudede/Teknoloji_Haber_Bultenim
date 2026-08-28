"""
Ne İşe Yarar: .env dosyasındaki Gmail bilgilerinizi kullanarak güvenli bir 
bağlantı (SSL/TLS) kurar ve hazırlanan HTML bültenini doğrudan gelen kutunuza gönderir.

"""

import os         # Sistem ve dosya yolları paketi
import sys        # Proje klasörünü arama listesine ekleme paketi
import smtplib    # E-posta göndermemizi sağlayan standart Python mektup taşıyıcısı
from email.mime.multipart import MIMEMultipart  # HTML ve metin içerikli zengin e-posta yapısı
from email.mime.text import MIMEText           # E-posta metin gövdesi oluşturucu
from datetime import datetime                 # Güncel tarihi almak için zaman paketi

# Ana proje klasörünü Python'ın arama listesine ekliyoruz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv  # Gizli şifreleri okuma paketi

# .env dosyasındaki bilgileri yüklüyoruz
load_dotenv()

def send_newsletter(html_content):
    """
    Hazırlanan HTML bülten içeriğini Gmail SMTP sunucusu üzerinden alıcı adresine gönderir.
    (Dijital mektubu zarfa koyup Gmail postanesinden adrese teslim etme işi yapar)
    """
    sender_email = os.getenv("SENDER_EMAIL")          # Gönderen Gmail adresi
    app_password = os.getenv("GMAIL_APP_PASSWORD")    # 16 haneli Gmail uygulama şifresi
    receiver_email = os.getenv("RECEIVER_EMAIL")      # Alıcı e-posta adresi

    if not sender_email or not app_password or not receiver_email:
        print("Hata: .env dosyasındaki e-posta bilgileri eksik!")
        return False

    # Bugünün tarihini Türkçe formatında alıyoruz (Örn: 28.08.2026)
    today_str = datetime.now().strftime("%d.%m.%Y")
    subject = f" Günlük Teknoloji Haber Bülteni - {today_str}"

    # E-posta mesajı (Zarf) nesnemizi oluşturuyoruz
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"Teknoloji Bülteni <{sender_email}>"
    message["To"] = receiver_email

    # HTML içeriği e-posta zarfına ekliyoruz
    html_part = MIMEText(html_content, "html", "utf-8")
    message.attach(html_part)

    try:
        print("Gmail SMTP sunucusuna bağlanılıyor ve e-posta gönderiliyor...")
        # Gmail SMTP sunucusuna güvenli port olan 465 ile bağlanıyoruz
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)             # Hesaba giriş yapıyoruz
            server.sendmail(sender_email, receiver_email, message.as_string())  # Mektubu atıyoruz
            
        print(" Bülten başarıyla Gmail adresinize gönderildi!")
        return True

    except Exception as error:
        print(f"E-posta gönderilirken hata oluştu: {error}")
        return False


# Modülü kendi içinde tek başına test etmek için kontrol bloğu
if __name__ == "__main__":
    test_html = "<h1>Teknoloji Bülteni Testi</h1><p>Bu bir test e-postasıdır.</p>"
    send_newsletter(test_html)
