

"""
Ne İşe Yarar: config.py dosyasında tanımladığımız 10 farklı dev teknoloji sitesini tek tek gezer. 
En son yayınlanan başlıkları ve özet içerikleri toplayıp bize derli toplu bir liste halinde verir.



"""





import sys  # Sistem ayarlarını yöneten Python paketi (klasör yollarını ayarlamak için)
import os   # Dosya ve klasör yollarını bulmamızı sağlayan paket

# Ana proje klasörünü Python'ın arama listesine ekliyoruz (config.py dosyasını bulabilsin diye)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import feedparser  # RSS haber akışlarını okumamızı sağlayan paket
from config import RSS_FEEDS, MAX_NEWS_COUNT  # Ayar dosyamızdan linkleri ve sınır sayısını aldık

def fetch_latest_news():
    """
    Belirtilen RSS kaynaklarını gezer ve en güncel haber başlıkları ile içeriklerini toplar.
    (Haber kaynaklarını tek tek dolaşıp son haberleri alet çantamıza toplama işi yapar)
    """
    collected_news = []  # Topladığımız haberleri koyacağımız boş bir haber sepeti
    
    print("Haber kaynakları taranıyor...")
    
    for feed_url in RSS_FEEDS:
        try:
            # RSS linkine bağlanıp haberleri okuyoruz
            parsed_feed = feedparser.parse(feed_url)
            
            # Kaynakta haber varsa ilk/en güncel haberi alıyoruz
            if parsed_feed.entries:
                first_entry = parsed_feed.entries[0]
                
                # Haberin başlığını ve kısa özetini/içeriğini alıyoruz
                title = first_entry.get("title", "Başlık Bulunamadı")
                description = first_entry.get("summary", first_entry.get("description", ""))
                link = first_entry.get("link", "")
                
                # Haber bilgisini düzenli bir paket yapıp sepetimize atıyoruz
                news_item = {
                    "title": title,
                    "description": description,
                    "link": link,
                    "source": parsed_feed.feed.get("title", "Teknoloji Kaynağı")
                }
                collected_news.append(news_item)
                
                # İstenen maksimum haber sayısına ulaştıysak döngüyü bitiriyoruz
                if len(collected_news) >= MAX_NEWS_COUNT:
                    break
                    
        except Exception as error:
            # Bir kaynakta sorun çıkarsa program durmasın, hatayı ekrana yazıp diğer kaynağa geçsin
            print(f"Haber çekilirken bir hata oluştu ({feed_url}): {error}")

    print(f"Toplam {len(collected_news)} adet haber başarıyla toplandı.")
    return collected_news


# Modülü kendi içinde tek başına test etmek için küçük bir kontrol bloğu
if __name__ == "__main__":
    news = fetch_latest_news()
    for item in news:
        print(f"- {item['title']} ({item['source']})")
