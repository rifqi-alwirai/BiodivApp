import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64

from konversi import konversi_biomassa, konversi_kelimpahan
from utils.ekspor_excel import prepare_tab, generate_excel_multisheet
from utils.loader import load_monitoring_file, load_basis_file
from utils.parser import parse_all_datauvc
from utils.indeks import (
    hitung_shannon,
    hitung_simpson,
    hitung_evenness,
    hitung_indeks_keseluruhan,
    hitung_indeks_per_stasiun
)
from utils.visual import (
    plot_indeks_ekologi,
    plot_pie_by_jenis,
    plot_pie_by_individu,
    plot_keanekaragaman_per_stasiun,
    plot_keanekaragaman_koralivora,
    plot_keanekaragaman_herbivora,
    plot_keanekaragaman_karnivora,
    plot_individu_per_stasiun,
    plot_kelimpahan_per_stasiun,
    plot_kelimpahan_koralivora,
    plot_kelimpahan_herbivora_famili,
    plot_kelimpahan_karnivora_famili,
    plot_biomassa_per_stasiun,
    plot_biomassa_by_kelompok,
    plot_biomassa_famili,
    plot_biomassa_by_spesies
)
from utils.summary import ringkasan_statistik
from utils.biomassa import hitung_biomassa

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="BiodivApp12", layout="wide")

bg_bin = get_base64_of_bin_file("assets/background.png")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
  background-image: url("data:image/png;base64,{bg_bin}");
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-blend-mode: darken;
  background-color: rgba(0, 0, 0, 0.7);
}}

