import pandas as pd
import folium
import json
from folium.features import GeoJsonTooltip

# Verileri yükle
df = pd.read_csv('..//datas//CullinaryMapDataset.csv')
with open('..//tr-cities-utf8.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Verileri hazırla
df['il'] = df['eslesen_sehir']  # Sütun adını kontrol edin

# Metrikleri hesapla
kullanici_sayilari = df.groupby('il')['profil_adi'].nunique().to_dict()
tarif_sayilari = df['il'].value_counts().to_dict()

# GeoJSON'a verileri ekle
for feature in geojson_data['features']:
    il_adi = feature['properties']['name']
    feature['properties']['kullanici'] = kullanici_sayilari.get(il_adi, 0)
    feature['properties']['tarif'] = tarif_sayilari.get(il_adi, 0)

# Haritayı oluştur
m = folium.Map(location=[39, 35], zoom_start=6, tiles='cartodbpositron')

# 1. KATMAN: Kullanıcı Dağılımı (Kırmızı tonları)
kullanici_colormap = folium.LinearColormap(
    ['#ffebee', '#c62828'],
    vmin=min(kullanici_sayilari.values()),
    vmax=max(kullanici_sayilari.values())
)


def kullanici_style(feature):
    return {
        'fillColor': kullanici_colormap(feature['properties']['kullanici']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }


kullanici_layer = folium.GeoJson(
    geojson_data,
    name='Kullanıcı Sayısı',
    style_function=kullanici_style,
    tooltip=GeoJsonTooltip(
        fields=['name', 'kullanici', 'tarif'],
        aliases=['Şehir:', 'Kullanıcı Sayısı:', 'Tarif Sayısı:'],
        localize=True,
        sticky=True,
        styles="""
            background-color: white;
            border: 1px solid black;
            border-radius: 3px;
            padding: 5px;
            font-size: 14px;
        """
    )
).add_to(m)

# 2. KATMAN: Tarif Dağılımı (Mavi tonları)
tarif_colormap = folium.LinearColormap(
    ['#e3f2fd', '#1565c0'],
    vmin=min(tarif_sayilari.values()),
    vmax=max(tarif_sayilari.values())
)


def tarif_style(feature):
    return {
        'fillColor': tarif_colormap(feature['properties']['tarif']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }


tarif_layer = folium.GeoJson(
    geojson_data,
    name='Tarif Sayısı',
    style_function=tarif_style,
    show=False  # Başlangıçta gizli
).add_to(m)

# Katman kontrol paneli
folium.LayerControl(collapsed=False).add_to(m)

# Çift renk skalalı lejant ekle
m.get_root().html.add_child(folium.Element('''
<style>
    #legend {
        position: fixed;
        bottom: 50px;
        left: 50px;
        z-index: 1000;
        padding: 10px;
        background: white;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.2);
        max-width: 200px;
    }
    .legend-item {
        margin-bottom: 10px;
    }
    .legend-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
</style>

<div id="legend">
    <div class="legend-item">
        <div class="legend-title">Kullanıcı Sayısı</div>
        ''' + kullanici_colormap._repr_html_() + '''
    </div>
    <div class="legend-item">
        <div class="legend-title">Tarif Sayısı</div>
        ''' + tarif_colormap._repr_html_() + '''
    </div>
</div>
'''))

m.save('..//turkiye_kullanici_tarif_haritasi.html')
print("Harita başarıyla oluşturuldu!")