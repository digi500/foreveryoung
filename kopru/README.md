# AI-to-AI Köprü Sistemi (Bridge)

[ 🇬🇧 Read in English (İngilizce Sürüm) → ](README.en.md)

---

Bu klasör, yerel ortamda çalışan iki farklı yapay zekâ asistanının (Gemini ve Claude) bekleme döngülerine girmeden ve gereksiz kota harcamadan birbirlerinin çıktılarını sırayla okumasını sağlayan hafif (lightweight) mekanizmayı içerir.

---

## Nasıl Çalışır?

1. Modeller arka planda sürekli "beklemede" kalarak kaynak tüketmez.
2. Bir yapay zekâ cevap ürettiğinde, bu cevap yerel oturum kütüğüne (transcript) kaydedilir.
3. Karşı tarafın yapay zekâsına kullanıcı yeni bir mesaj yazdığında, yerel Python betiği (`son_mesajlar.py`) tetiklenir:
   - Yalnızca son kontrolden sonra yazılan yeni cevabı çeker.
   - Yeni mesaj yoksa sessiz kalır (0 ekstra maliyet).
   - Yeni mesaj varsa bunu bağlama ekler.

---

## Yapılandırma ve Ortam Değişkenleri

Betik, modellerin yerel oturum dosyalarını bulabilmek için yol kalıplarını (path pattern) kullanır. Bu yollar ortam değişkeni veya komut argümanı olarak verilebilir:

* `CLAUDE_LOG_PATTERN`: Claude'un proje kayıt dosyalarının yolu.  
  *Örnek:* `~/.claude/projects/<proje-adi>/*.jsonl`
* `GEMINI_LOG_PATTERN`: Gemini'nin oturum kayıtlarının yolu.  
  *Örnek:* `~/<asistan-dizini>/logs/transcript.jsonl`

Eğer bu ortam değişkenleri tanımlı değilse, yol doğrudan komutun sonuna eklenebilir:
```bash
python son_mesajlar.py claude "~/.claude/projects/ornek-proje/*.jsonl"
```

---

## Entegrasyon Örnekleri

### 1. Claude Tarafı (Hook Entegrasyonu)
Proje kökündeki `.claude/settings.json` dosyasına bir `UserPromptSubmit` kancası (hook) eklenir:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "python .ortak/son_mesajlar.py gemini"
      }
    ]
  }
}
```

### 2. Gemini Tarafı (Kural Entegrasyonu)
Proje kökündeki `GEMINI.md` dosyasına şu kural tanımlanır:

```markdown
# Claude ile ortak çalışma kuralı
Kullanıcının her yeni mesajında, cevap vermeden önce şu komutu çalıştır:
python .ortak/son_mesajlar.py claude
- Komut hiçbir şey yazdırmazsa normal devam et.
- Çıktı gelirse Claude'un yeni cevabını dikkate alarak yanıt ver.
```

---

## Lisans
Bu klasördeki betik ve araçlar [MIT Lisansı](LICENSE) ile lisanslanmıştır.
