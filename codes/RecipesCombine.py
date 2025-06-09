import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

recipes_100 = pd.read_csv('../datas/recipes_100.csv')
recipes_500 = pd.read_csv('../datas/recipes_500.csv')
recipes_1500 = pd.read_csv('../datas/recipes_1500.csv')
recipes_2000 = pd.read_csv('../datas/recipes_2000.csv')

df = pd.concat([recipes_100, recipes_500, recipes_1500, recipes_2000], ignore_index=True)

# Toplam satır sayısı
total_rows = len(df)

# Tekrar olmayan URL sayısı
unique_url_rows = df['tarif_url'].nunique()

# Tekrarlayan kayıt sayısı
duplicate_count = total_rows - unique_url_rows

print(f"Toplam {duplicate_count} adet tekrar eden tarif_url bulundu.")
print("Toplam satır sayısı:", total_rows)
print("Tarif URL sayısı:", df['tarif_url'].nunique())
print("Tarif adı sayısı:", df['tarif_adi'].nunique())
print("Profil adı sayısı:", df['profil_adi'].nunique())

df = df.drop_duplicates(subset='tarif_url', keep='first')

df.to_csv('../datas/recipes_combined.csv', index=False)


"""
Toplam 101900 adet tekrar eden tarif_url bulundu.
Toplam satır sayısı: 902040
Tarif URL sayısı: 800140
Tarif adı sayısı: 380235
Profil adı sayısı: 74910
tarif_url, tarif_adi ve profil_adi açısından tamamen benzersiz 800156 tarif var.
"""