from flask import Flask, render_template, request, send_file, url_for
import qrcode
import os

app = Flask(__name__)

# تأكد من وجود مجلد static، وإذا لم يكن موجودًا، أنشئه
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    # استلام النص الذي أدخله المستخدم
    qr_text = request.form['qr_text']
    
    # إنشاء كود QR
    img = qrcode.make(qr_text)
    
    # حفظ الصورة مؤقتًا في ملف
    img_path = "static/qr_code.png"  # حفظ الصورة في مجلد static
    img.save(img_path)
    
    # عرض الصورة مع زر التحميل
    return render_template('index.html', qr_image=img_path)

@app.route('/download_qr')
def download_qr():
    # تنزيل الصورة من المسار المحفوظ
    img_path = "static/qr_code.png"
    return send_file(img_path, as_attachment=True, download_name="qr_code.png")

if __name__ == '__main__':
    app.run(debug=True)
