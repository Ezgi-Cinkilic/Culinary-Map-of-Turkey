
"""import pandas as pd

# CSV dosyasını oku
df = pd.read_csv('../datas/profiles.csv')

# 'sehir' sütunu boş olmayan satırların sayısı

dolu_sehir_sayisi = df['sehir'].notna().sum()

print("Profil sayısı:", len(df))
print(f"Şehir bilgisi dolu olan profil sayısı: {dolu_sehir_sayisi}")
"""
"""
import pandas as pd

# 1. Dosyaları oku
recipes_df = pd.read_csv('../datas/recipes_combined.csv')
profiles_df = pd.read_csv('../datas/profiles.csv')

def normalize_username(name):
    if pd.isna(name):
        return None
    return str(name).strip().lower()


recipes_df['profil_adi'] = recipes_df['profil_adi'].apply(normalize_username)
profiles_df['profil_adi'] = profiles_df['profil_adi'].apply(normalize_username)

profilleri_sehirli = profiles_df[profiles_df['sehir'].notna() & (profiles_df['sehir'].str.strip() != '')]

merge_df = pd.merge(recipes_df, profilleri_sehirli, on='profil_adi', how='inner')

tarif_sayisi = merge_df.shape[0]
print(f"Şehir bilgisi olan profillerle eşleşen tarif sayısı: {tarif_sayisi}")

# 6. Her kullanıcının kaç tarif yüklediğini bul
tarif_sayilari = merge_df['profil_adi'].value_counts().reset_index()
tarif_sayilari.columns = ['profil_adi', 'tarif_sayisi']

# 7. Şehir bilgisiyle birlikte göstermek istersen:
tarif_sehir_df = pd.merge(tarif_sayilari, profilleri_sehirli[['profil_adi', 'sehir']], on='profil_adi', how='left')

# 8. Sonuçları göster
print(tarif_sehir_df.head())

# 9. (Opsiyonel) Kaydet
# tarif_sehir_df.to_csv('../datas/tarif_sayilari_sehirli.csv', index=False, encoding='utf-8')
"""

import pandas as pd

def normalize_sehir(sehir):
    if pd.isna(sehir):
        return None
    sehir = sehir.strip().lower()
    replacements = {
        'ç': 'c',
        'ğ': 'g',
        'ı': 'i',
        'ö': 'o',
        'ş': 's',
        'ü': 'u',
        'â': 'a',
        'î': 'i',
        'û': 'u'
    }
    for turkce, ascii_karsilik in replacements.items():
        sehir = sehir.replace(turkce, ascii_karsilik)
    return sehir

# 1. Dosyayı oku
profiles_df = pd.read_csv('../datas/profiles.csv')

# 2. Geçerli şehirleri filtrele ve normalize et
profiles_df['sehir_normalize'] = profiles_df['sehir'].dropna().apply(normalize_sehir)
gecerli_sehirler = profiles_df['sehir_normalize'].dropna().loc[lambda x: x != '']
benzersiz_sehir_sayisi = gecerli_sehirler.nunique()

print(f"Benzersiz şehir sayısı: {benzersiz_sehir_sayisi}")

# 3. Say ve sırala
sehir_sayilari = gecerli_sehirler.value_counts().reset_index()
sehir_sayilari.columns = ['sehir', 'kullanici_sayisi']
sehir_sayilari = sehir_sayilari.sort_values(by='sehir').reset_index(drop=True)

# 4. Yazdır
print(sehir_sayilari)