'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import toast, { Toaster } from 'react-hot-toast'
import { 
  Upload, 
  MessageSquare, 
  Phone, 
  FileSpreadsheet, 
  Send, 
  Loader2,
  CheckCircle,
  AlertCircle,
  Info
} from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export default function Home() {
  const [message, setMessage] = useState('')
  const [phoneNumbers, setPhoneNumbers] = useState('')
  const [excelFile, setExcelFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [uploadedFileName, setUploadedFileName] = useState('')

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
      setExcelFile(file)
      setUploadedFileName(file.name)
      toast.success('Excel dosyası yüklendi!')
    } else {
      toast.error('Lütfen geçerli bir Excel (.xlsx) dosyası seçin!')
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    multiple: false
  })

  const normalizePhoneNumbers = (numbers: string) => {
    return numbers
      .split(',')
      .map(num => num.trim())
      .filter(num => num.length > 0)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!message.trim()) {
      toast.error('Lütfen bir mesaj girin!')
      return
    }

    if (!phoneNumbers.trim() && !excelFile) {
      toast.error('Lütfen telefon numaraları girin veya Excel dosyası yükleyin!')
      return
    }

    setIsLoading(true)

    try {
      const phoneNumbersList = normalizePhoneNumbers(phoneNumbers)
      let excelFileBase64 = null

      if (excelFile) {
        const reader = new FileReader()
        excelFileBase64 = await new Promise((resolve) => {
          reader.onload = () => resolve(reader.result)
          reader.readAsDataURL(excelFile)
        })
      }

      const response = await axios.post(`${API_URL}/api/send-messages`, {
        message: message.trim(),
        phone_numbers: phoneNumbersList,
        excel_file: excelFileBase64
      })

      if (response.data.success) {
        toast.success(`✅ ${response.data.sent_count} mesaj başarıyla gönderildi!`)
        setMessage('')
        setPhoneNumbers('')
        setExcelFile(null)
        setUploadedFileName('')
      } else {
        toast.error(`❌ Hata: ${response.data.error}`)
      }
    } catch (error: any) {
      console.error('Error:', error)
      toast.error(`❌ Sunucu hatası: ${error.response?.data?.error || error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700">
      <Toaster position="top-right" />
      
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">
              📲 WhatsApp Mesaj Gönderici
            </h1>
            <p className="text-white/80">
              Toplu WhatsApp mesajları göndermek için modern ve güvenli platform
            </p>
          </div>

          {/* Main Form */}
          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              
              {/* Excel Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <FileSpreadsheet className="inline w-4 h-4 mr-2" />
                  Excel Dosyası Yükle (.xlsx)
                </label>
                <div
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                    isDragActive 
                      ? 'border-blue-500 bg-blue-50' 
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <input {...getInputProps()} />
                  <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  {uploadedFileName ? (
                    <p className="text-sm text-green-600 font-medium">
                      ✅ {uploadedFileName}
                    </p>
                  ) : (
                    <div>
                      <p className="text-sm text-gray-600">
                        {isDragActive 
                          ? 'Dosyayı buraya bırakın...' 
                          : 'Dosyayı sürükleyin veya tıklayın'
                        }
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        Sadece .xlsx dosyaları kabul edilir
                      </p>
                    </div>
                  )}
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  Excel dosyasında "Telefon" sütunu bulunmalıdır
                </p>
              </div>

              {/* Manual Phone Numbers */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Phone className="inline w-4 h-4 mr-2" />
                  Manuel Telefon Numaraları
                </label>
                <textarea
                  value={phoneNumbers}
                  onChange={(e) => setPhoneNumbers(e.target.value)}
                  placeholder="+905321234567, 05341234567, +905551234567"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  rows={3}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Birden fazla numara için virgül kullanın
                </p>
              </div>

              {/* Message */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <MessageSquare className="inline w-4 h-4 mr-2" />
                  Mesaj
                </label>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Göndermek istediğiniz mesajı buraya yazın..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  rows={6}
                  required
                />
              </div>

              {/* Info Box */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-start">
                  <Info className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
                  <div className="text-sm text-blue-800">
                    <p className="font-medium mb-2">Önemli Bilgiler:</p>
                    <ul className="space-y-1 text-xs">
                      <li>• Mesajlar arasında 2 saniye bekleme süresi vardır</li>
                      <li>• İlk kullanımda WhatsApp Web QR kodunu okutmanız gerekir</li>
                      <li>• WhatsApp kurallarına uygun kullanın</li>
                      <li>• Çok fazla mesaj göndermekten kaçının</li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-purple-700 focus:ring-4 focus:ring-blue-300 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Mesajlar Gönderiliyor...
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5 mr-2" />
                    Mesaj Gönder
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Footer */}
          <div className="text-center mt-8">
            <p className="text-white/60 text-sm">
              © 2024 WhatsApp Mesaj Gönderici. Eğitim amaçlı geliştirilmiştir.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
} 