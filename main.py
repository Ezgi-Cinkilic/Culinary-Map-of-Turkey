import requests
from bs4 import BeautifulSoup

# Hedef URL
url = "https://www.nefisyemektarifleri.com/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Sayfayı çek
response = requests.get(url, headers=headers)

# Sayfa başarıyla yüklendiyse devam et
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    # a.title etiketlerini bul
    recipes = soup.select("a.title")[:3]  # İlk 3 tarifi al

    print("İlk 3 tarif:")
    for i, recipe in enumerate(recipes, 1):
        name = recipe.get_text(strip=True)
        link = recipe["href"]
        print(f"{i}. {name} --> {link}")
else:
    print(f"Sayfa yüklenemedi. Durum kodu: {response.status_code}")
