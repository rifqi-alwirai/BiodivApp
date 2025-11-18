@echo off
echo ================================
echo 🐟 Biodiversitas App Installer 🐟
echo ================================

echo 🔹 Membuat virtual environment baru...
python -m venv venv

echo 🔹 Mengaktifkan environment...
call venv\Scripts\activate

echo 🔹 Upgrade pip ke versi terbaru...
python -m pip install --upgrade pip

echo 🔹 Install semua package dari BiodivApp_requirements.txt...
pip install --upgrade -r BiodivApp_requirements.txt

echo.
echo ✅ Setup selesai!
echo Untuk menjalankan aplikasi, gunakan perintah berikut:
echo streamlit run app.py
pause