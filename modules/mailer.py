import os         # Sistem ve dosya yolları paketi
import sys        # Proje klasörünü arama listesine ekleme paketi
import smtplib    # E-posta göndermemizi sağlayan standart Python mektup taşıyıcısı
from email.mime.multipart import MIMEMultipart  # HTML ve metin içerikli zengin e-posta yapısı
from email.mime.text import MIMEText           # E-posta metin gövdesi oluşturucu
from email.header import Header                # Türkçe karakterli başlıklar için
from email.utils import formataddr             # E-posta adresini doğru formatlamak için
from datetime import datetime                 # Güncel tarihi almak için zaman paketi

# Ana proje klasörünü Python'ın arama listesine ekliyoruz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv  # Gizli şifreleri okuma paketi

# .env dosyasındaki bilgileri yüklüyoruz
load_dotenv()

def send_newsletter(html_content):
    """
    Hazırlanan HTML bülten içeriğini Gmail SMTP sunucusu üzerinden alıcı adresine gönderir.
    """
    sender_email = os.getenv("SENDER_EMAIL")          # Gönderen Gmail adresi
    app_password = os.getenv("GMAIL_APP_PASSWORD")    # 16 haneli Gmail uygulama şifresi
    receiver_email = os.getenv("RECEIVER_EMAIL")      # Alıcı e-posta adresi

    if not sender_email or not app_password or not receiver_email:
        print("Hata: .env dosyasındaki e-posta bilgileri eksik!")
        return False

    # Bugünün tarihini Türkçe formatında alıyoruz
    today_str = datetime.now().strftime("%d.%m.%Y")
    subject = f"Günlük Teknoloji Haber Bülteni - {today_str}"

    # E-posta mesajı (Zarf) nesnemizi oluşturuyoruz
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    
    # Türkçe karakterleri UTF-8 ile paketleyip gönderen adını sabitliyoruz
    message["From"] = formataddr((str(Header("Günlük Teknoloji Bültenim", "utf-8")), sender_email))
    message["To"] = receiver_email

    # HTML içeriği e-posta zarfına ekliyoruz
    html_part = MIMEText(html_content, "html", "utf-8")
    message.attach(html_part)

    try:
        print("Gmail SMTP sunucusuna bağlanılıyor ve e-posta gönderiliyor...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            
        print("Bülten başarıyla Gmail adresinize gönderildi!")
        return True

    except Exception as error:
        print(f"E-posta gönderilirken hata oluştu: {error}")
        return False


if __name__ == "__main__":
    test_html = "<h1>Teknoloji Bülteni Testi</h1><p>Bu bir test e-postasıdır.</p>"
    send_newsletter(test_html)
