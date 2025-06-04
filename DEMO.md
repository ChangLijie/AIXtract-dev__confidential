# 🧠 AIXtract Demo

This script provides a simple UI for **AIXtract**.  
The frontend is built with **Streamlit** for easy interaction.

---

## 📦 Pre-installation

> ✅ **Recommended Python version**: `3.8+`

### 💡 (Optional) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       
```

### 1. Install AIXtract backend dependencies

```bash
pip install -r requirements.txt
```
### 2. Install frontend (UI) dependencies

```bash
pip install streamlit PyMuPDF pillow

```

## 🚀 Run the UI
```bash
streamlit run run_demo_ui.py
```
This will start the AIXtract visual interface in your browser.

## 🗂 Recommended Project Structure

Please make sure to place the PDF files you want to process inside the **`data/`** folder.
```kotlin
AIXtract/
├── run_demo_ui.py
├── data/
│   └── EMPU_3401_Datasheet.pdf ← PDF files should be placed here
└── requirements.txt
```
