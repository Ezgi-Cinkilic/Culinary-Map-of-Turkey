import pandas as pd
import folium
import json
from folium.features import GeoJsonTooltip
import branca.colormap as cm

# Veri ve GeoJSON dosyalarını oku
df = pd.read_csv('..//datas//CullinaryMapDataset.csv')
with open('..//tr-cities-utf8.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# İl bazında kullanıcı sayısı ve tarif sayısı hesapla
kullanici_sayisi = df.groupby('eslesen_sehir')['profil_adi'].nunique().reset_index()
kullanici_sayisi.columns = ['il', 'kullanici_sayisi']

tarif_sayisi = df['eslesen_sehir'].value_counts().reset_index()
tarif_sayisi.columns = ['il', 'tarif_sayisi']

kullanici_dict = dict(zip(kullanici_sayisi['il'], kullanici_sayisi['kullanici_sayisi']))
tarif_dict = dict(zip(tarif_sayisi['il'], tarif_sayisi['tarif_sayisi']))

kullanici_min, kullanici_max = kullanici_sayisi['kullanici_sayisi'].min(), kullanici_sayisi['kullanici_sayisi'].max()
tarif_min, tarif_max = tarif_sayisi['tarif_sayisi'].min(), tarif_sayisi['tarif_sayisi'].max()

kullanici_colormap = cm.LinearColormap(['white', 'red'], vmin=kullanici_min, vmax=kullanici_max)
tarif_colormap = cm.LinearColormap(['white', 'red'], vmin=tarif_min, vmax=tarif_max)

m = folium.Map(location=[39, 35], zoom_start=6)

# Style fonksiyonları
def style_function_kullanici(feature):
    il = feature['properties']['name']
    val = kullanici_dict.get(il, 0)
    return {
        'fillColor': kullanici_colormap(val),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7
    }

def style_function_tarif(feature):
    il = feature['properties']['name']
    val = tarif_dict.get(il, 0)
    return {
        'fillColor': tarif_colormap(val),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7
    }

# Tooltip formatları (il + sayı)
def tooltip_kullanici(feature):
    il = feature['properties']['name']
    val = kullanici_dict.get(il, 0)
    return f"<b>İl:</b> {il}<br><b>Kullanıcı Sayısı:</b> {val}"

def tooltip_tarif(feature):
    il = feature['properties']['name']
    val = tarif_dict.get(il, 0)
    return f"<b>İl:</b> {il}<br><b>Tarif Sayısı:</b> {val}"

# Kullanıcı katmanı
kullanici_layer = folium.FeatureGroup(name='Kullanıcı Sayısı', show=True)

geojson_kullanici = folium.GeoJson(
    geojson_data,
    style_function=style_function_kullanici,
    tooltip=folium.GeoJsonTooltip(
        fields=[],
        aliases=[],
        labels=False,
        sticky=True,
        localize=True,
        style="background-color: white; font-weight: bold;"
    )
)
# Dinamik tooltip ayarı için JS ile güncelleme yapacağız
geojson_kullanici.add_to(kullanici_layer)
kullanici_layer.add_to(m)

# Tarif katmanı
tarif_layer = folium.FeatureGroup(name='Tarif Sayısı', show=False)

geojson_tarif = folium.GeoJson(
    geojson_data,
    style_function=style_function_tarif,
    tooltip=folium.GeoJsonTooltip(
        fields=[],
        aliases=[],
        labels=False,
        sticky=True,
        localize=True,
        style="background-color: white; font-weight: bold;"
    )
)
geojson_tarif.add_to(tarif_layer)
tarif_layer.add_to(m)

# Colormap'lar (legend)
kullanici_colormap.caption = 'Kullanıcı Sayısı'
kullanici_colormap.add_to(m)

tarif_colormap.caption = 'Tarif Sayısı'
tarif_colormap.add_to(m)

# Layer Control
folium.LayerControl(collapsed=False).add_to(m)

# Dinamik tooltip ve tek katman görünürlüğü için JS kodu

js = f'''
<script>
    // GeoJson feature ları ve veriler
    var kullaniciData = {json.dumps(kullanici_dict)};
    var tarifData = {json.dumps(tarif_dict)};

    // Kullanıcı ve Tarif layer referansları
    var kullaniciLayerName = 'Kullanıcı Sayısı';
    var tarifLayerName = 'Tarif Sayısı';

    // LayerControl inputları (radio gibi yapıldı)
    var inputs = document.querySelectorAll('.leaflet-control-layers-selector');
    inputs.forEach(input => {{
        input.type = 'radio';
        input.name = 'base-map-layer';
    }});

    // Önce tüm katmanları alın
    var layerMap = {{}};
    inputs.forEach(input => {{
        var label = input.nextSibling.textContent.trim();
        layerMap[label] = input;
    }});

    // Harita ve GeoJson'lar
    var map = window.map; // Folium'dan gelen map objesi

    // Katmanları bulmak için Leaflet layerlar
    var allLayers = [];
    map.eachLayer(layer => {{
        if (layer.feature) {{
            allLayers.push(layer);
        }}
    }});

    // Tüm tooltipleri kapat
    function closeAllTooltips() {{
        allLayers.forEach(layer => {{
            layer.unbindTooltip();
        }});
    }}

    // Tooltip gösterme fonksiyonu
    function showTooltip(layer, content) {{
        layer.bindTooltip(content, {{sticky:true, className: "custom-tooltip"}}).openTooltip();
    }}

    // Her feature için tooltip ayarla
    function setTooltip(layer, type) {{
        var il = layer.feature.properties.name;
        var val = 0;
        if(type === 'kullanici') {{
            val = kullaniciData[il] || 0;
            var content = '<b>İl:</b> ' + il + '<br><b>Kullanıcı Sayısı:</b> ' + val;
            showTooltip(layer, content);
        }} else if(type === 'tarif') {{
            val = tarifData[il] || 0;
            var content = '<b>İl:</b> ' + il + '<br><b>Tarif Sayısı:</b> ' + val;
            showTooltip(layer, content);
        }}
    }}

    // Katmanların görünürlük durumunu ayarla, tooltipleri güncelle
    function updateLayers(selectedLayerName) {{
        allLayers.forEach(layer => {{
            var layerName = layer.options && layer.options.name;
            if(!layerName) {{
                // GeoJson Layer ise
                var parent = layer._map._layers;
                // Ancak biz zaten feature layerlar üzerinde çalışıyoruz, burayı boş bırakıyoruz
            }}
        }});
        // Kullanıcı layer görünür ise sadece o tooltip aktif
        if(selectedLayerName === kullaniciLayerName) {{
            map.removeLayer(tarifLayer);
            map.addLayer(kullaniciLayer);

            kullaniciLayer.eachLayer(function(layer) {{
                setTooltip(layer, 'kullanici');
            }});
        }} else if(selectedLayerName === tarifLayerName) {{
            map.removeLayer(kullaniciLayer);
            map.addLayer(tarifLayer);

            tarifLayer.eachLayer(function(layer) {{
                setTooltip(layer, 'tarif');
            }});
        }}
    }}

    // Başlangıçta kullanıcı katmanı tooltipleri ayarlansın
    kullaniciLayer.eachLayer(function(layer) {{
        setTooltip(layer, 'kullanici');
    }});

    // LayerControl'daki seçim değişince katmanları ve tooltipleri güncelle
    inputs.forEach(input => {{
        input.addEventListener('change', function() {{
            updateLayers(this.nextSibling.textContent.trim());
        }});
    }});

</script>
'''

m.get_root().html.add_child(folium.Element(js))

# Kaydet
m.save('..//turkiye_katmanli_radio_harita_dinamik_tooltip.html')
print("Harita kaydedildi: turkiye_katmanli_radio_harita_dinamik_tooltip.html")
