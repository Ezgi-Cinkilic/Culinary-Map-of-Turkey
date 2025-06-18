import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

def parse_join_months(text):
    try:
        yil = 0
        ay = 0
        yil_eslesme = re.search(r'(\d+)\s*yıl', text)
        ay_eslesme = re.search(r'(\d+)\s*ay', text)
        if yil_eslesme:
            yil = int(yil_eslesme.group(1))
        if ay_eslesme:
            ay = int(ay_eslesme.group(1))
        return yil * 12 + ay
    except:
        return None

def scrape_user_profile(profile_url, max_retries=3):
    retry_delay = 60  # 429 için varsayılan bekleme süresi
    retries = 0

    while retries < max_retries or max_retries == -1:  # -1 ise sonsuz deneme
        try:
            response = requests.get(profile_url, headers=headers, timeout=10)

            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                wait_time = int(retry_after) if retry_after and retry_after.isdigit() else retry_delay
                print(f"[!] 429 Too Many Requests: {profile_url} — {wait_time} sn bekleniyor...")
                time.sleep(wait_time)
                retries += 1
                continue  # yeniden dene

            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            kullanici_verisi = {
                'profil_adi': None,
                'kayit_ay': None,
                'tarif_sayisi': None,
                'takipci': None,
                'takip': None,
                'sehir': None,
            }

            # Profil Adı
            username_tag = soup.find('span', class_='user-login')
            if username_tag:
                kullanici_verisi['profil_adi'] = username_tag.text.strip().replace('@', '')

            # Kayıt Tarihi ve Ay
            join_date_tag = soup.find('li', class_='clock')
            if join_date_tag:
                metin = join_date_tag.text.strip()
                kullanici_verisi['kayit_ay'] = parse_join_months(metin)

            # Tarif Sayısı
            recipes_tag = soup.find('a', title='Gönderdiği Tarifler')
            if recipes_tag:
                count_span = recipes_tag.find('span', class_='count')
                if count_span:
                    kullanici_verisi['tarif_sayisi'] = int(count_span.text.strip().replace('.', ''))

            # Takipçi
            followers_tag = soup.find('span', class_='count followers')
            if followers_tag:
                kullanici_verisi['takipci'] = int(followers_tag.text.strip().replace('.', ''))

            # Takip
            following_tag = soup.find('span', class_='count following')
            if following_tag:
                kullanici_verisi['takip'] = int(following_tag.text.strip().replace('.', ''))

            # Şehir
            city_tag = soup.find('li', class_='address')
            if city_tag:
                kullanici_verisi['sehir'] = city_tag.text.strip().lower()

            return kullanici_verisi

        except requests.exceptions.RequestException as e:
            print(f"[!] Bağlantı hatası ({retries + 1}. deneme): {profile_url}: {e}")
            retries += 1
            time.sleep(10)  # geçici bağlantı hatalarında kısa bekleme
        except Exception as e:
            print(f"[!] Ayrıştırma hatası: {profile_url}: {e}")
            return None

    print(f"[!] {profile_url} için maksimum tekrar sayısına ulaşıldı, veri alınamadı.")
    return None


def main():
    BATCH_SIZE = 10000  # Her seferde çekilecek profil sayısı
    try:
        # Yeni tarif verilerini oku
        recipes_df = pd.read_csv('../datas/recipes_combined.csv')
        yeni_usernames = set(recipes_df['profil_adi'].dropna().unique())
    except FileNotFoundError:
        print("recipes_combined.csv bulunamadı.")
        return
    except KeyError:
        print("'profil_adi' sütunu bulunamadı.")
        return

    profiles_path = '../datas/profiles.csv'
    try:
        mevcut_profiles_df = pd.read_csv('../datas/profiles.csv')
        mevcut_usernames = set(mevcut_profiles_df['profil_adi'].dropna().unique())
        print(f"{len(mevcut_usernames)} profil zaten mevcut.")
    except FileNotFoundError:
        mevcut_usernames = set()
        mevcut_profiles_df = pd.DataFrame()
        print("profiles.csv bulunamadı, sıfırdan başlıyoruz.")

    # Yeni kullanıcıları belirle
    eksik_usernames = list(yeni_usernames - mevcut_usernames)
    print(f"{len(eksik_usernames)} yeni profil indirilecek.")

    batch_usernames = eksik_usernames[:BATCH_SIZE]
    print(f"{len(batch_usernames)} profil şimdi çekilecek...")

    tum_profiller = []
    for i, username in enumerate(batch_usernames, start=1):
        profile_url = f"https://www.nefisyemektarifleri.com/u/{username}/"
        print(f"[{i}/{len(batch_usernames)}] Scraping: {profile_url}")
        veri = scrape_user_profile(profile_url)
        if veri:
            tum_profiller.append(veri)
        time.sleep(random.uniform(0.5, 1.5))

    # 5. Kaydet
    if tum_profiller:
        yeni_profiles_df = pd.DataFrame(tum_profiller)
        guncel_df = pd.concat([mevcut_profiles_df, yeni_profiles_df], ignore_index=True)
        guncel_df.drop_duplicates(subset='profil_adi', keep='first', inplace=True)
        guncel_df.to_csv(profiles_path, index=False, encoding='utf-8')
        print(f"{len(tum_profiller)} yeni profil eklendi. Toplam kayıt: {guncel_df.shape[0]}")
    else:
        print("Yeni profil verisi alınamadı.")

if __name__ == "__main__":
    main()
