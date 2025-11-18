import pandas as pd

def hitung_biomassa(df_data, df_basis):
    """
    Hitung biomassa hanya untuk ikan non-koralivora yang memiliki ukuran dan koefisien a-b.
    """
    df = df_data.copy()

    # Gabungkan basis ikan berdasarkan spesies
    df = df.merge(df_basis[["Spesies", "a", "b"]], on="Spesies", how="left")

    # Hanya hitung biomassa jika:
    # - memiliki nilai 'Ukuran_cm'
    # - bukan kelompok Koralivora
    # - memiliki nilai a dan b
    mask = (
        df["Kelompok"].isin(["Herbivora", "Karnivora"]) &
        df["Ukuran_cm"].notna() &
        df["a"].notna() & df["b"].notna()
    )

    # Biomassa: W = a * L^b
    df.loc[mask, "biomassa_total"] = df.loc[mask].apply(
        lambda row: row["a"] * (row["Ukuran_cm"] ** row["b"]),
        axis=1
    )

    # Biomassa untuk entri lainnya dibiarkan kosong (NaN)
    return df