import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, formatdate, make_msgid
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

def send_newsletter(html_content):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not sender_email or not app_password or not receiver_email:
        print("Hata: .env dosyasındaki e-posta bilgileri eksik!")
        return False

    today_str = datetime.now().strftime("%d.%m.%Y")
    subject = f"Günlük Teknoloji Haber Bülteni - {today_str}"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = formataddr((str(Header("Günlük Teknoloji Bültenim", "utf-8")), sender_email))
    message["To"] = receiver_email
    
    # GMAIL FILTRESINI GEÇMEK IÇIN EKLEMLER (CRITICAL FIX)
    message["Date"] = formatdate(localtime=True)  # Standart e-posta tarihi
    message["Message-ID"] = make_msgid(domain=sender_email.split('@')[-1])  # Benzersiz e-posta ID'si
    message["Reply-To"] = sender_email

    html_part = MIMEText(html_content, "html", "utf-8")
    message.attach(html_part)

    try:
        print("Gmail SMTP sunucusuna bağlanılıyor ve e-posta gönderiliyor...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, [receiver_email], message.as_string())
            
        print("Bülten başarıyla Gmail adresinize gönderildi!")
        return True

    except Exception as error:
        print(f"E-posta gönderilirken hata oluştu: {error}")
        return False


if __name__ == "__main__":
    test_html = "<h1>Teknoloji Bülteni Testi</h1><p>Bu bir test e-postasıdır.</p>"
    send_newsletter(test_html)
