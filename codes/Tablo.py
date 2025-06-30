import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
# === 1. Temizlenmiş profilleri oku ===
profiles_df = pd.read_csv('../datas/profiles_clean.csv')

# === 2. Geçerli şehirleri filtrele ===
profiles_df_filtered = profiles_df[profiles_df['eslesen_sehir'].notna()]

# === 3. Kullanıcı sayılarını şehir bazında say ===
kullanici_counts = profiles_df_filtered['eslesen_sehir'].value_counts().reset_index()
kullanici_counts.columns = ['il', 'kullanici_sayisi']

# === 6. Toplam satırı ekle ===
total_row = pd.DataFrame({
    'il': ['Toplam'],
    'kullanici_sayisi': [sehir_counts['kullanici_sayisi'].sum()],
    'tarif_sayisi': [sehir_counts['tarif_sayisi'].sum()]
})
sehir_counts_with_total = pd.concat([sehir_counts, total_row], ignore_index=True)

# === 7. PNG tabloyu kaydet ===
fig, ax = plt.subplots(figsize=(10, len(sehir_counts_with_total) * 0.4))
ax.axis('off')
tbl = table(ax, sehir_counts_with_total, loc='center', cellLoc='center', colWidths=[0.3]*3)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.5)
plt.tight_layout()
plt.savefig('../sehir_kullanicilar_tarifler_tablosu.png', dpi=300)
print("📊 Tablo başarıyla kaydedildi: sehir_kullanicilar_tarifler_tablosu.png")