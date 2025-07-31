from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import time
import os
import json
import subprocess
import threading
import queue
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Frontend'den gelen isteklere izin ver

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# WhatsApp Web.js için gerekli dosyalar
WHATSAPP_SCRIPT = 'whatsapp_sender.js'
WHATSAPP_CONFIG = 'whatsapp_config.json'

def normalize_tel(tel):
    """Telefon numarasını normalize eder"""
    tel = ''.join(filter(str.isdigit, str(tel)))
    if tel.startswith('0'):
        return '+9' + tel
    elif not tel.startswith('90'):
        return '+90' + tel
    else:
        return '+' + tel

def create_whatsapp_script():
    """WhatsApp Web.js script dosyasını oluşturur"""
    script_content = '''
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

// WhatsApp client oluştur
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// QR kod oluşturulduğunda
client.on('qr', (qr) => {
    console.log('QR_CODE:', qr);
});

// Client hazır olduğunda
client.on('ready', () => {
    console.log('READY');
});

// Mesaj gönderme fonksiyonu
async function sendMessage(phoneNumber, message) {
    try {
        const chatId = phoneNumber.includes('@c.us') ? phoneNumber : phoneNumber + '@c.us';
        await client.sendMessage(chatId, message);
        return { success: true, phoneNumber };
    } catch (error) {
        return { success: false, phoneNumber, error: error.message };
    }
}

// Ana fonksiyon
async function main() {
    const config = JSON.parse(process.argv[2]);
    const { phoneNumbers, message } = config;
    
    client.initialize();
    
    // Client hazır olana kadar bekle
    await new Promise((resolve) => {
        client.on('ready', resolve);
    });
    
    console.log('WhatsApp hazır, mesajlar gönderiliyor...');
    
    const results = [];
    for (const phoneNumber of phoneNumbers) {
        console.log(`Gönderiliyor: ${phoneNumber}`);
        const result = await sendMessage(phoneNumber, message);
        results.push(result);
        
        if (result.success) {
            console.log(`✅ Başarılı: ${phoneNumber}`);
        } else {
            console.log(`❌ Hata: ${phoneNumber} - ${result.error}`);
        }
        
        // Rate limiting - 2 saniye bekle
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    console.log('RESULTS:', JSON.stringify(results));
    client.destroy();
}

main().catch(console.error);
'''
    
    with open(WHATSAPP_SCRIPT, 'w', encoding='utf-8') as f:
        f.write(script_content)

def create_package_json():
    """package.json dosyasını oluşturur"""
    package_content = {
        "name": "whatsapp-oto-backend",
        "version": "1.0.0",
        "description": "WhatsApp Otomatik Mesaj Gönderici Backend",
        "main": "whatsapp_sender.js",
        "dependencies": {
            "whatsapp-web.js": "^1.23.0",
            "qrcode-terminal": "^0.12.0"
        },
        "scripts": {
            "start": "node whatsapp_sender.js"
        }
    }
    
    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(package_content, f, indent=2)

def install_dependencies():
    """Node.js bağımlılıklarını yükler"""
    try:
        subprocess.run(['npm', 'install'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"NPM install hatası: {e}")
        return False

def send_whatsapp_messages(phone_numbers, message):
    """WhatsApp mesajlarını gönderir"""
    config = {
        'phoneNumbers': phone_numbers,
        'message': message
    }
    
    # Config dosyasını oluştur
    with open(WHATSAPP_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    try:
        # WhatsApp script'ini çalıştır
        result = subprocess.run(
            ['node', WHATSAPP_SCRIPT, json.dumps(config)],
            capture_output=True,
            text=True,
            timeout=300  # 5 dakika timeout
        )
        
        if result.returncode == 0:
            return {'success': True, 'output': result.stdout}
        else:
            return {'success': False, 'error': result.stderr}
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Timeout: İşlem çok uzun sürdü'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/api/health', methods=['GET'])
def health_check():
    """API sağlık kontrolü"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'WhatsApp Oto Backend'
    })

@app.route('/api/send-messages', methods=['POST'])
def send_messages():
    """Mesaj gönderme API endpoint'i"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON verisi gerekli'}), 400
        
        message = data.get('message')
        phone_numbers = data.get('phone_numbers', [])
        excel_file = data.get('excel_file')  # Base64 encoded Excel file
        
        if not message:
            return jsonify({'error': 'Mesaj gerekli'}), 400
        
        if not phone_numbers and not excel_file:
            return jsonify({'error': 'Telefon numaraları veya Excel dosyası gerekli'}), 400
        
        hedef_numaralar = set()
        
        # Excel dosyasından numaraları al
        if excel_file:
            try:
                import base64
                import io
                
                # Base64'ten decode et
                excel_data = base64.b64decode(excel_file.split(',')[1])
                excel_io = io.BytesIO(excel_data)
                
                df = pd.read_excel(excel_io)
                if 'Telefon' in df.columns:
                    for tel in df['Telefon']:
                        if pd.notna(tel):
                            hedef_numaralar.add(normalize_tel(tel))
                else:
                    return jsonify({'error': 'Excel dosyasında "Telefon" sütunu bulunamadı'}), 400
                    
            except Exception as e:
                return jsonify({'error': f'Excel okuma hatası: {str(e)}'}), 400
        
        # Manuel numaraları ekle
        for tel in phone_numbers:
            if tel.strip():
                hedef_numaralar.add(normalize_tel(tel))
        
        if not hedef_numaralar:
            return jsonify({'error': 'Hiçbir geçerli numara bulunamadı'}), 400
        
        # WhatsApp mesajlarını gönder
        phone_list = list(hedef_numaralar)
        result = send_whatsapp_messages(phone_list, message)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Mesajlar başarıyla gönderildi',
                'sent_count': len(phone_list),
                'phone_numbers': phone_list
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({'error': f'Sunucu hatası: {str(e)}'}), 500

@app.route('/api/validate-numbers', methods=['POST'])
def validate_numbers():
    """Telefon numaralarını doğrular"""
    try:
        data = request.get_json()
        phone_numbers = data.get('phone_numbers', [])
        
        validated_numbers = []
        invalid_numbers = []
        
        for tel in phone_numbers:
            normalized = normalize_tel(tel)
            if len(normalized) >= 10:  # Basit doğrulama
                validated_numbers.append(normalized)
            else:
                invalid_numbers.append(tel)
        
        return jsonify({
            'valid_numbers': validated_numbers,
            'invalid_numbers': invalid_numbers,
            'total_valid': len(validated_numbers),
            'total_invalid': len(invalid_numbers)
        })
        
    except Exception as e:
        return jsonify({'error': f'Doğrulama hatası: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """WhatsApp bağlantı durumunu kontrol eder"""
    return jsonify({
        'status': 'ready',
        'timestamp': datetime.now().isoformat()
    })

# Render için başlangıçta gerekli dosyaları oluştur
def initialize_app():
    """Uygulama başlangıcında gerekli dosyaları oluşturur"""
    try:
        create_whatsapp_script()
        create_package_json()
        
        # Sadece development'ta bağımlılıkları yükle
        if os.environ.get('FLASK_ENV') != 'production':
            print("Node.js bağımlılıkları yükleniyor...")
            if install_dependencies():
                print("✅ Bağımlılıklar yüklendi")
            else:
                print("❌ Bağımlılık yükleme hatası")
    except Exception as e:
        print(f"Başlangıç hatası: {e}")

# Uygulama başlangıcında dosyaları oluştur
initialize_app()

if __name__ == '__main__':
    # Production için port ayarı
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 