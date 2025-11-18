# BiodivApp12 — Aplikasi Analisis Biodiversitas Ikan Karang 🐠

**Pengembang:** Rifqi Maulid (@al-wira’i)  
**Hak Cipta:** © 2025  
**Kontak:** rifqi.maulid@gmail.com  

## 🎯 Tujuan
BiodivApp12 adalah aplikasi berbasis Streamlit untuk memvisualisasikan dan menganalisis data monitoring ikan karang berdasarkan biomassa, kelimpahan, indeks ekologi, dan persebaran per stasiun. Dirancang untuk mendukung tim konservasi dan masyarakat pesisir dalam interpretasi hasil survei bawah laut.

## 🔧 Fitur Utama
- Parsing data UVC (jumlah dan ukuran)
- Perhitungan indeks Shannon, Simpson, dan Evenness
- Visualisasi biomassa & kelimpahan per kelompok/famili
- Ekspor Excel multi-sheet berdasarkan spesies dan famili
- Mode konversi ke satuan per hektar

## 📦 Dependensi Utama (Bebas Pakai)
- Streamlit, Pandas, NumPy
- Matplotlib, Seaborn, openpyxl, XlsxWriter
- Plotly, scikit-learn, SciPy
- xlrd

Semua library diinstal melalui `BiodivApp_requirements.txt` dan tunduk pada lisensi open-source (MIT, BSD, Apache 2.0).

## 💾 Instalasi

=======================================
📦 Panduan Instalasi & Pemakaian BiodivApp12
=======================================

Versi: 1.0
Pengembang: Rifqi
Tujuan: Aplikasi visualisasi monitoring biodiversitas laut

--------------------------------------------------
🖥️ Cara Instalasi di Windows
--------------------------------------------------

1. Ekstrak folder 'BiodivApp' ke lokasi aman, misalnya: C:\BiodivApp12

2. Klik dua kali file:
   - setup_env.bat   → Untuk membuat environment dan menginstal pustaka
   - run_app.bat     → Untuk menjalankan aplikasi

3. Aplikasi akan terbuka di browser melalui Streamlit

*Pastikan sudah terinstal Python 3.8+*

--------------------------------------------------
🍎 Cara Instalasi di MacOS
--------------------------------------------------

1. Ekstrak folder 'BiodivApp' ke dalam folder:
   ~/Documents/BiodivApp/

2. Klik dua kali file:
   setup_env.command   → Proses setup dan menjalankan app secara otomatis

*Jika file tidak bisa dijalankan:*

- Buka Terminal (Cmd + Space → ketik "Terminal")
- Jalankan perintah:
  chmod +x ~/Documents/BiodivApp/setup_env.command

3. Aplikasi akan terbuka di browser secara otomatis

--------------------------------------------------
⚠️ Troubleshooting Virtualenv
--------------------------------------------------

- Jika muncul error 'ModuleNotFoundError':
  → Pastikan virtual environment aktif dan install ulang:
     pip install -r BiodivApp_requirements.txt

- Jika Streamlit tidak terdeteksi:
  → Install manual dengan: pip install streamlit

- Jika menggunakan chip M1/M2:
  → Install freetype dengan Homebrew:
     brew install freetype
     pip install matplotlib --no-binary :all:

--------------------------------------------------
📁 Struktur Folder Direkomendasikan
--------------------------------------------------

BiodivApp/
├── app.py
├── setup_env.bat               ← Windows
├── run_app.bat                 ← Windows
├── setup_env.sh                ← MacOS shell
├── setup_env.command           ← MacOS klik langsung
├── BiodivApp_requirements.txt  ← pustaka Python
├── data/                       ← data monitoring
├── utils/                      ← modul visualisasi dan tools
├── env/                        ← virtualenv (otomatis dibuat)

--------------------------------------------------
✅ Tips
--------------------------------------------------

- Pastikan koneksi internet saat pertama install
- Jalankan dengan virtualenv agar tidak ganggu Python sistem
- Untuk pemakaian tim, cukup kirim file ZIP berisi folder BiodivApp
- Jangan mengedit .command/.bat tanpa cek isi

--------------------------------------------------
📬 Kontak Teknis
--------------------------------------------------

Pengelola: Rifqi
Pertanyaan teknis: silakan hubungi via email atau grup internal konservasi

# 🐠 BiodivApp – Aplikasi Visualisasi Biodiversitas Ikan Karang

**BiodivApp** adalah aplikasi berbasis Streamlit yang dirancang untuk memvisualisasikan dan menganalisis keanekaragaman hayati ikan karang berdasarkan data ekologis lapangan. Aplikasi ini dirancang secara interaktif, fleksibel, dan siap pakai untuk konservasi, penelitian, atau edukasi.

## 🚀 Fitur Utama

