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

## Kurulum

1. Bu klasörü bilgisayarınıza kopyalayın (örnek: `C:\kopru`).
2. Projeye kurun:
   ```
   python C:\kopru\kur.py C:\proje_klasoru
   ```
3. Claude Code oturumunu yeniden açın. Gemini'ye yeni sohbet açın ya da "GEMINI.md'yi oku" deyin.

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
