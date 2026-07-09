"""
📊 Format Laporan Komprehensif Biodiversitas
============================================
Menghasilkan tabulasi format profesional dengan:
- Baris: Kategori data + satuan (dinamis sesuai mode tampilan)
- Kolom: Stasiun (ID) + Rata-rata
- Multi-sheet export
- Support mode: "Data Asli" atau "Data Terkonversi"
"""

import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows


def get_satuan_labels(mode_tampilan="Data Terkonversi"):
    """
    Dapatkan label satuan sesuai mode tampilan.
    
    Parameters:
    -----------
    mode_tampilan : str
        "Data Asli" atau "Data Terkonversi"
    
    Returns:
    --------
    dict
        {
            'kelimpahan': 'ind/ha' or 'ind (350m²)',
            'biomassa': 'kg/ha' or 'g (350m²)',
            'biomassa_unit': 'kg/ha' or 'g'
        }
    """
    if mode_tampilan == "Data Terkonversi":
        return {
            'kelimpahan': 'ind/ha',
            'biomassa': 'kg/ha',
            'biomassa_unit': 'kg'
        }
    else:  # Data Asli
        return {
            'kelimpahan': 'ind (350m²)',
            'biomassa': 'g (350m²)',
            'biomassa_unit': 'g'
        }


def prepare_comprehensive_report(df_merge, df_indeks, mode_tampilan="Data Terkonversi", stasiun_order=None):
    """
    Siapkan laporan komprehensif dengan format:
    - Baris 1: Header (Data/Stasiun | Stasiun1 | Stasiun2 | ... | Rata-rata)
    - Baris 2+: Kategori data (Indeks, Kelimpahan, Biomassa, Keanekaragaman)
    
    Parameters:
    -----------
    df_merge : DataFrame
        Data hasil merge dari struktur.py (dengan Biomassa, Kelimpahan, Keanekaragaman)
    df_indeks : DataFrame
        Data indeks per stasiun (Shannon, Simpson, Evenness)
    mode_tampilan : str
        "Data Asli" atau "Data Terkonversi" (default: "Data Terkonversi")
    stasiun_order : list, optional
        Urutan stasiun yang diinginkan
    
    Returns:
    --------
    dict
        {
            'Indeks': DataFrame indeks ekologi,
            'Kelimpahan': DataFrame kelimpahan per kelompok,
            'Biomassa': DataFrame biomassa per kelompok,
            'Keanekaragaman': DataFrame keanekaragaman per kelompok
        }
    """
    
    if stasiun_order is None:
        stasiun_order = sorted(df_indeks["Stasiun"].unique())
    
    # Pastikan kolom Stasiun ada di df_merge
    if "Stasiun" not in df_merge.columns:
        raise ValueError("df_merge harus memiliki kolom 'Stasiun'")
    
    # Dapatkan label satuan sesuai mode
    satuan = get_satuan_labels(mode_tampilan)
    
    reports = {}
    
    # ========== 1. INDEKS EKOLOGI ==========
    df_indeks_report = df_indeks[["Stasiun", "Shannon", "Simpson", "Evenness"]].copy()
    df_indeks_report = df_indeks_report[df_indeks_report["Stasiun"].isin(stasiun_order)]
    df_indeks_report = df_indeks_report.set_index("Stasiun").reindex(stasiun_order)
    
    # Transform menjadi format: kategori × stasiun
    indeks_data = []
    for idx_name in ["Shannon", "Simpson", "Evenness"]:
        row_data = {"Kategori": f"Indeks {idx_name}"}
        values = []
        
        for stasiun in stasiun_order:
            value = df_indeks_report.loc[stasiun, idx_name] if stasiun in df_indeks_report.index else 0
            row_data[stasiun] = round(value, 4)
            values.append(value)
        
        rata_rata = sum(values) / len(values) if values else 0
        row_data["Rata-rata"] = round(rata_rata, 4)
        indeks_data.append(row_data)
    
    reports["Indeks"] = pd.DataFrame(indeks_data)
    
    # ========== 2. KELIMPAHAN PER KELOMPOK ==========
    kelompok_list = sorted(df_merge["Kelompok"].unique())
    kelimpahan_data = []
    
    for kelompok in kelompok_list:
        df_k = df_merge[df_merge["Kelompok"] == kelompok]
        row_data = {"Kategori": f"Kelimpahan {kelompok} ({satuan['kelimpahan']})"}
        values = []
        
        for stasiun in stasiun_order:
            df_st = df_k[df_k["Stasiun"] == stasiun]
            kelimpahan = len(df_st)  # Jumlah individu
            row_data[stasiun] = kelimpahan
            values.append(kelimpahan)
        
        rata_rata = sum(values) / len(stasiun_order) if values else 0
        row_data["Rata-rata"] = round(rata_rata, 2)
        kelimpahan_data.append(row_data)
    
    reports["Kelimpahan"] = pd.DataFrame(kelimpahan_data)
    
    # ========== 3. BIOMASSA PER KELOMPOK ==========
    biomassa_data = []
    
    for kelompok in kelompok_list:
        df_k = df_merge[df_merge["Kelompok"] == kelompok]
        row_data = {"Kategori": f"Biomassa {kelompok} ({satuan['biomassa']})"}
        values = []
        
        for stasiun in stasiun_order:
            df_st = df_k[df_k["Stasiun"] == stasiun]
            biomassa = df_st["Biomassa"].sum() if "Biomassa" in df_st.columns else 0
            row_data[stasiun] = round(biomassa, 2)
            values.append(biomassa)
        
        rata_rata = sum(values) / len(stasiun_order) if values else 0
        row_data["Rata-rata"] = round(rata_rata, 2)
        biomassa_data.append(row_data)
    
    reports["Biomassa"] = pd.DataFrame(biomassa_data)
    
    # ========== 4. KEANEKARAGAMAN JENIS PER KELOMPOK ==========
    keanekaragaman_data = []
    
    for kelompok in kelompok_list:
        df_k = df_merge[df_merge["Kelompok"] == kelompok]
        row_data = {"Kategori": f"Keanekaragaman Jenis {kelompok}"}
        values = []
        
        for stasiun in stasiun_order:
            df_st = df_k[df_k["Stasiun"] == stasiun]
            n_spesies = df_st["Spesies"].nunique() if "Spesies" in df_st.columns else 0
            row_data[stasiun] = n_spesies
            values.append(n_spesies)
        
        rata_rata = sum(values) / len(stasiun_order) if values else 0
        row_data["Rata-rata"] = round(rata_rata, 1)
        keanekaragaman_data.append(row_data)
    
    reports["Keanekaragaman"] = pd.DataFrame(keanekaragaman_data)
    
    # ========== 5. SHEET INFORMASI MODE ==========
    # Tambahkan sheet terpisah untuk dokumentasi mode & satuan
    info_data = {
        "Kategori": ["Mode Tampilan", "Satuan Kelimpahan", "Satuan Biomassa", "Area Survey", "Faktor Konversi ke/ha"],
        "Nilai": [
            mode_tampilan,
            satuan['kelimpahan'],
            satuan['biomassa'],
            "350 m²",
            "10,000 m² / 350 m² = 28.57"
        ]
    }
    reports["Info"] = pd.DataFrame(info_data)
    
    return reports


