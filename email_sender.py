import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_bulten_email(html_content):
    sender_email = os.getenv("GMAIL_USER")
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient_email = sender_email  # Bülten kendi e-postana gelecek

    if not sender_email or not app_password:
        print("❌ HATA: .env dosyasında e-posta bilgileri eksik!")
        return

    # E-posta Başlık Yapısı
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "📰 Günlük Teknoloji Haber Bülteni"
    msg['From'] = f"Teknoloji Bültenim <{sender_email}>"
    msg['To'] = recipient_email

    # HTML İçeriğini Bağlama
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    try:
        # Gmail SMTP Bağlantısı
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("🚀 E-posta başarıyla kutuna gönde    except Exception as e:
        print(f"❌ Mail gönderilirken hata oluştu: {e}")

if __name__ == "__main__":
    from news_fetcher import fetch_latest_news
    from ai_summarizer import summarize_and_translate_news

    print("🔄 Test akışı başlatılıyor...")
    news = fetch_latest_news()
    html_bulten = summarize_and_translate_news(news)
    send_bulten_email(html_bulten)
