import requests
from bs4 import BeautifulSoup
import csv
import time

def kategori_linklerini_al():
    url = "https://www.nefisyemektarifleri.com/tarifler/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    kategoriler = []
    for a_tag in soup.select("div.category a"):
        href = a_tag.get("href")
        if href and "kategori/tarifler" in href and href.count("/") > 6:
            kategoriler.append(href.rstrip('/'))

    return sorted(set(kategoriler))

def get_page_count(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        last_link = soup.find("a", class_="last")
        if last_link:
            page_text = last_link.text.strip().replace('.', '')
            if page_text.isdigit():
                return int(page_text)

        page_numbers = []
        for a in soup.select("ul.pagination a"):
            text = a.text.strip().replace('.', '')
            if text.isdigit():
                page_numbers.append(int(text))
        return max(page_numbers) if page_numbers else 1
    except Exception as e:
        print(f"Error getting page count for {url}: {e}")
        return 1

def save_kategori_linkleri(urls):
    with open('../datas/categories.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['kategori_id', 'ana_kategori', 'alt_kategori', 'kategori_url', 'sayfa_sayisi'])
        for idx, url in enumerate(urls, start=1):
            parts = url.strip('/').split('/')

            # Ana kategori ismini çıkar
            s1 = parts[5]
            kelimeler = s1.strip('-').split('-')
            ana_kategori = '-'.join([k for k in kelimeler if k not in ('tarifler', 'tarifleri')])

            # Alt kategori varsa al, yoksa ana kategori ile aynı yap
            if len(parts) > 6:
                s2 = parts[-1]
                alt_kelimeler = s2.strip('-').split('-')
                alt_kategori = '-'.join([k for k in alt_kelimeler if k not in ('tarifler', 'tarifleri')])
            else:
                alt_kategori = ana_kategori

            print("Kategori urlsi bulundu, sayfa sayısı alınıyor:", url)
            sayfa_sayisi = get_page_count(url)
            writer.writerow([idx, ana_kategori, alt_kategori, url, sayfa_sayisi])
            print("Kategori bilgileri kaydedildi:", idx, ana_kategori, alt_kategori, url, sayfa_sayisi)
            time.sleep(1)

if __name__ == "__main__":
    urls = kategori_linklerini_al()
    save_kategori_linkleri(urls)
    print(f"{len(urls)} kategori linki kaydedildi.")