def generate_comprehensive_excel(df_merge, df_indeks, mode_tampilan="Data Terkonversi", stasiun_order=None):
    """
    Generate Excel multi-sheet dengan format laporan komprehensif.
    
    Parameters:
    -----------
    df_merge : DataFrame
    df_indeks : DataFrame
    mode_tampilan : str
        "Data Asli" atau "Data Terkonversi" (default: "Data Terkonversi")
    stasiun_order : list, optional
    
    Returns:
    --------
    BytesIO
        Excel file buffer siap untuk download
    """
    
    reports = prepare_comprehensive_report(df_merge, df_indeks, mode_tampilan, stasiun_order)
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for sheet_index, (sheet_name, df_report) in enumerate(reports.items()):
            df_report.to_excel(writer, sheet_name=sheet_name, index=False)
            
            worksheet = writer.sheets[sheet_name]
            
            # 🖌️ Format header - berbeda untuk sheet "Info"
            if sheet_name == "Info":
                header_fill = PatternFill(start_color="666666", end_color="666666", fill_type="solid")
            else:
                header_fill = PatternFill(start_color="003f5c", end_color="003f5c", fill_type="solid")
            
            header_font = Font(bold=True, color="FFFFFF", size=11)
            border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            for col_num, col_name in enumerate(df_report.columns, 1):
                cell = worksheet.cell(row=1, column=col_num)
                cell.value = col_name
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                cell.border = border
            
            # 🎨 Format data cells
            for row_num, row in enumerate(dataframe_to_rows(df_report, index=False, header=False), 2):
                for col_num, value in enumerate(row, 1):
                    cell = worksheet.cell(row=row_num, column=col_num)
                    cell.value = value
                    cell.border = border
                    
                    # Kolom pertama (Kategori) - bold
                    if col_num == 1:
                        cell.font = Font(bold=True)
                        cell.alignment = Alignment(horizontal='left', wrap_text=True)
                    
                    # Kolom Rata-rata (terakhir) - highlight
                    elif col_num == len(df_report.columns):
                        cell.fill = PatternFill(start_color="e8f4f8", end_color="e8f4f8", fill_type="solid")
                        cell.font = Font(bold=True)
                        cell.alignment = Alignment(horizontal='right')
                        if isinstance(value, (int, float)) and "." in str(value):
                            cell.number_format = '0.00'
                    
                    # Data cells (Stasiun) - right align
                    else:
                        cell.alignment = Alignment(horizontal='right')
                        if isinstance(value, (int, float)):
                            if "." in str(value):
                                cell.number_format = '0.00'
            
            # 📐 Auto column width
            for col_num, col_name in enumerate(df_report.columns, 1):
                col_letter = worksheet.cell(row=1, column=col_num).column_letter
                max_length = len(str(col_name))
                for row in worksheet.iter_rows(max_row=len(df_report) + 1, min_col=col_num, max_col=col_num):
                    try:
                        if len(str(row[0].value)) > max_length:
                            max_length = len(str(row[0].value))
                    except:
                        pass
                
                # Kategori kolom lebih lebar
                if col_num == 1:
                    worksheet.column_dimensions[col_letter].width = max(max_length + 3, 25)
                else:
                    worksheet.column_dimensions[col_letter].width = max(max_length + 2, 14)
            
            # Set row height untuk header
            worksheet.row_dimensions[1].height = 30
    
    buffer.seek(0)
    return buffer
