#!/bin/bash
python3 -m venv env
source env/bin/activate
pip install -r BiodivApp_requirements.txt
streamlit run app.py
