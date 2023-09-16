import os
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    quality = int(request.form['quality'])

    if file:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        compressed_filename = os.path.join(app.config['COMPRESSED_FOLDER'], file.filename)

        file.save(filename)

        img = Image.open(filename)
        img.save(compressed_filename, optimize=True, quality=quality)

        return send_file(compressed_filename, as_attachment=True)
    return "Error"

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
