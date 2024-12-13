from flask import Flask, request, send_from_directory, render_template
import qrcode
import os
from PIL import Image

app = Flask(__name__)

# upload folder to be relative to the location of app.py
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Save the file locally
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # file link
    file_link = f"/uploads/{file.filename}"

    # Generate a QR code for the file link
    qr_code_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file.filename}.png")
    qr = qrcode.QRCode()
    qr.add_data(f"http://127.0.0.1:9000{file_link}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_code_path)

    return render_template('success.html', file_link=file_link, qr_code_path=f"/qr_code/{file.filename}")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/qr_code/<filename>')
def qr_code(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], f"{filename}.png")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, threaded=False)