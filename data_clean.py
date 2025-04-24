import os
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

# Hatalı kod satırları
nltk.download('punkt')

# Sadece bu dosyayı işlemeye alıyoruz
input_filename = "Ali_Iskefli.csv"
input_folder = "C:\Users\ASUS\OneDrive\Desktop\ML_Proje\data\korkusuz"
output_folder = "C:\Users\ASUS\OneDrive\Desktop\ML_Proje\cleaned_data"
os.makedirs(output_folder, exist_ok=True)

filepath = os.path.join(input_folder, input_filename)
df = pd.read_csv(filepath)

# 'Cümle' sütununun olup olmadığını kontrol et
if "Cümle" not in df.columns:
    print(f"{input_filename} içinde 'Cümle' sütunu bulunamadı.")
else:
    all_rows = []

    # Her satırdaki metni parçalayıp işleme
    for idx, row in df.iterrows():
        if pd.isna(row["Cümle"]): continue

        # Paragrafları cümlelere ayır
        sentences = sent_tokenize(row["Cümle"])
        for sent in sentences:
            # Yeni satır oluşturma
            new_row = {
                "Yazar": row.get("Yazar", ""),
                "Ay": row.get("Ay", ""),
                "Sene": row.get("Sene", ""),
                "Başlık": row.get("Başlık", ""),
                "Cümle": sent.strip()
            }
            all_rows.append(new_row)

    # Yeni DataFrame oluştur ve dosyayı kaydet
    output_df = pd.DataFrame(all_rows)
    
    # Yeni dosya adı: "cümle_Ali_Iskefli.csv"
    output_filename = f"cümle_{os.path.splitext(input_filename)[0]}.csv"
    output_path = os.path.join(output_folder, output_filename)
    output_df.to_csv(output_path, index=False)
    print(f"{input_filename} işlendi ve {output_path} oluşturuldu.")