- 📊 Visualisasi kelimpahan ikan per stasiun dan famili
- ⚖️ Visualisasi biomassa herbivora dan karnivora
- 🧬 Indeks ekologi (Shannon, Simpson, Evenness)
- 🌀 Mode tampilan: Data Asli vs Data Terkonversi (per hektar atau kg/ha)
- 📌 Label total individu atau biomassa di atas grafik batang
- 🎨 Skema warna ramah pembaca berdasarkan kelompok dan famili
- 🔁 Arsitektur modular dan mudah dikembangkan

## 🧱 Struktur Folder
├── app.py                 # Entry point utama Streamlit 
├── visual.py             # Kumpulan fungsi visualisasi
├── konversi.py           # Logika konversi satuan
├── data/                 # Folder untuk file CSV atau Excel
├── assets/               # Ikon, logo, atau palet warna
└── README.md             # Dokumentasi proyek


## 🛠️ Cara Menjalankan

1. Pastikan Python & pip sudah ter-install
2. Aktifkan virtual environment (opsional namun disarankan)
3. Install dependensi:

```bash
pip install -r requirements.txt

4. Jalankan aplikasi:

streamlit run app.py

📦 Mode Distribusi
Untuk mengubah menjadi aplikasi .exe:
pip install pyinstaller
echo streamlit run app.py > run_app.py
pyinstaller --onefile run_app.py

📁 Catatan Perkembangan (per 7 Juli 2025)
- ✅ Refactor seluruh fungsi visualisasi kelimpahan & biomassa agar responsif terhadap mode_tampilan
- ✅ Tambahkan label total di atas batang bertumpuk
- ✅ Perbaikan label sumbu Y dinamis (gram ↔ kg/ha)
- ✅ Menyusun strategi distribusi .exe
🤝 Kontribusi
Proyek ini dapat digunakan dan dikembangkan untuk kegiatan konservasi, pendidikan, atau riset komunitas. Ingin kontribusi atau ajukan fitur? Silakan kontak langsung ✉️

---

==============================================
📝 BIODIVAPP - Fitur Ekspor Biodiversitas (.xlsx)
==============================================

Versi: Refactor Ekspor Ekologis
Tanggal: [Update Terakhir: Juli 2025]

Penanggung jawab: Rifqi
Tujuan: Menyusun data biodiversitas berbasis UVC dalam format Excel yang terstruktur secara ekologis, untuk keperluan analisis dan pelaporan konservasi.

------------------------------------------------------------
1. 📦 Struktur Sheet Excel Hasil Ekspor
------------------------------------------------------------
- Setiap sheet menyajikan nilai agregat (biomassa, kelimpahan, keanekaragaman) per stasiun
- Sheet terbagi berdasarkan jenis data:
  - Sheet: "Biomassa"
  - Sheet: "Kelimpahan"
  - Sheet: "Keanekaragaman"

------------------------------------------------------------
2. 📊 Pengurutan Famili dan Spesies
------------------------------------------------------------
✅ Urutan Famili (berdasarkan kelompok ekologis):
  1. Chaetodontidae      → Koralivora
  2. Acanthuridae        → Herbivora
  3. Scaridae            → Herbivora
  4. Siganidae           → Herbivora
  5. Haemulidae          → Karnivora
  6. Lethrinidae         → Karnivora
  7. Lutjanidae          → Karnivora
  8. Serranidae          → Karnivora

✅ Urutan Spesies:
  - Spesies dikelompokkan sesuai famili di atas
  - Diurutkan alfabetis A–Z dalam masing-masing famili

------------------------------------------------------------
3. ⚙️ Fungsi Kunci
------------------------------------------------------------
- `prepare_tab(df, value_col, group_by, stasiun_order)`:
  → Membentuk tabulasi ekspor dengan urutan ekologis
- `generate_excel_multisheet(...)`:
  → Menghasilkan file .xlsx multi-sheet dengan styling & highlight dominan

------------------------------------------------------------
4. 📥 Catatan Penggunaan
------------------------------------------------------------
- Data yang diekspor berasal dari `df_merge` (hasil visualisasi dan konversi)
- Kolom penting: "Stasiun", "Famili", "Spesies", "Biomassa", "Kelimpahan", "Keanekaragaman"
- Validasi visual dan manual tetap disarankan sebelum digunakan dalam publikasi resmi

------------------------------------------------------------
5. 🔜 To-Do Berikutnya
------------------------------------------------------------
[ ] Audit perbedaan nilai ekspor vs hitungan manual
[ ] Tambah metadata stasiun ke sheet baru
[ ] Tambah ekspor CSV / PDF
[ ] Preview sheet sebelum unduh
[ ] Filter spesifik per kelompok / habitat / lokasi

------------------------------------------------------------
Terima kasih sudah menggunakan BiodivApp.
Selamat beristirahat 🌊
------------------------------------------------------------
