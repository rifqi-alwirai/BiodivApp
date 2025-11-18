import pandas as pd
import io

# 🧬 Urutan famili ekologis: kelompok → famili
URUTAN_FAMILI = [
    "Chaetodontidae",  # Koralivora
    "Acanthuridae", "Scaridae", "Siganidae",  # Herbivora
    "Haemulidae", "Lethrinidae", "Lutjanidae", "Serranidae"  # Karnivora
]
FAM_ORDER = {fam: i for i, fam in enumerate(URUTAN_FAMILI)}

def urutkan_spesies(df):
    df = df.copy()
    df["Famili_Order"] = df["Famili"].map(FAM_ORDER)
    df_sorted = df.sort_values(by=["Famili_Order", "Famili", "Spesies"])
    return df_sorted.drop(columns=["Famili_Order"])


def urutkan_famili(df):
    df = df.copy()
    df["Famili_Order"] = df[group_by].map(FAM_ORDER)
    df_sorted = df.sort_values(by="Famili_Order")
    return df_sorted.drop(columns=["Famili_Order"])


def prepare_tab(df, value_col, group_by="Spesies", stasiun_order=None):
    df = df.copy()

    # Urutan famili ekologis
    urutan_famili = [
        "Chaetodontidae",
        "Acanthuridae", "Scaridae", "Siganidae",
        "Haemulidae", "Lethrinidae", "Lutjanidae", "Serranidae"
    ]
    fam_order_map = {fam: i for i, fam in enumerate(urutan_famili)}

    if group_by == "Spesies":
        df["Famili_order"] = df["Famili"].map(fam_order_map)
        df = df[df["Famili_order"].notna()]
        df = df.sort_values(by=["Famili_order", "Famili", "Spesies"])
        ordered_index = df["Spesies"].drop_duplicates().tolist()

    elif group_by == "Famili":
        df["Famili_order"] = df[group_by].map(fam_order_map)
        df = df[df["Famili_order"].notna()]
        df = df.sort_values("Famili_order")
        ordered_index = df[group_by].drop_duplicates().tolist()

    else:
        ordered_index = df[group_by].drop_duplicates().tolist()

    # 🔄 Pivot
    df_pivot = df.pivot_table(
        index=group_by,
        columns="Stasiun",
        values=value_col,
        aggfunc="sum",
        fill_value=0
    )

    # 🧼 Bersihkan duplikat kolom dan stasiun
    df_pivot = df_pivot.loc[:, ~df_pivot.columns.duplicated()]
    if stasiun_order:
        valid_order = [s for s in stasiun_order if s in df_pivot.columns]
        df_pivot = df_pivot.reindex(columns=valid_order)

    # 📐 Reindex hasil agar mengikuti urutan yang disusun manual
    df_pivot = df_pivot.reindex(index=ordered_index)

    # ➕ Tambahkan Rata-rata
    df_pivot["Rata-rata"] = df_pivot.mean(axis=1)

    return df_pivot.reset_index()
    
def generate_excel_multisheet(df_base, group_by="Spesies", value_columns=None):
    if not value_columns:
        raise ValueError("value_columns tidak boleh kosong.")

    stasiun_order = sorted(df_base["Stasiun"].dropna().unique())
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        workbook = writer.book

        for value_col in value_columns:
            if value_col not in df_base.columns:
                continue

            # 🧮 Siapkan tabulasi dengan urutan ekologis
            df_sheet = prepare_tab(df_base, value_col, group_by, stasiun_order)
            df_sheet.to_excel(writer, sheet_name=value_col, index=False)
            worksheet = writer.sheets[value_col]

            # 🖌️ Format header
            header_fmt = workbook.add_format({
                "bold": True, "bg_color": "#dbeeff", "border": 1
            })
            for col_num, col_name in enumerate(df_sheet.columns):
                worksheet.write(0, col_num, col_name, header_fmt)
                worksheet.set_column(col_num, col_num, 18)

            # ✨ Highlight dominan
            for col_num in range(1, len(df_sheet.columns)):
                col_data = df_sheet.iloc[:, col_num]
                if col_data.notnull().any():
                    max_row = col_data.idxmax() + 1
                    highlight_fmt = workbook.add_format({"bg_color": "#ffefc4"})
                    worksheet.write(
                        max_row,
                        col_num,
                        col_data.iloc[max_row - 1],
                        highlight_fmt
                    )

    buffer.seek(0)
    return buffer