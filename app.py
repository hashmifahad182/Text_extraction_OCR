from flask import Flask, render_template, request
import pytesseract
import cv2
import os
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def normalize_date(raw):
    raw = raw.replace('-', '/').replace(' ', '')
    date_formats = ['%d/%m/%Y', '%d/%m/%y', '%m/%Y', '%m/%y', '%Y/%m/%d', '%Y/%d/%m']

    for fmt in date_formats:
        try:
            parsed = datetime.strptime(raw, fmt)
            return parsed.strftime('%d/%m/%Y')
        except ValueError:
            continue
    return raw  

def extract_fields_from_text(text):
    lines = text.split('\n')
    data = {
        "MRP": "Not found",
        "Expiry Date": "Not found",
        "Manufacturing Date": "Not found"
    }

    expiry_keywords = ['exp', 'expiry', 'exp date', 'best before', 'use by','Expiry Date','EXP ']
    mfg_keywords = ['mfg','Mfg Date', 'manufacturing', 'mfd', 'manuf date', 'packed on','MFD']
    # mrp_keywords=['MRP ','mrp','price']

    for line in lines:
        line_clean = line.strip().lower()

        if "mrp" in line_clean or "price" in line_clean or "MRP ₹" in line_clean or "MRP " in line_clean:
            value = ''.join([c for c in line if c.isdigit() or c == '₹' or c == '.'])
            if value:
                data["MRP"] = value

        elif any(keyword in line_clean for keyword in expiry_keywords):
            possible_date = ''.join([c for c in line if c.isdigit() or c in ['/', '-', ' ']])
            formatted = normalize_date(possible_date.strip())
            if formatted:
                data["Expiry Date"] = formatted

        elif any(keyword in line_clean for keyword in mfg_keywords):
            possible_date = ''.join([c for c in line if c.isdigit() or c in ['/', '-', ' ']])
            formatted = normalize_date(possible_date.strip())
            if formatted:
                data["Manufacturing Date"] = formatted

    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_data = {}
    image_url = None
    error = None
    full_text = None

    if request.method == 'POST':
        if 'image' not in request.files:
            error = 'No file part in request.'
        else:
            file = request.files['image']
            if file.filename == '':
                error = 'No selected file.'
            else:
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)
                image_url = image_path

                try:
                    processed = preprocess_image(image_path)
                    pil_img = Image.fromarray(processed)
                    text = pytesseract.image_to_string(pil_img)

                    full_text = text

                    extracted_data = extract_fields_from_text(text)
                except Exception as e:
                    error = f"Error processing image: {str(e)}"

    return render_template('index.html', data=extracted_data, image=image_url, error=error, full_text=full_text)

if __name__ == '__main__':
    app.run(debug=True)
