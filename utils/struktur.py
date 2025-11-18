import pandas as pd
from utils.biomassa import hitung_biomassa
from konversi import konversi_biomassa
from utils.indeks import hitung_indeks_per_stasiun

def proses_semua_data(df_parsed, basis_ikan, mode_tampilan):
    # ⚖️ Hitung biomassa terlebih dahulu
    df_biomassa = hitung_biomassa(df_parsed, basis_ikan)

    # 🎨 Rename agar konsisten downstream
    if "biomassa_total" in df_biomassa.columns:
        df_biomassa = df_biomassa.rename(columns={"biomassa_total": "Biomassa"})

    # 💾 Terapkan konversi jika diperlukan
    is_terkonversi = mode_tampilan == "Data Terkonversi"
    df_merge = konversi_biomassa(df_biomassa.copy()) if is_terkonversi else df_biomassa.copy()

    # 🧮 Tambahkan kolom Kelimpahan (jumlah individu per spesies)
    kelimpahan_df = (
        df_merge.groupby(["Stasiun", "Famili", "Spesies"])
        .size().reset_index(name="Kelimpahan")
    )
    df_merge = df_merge.merge(kelimpahan_df, on=["Stasiun", "Famili", "Spesies"], how="left")

    # 📊 Hitung indeks keanekaragaman per stasiun
    df_indeks = hitung_indeks_per_stasiun(df_parsed)

    # 🧠 Gabungkan keanekaragaman ke df_merge (ambil nilai Shannon saja)
    if "Shannon" in df_indeks.columns:
        df_merge = df_merge.merge(
            df_indeks[["Stasiun", "Shannon"]].rename(columns={"Shannon": "Keanekaragaman"}),
            on="Stasiun",
            how="left"
        )

    return df_merge