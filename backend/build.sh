#!/usr/bin/env bash
# Render build script

echo "🚀 Render build başlıyor..."

# Python bağımlılıklarını yükle
echo "📦 Python bağımlılıkları yükleniyor..."
pip install -r requirements.txt

# Node.js bağımlılıklarını yükle
echo "📦 Node.js bağımlılıkları yükleniyor..."
npm install

echo "✅ Build tamamlandı!" 