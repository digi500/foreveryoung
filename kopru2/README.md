# Köprü 2 — Claude ↔ Gemini Ortak Çalışma Sistemi

[ 🇬🇧 Read in English (İngilizce Sürüm) → ](README.en.md)

---

İlk sürüm ([`kopru/`](../kopru/)) iki yapay zekânın birbirinin cevabını okumasını sağlıyordu. **Köprü 2** bunu bir çalışma düzenine çevirir: tek komutla her projeye kurulur, roller ve kurallar bellidir, görevler ve raporlar ortak dosyalarda tutulur.

## İlk sürümden farkları

| | Köprü 1 | Köprü 2 |
|---|---|---|
| Kurulum | Elle (hook ve kural kopyalanır) | `python kur.py <proje>` tek komut, tekrar çalıştırmak güvenli |
| Betik | Her projede ayrı kopya | Tüm projeler için tek kopya |
| Kayıt yolu | Ortam değişkeni ile verilir | Proje yolundan otomatik bulunur (Claude ve Gemini/Antigravity) |
| Okuma durumu | Betiğin yanında, tek dosya | Her projenin kendi `.ortak/durum_*.json` dosyası |
| Roller ve kurallar | Yok | `bilgi.md`: yönetici/kontrolcü, çalışan, karar verici; sahte veri yok, gizli bilgi ekrana düşmez |
| Görev akışı | Yok | `.ortak/gorevler.md` → `rapor.md` → `kontrol.md` |

## Gerekenler

- **Python 3** (`python --version` ile kontrol edin; Linux/macOS'ta `python3`)
- **Claude Code** (terminal, masaüstü uygulaması veya IDE eklentisi)
- **Gemini, Antigravity IDE içinde**
- İkisinin de aynı proje klasöründe çalışması

## Kurulum (adım adım)

1. **İndirin.** GitHub'da yeşil **Code → Download ZIP** ile indirin ya da:
   ```
   git clone https://github.com/digi500/foreveryoung.git
   ```
2. **`kopru2` klasörünü kalıcı bir yere kopyalayın**, örneğin `C:\kopru`. Sonra bu klasörü taşımayın: kurulum, betiklerin tam yolunu projeye yazar. Taşırsanız kurulumu tekrar yapın.
3. **Projenize kurun** (terminalde):
   ```
   python C:\kopru\kur.py C:\proje_klasoru
   ```
   Ekranda `Köprü kuruldu` ve yapılanların listesi çıkar. Tekrar çalıştırmak güvenlidir.
4. **Claude Code'u o proje klasöründe yeniden açın.** Hook ancak yeni oturumda devreye girer.
5. **Antigravity'de yeni sohbet açın** ve Gemini'ye şunu yazın:
   > `GEMINI.md` dosyasını ve köprü klasöründeki `bilgi.md` dosyasını oku.

## Çalıştığını nasıl anlarım?

1. Gemini'ye bir soru sorun, cevap versin.
2. Claude'a herhangi bir mesaj yazın. Claude'un ekranında **"[Gemini'nin son kontrolden bu yana yazdığı yeni cevaplar]"** başlığıyla Gemini'nin cevabı görünür.
3. Tersini deneyin: Claude bir şey yazsın, sonra Gemini'ye mesaj atın. Gemini her mesajda komutu çalıştırıp Claude'un yeni cevabını okur.

İlk çalıştırmada eski konuşma aktarılmaz, sadece kurulumdan sonra yazılanlar gelir.

## Günlük kullanım

1. Claude'a ne istediğinizi söyleyin. Claude görevi `.ortak/gorevler.md` dosyasına yazar.
2. Gemini'ye "`.ortak/gorevler.md`'deki görevi yap, bitince `.ortak/rapor.md`'ye yaz" deyin.
3. Claude'a "kontrol et" deyin. Claude raporu gerçek dosya ve çıktılardan doğrular, düzeltmeleri `.ortak/kontrol.md`'ye yazar.
4. Commit, push ve yayın kararı sizindir.

## Sorun giderme

| Belirti | Çözüm |
|---|---|
| Claude'da Gemini'nin cevabı görünmüyor | Claude Code oturumunu proje klasöründe yeniden açın. `.claude/settings.json` içinde `son_mesajlar.py` satırı var mı bakın. |
| Gemini, Claude'u okumuyor | Antigravity'de yeni sohbet açın ve "GEMINI.md'yi oku" deyin. |
| `python` bulunamadı | Python 3'ü kurun. Linux/macOS'ta `python3` kullanılır. |
| Köprü klasörünü taşıdım | `kur.py`'yi yeni yerden tekrar çalıştırın. Eski hook satırını `.claude/settings.json`'dan, eski kuralı `GEMINI.md`'den silin. |

`kur.py` şunları yapar:
- `<proje>/.ortak/` klasörünü ve `gorevler.md`, `rapor.md`, `kontrol.md` dosyalarını oluşturur.
- `<proje>/.claude/settings.json` dosyasına, her kullanıcı mesajında Gemini'nin yeni cevaplarını getiren `UserPromptSubmit` hook'unu ekler.
- `<proje>/GEMINI.md` dosyasına, her mesajda Claude'un yeni cevaplarını okuma kuralını ekler.
- `.gitignore` dosyasına bu yerel dosyaları ekler.

## Nasıl çalışır

- `son_mesajlar.py gemini|claude [proje]`: Karşı tarafın son kontrolden beri yazdığı yeni cevapları yazdırır. Yeni bir şey yoksa hiçbir şey yazdırmaz (sıfır token).
- Claude kayıtları: `~/.claude/projects/<proje yolu>/*.jsonl`
- Gemini (Antigravity) kayıtları: `~/.gemini/antigravity-ide/brain/*/.system_generated/logs/transcript.jsonl`. Bunlar projeye göre ayrılmadığı için betik, en yeni 15 oturum içinden proje yolunu içeren ilkini seçer.
- Her cevaptan en fazla 4.500, tek seferde en fazla 9.000 karakter aktarılır.

Ayrıntılı çalışma düzeni ve kurallar: [`bilgi.md`](bilgi.md)

## Notlar

- Yollar Windows örnekleriyle yazılmıştır. Betikler Linux ve macOS'ta da çalışır.
- Gemini kayıt yolu Antigravity IDE'ye göredir. Farklı bir istemci kullanıyorsanız `son_mesajlar.py` içindeki `GEMINI_KAYITLARI` değerini değiştirin.

## Lisans

[MIT Lisansı](LICENSE)
