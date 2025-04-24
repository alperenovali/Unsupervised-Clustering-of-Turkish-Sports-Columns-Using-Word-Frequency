from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import pandas as pd
import re

base_url = 'https://www.sozcu.com.tr/'
base_dir = r"C:\Users\ASUS\OneDrive\Desktop\ML_Proje\data\sozcu"
other_dir = r"C:\Users\ASUS\OneDrive\Desktop\ML_Proje\data\korkusuz"
other_url = "https://www.korkusuz.com.tr/"
driver_path = 'chromedriver.exe'
years = [2025,2024]

base_authors ={
    "Fatih Soylemezoglu" : "fatih-soylemezoglu-a61",
    "Ercan Taner" : 'ercan-taner-a49',
    "Tarık Eryigit" : 'tarik-eryigit-a57',
    "Huseyin Suekinci" : 'huseyin-suekinci-a2295',
    "Yasin Yildirim" : 'yasin-yildirim-a53',
    "Umit Genc" : 'umit-genc-a60',
    "Erman Toroglu" : 'erman-toroglu-a2294',
    "Bahadır Cokisler" : "bahadir-cokisler-a59",
}
other_authors ={
    "Argun Darici" : "argun-darici-a16",
    "Ali Iskefli" : "ali-iskefli-a14",
    "Alper Mert" : "alper-mert-a15"
}

chrome_options = Options()
chrome_options.add_argument("--headless") # Sekme açmadan çalıştırmak için (daha güvenli)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--log-level=3")

def start_driver():
    service = Service(executable_path=driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def split_into_sentences(paragraph):
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    return [s.strip() for s in sentences if s.strip]

def get_csv_filename_for_author(author_name):
    filename = f"{author_name.replace(' ', '_')}.csv"
    return os.path.join(other_dir,filename)

def write_to_csv_for_author(data, author_name):
    filename = get_csv_filename_for_author(author_name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Klasörü oluştur

    df_new = pd.DataFrame(data, columns=["Yazar", "Ay", "Sene", "Baslik", "Paragraf"])
    
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(filename, index=False, encoding='utf-8')


def visit_authors(authors_dicts,site_url):
    for name,link in authors_dicts.items():
        driver = start_driver()
        for year in years:
            for month in range(1,13):
                # sozcu.com.tr/ercan-taner-a49?SelectedMonth=1&SelectedYear=2024
                full_url = f"{site_url}{link}?SelectedMonth={month}&SelectedYear={year}"
                driver.get(full_url)
                time.sleep(3)

                driver.execute_script("window.scrollBy(0,400);")
                time.sleep(2)

                list_group = driver.find_element(By.CLASS_NAME, "list-group")
                links = list_group.find_elements(By.TAG_NAME, "a")
                hrefs = [a.get_attribute("href") for a in links]
                time.sleep(2)

                content_data = []

                if(len(links) > 0):
                    for idx, href in enumerate(hrefs):
                        print(f"{idx+1}.linke gidiliyor : {href}")
                        driver.get(href)
                        time.sleep(3)

                        driver.execute_script("window.scrollBy(0,400);")
                        time.sleep(1)

                        title_element = driver.find_element(By.CLASS_NAME, "author-content-title")
                        title = title_element.text.strip()

                        article_body = driver.find_element(By.CLASS_NAME, "article-body")
                        paragraphs = article_body.find_elements(By.TAG_NAME, "p")
                        content = "\n".join([p.text for p in paragraphs])
                        """"
                        # Cümleleri ayırdığımız kısım ama veriyi yeterince toplayamıyor
                        for p in paragraphs:
                            sentences = split_into_sentences(p.text)
                            for sentence in sentences:
                                if len(sentence) > 0:
                                    content_data.append([name,month,year,title,sentence])
                        """
                        content_data.append([name,month,year,title,content])

                    write_to_csv_for_author(content_data,name)
                    content_data.clear()
                else:
                    continue

        driver.quit()

visit_authors(other_authors,other_url)