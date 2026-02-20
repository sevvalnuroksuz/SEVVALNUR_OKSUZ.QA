# Insider One Hiring Page Automation

Bu proje, Insider One işe alım sayfası için otomasyon testlerini içermektedir.

## Gereksinimler

- Python 3.7 veya üzeri
- Chrome tarayıcısı

## Kurulum

1. Projeyi klonlayın veya indirin
2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

## Proje Yapısı

```
ŞEVVALNUR_ÖKSÜZ.QA/
├── config.py                 # Konfigürasyon dosyası
├── requirements.txt          # Python bağımlılıkları
├── pages/                    # Page Object Model sınıfları
│   ├── __init__.py
│   ├── base_page.py         # Temel sayfa sınıfı
│   ├── home_page.py         # Ana sayfa
│   ├── career_page.py       # Kariyer sayfası
│   └── job_listing_page.py  # İş ilanları sayfası
├── utils/                    # Yardımcı modüller
│   ├── __init__.py
│   └── screenshot_handler.py # Ekran görüntüsü alma
├── tests/                    # Test dosyaları
│   └── test_hiring_page.py  # Ana test case
└── screenshots/              # Test başarısız olduğunda ekran görüntüleri (otomatik oluşturulur)
```

## Test Çalıştırma

Testi çalıştırmak için:

```bash
python -m pytest tests/test_hiring_page.py -v
```

veya

```bash
python tests/test_hiring_page.py
```

## Test Senaryosu

Test aşağıdaki adımları gerçekleştirir:

1. ✅ https://insiderone.com/ adresini ziyaret eder ve Insider One ana sayfasında olduğunu doğrular
2. ✅ "We're hiring" yazısına tıklar ve Career sayfasında olduğunu doğrular
3. ✅ "Explore open roles" butonunun bulunduğunu kontrol eder
4. ✅ "Explore open roles" butonuna tıklar
5. ✅ Software Development bloğu altında yer alan "xx Open Positions" bağlantısına tıklar
6. ✅ Location filtresini "Istanbul, Turkiye" olarak seçer
7. ✅ Team filtresini "Quality Assurance" olarak seçer
8. ✅ İş ilanı listesinin görüntülendiğini doğrular
9. ✅ Listelenen tüm iş ilanlarında, pozisyon bilgisinin "Quality Assurance" içerdiğini ve Location alanının "Istanbul, Turkiye" içerdiğini kontrol eder
10. ✅ "Apply" butonuna tıklar ve Lever Application Form sayfasına yönlendirildiğini doğrular

## Özellikler

- **Page Object Model (POM)**: Tüm sayfa elementleri ve işlemleri Page Object Model pattern'i ile organize edilmiştir
- **Otomatik Ekran Görüntüsü**: Herhangi bir test adımı başarısız olursa otomatik olarak ekran görüntüsü alınır
- **Esnek Locator Stratejileri**: Farklı sayfa yapılarına uyum sağlamak için çoklu locator stratejileri kullanılmıştır
- **Hata Yönetimi**: Tüm hatalar yakalanır ve ekran görüntüsü ile birlikte raporlanır

## Notlar

- Test çalıştırıldığında Chrome tarayıcısı otomatik olarak açılacaktır
- Test başarısız olduğunda ekran görüntüleri `screenshots/` klasörüne kaydedilir
- WebDriver otomatik olarak ChromeDriverManager ile yüklenir

