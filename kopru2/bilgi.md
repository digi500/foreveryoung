# Köprü — Claude ↔ Gemini ortak çalışma sistemi

Bu dosyayı okuyan yapay zekâ (Claude veya Gemini): aşağıdakileri uygula, ayrıca arama yapma.

## 1. Yeni projede ilk iş
Kullanıcı "C:\kopru\bilgi.md'yi oku" dediyse ve projede köprü yoksa (`<proje>\.ortak\` klasörü yoksa) çalıştır:

```
python C:\kopru\kur.py <proje_klasoru>
```

Bu komut şunları yapar (tekrar çalıştırmak güvenlidir):
- `<proje>\.ortak\` klasörünü kurar: `gorevler.md`, `rapor.md`, `kontrol.md` ve okuma durumu dosyaları.
- `<proje>\.claude\settings.json`: Claude'a, her kullanıcı mesajında Gemini'nin yeni cevaplarını otomatik
  getiren hook ekler.
- `<proje>\GEMINI.md`: Gemini'ye, her mesajda Claude'un yeni cevaplarını okuma kuralı ekler.
- `.gitignore`: bu yerel dosyalar repoya girmesin diye satır ekler.

Claude'un hook'u bir sonraki mesajda veya oturum yeniden açılınca devreye girer. Gemini'nin yeni kuralı
görmesi için yeni sohbet açılmalı ya da Gemini'ye "GEMINI.md'yi oku" denmeli.

## 2. Roller
- **Claude = yönetici ve kontrolcü.** Görevleri `.ortak\gorevler.md`'ye yazar. Gemini'nin işini gerçek
  dosyalardan, diff'lerden ve ham çıktılardan doğrular. Düzeltmeleri `.ortak\kontrol.md`'ye yazar. Kod yazmaz,
  tokenlarını yönetim ve kontrole harcar.
- **Gemini = çalışan.** Kodu yazar ve çalıştırır. Bitince `.ortak\rapor.md`'ye değişen dosyaları,
  çalıştırdığı komutları ve bunların GERÇEK çıktılarını yazar.
- **Kullanıcı = karar verici.** Commit, push, yayın ve anahtar işlemlerini onaylar ya da kendisi yapar.

## 3. Mesajlaşma nasıl çalışıyor
- Betik: `C:\kopru\son_mesajlar.py gemini|claude [proje]`. Karşı tarafın son kontrolden beri yazdığı
  yeni cevapları basar. Yeni bir şey yoksa hiçbir şey yazmaz (sıfır token).
- Claude kayıtları: `~\.claude\projects\<proje yolu, harf/rakam dışı karakterler '-'>\*.jsonl`
- Gemini kayıtları: `~\.gemini\antigravity-ide\brain\*\.system_generated\logs\transcript.jsonl`. Bunlar
  projeye göre ayrılmaz. Betik, en yeni 15 oturum içinden proje yolunu içeren ilkini seçer.
- Okuma durumu: `<proje>\.ortak\durum_gemini.json` ve `durum_claude.json`. İlk çalıştırma sadece
  başlangıç noktasını kaydeder, eski konuşmayı aktarmaz.

## 4. Kesin kurallar (ikisi için de)
1. **Sahte veri yok.** Mock, uydurma sayı ya da "başarılı" varsayımı yok. Çalıştırılmadıysa "çalıştırmadım"
   yazılır. Claude, Gemini'nin her sayısını ham kaynaktan doğrular.
2. **Gizli bilgi ekrana düşmez.** Anahtar, şifre ve token DEĞERLERİ hiçbir zaman sohbete, rapora,
   dosyaya ya da komut çıktısına yazılmaz. Değer okuyan komutların çıktısı gizlenir. Doğrulamada sadece
   "tanımlı/tanımsız" gösterilir. Secret'ları kullanıcı kendisi girer (tarayıcıdan ya da kendi
   terminalinden, örneğin `gh secret set`). Yapay zekâya anahtar verilmez, çünkü her şey bu kayıtlara düşer.
3. **Kapsam.** Sadece görevde yazan yapılır. Tarayıcı, ekran paylaşımı ve oturumlara istenmedikçe
   dokunulmaz.
4. **Canlı sisteme dikkat.** Canlı veritabanına yazan ya da e-posta veya bildirim gönderen betikler
   görevde açıkça istenmedikçe çalıştırılmaz.
5. **Git.** Commit ve push, Claude kontrol edip kullanıcı onayladıktan sonra yapılır.
6. **Kısa cevap.** Kullanıcının ekranı küçük, cevaplar kısa ve öz olmalı.

## 5. Dosyalar
| Dosya | Görevi |
|---|---|
| `C:\kopru\bilgi.md` | Bu rehber |
| `C:\kopru\kur.py` | Projeye köprüyü kurar |
| `C:\kopru\son_mesajlar.py` | Yeni mesajları okur (tüm projeler için tek kopya) |
