from flask import Flask, render_template, request
import pandas as pd
import pywhatkit
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def normalize_tel(tel):
    tel = ''.join(filter(str.isdigit, str(tel)))
    if tel.startswith('0'):
        return '+9' + tel
    elif not tel.startswith('90'):
        return '+90' + tel
    else:
        return '+' + tel

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mesaj = request.form.get('mesaj')
        excel_file = request.files.get('excel_file')
        manuel_input = request.form.get('manuel_numaralar')

        hedef_numaralar = set()

        # Excel dosyasından numaraları al
        if excel_file and excel_file.filename.endswith('.xlsx'):
            file_path = os.path.join(UPLOAD_FOLDER, excel_file.filename)
            excel_file.save(file_path)
            try:
                df = pd.read_excel(file_path)
                if 'Telefon' in df.columns:
                    for tel in df['Telefon']:
                        if pd.notna(tel):
                            hedef_numaralar.add(normalize_tel(tel))
            except Exception as e:
                return f"Excel okuma hatası: {e}"

        # Manuel girilen numaraları işle
        if manuel_input:
            manuel_list = manuel_input.split(',')
            for tel in manuel_list:
                tel = tel.strip()
                if tel:
                    hedef_numaralar.add(normalize_tel(tel))

        # Numara yoksa uyar
        if not hedef_numaralar:
            return "❌ Hiçbir numara belirtilmedi."

        # Mesajları gönder
        for i, numara in enumerate(hedef_numaralar):
            try:
                print(f"📤 Gönderiliyor: {numara}")
                pywhatkit.sendwhatmsg_instantly(numara, mesaj, wait_time=10, tab_close=True)
                print("✅ Gönderildi.")
                time.sleep(60)  # 1 dakika bekle
            except Exception as e:
                print(f"❌ Hata ({numara}): {e}")

        return "✅ Tüm mesajlar gönderildi!"

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
