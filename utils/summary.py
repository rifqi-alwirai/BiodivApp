import pandas as pd

def ringkasan_statistik(df_merge, df_indeks):
    kelompok_list = df_merge["Kelompok"].unique()
    hasil = []

    for kelompok in kelompok_list:
        df_k = df_merge[df_merge["Kelompok"] == kelompok]

        # Kelimpahan & biomassa
        total_jumlah = df_k.shape[0]  # karena 1 baris = 1 individu
        total_biomassa = df_k["Biomassa"].sum()
        total_individu = df_k.shape[0]  # jumlah baris = jumlah individu
        total_spesies = df_k["Spesies"].nunique()
        total_stasiun = df_k["Stasiun"].nunique()

        rata_per_stasiun = df_k.groupby("Stasiun").agg({
            "Biomassa": "sum"
        })
        rata_per_stasiun["Jumlah Individu"] = df_k.groupby("Stasiun").size()

        # Ambil rata-ratanya
        rata2_individu = rata_per_stasiun["Jumlah Individu"].mean()
        rata2_biomassa = rata_per_stasiun["Biomassa"].mean()

        # Spesies dominan
        spesies_terbanyak = df_k.groupby("Spesies").size().idxmax()

        # Indeks ekologi: rata-rata per stasiun untuk kelompok tsb
        indeks_rata = df_indeks[df_merge["Kelompok"] == kelompok].mean(numeric_only=True)

        hasil.append({
            "Kelompok": kelompok,
            "Jumlah Individu": total_individu,
            "Jumlah Spesies": total_spesies,
            "Jumlah Stasiun": total_stasiun,
            "Total Biomassa (g)": round(total_biomassa, 2),
            "Rata2 Individu/Stasiun": round(rata2_individu, 1),
            "Rata2 Biomassa/Stasiun (g)": round(rata2_biomassa, 1),
            "Spesies Terbanyak": spesies_terbanyak
        })

    return pd.DataFrame(hasil)