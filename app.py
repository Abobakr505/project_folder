from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    # استلام النص الذي أدخله المستخدم
    qr_text = request.form['qr_text']
    
    # إنشاء كود QR
    img = qrcode.make(qr_text)
    
    # إنشاء كائن بايت في الذاكرة
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)  # إعادة المؤشر إلى البداية

    # تحويل الصورة إلى base64
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    # عرض الصورة مع زر التحميل
    return render_template('index.html', img_base64=img_base64)

@app.route('/download_qr')
def download_qr():
    # تنزيل الصورة بشكل مؤقت
    img_bytes = BytesIO()
    img_bytes.write(base64.b64decode(request.args.get('img_bytes')))
    img_bytes.seek(0)  # إعادة المؤشر إلى البداية
    
    return send_file(img_bytes, as_attachment=True, download_name="qr_code.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
