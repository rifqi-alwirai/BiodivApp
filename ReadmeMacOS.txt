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

=========================================
📘 Panduan Instalasi & Penggunaan BiodivApp12 (macOS)
=========================================

Versi: 1.0
Pengembang: Rifqi
Tujuan: Aplikasi visualisasi monitoring biodiversitas laut berbasis Streamlit

--------------------------------------------------
🖥️ Persiapan Awal
--------------------------------------------------

1. Ekstrak folder BiodivApp ke dalam:
   ~/Documents/BiodivApp/

2. Pastikan isi folder mencakup:
   - app.py
   - BiodivApp_requirements.txt
   - setup_env.sh
   - setup_env.command
   - run_app.command
   - [utils/, data/, env/, dll]

--------------------------------------------------
📦 Instalasi Pertama (Wajib Sekali Saja)
--------------------------------------------------

1. Klik dua kali file: setup_env.command

   Yang terjadi:
   - Membuat virtual environment `env/`
   - Install dependencies dari BiodivApp_requirements.txt
   - Menjalankan aplikasi Streamlit

2. Jika muncul pesan "file rusak" atau gagal klik:
   a. Buka Terminal (Cmd + Space → ketik "Terminal")
   b. Jalankan:

      cd ~/Documents/BiodivApp
      chmod +x setup_env.command

   Lalu coba klik lagi file tersebut.

3. Jangan tutup Terminal selama proses berjalan agar aplikasi tetap aktif

--------------------------------------------------
🚀 Menjalankan Ulang Aplikasi (Setelah Setup)
--------------------------------------------------

1. Klik dua kali file: run_app.command

   Ini akan:
   - Mengaktifkan virtual environment
   - Menjalankan BiodivApp di browser

--------------------------------------------------
🛠️ Cara Membuat File Setup Secara Manual di macOS
--------------------------------------------------

📌 Semua pembuatan dilakukan via Terminal

1. Buka Terminal dan masuk ke folder proyek:

      cd ~/Documents/BiodivApp

2. Buat file `setup_env.sh`:

      nano setup_env.sh

   Isi dengan:

      #!/bin/bash
      python3 -m venv env
      source env/bin/activate
      pip install -r BiodivApp_requirements.txt
      streamlit run app.py

   Simpan:
   - Tekan Control + O → Enter → Control + X

   Lalu beri izin:

      chmod +x setup_env.sh

---

3. Buat file `setup_env.command`:

      nano setup_env.command

   Isi dengan:

      #!/bin/bash
      cd "$HOME/Documents/BiodivApp"
      chmod +x setup_env.sh
      ./setup_env.sh

   Simpan dan beri izin:

      chmod +x setup_env.command

---

4. Buat file `run_app.command`:

      nano run_app.command

   Isi dengan:

      #!/bin/bash
      cd "$HOME/Documents/BiodivApp"
      source env/bin/activate
      streamlit run app.py

   Simpan dan beri izin:

      chmod +x run_app.command

📌 Sekarang pengguna bisa klik dua kali file `.command` untuk menjalankan aplikasi langsung dari Finder

--------------------------------------------------
⚠️ Hal-Hal Penting yang Perlu Diperhatikan
--------------------------------------------------

✅ Wajib:
- Simpan dan buat file `.sh` dan `.command` langsung dari macOS
- Format baris harus UNIX (LF) agar tidak muncul error `/bin/bash^M`

🔍 Jika muncul error seperti:

    bad interpreter: /bin/bash^M

→ Solusinya:
- Buat ulang file via nano (lihat bagian "Cara Membuat File Setup")

--------------------------------------------------
📁 Struktur Folder Final yang Disarankan
--------------------------------------------------

BiodivApp/
├── app.py
├── setup_env.sh
├── setup_env.command
├── run_app.command
├── BiodivApp_requirements.txt
├── utils/
├── data/
└── env/   ← otomatis dibuat setelah instalasi

--------------------------------------------------
📬 Kontak Teknis
--------------------------------------------------

Pengelola: Rifqi
Pertanyaan atau permintaan modifikasi:
Silakan hubungi via email atau grup internal konservasi laut
