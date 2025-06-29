import pandas as pd
import unicodedata
import folium
import json
import matplotlib.pyplot as plt
from pandas.plotting import table

# === 1. Yardımcı Fonksiyonlar ===

def normalize_text(text):
    if pd.isna(text):
        return None
    return unicodedata.normalize('NFC', text).strip().lower()

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

# === 2. Şehir listesi (GeoJSON ile uyumlu) ===
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
    'Tunceli', 'Uşak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak'
]
geojson_iller_map = {normalize_text(il): il for il in geojson_iller}

def duzelt_il(isim):
    if isim is None:
        return None
    if 'yurt disi' in isim or 'yurtdisi' in isim or isim in ['yurtdisi', 'bilinmiyor', 'diğer', 'diger']:
        return None
    return geojson_iller_map.get(isim, None)

# === 3. Verileri oku ===
profiles_df = pd.read_csv('../datas/profiles.csv')
recipes_df = pd.read_csv('../datas/recipes_combined.csv')

# === 4. Normalize işlemleri ===
profiles_df['sehir_normalize'] = profiles_df['sehir'].apply(normalize_text)
profiles_df['sehir_geojson'] = profiles_df['sehir_normalize'].apply(duzelt_il)
profiles_df['profil_adi_normalize'] = profiles_df['profil_adi'].apply(normalize_text)
recipes_df['profil_adi_normalize'] = recipes_df['profil_adi'].apply(normalize_text)

# === 5. Merge işlemi ===
merged_df = recipes_df.merge(
    profiles_df[['profil_adi_normalize', 'sehir_geojson']],
    on='profil_adi_normalize',
    how='left'
)

# === 6. Kullanıcı ve Tarif Sayısı ===
profiles_df_filtered = profiles_df[profiles_df['sehir_geojson'].notna()]
kullanici_counts = profiles_df_filtered['sehir_geojson'].value_counts().reset_index()
kullanici_counts.columns = ['il', 'kullanici_sayisi']

tarif_counts = merged_df['sehir_geojson'].value_counts().reset_index()
tarif_counts.columns = ['il', 'tarif_sayisi']

sehir_counts = kullanici_counts.merge(tarif_counts, on='il', how='left')
sehir_counts['tarif_sayisi'] = sehir_counts['tarif_sayisi'].fillna(0).astype(int)

# === 7. Toplam satırı ekle ===
total_row = pd.DataFrame({
    'il': ['Toplam'],
    'kullanici_sayisi': [sehir_counts['kullanici_sayisi'].sum()],
    'tarif_sayisi': [sehir_counts['tarif_sayisi'].sum()]
})
sehir_counts_with_total = pd.concat([sehir_counts, total_row], ignore_index=True)

# === 8. PNG Tablo Kaydet ===
fig, ax = plt.subplots(figsize=(10, len(sehir_counts_with_total) * 0.4))
ax.axis('off')
tbl = table(ax, sehir_counts_with_total, loc='center', cellLoc='center', colWidths=[0.3]*3)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.5)
plt.tight_layout()
plt.savefig('../sehir_kullanicilar_tarifler_tablosu.png', dpi=300)
print("📊 Tablo başarıyla kaydedildi: sehir_kullanicilar_tarifler_tablosu.png")

# === 9. Harita ===
with open('../tr-cities-utf8.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

kullanici_dict = dict(zip(sehir_counts['il'], sehir_counts['kullanici_sayisi']))
tarif_dict = dict(zip(sehir_counts['il'], sehir_counts['tarif_sayisi']))

for feature in geojson_data['features']:
    il_adi = feature['properties']['name']
    feature['properties']['kullanici_sayisi'] = kullanici_dict.get(il_adi, 0)
    feature['properties']['tarif_sayisi'] = tarif_dict.get(il_adi, 0)

turkey_map = folium.Map(location=[39.0, 35.0], zoom_start=6)

choropleth = folium.Choropleth(
    geo_data=geojson_data,
    name='İl Bazlı Kullanıcı ve Tarif Yoğunluğu',
    data=sehir_counts,
    columns=['il', 'kullanici_sayisi', 'tarif_sayisi'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    nan_fill_color='white',
    legend_name='Şehir Bazlı Kullanıcı Sayısı',
    highlight=True
).add_to(turkey_map)

tooltip = folium.GeoJsonTooltip(
    fields=['name', 'kullanici_sayisi', 'tarif_sayisi'],
    aliases=['Şehir Adı:', 'Kullanıcı Sayısı:', 'Tarif Sayısı:'],
    localize=True,
    sticky=True
)
choropleth.geojson.add_child(tooltip)
folium.LayerControl().add_to(turkey_map)
turkey_map.save('../turkiye_il_kullanicilar.html')
print("🗺️ Harita başarıyla kaydedildi: türkiye_il_kullanıcılar.png")