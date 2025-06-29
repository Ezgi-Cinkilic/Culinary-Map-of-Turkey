import pandas as pd
import folium
import json

# 1. Şehir normalizasyon fonksiyonu
def normalize_sehir(sehir):
    if pd.isna(sehir):
        return None
    sehir = sehir.strip().lower()
    replacements = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'â': 'a', 'î': 'i', 'û': 'u'
    }
    for turkce, ascii_karsilik in replacements.items():
        sehir = sehir.replace(turkce, ascii_karsilik)
    return sehir

# 2. Türkçe normalizasyon eşleme tablosu
il_listesi = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın",
    "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa",
    "Çanakkale", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir",
    "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir",
    "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir",
    "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir",
    "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak",
    "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"
]

normalize_to_original = {normalize_sehir(il): il for il in il_listesi}

# 3. Veriyi oku
profiles_df = pd.read_csv('../datas/profiles.csv')
profiles_df['sehir_normalize'] = profiles_df['sehir'].apply(normalize_sehir)

# 4. Kullanıcı sayısını hesapla
sehir_counts = profiles_df['sehir_normalize'].dropna().value_counts().reset_index()
sehir_counts.columns = ['sehir_normalize', 'kullanici_sayisi']

# 5. Orijinal şehir adlarını ekle (GeoJSON ile uyumlu)
sehir_counts['il'] = sehir_counts['sehir_normalize'].map(normalize_to_original)
sehir_counts = sehir_counts.dropna(subset=['il'])  # eşleşemeyen şehirleri at

# 6. GeoJSON dosyasını oku
with open('../tr-cities-utf8.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 7. Harita oluştur
turkey_map = folium.Map(location=[39.0, 35.0], zoom_start=6)

kullanici_dict = dict(zip(sehir_counts['il'], sehir_counts['kullanici_sayisi']))
for feature in geojson_data['features']:
    il_adi = feature['properties']['name']
    feature['properties']['kullanici_sayisi'] = kullanici_dict.get(il_adi, 0)  # yoksa 0

# Choropleth ekleme
choropleth = folium.Choropleth(
    geo_data=geojson_data,
    name='İl Bazlı Kullanıcı Yoğunluğu',
    data=sehir_counts,
    columns=['il', 'kullanici_sayisi'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    nan_fill_color='white',
    legend_name='Şehir Bazlı Kullanıcı Sayısı',
    highlight=True
).add_to(turkey_map)

# Tooltip ile kullanıcı sayısını göster
folium.features.GeoJsonTooltip(
    fields=['name'],
    aliases=['İl:'],
    labels=True,
    sticky=True
).add_to(choropleth.geojson)



# Tooltip ayarları: hem il adı hem kullanıcı sayısını göster
tooltip = folium.features.GeoJsonTooltip(
    fields=['name', 'kullanici_sayisi'],
    aliases=['İl:', 'Kullanıcı Sayısı:'],
    localize=True,
    sticky=True,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 1px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
)

choropleth.geojson.add_child(tooltip)

# 8. Kaydet
turkey_map.save('../turkiye_il_kullanicilar.html')
print("✅ Harita başarıyla oluşturuldu: turkiye_il_kullanicilar.html")

# GeoJSON'daki şehir isimleri
geojson_iller = set([feature['properties']['name'] for feature in geojson_data['features']])

# Kullanıcı şehirleri
kullanici_iller = set(profiles_df['sehir_normalize'].dropna().unique())

# GeoJSON'da olmayan şehirler
farkli_iller = kullanici_iller - geojson_iller

print(f"GeoJSON'da olmayan şehirler: {farkli_iller}")

import pandas as pd
import unicodedata

# 1. Unicode normalizasyon ve küçük harfe çevirme fonksiyonu
def normalize_unicode(text):
    if pd.isna(text):
        return None
    text = unicodedata.normalize('NFC', text)
    return text.strip().lower()

profiles_df['sehir_normalize'] = profiles_df['sehir'].apply(normalize_unicode)

# 2. GeoJSON şehir isimleri (doğru ve büyük harfli halleri)
geojson_iller = [
    'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Aksaray', 'Amasya', 'Ankara',
    'Antalya', 'Ardahan', 'Artvin', 'Aydın', 'Balıkesir', 'Bartın', 'Batman', 'Bayburt',
    'Bilecik', 'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı',
    'Çorum', 'Denizli', 'Diyarbakır', 'Düzce', 'Edirne', 'Elazığ', 'Erzincan', 'Erzurum',
    'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkari', 'Hatay', 'Iğdır', 'Isparta',
    'İstanbul', 'İzmir', 'Kahramanmaraş', 'Karabük', 'Karaman', 'Kastamonu', 'Kayseri',
    'Kırıkkale', 'Kırklareli', 'Kocaeli', 'Konya', 'Kütahya', 'Malatya', 'Manisa', 'Mardin',
    'Mersin', 'Muğla', 'Muş', 'Nevşehir', 'Niğde', 'Ordu', 'Osmaniye', 'Rize', 'Sakarya',
    'Samsun', 'Siirt', 'Sinop', 'Sivas', 'Şanlıurfa', 'Şırnak', 'Tekirdağ', 'Tokat', 'Trabzon',
    'Tunceli', 'Uşak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak', 'Kıbrıs'
]

# 3. Küçük harfli ve Unicode normalize edilmiş hali ile sözlük oluştur
geojson_iller_map = {unicodedata.normalize('NFC', il).lower(): il for il in geojson_iller}

# 4. Elimizdeki normalize şehir isimlerini GeoJSON uyumlu hale getir
def duzelt_il(isim):
    if isim is None:
        return None
    # Yurt dışı, bilinmeyen gibi girdileri None yap
    if 'yurt disi' in isim or 'yurtdisi' in isim or isim in ['yurtdisi', 'bilinmiyor', 'diğer', 'diger']:
        return None
    # Düzeltme sözlüğü ile eşleştirme yoksa isim olduğu gibi kalacak
    return geojson_iller_map.get(isim, None)

profiles_df['sehir_geojson'] = profiles_df['sehir_normalize'].apply(duzelt_il)

# GeoJSON ile eşleşenleri filtrele
profiles_df_filtered = profiles_df[profiles_df['sehir_geojson'].notna()]

# Kullanıcı sayısını hesapla
sehir_counts = profiles_df_filtered['sehir_geojson'].value_counts().reset_index()
recipes_df = pd.read_csv('../datas/recipes_combined.csv')
sehir_counts.columns = ['il', 'kullanici_sayisi']

print(sehir_counts)