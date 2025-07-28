import pandas as pd
import folium
import json
from copy import deepcopy
from folium.features import GeoJsonTooltip

# Veri ve geojson yükleme
df = pd.read_csv('..//datas//CullinaryMapDataset.csv')
with open('..//tr-cities-utf8.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Tüm alt kategoriler listesi
all_cats = df['alt_kategori'].unique()

# Şehirlerin alt kategorilere göre gruplanması (set olarak)
cat_to_cities = {
    cat: set(df.loc[df["alt_kategori"] == cat, "eslesen_sehir"].unique())
    for cat in all_cats
}

# Türkiye haritası
m = folium.Map(location=[39.0, 35.0], zoom_start=6, tiles='cartodbpositron')

for cat in all_cats:
    geojson_copy = deepcopy(geojson_data)

    for feature in geojson_copy['features']:
        city_name = feature['properties']['name']
        feature['properties']['has_cat'] = city_name in cat_to_cities[cat]

    def style_function(feature):
        if feature['properties']['has_cat']:
            return {
                'fillColor': '#3186cc',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7,
            }
        else:
            return {
                'fillColor': '#f0f0f0',
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.1,
            }

    gj = folium.GeoJson(
        geojson_copy,
        name=cat.replace('-', ' ').title(),
        style_function=style_function,
        tooltip=GeoJsonTooltip(fields=['name', 'has_cat'], aliases=['City:', 'Has Category:']),
        show=False  # Başlangıçta kapalı olsun
    )
    gj.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

m.save('..//graphs//turkey_alt_categories_map_all_cats.html')
print("Harita başarıyla oluşturuldu: turkey_alt_categories_map_all_cats.html")