[data-testid="stAppViewContainer"] > .main {{
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  padding: 1rem;
}}
</style>
""", unsafe_allow_html=True)

col_main, col_side = st.columns([7, 3])

with col_main:
    st.title("📊 BiodivApp12")
    st.markdown("""
    <div style="
        background-color:#003f5c;
        padding:15px;
        border-radius:10px;
        border:1px solid #2c587a;
        font-size:16px;
        color:white;
        line-height:1.5;
    ">
    Selamat datang di aplikasi analisis biodiversitas ikan karang 🐠<br>
    Semoga bermanfaat untuk para kolega konservasi semua 😉<br><br>
    <strong>Copyright © Al-wira’i, Rifqi Maulid 🤿</strong><br>
    <strong>Kontak: rifqi.maulid@gmail.com 📧</strong>
    </div>
    """, unsafe_allow_html=True)    

    st.header("📥 Unggah Data Monitoring")
    file_monitoring = st.file_uploader("Unggah file hasil monitoring:", type=["xlsx"], key="monitoring")

    st.header("📚 Unggah Basis Data Ikan")
    file_basis = st.file_uploader("Unggah basis data referensi:", type=["xlsx"], key="basis")

if file_monitoring and file_basis:
    data_uvc, kondisi_stasiun = load_monitoring_file(file_monitoring)
    basis_ikan = load_basis_file(file_basis)
    excel_file = pd.ExcelFile(file_monitoring)

    if data_uvc is not None and basis_ikan is not None:
        st.success("✅ Semua data berhasil dimuat!")

        # 🧼 Normalisasi kolom
        data_uvc.columns = data_uvc.columns.str.strip()
        basis_ikan.columns = basis_ikan.columns.str.strip()

        try:
            df_parsed = parse_all_datauvc(data_uvc)
        except ValueError as e:
            st.error(f"❌ {e}")
            st.stop()

        if df_parsed.empty:
            st.warning("⚠️ Tidak ada data berhasil diparsing. Pastikan ada entri berformat 'jumlah (ukuran)'.")
            st.stop()

        # Pilihan mode tampilan
        mode_tampilan = st.radio(
            "Pilih jenis tampilan data:",
            ["Data Asli", "Data Terkonversi"],
            index=1,
            horizontal=True
        )

        from utils.struktur import proses_semua_data
        df_merge = proses_semua_data(df_parsed, basis_ikan, mode_tampilan)

        # 📄 Baca metadata stasiun
        df_kondisi_stasiun = excel_file.parse("Kondisi_Stasiun")
        df_meta = df_kondisi_stasiun.set_index("Parameter").T
        df_meta.index.name = "Stasiun"
        df_meta.reset_index(inplace=True)

        with st.sidebar:
            st.markdown("### 🧭 Metadata Kondisi Stasiun")

            if "df_meta" in locals():
                stasiun_opsi = df_meta["Stasiun"].tolist()
                stasiun_terpilih = st.selectbox("Pilih Stasiun", stasiun_opsi)

                st_data = df_meta[df_meta["Stasiun"] == stasiun_terpilih].squeeze()

                st.markdown("#### 📌 Kondisi Lapangan:")
                for kolom in df_meta.columns:
                    if kolom == "Stasiun":
                        continue
                    nilai = st_data[kolom]
                    st.markdown(f"- **{kolom}**: {nilai if pd.notna(nilai) else '–'}")
            else:
                st.info("Sheet 'Kondisi_Stasiun' belum tersedia atau gagal dibaca.")

        # 🔠 Hitung indeks ekologi keseluruhan & per stasiun
        indeks_umum = hitung_indeks_keseluruhan(df_parsed)
        df_indeks = hitung_indeks_per_stasiun(df_parsed)

        # ✅ Tambahkan kolom "Indeks" gabungan jika belum tersedia
        if "Indeks" not in df_indeks.columns:
            kolom_indeks = [col for col in ["Shannon", "Simpson", "Evenness"] if col in df_indeks.columns]
            if kolom_indeks:
                df_indeks["Indeks"] = df_indeks[kolom_indeks].mean(axis=1)
            else:
                st.warning("⚠️ Tidak dapat menghitung indeks gabungan — kolom dasar belum tersedia")

        # ✅ Gabungkan seluruh data ke df_merge lewat fungsi modular

        from utils.struktur import proses_semua_data
        df_merge = proses_semua_data(df_parsed, basis_ikan, mode_tampilan)
        
        # ✅ Setup konversi kelimpahan
        from konversi import konversi_kelimpahan
        is_terkonversi = mode_tampilan == "Data Terkonversi"
        df_kelimpahan = df_parsed.copy()

        if is_terkonversi:
            df_kelimpahan["Kelimpahan_Terkonversi"] = True
            def konversi_groupcount(grouped):
                return konversi_kelimpahan(grouped)
        else:
            def konversi_groupcount(grouped):
                return grouped  # tidak dikonversi

        # 🌍 Tampilkan Indeks Ekologi Keseluruhan
        with st.expander("🌍 Indeks Ekologi Seluruh Monitoring", expanded=True):
            col1, col2, col3 = st.columns(3)

            nilai_shannon = indeks_umum.get("Shannon")
            nilai_evenness = indeks_umum.get("Evenness")
            nilai_simpson = indeks_umum.get("Simpson")

            col1.metric("🔠 Shannon", nilai_shannon if nilai_shannon is not None else "–")
            col2.metric("⚖️ Evenness", nilai_evenness if nilai_evenness is not None else "–")
            col3.metric("🧩 Simpson", nilai_simpson if nilai_simpson is not None else "–")

        # 📊 Tampilkan Indeks Ekologi per Stasiun
        with st.expander("📊 Indeks Ekologi per Stasiun", expanded=True):
            if not df_indeks.empty:
                stasiun_index = "Stasiun" if "Stasiun" in df_indeks.columns else None
                styled_df = df_indeks.set_index(stasiun_index).style if stasiun_index else df_indeks.style
                st.dataframe(styled_df.format(precision=3))
            else:
                st.warning("⚠️ Tidak ada indeks yang dapat dihitung dari data ini.")

        # Tambahan visual poin 2–3 di sini

        with st.expander("🥧 Komposisi Kelompok Berdasarkan Jumlah Jenis"):
            plot_pie_by_jenis(df_parsed)

        with st.expander("🥧 Komposisi Kelompok Berdasarkan Jumlah Individu"):
            plot_pie_by_individu(df_parsed)

        # ⬇️ Tambahkan di sini (Poin 4 - 14)

        # 📊 Visualisasi Keanekaragaman Jenis per Stasiun dan per Kelompok

        with st.expander("📊 Keanekaragaman Jenis per Stasiun (Semua Kelompok)"):
            plot_keanekaragaman_per_stasiun(df_parsed)

        with st.expander("📊 Keanekaragaman Jenis Ikan Koralivora per Stasiun"):
            plot_keanekaragaman_koralivora(df_parsed)

        with st.expander("📊 Keanekaragaman Jenis Herbivora per Stasiun"):
            plot_keanekaragaman_herbivora(df_parsed)

        with st.expander("📊 Keanekaragaman Jenis Karnivora per Stasiun"):
            plot_keanekaragaman_karnivora(df_parsed)

        # 📊 Visualisasi Kelimpahan Individu

        with st.expander("📊 Kelimpahan Ikan per Stasiun (berdasarkan Kelompok)"):
            plot_kelimpahan_per_stasiun(df_kelimpahan, konversi_groupcount, mode_tampilan)

        with st.expander("📊 Kelimpahan Ikan Koralivora per Famili per Stasiun"):
            plot_kelimpahan_koralivora(df_kelimpahan, konversi_groupcount, mode_tampilan)

        with st.expander("📊 Kelimpahan Herbivora per Famili per Stasiun"):
            plot_kelimpahan_herbivora_famili(df_kelimpahan, konversi_groupcount, mode_tampilan)

        with st.expander("📊 Kelimpahan Karnivora per Famili per Stasiun"):
            plot_kelimpahan_karnivora_famili(df_kelimpahan, konversi_groupcount, mode_tampilan)

       # ⚖️ Visualisasi Biomassa

        with st.expander("📊 Biomassa Ikan Herbivora & Karnivora per Stasiun"):
            plot_biomassa_per_stasiun(df_merge, mode_tampilan)

        with st.expander("📊 Biomassa Herbivora per Famili per Stasiun"):
            plot_biomassa_famili(df_merge, target_kelompok="Herbivora", mode_tampilan=mode_tampilan)

        with st.expander("📊 Biomassa Karnivora per Famili per Stasiun"):
            plot_biomassa_famili(df_merge, target_kelompok="Karnivora", mode_tampilan=mode_tampilan)
            
        #ringkasan statistik (poin 15)

        st.markdown("### 📋 Kesimpulan Statistik per Kelompok")
        df_summary = ringkasan_statistik(df_merge, df_indeks)
        st.dataframe(df_summary)

        with st.expander("🔍 Keterangan"):
            st.markdown("""
            - **Total Individu & Biomassa**: jumlah keseluruhan seluruh stasiun
            - **Rata-rata per stasiun**: dihitung dari rerata tiap stasiun
            - **Spesies Dominan**: spesies paling sering muncul (jumlah tertinggi)
            """)
            
            if "Indeks" not in df_merge.columns:
                df_merge = df_merge.merge(
                    df_indeks[["Stasiun", "Indeks"]],
                    on="Stasiun",
                    how="left"
                )

            df_merge = df_merge.rename(columns={
                "biomassa_total": "Biomassa",
                "abundance": "Kelimpahan",
                "shannon_index": "Keanekaragaman",
                "index_stasiun": "Indeks"
            })

        st.header("📤 Ekspor Biodiversitas Excel Multi-Sheet")

        group_by = st.radio("Tabulasi berdasarkan:", ["Spesies", "Famili"])
        value_cols = [col for col in ["Biomassa", "Kelimpahan", "Keanekaragaman"] if col in df_merge.columns]

        if not value_cols:
            st.warning("⚠️ Kolom untuk ekspor belum tersedia (Biomassa, Kelimpahan, Keanekaragaman).")
        else:
            # ✅ Preview tabulasi hanya jika value_cols tersedia
            st.markdown("### Preview Tabulasi")
            preview_tab = prepare_tab(df_merge, value_col=value_cols[0], group_by=group_by)
            st.dataframe(preview_tab.head(10))

            # ✅ Tombol ekspor
            if st.button("🧾 Unduh Excel Biodiversitas"):
                excel_buffer = generate_excel_multisheet(
                    df_base=df_merge,
                    group_by=group_by,
                    value_columns=value_cols
                )
                st.download_button(
                    label="📥 Unduh Excel Multi-Sheet",
                    data=excel_buffer.getvalue(),
                    file_name="BiodivApp_Export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )