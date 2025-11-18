# Konstanta: area swept = 350 m², target = per hektar (10,000 m²)
KONVERSI_BIOMASSA_KG_PER_HA = 10000 / 350 / 1000       # gram → kg, lalu ke per hektar
KONVERSI_KELIMPAHAN_PER_HA = 10000 / 350              # jumlah → per hektar

def konversi_biomassa(df, kolom="Biomassa"):
    """
    Mengonversi kolom biomassa dari gram/350m² menjadi kg/ha.
    """
    if kolom in df.columns:
        df[kolom] = df[kolom] * KONVERSI_BIOMASSA_KG_PER_HA
    return df

def konversi_kelimpahan(series):
    """
    Mengonversi Series kelimpahan dari jumlah/350m² menjadi jumlah/ha.
    """
    return series * KONVERSI_KELIMPAHAN_PER_HA