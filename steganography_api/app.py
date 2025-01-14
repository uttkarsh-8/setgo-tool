from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from simple_steganography import SimpleImageSteganography

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/hide', methods=['POST'])
def hide_message():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    message = request.form.get('message', '')
    password = request.form.get('password', '')
    
    if not message or not password:
        return jsonify({'error': 'Message and password are required'}), 400
    
    try:
        input_filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        file.save(input_path)
        
        output_filename = f"hidden_{input_filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        stego = SimpleImageSteganography()
        stego.hide_message(input_path, message, password, output_path)
        
        return send_file(output_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract', methods=['POST'])
def extract_message():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    password = request.form.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    try:
        input_filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        file.save(input_path)
        
        stego = SimpleImageSteganography()
        message = stego.extract_message(input_path, password)
        
        if message is None:
            return jsonify({'error': 'No message found'}), 404
        
        return jsonify({'message': message})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)