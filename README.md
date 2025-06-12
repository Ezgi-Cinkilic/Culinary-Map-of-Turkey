# 🇹🇷 Türkiye'nin Dijital Lezzet Haritası 🍲

## 📌 Proje Tanımı

Bu proje, **tarif paylaşım platformlarından elde edilen verilerle Türkiye’nin il bazlı dijital yemek haritasını oluşturmayı** amaçlamaktadır. Nefis Yemek Tarifleri platformundaki tarif ve kullanıcı verileri kullanılarak, **bölgelere özgü yemek türleri**, **yöresel mutfak farklılıkları** ve **lezzet yoğunlukları** analiz edilecektir.

Amaç, Türkiye genelinde tariflerin türlerine göre nasıl bir dağılım gösterdiğini **veri madenciliği**, **coğrafi veri analizi** ve **görselleştirme** yöntemleriyle ortaya koymaktır.

---

## ❓ Araştırma Soruları

- Türkiye'nin farklı illerinde en sık paylaşılan yemek türleri nelerdir?  
- Belirli yemek kategorileri bazı illerde ya da bölgelerde mi yoğunlaşmıştır?  
- Kümelenmiş veriyle "Türkiye Lezzet Bölgeleri" tanımlanabilir mi?  
- Malzeme ve içerik bazlı olarak bölgesel mutfak farklılıkları tespit edilebilir mi?

---

## 🎯 Hedefler

- Tarif kategorilerinin iller bazında dağılımını analiz etmek  
- Belirli yemek türlerinin yöresel yoğunluğunu görselleştirmek  
- **Kümeleme algoritmaları** ile Türkiye lezzet bölgeleri tanımlamak  
- Tarif içerikleri ve malzemeler üzerinden bölgesel mutfak farklarını incelemek  
- Türkiye’nin **veriye dayalı dijital yemek haritasını** oluşturmak  

---

## 🧩 Yöntemler ve Araçlar

**Veri Toplama**  
- `Web Scraping` (BeautifulSoup)  
- Hedef site: [Nefis Yemek Tarifleri](https://www.nefisyemektarifleri.com/tarifler/)

**Veri Temizleme ve Ön İşleme**  
- Etiket/Kategori standardizasyonu  
- One-Hot Encoding  
- Malzeme listesi işleme  
- İl bilgisi eşleme

**Analiz ve Görselleştirme**  
- `GeoPandas`, `Folium` → Harita çizimleri  
- `Matplotlib`, `Seaborn` → Grafikler  
- `Choropleth Map` → Bölgesel yoğunluk gösterimi  
- `TF-IDF`, `Bag-of-Words`, `Bag-of-Ingredients` → Metin/malzeme analizi

**Makine Öğrenmesi**  
- `K-Means`, `Hiyerarşik Kümeleme` → Bölgesel kümeleme  
- (Opsiyonel) `XGBoost`, `Neural Networks` → Supervised modeller ile malzeme-tarif analizi

---

## 📊 Elde Edilecek Veriler

### Tarif Sayfası  
- Tarif Başlığı  
- Kategori ve Etiketler  
- Malzemeler ve miktarlar  
- Pişirme / Hazırlık süreleri  
- Porsiyon sayısı  
- Tarif açıklaması  
- Yorumlar ve puanlar  
- Tarif görselleri  

### Kullanıcı Profil Sayfası  
- Kullanıcı adı  
- Katılım tarihi  
- Toplam tarif sayısı  
- Takipçi sayısı  
- Yaşanılan şehir  
- Paylaşılan tarif listesi  

---


## 🗓 Zaman Çizelgesi

| Tarih Aralığı             | Yapılacak İş                                    |
|---------------------------|-------------------------------------------------|
| 31 Mayıs – 17 Haziran     | Literatür taraması ve veri toplama              |
| 18 Haziran – 24 Haziran   | Veri ön işleme                                  |
| 25 Haziran – 30 Haziran   | Veri analizi ve temel görselleştirme            |
| 01 Temmuz – 14 Temmuz     | Metotların uygulanması (K-Means vb.)            |
| 15 Temmuz – 20 Temmuz     | Sonuçların analizi ve sunum hazırlığı           |
| 21 veya 24 Temmuz         | Sözlü sunum                                     |
| 22 Temmuz – 29 Temmuz     | Rapor yazımı                                    |
| 31 Temmuz                 | Final rapor teslimi                             |

---

Herhangi bir soru, öneri ya da iş birliği için benimle iletişime geçebilirsiniz.  
Teşekkürler! 🙌