import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urlparse
import random

def extract_username_from_url(url):
    path = urlparse(url).path
    parts = path.strip('/').split('/')
    if len(parts) >= 2 and parts[0] == 'u':
        return parts[1]
    return None

def read_categories(file_path):
    categories = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories.append({
                'kategori_id': row['kategori_id'],
                'url': row['kategori_url'],
                'sayfa': int(row['sayfa_sayisi'])
            })
    return categories


def get_recipes_from_page(page_url, max_retries=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(page_url, headers=headers)
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                wait_time = int(retry_after) if retry_after and retry_after.isdigit() else 60
                print(f"429 Too Many Requests hatası alındı. {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
                retries += 1
                continue  # tekrar dene

            response.raise_for_status()  # Diğer HTTP hatalarını yakala
            soup = BeautifulSoup(response.content, "html.parser")

            # Tarif kartlarını seç
            cards = soup.select("div.col-md-4.col-sm-6.col-xs-12 > div.recipe-cards")
            for card in cards:
                # Tarif linki ve adı
                title_tag = card.select_one("a.title")
                if title_tag:
                    recipe_url = title_tag.get("href")
                    recipe_name = title_tag.text.strip()
                else:
                    recipe_url = None
                    recipe_name = None

                # Profil URL'si
                profile_tag = card.select_one(".recipe-owner")
                profile_url = profile_tag.get("data-jshref") if profile_tag and profile_tag.get("data-jshref") else ""
                kullanici_adi = extract_username_from_url(profile_url)

                if recipe_url and recipe_name:
                    results.append((recipe_name, recipe_url, kullanici_adi))

            break  # Başarıyla tamamlandı, döngüden çık

        except requests.RequestException as e:
            print(f"Hata oluştu: {e}")
            retries += 1
            wait_time = 5 * retries  # Bekleme süresini artan şekilde ayarlayabilirsin
            print(f"{wait_time} saniye bekleniyor ve tekrar deneniyor...")
            time.sleep(wait_time)

    if retries == max_retries:
        print("Maksimum deneme sayısına ulaşıldı, işlem başarısız oldu.")

    return results


def scrape_all_recipes(categories):
    with open('../datas/recipes_2000.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['kategori_id', 'tarif_adi', 'tarif_url', 'profil_adi'])

        for cat in categories:
            kategori_id = cat['kategori_id']
            base_url = cat['url']
            page_count = cat['sayfa']
            if page_count >1500:
                for page in range(1500, page_count + 1):
                    if page == 1:
                        page_url = base_url
                    else:
                        page_url = f"{base_url.rstrip('/')}/page/{page}/"

                    print(f"Visiting: {page_url}")
                    try:
                        recipes = get_recipes_from_page(page_url)
                        print(f"Found {len(recipes)} recipes on page {page_url}")
                        for name, url, profile in recipes:
                            writer.writerow([kategori_id, name, url, profile])
                            print("Saved:", name, url)
                    except Exception as e:
                        print(f"Error on page {page_url}: {e}")
                    time.sleep(random.uniform(1, 3))


if __name__ == "__main__":
    categories = read_categories("../datas/categories_clean.csv")
    scrape_all_recipes(categories)
    print("Tarif verileri başarıyla kaydedildi.")