# 🧠 Smart Product Information Extractor using OCR 🧾

This is a Flask-based web application that extracts useful product information like **MRP**, **Expiry Date**, and **Manufacturing Date** from uploaded images using **OCR (Optical Character Recognition)**.

---

## 📂 Project Structure

myproject/
│
├── .vscode/ # VSCode settings (ignored in Git)
├── data/ # Optional data folder
├── static/
│ └── uploads/ # Image uploads (ignored in Git)
├── templates/
│ └── index.html # Main frontend UI
├── app.py # Main Flask backend
├── .gitignore # Git ignore rules
└── README.md # Project description

---

## 🚀 Features

- Upload a product label image
- Extract text using Tesseract OCR
- Preprocess image using OpenCV
- Identify:
  - MRP (Price)
  - Expiry Date
  - Manufacturing Date
- Stylish UI with preview and loader

---

## ⚙️ Setup Instructions

1. **Clone this repo**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. **Create a virtual environment**:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate

3. **Install requirements**:
   ```bash
    pip install -r requirements.txt

4. **Run the app**:
   ```bash
    python app.py


##   📦 Requirements
Make sure the following are installed:

    • Flask
    • OpenCV (cv2)
    • pytesseract
    • Pillow

## 👨‍💻 Author
Fahad Hashmi


