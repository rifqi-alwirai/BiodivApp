import numpy as np
import pandas as pd

def hitung_shannon(data):
    """
    Menghitung indeks Shannon (H') dari DataFrame yang terdiri dari baris per individu.
    """
    # Hitung jumlah per spesies
    jumlah_per_spesies = data["Spesies"].value_counts()

    total = jumlah_per_spesies.sum()
    if total == 0:
        return 0

    proporsi = jumlah_per_spesies / total
    shannon = - (proporsi * proporsi.apply(lambda p: np.log(p))).sum()
    return shannon

def hitung_simpson(data):
    jumlah_per_spesies = data["Spesies"].value_counts()
    total = jumlah_per_spesies.sum()
    if total == 0:
        return 0
    proporsi = jumlah_per_spesies / total
    return (proporsi ** 2).sum()

def hitung_evenness(data):
    jumlah_per_spesies = data["Spesies"].value_counts()
    k = len(jumlah_per_spesies)
    if k <= 1:
        return 0
    H = hitung_shannon(data)
    return H / np.log(k)

def hitung_indeks_keseluruhan(df):
    """
    Menghitung indeks Shannon, Evenness, dan Simpson untuk seluruh data monitoring (tanpa memisah per stasiun).
    """
    if df.empty or "Spesies" not in df.columns:
        return {"Shannon": None, "Evenness": None, "Simpson": None}

    H = hitung_shannon(df)
    E = hitung_evenness(df)
    D = hitung_simpson(df)

    return {
        "Shannon": round(H, 3),
        "Evenness": round(E, 3),
        "Simpson": round(D, 3)
    }

def hitung_indeks_per_stasiun(df: pd.DataFrame) -> pd.DataFrame:
    hasil_indeks = []
    stasiun_list = df["Stasiun"].unique()

    for stasiun in stasiun_list:
        data_stasiun = df[df["Stasiun"] == stasiun]
        hasil_indeks.append({
            "Stasiun": stasiun,
            "Shannon": round(hitung_shannon(data_stasiun), 3),
            "Evenness": round(hitung_evenness(data_stasiun), 3),
            "Simpson": round(hitung_simpson(data_stasiun), 3)
        })

    return pd.DataFrame(hasil_indeks)