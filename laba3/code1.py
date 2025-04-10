
import urllib.request
from datetime import datetime
import os
import time

def clean_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"[+] Directory created successfully.")
        return True  # Повертаємо True, якщо директорія була створена, означає, що потрібно завантажити нові дані
    
    if len(os.listdir(directory)) == 0:
        print(f"[+] Directory is empty. Downloading fresh data.")
        return True  # Якщо директорія порожня, потрібно завантажити нові дані
    else:
        print(f"[+] Directory already contains data, using existing data.")
        return False  # Якщо є файли, не завантажуємо нові дані
 # Returning False as user chose not to clean directory, implying existing data should be used

def download_csv(country, year_1, year_2, type_data, directory):
    clean_existing_data = clean_directory(directory)  # Перевіряємо, чи потрібно завантажувати нові дані
    
    if clean_existing_data:
        for province_ID in range(1, 28):
            url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country={country}&provinceID={province_ID}&year1={year_1}&year2={year_2}&type={type_data}"
            
            retries = 3
            for attempt in range(retries):
                try:
                    with urllib.request.urlopen(url) as wp:
                        text = wp.read()
                    break
                except urllib.error.URLError as e:
                    print(f"Error downloading data for ID {province_ID}: {e}")
                    if attempt < retries - 1:
                        print(f"Retrying download for ID {province_ID} in 5 seconds...")
                        time.sleep(5)
                    else:
                        print(f"Failed to download data for ID {province_ID} after {retries} attempts.")
                        continue
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"NOAA_ID_{province_ID}_Wed_{timestamp}.csv"
            filepath = os.path.join(directory, filename)

            try:
                with open(filepath, 'wb') as out:
                    out.write(text)
                print(f"Process is downloading:\nfile_csv:{filename}...\n")
                print(f"File_csv:{filename} downloaded successfully.")
                print(f"="*80)
            except IOError as e:
                print(f"Error writing file {filename}: {e}")
    else:
        print("Using existing data in the directory.")
