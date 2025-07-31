# WhatsApp Otomatik Mesaj Gönderici

Bu proje, `whatsapp-web.js` kullanarak WhatsApp üzerinden otomatik mesaj göndermenizi sağlar. Modern bir frontend/backend mimarisi ile geliştirilmiştir.

## 🏗️ Mimari

- **Frontend**: Next.js + React + TypeScript + Tailwind CSS (Vercel'de deploy)
- **Backend**: Flask + Python (Heroku/Railway'de deploy)
- **WhatsApp API**: whatsapp-web.js (Node.js)

## 🚀 Özellikler

- ✅ Modern React frontend
- ✅ RESTful API backend
- ✅ Excel dosyasından telefon numaralarını okuma
- ✅ Manuel numara girişi
- ✅ Drag & drop dosya yükleme
- ✅ Real-time bildirimler
- ✅ Responsive tasarım
- ✅ TypeScript desteği
- ✅ CORS desteği

## 📁 Proje Yapısı

```
whatsapp_oto/
├── frontend/                 # React/Next.js Frontend
│   ├── app/
│   │   ├── page.tsx         # Ana sayfa
│   │   ├── layout.tsx       # Layout bileşeni
│   │   └── globals.css      # Global stiller
│   ├── package.json         # Frontend bağımlılıkları
│   ├── next.config.js       # Next.js konfigürasyonu
│   ├── tailwind.config.js   # Tailwind CSS konfigürasyonu
│   └── vercel.json          # Vercel deploy konfigürasyonu
├── backend/                  # Flask Backend
│   ├── app.py               # Ana Flask uygulaması
│   ├── requirements.txt     # Python bağımlılıkları
│   └── Procfile            # Heroku/Railway deploy konfigürasyonu
└── README.md               # Bu dosya
```

## 🛠️ Kurulum

### Backend Kurulumu

1. **Backend klasörüne gidin:**
```bash
cd backend
```

2. **Python bağımlılıklarını yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Backend'i çalıştırın:**
```bash
python app.py
```

Backend `http://localhost:5000` adresinde çalışacaktır.

### Frontend Kurulumu

1. **Frontend klasörüne gidin:**
```bash
cd frontend
```

2. **Node.js bağımlılıklarını yükleyin:**
```bash
npm install
```

3. **Frontend'i çalıştırın:**
```bash
npm run dev
```

Frontend `http://localhost:3000` adresinde çalışacaktır.

## 🚀 Deploy

### Backend Deploy (Heroku/Railway)

1. **Heroku için:**
```bash
cd backend
heroku create your-app-name
git add .
git commit -m "Initial backend deployment"
git push heroku main
```

2. **Railway için:**
- Railway dashboard'da yeni proje oluşturun
- GitHub repo'nuzu bağlayın
- Backend klasörünü deploy edin

### Frontend Deploy (Vercel)

1. **Vercel CLI ile:**
```bash
cd frontend
vercel
```

2. **Vercel Dashboard ile:**
- Vercel'de yeni proje oluşturun
- GitHub repo'nuzu bağlayın
- Frontend klasörünü deploy edin

### Environment Variables

Frontend'de `.env.local` dosyası oluşturun:
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com
```

## 📱 Kullanım

1. **Frontend'e erişin:** `https://your-frontend.vercel.app`
2. **Excel dosyası yükleyin** veya **manuel numara girin**
3. **Mesajınızı yazın**
4. **Gönder butonuna tıklayın**

## 🔧 API Endpoints

### Backend API

- `GET /api/health` - Sağlık kontrolü
- `POST /api/send-messages` - Mesaj gönderme
- `POST /api/validate-numbers` - Numara doğrulama
- `GET /api/status` - Durum kontrolü

### Örnek API Kullanımı

```javascript
// Mesaj gönderme
const response = await fetch('https://your-backend.herokuapp.com/api/send-messages', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Merhaba!',
    phone_numbers: ['+905321234567'],
    excel_file: null
  })
})
```

## 📊 Excel Dosya Formatı

Excel dosyanızda "Telefon" sütunu bulunmalıdır:

| Telefon      | Ad    | Diğer Bilgiler |
|--------------|-------|----------------|
| +905321234567| Ahmet | ...            |
| 05341234567  | Ayşe  | ...            |

## ⚠️ Önemli Notlar

- **Rate Limiting**: Mesajlar arasında 2 saniye bekleme süresi
- **WhatsApp Kuralları**: WhatsApp'ın kullanım şartlarına uygun kullanın
- **QR Kod**: İlk kullanımda QR kodu okutmanız gerekir
- **CORS**: Backend CORS ayarları yapılandırılmıştır

## 🐛 Sorun Giderme

### Backend Sorunları
```bash
# Logları kontrol edin
heroku logs --tail

# Bağımlılıkları yeniden yükleyin
pip install -r requirements.txt
```

### Frontend Sorunları
```bash
# Node modules'u temizleyin
rm -rf node_modules package-lock.json
npm install

# Build cache'ini temizleyin
npm run build
```

### CORS Sorunları
- Backend'de CORS ayarlarını kontrol edin
- Frontend URL'ini backend CORS ayarlarına ekleyin

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım için WhatsApp'ın resmi API'lerini kullanmanız önerilir.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📞 Destek

Sorunlarınız için GitHub Issues bölümünü kullanabilirsiniz. 