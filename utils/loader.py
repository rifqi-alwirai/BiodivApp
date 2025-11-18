import pandas as pd
import streamlit as st

def load_monitoring_file(file):
    try:
        xls = pd.ExcelFile(file)
        data_uvc = pd.read_excel(xls, sheet_name="Data_UVC")
        kondisi_stasiun = pd.read_excel(xls, sheet_name="Kondisi_Stasiun")
        
        # Bersihkan nama kolom agar tidak ada spasi tersembunyi
        data_uvc.columns = data_uvc.columns.str.strip()
        kondisi_stasiun.columns = kondisi_stasiun.columns.str.strip()

        return data_uvc, kondisi_stasiun
    except Exception as e:
        st.error(f"❌ Gagal memuat file monitoring: {e}")
        return None, None

def load_basis_file(file):
    try:
        xls = pd.ExcelFile(file)
        basis_ikan = pd.read_excel(xls, sheet_name="Basis_Ikan")
        basis_ikan.columns = basis_ikan.columns.str.strip()
        return basis_ikan
    except Exception as e:
        st.error(f"❌ Gagal memuat basis ikan: {e}")
        return None