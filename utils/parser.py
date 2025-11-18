import pandas as pd
import re

def parse_ukuran_string(ukuran_str, stasiun, spesies, kelompok, famili):
    hasil = []

    if pd.isna(ukuran_str):
        return hasil

    ukuran_str = str(ukuran_str)
    pattern = r"(\d+)\s*\((\d+)\)"
    pasangan = re.findall(pattern, ukuran_str)

    for jumlah, ukuran in pasangan:
        hasil.append({
            "Stasiun": stasiun,
            "Spesies": spesies,
            "Kelompok": kelompok,
            "Famili": famili,
            "Ukuran_cm": float(ukuran),
            "Jumlah": int(jumlah)
        })

    return hasil

def parse_all_datauvc(df_monitoring):
    """
    Parsing data hasil UVC dari format wide menjadi long,
    lalu pecah entri "n (ukuran)" atau hanya "n" menjadi baris individu.
    """
    kolom_statis = ["Kelompok", "Famili", "Spesies"]
    kolom_stasiun = [col for col in df_monitoring.columns if col not in kolom_statis]

    # Wide → Long
    df_long = df_monitoring.melt(
        id_vars=kolom_statis,
        value_vars=kolom_stasiun,
        var_name="Stasiun",
        value_name="Data"
    ).dropna(subset=["Data"])

    hasil = []

    for _, row in df_long.iterrows():
        kelompok = row["Kelompok"]
        famili = row["Famili"]
        spesies = row["Spesies"]
        stasiun = row["Stasiun"]
        data = str(row["Data"])

        entri_list = [e.strip() for e in data.split(",") if e.strip()]

        for entri in entri_list:
            if "(" in entri:
                try:
                    jumlah = int(entri.split("(")[0].strip())
                    ukuran = float(entri.split("(")[1].replace(")", "").strip())
                    for _ in range(jumlah):
                        hasil.append({
                            "Stasiun": stasiun,
                            "Spesies": spesies,
                            "Kelompok": kelompok,
                            "Famili": famili,
                            "Ukuran_cm": ukuran
                        })
                except:
                    continue
            else:
                try:
                    jumlah = int(entri)
                    for _ in range(jumlah):
                        hasil.append({
                            "Stasiun": stasiun,
                            "Spesies": spesies,
                            "Kelompok": kelompok,
                            "Famili": famili,
                            "Ukuran_cm": None  # Tidak ada ukuran
                        })
                except:
                    continue

    return pd.DataFrame(hasil)