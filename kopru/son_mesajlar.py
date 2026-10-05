"""
AI-to-AI Köprüsü (Bridge Script)
Karşı tarafın (Gemini veya Claude) son kontrolden bu yana yazdığı YENİ cevaplarını okur.

Kullanım:
  python son_mesajlar.py gemini [kaynak_yol_veya_proje]
  python son_mesajlar.py claude [kaynak_yol_veya_proje]

Yeni bir mesaj yoksa hiçbir şey yazdırmaz (sıfır ek tüketim).
"""
import glob
import json
import os
import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HOME = os.path.expanduser("~")
KLASOR = os.path.dirname(os.path.abspath(__file__))
MESAJ_SINIRI = 4500   # Her bir cevaptan en fazla bu kadar karakter alınır
TOPLAM_SINIR = 9000   # Tek seferde en fazla bu kadar karakter aktarılır

# Ortam değişkenleriyle yapılandırılabilir log yolları
GEMINI_LOG_YOLU = os.environ.get("GEMINI_LOG_PATTERN", "")
CLAUDE_LOG_YOLU = os.environ.get("CLAUDE_LOG_PATTERN", "")


def get_kaynaklar(hedef):
    kaynaklar = {
        "gemini": GEMINI_LOG_YOLU,
        "claude": CLAUDE_LOG_YOLU,
    }
    return kaynaklar.get(hedef, "")


def gemini_metni(d):
    if d.get("source") == "MODEL" and d.get("type") == "PLANNER_RESPONSE":
        return d.get("content") or ""
    return ""


def claude_metni(d):
    if d.get("type") != "assistant":
        return ""
    icerik = d.get("message", {}).get("content")
    if isinstance(icerik, str):
        return icerik
    if isinstance(icerik, list):
        return "\n".join(p.get("text", "") for p in icerik
                         if isinstance(p, dict) and p.get("type") == "text")
    return ""


def main():
    if len(sys.argv) < 2:
        print("Kullanım: python son_mesajlar.py gemini|claude [ozel_yol_pattern]")
        return

    kim = sys.argv[1].lower()
    ozel_yol = sys.argv[2] if len(sys.argv) > 2 else ""
    yol_pattern = ozel_yol or get_kaynaklar(kim)

    if not yol_pattern:
        print(f"Hata: {kim.upper()} için log yolu tanımlanmamış.")
        print(f"Lütfen '{kim.upper()}_LOG_PATTERN' ortam değişkenini ayarlayın veya komutun sonuna dosya yolu ekleyin.")
        print(f"Örnek: python son_mesajlar.py {kim} \"~/.{kim}/projects/<proje-adi>/*.jsonl\"")
        return

    dosyalar = glob.glob(yol_pattern)
    if not dosyalar:
        # Belirtilen yolda dosya yoksa sessizce çık veya bilgilendir
        return
    dosya = max(dosyalar, key=os.path.getmtime)  # En son kullanılan oturum

    durum_yolu = os.path.join(KLASOR, f"durum_{kim}.json")
    try:
        with open(durum_yolu, "r", encoding="utf-8") as f:
            durum = json.load(f)
    except Exception:
        durum = {}

    ilk_kurulum = not durum
    okunan = durum.get(dosya, 0)

    try:
        with open(dosya, encoding="utf-8", errors="replace") as f:
            satirlar = f.readlines()
    except Exception:
        return

    # Yarım yazılmış son satırı bir sonraki kontrole bırak
    if satirlar and not satirlar[-1].endswith("\n"):
        satirlar = satirlar[:-1]

    yeniler = []
    for satir in satirlar[okunan:]:
        try:
            d = json.loads(satir)
        except Exception:
            continue
        metin = (gemini_metni(d) if kim == "gemini" else claude_metni(d)).strip()
        if metin:
            if len(metin) > MESAJ_SINIRI:
                metin = metin[:MESAJ_SINIRI] + " …(kısaltıldı)"
            yeniler.append(metin)

    durum[dosya] = len(satirlar)
    try:
        with open(durum_yolu, "w", encoding="utf-8") as f:
            json.dump(durum, f)
    except Exception:
        pass

    # İlk kurulumda eski konuşmayı getirme, sadece bundan sonrakileri getir
    if ilk_kurulum or not yeniler:
        return

    cikti = "\n\n---\n\n".join(yeniler)
    if len(cikti) > TOPLAM_SINIR:
        cikti = "…(önceki kısım kısaltıldı)\n" + cikti[-TOPLAM_SINIR:]
    ad = "Gemini" if kim == "gemini" else "Claude"
    print(f"[{ad}'nin son kontrolden bu yana yazdığı yeni cevaplar]\n\n{cikti}")


if __name__ == "__main__":
    main()
