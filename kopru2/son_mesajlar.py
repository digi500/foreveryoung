# Karşı tarafın (Gemini veya Claude) son kontrolden bu yana yazdığı YENİ cevaplarını yazdırır.
# Tek kopya, tüm projeler için ortak. Proje klasörü verilmezse çalışılan klasör kullanılır.
# Kullanım:
#   python C:\kopru\son_mesajlar.py gemini [proje_klasoru]   -> Claude için: Gemini'nin yeni cevapları
#   python C:\kopru\son_mesajlar.py claude [proje_klasoru]   -> Gemini için: Claude'un yeni cevapları
# Yeni bir şey yoksa hiçbir şey yazdırmaz (ekstra token harcanmaz).
# Okuma durumu her projenin kendi <proje>\.ortak\durum_*.json dosyasında tutulur.
import glob, json, os, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")
MESAJ_SINIRI = 4500   # her cevaptan en fazla bu kadar karakter
TOPLAM_SINIR = 9000   # tek seferde en fazla bu kadar karakter
GEMINI_TARAMA = 15    # projeyi bulmak için bakılacak en yeni Gemini oturumu sayısı

GEMINI_KAYITLARI = os.path.join(HOME, ".gemini", "antigravity-ide", "brain", "*",
                                ".system_generated", "logs", "transcript.jsonl")


def claude_klasoru(proje):
    # Claude Code, proje yolundaki harf/rakam dışı her karakteri '-' yapar: C:\deprem -> C--deprem
    return os.path.join(HOME, ".claude", "projects", re.sub(r"[^A-Za-z0-9]", "-", proje))


def claude_dosyasi(proje):
    dosyalar = glob.glob(os.path.join(claude_klasoru(proje), "*.jsonl"))
    return max(dosyalar, key=os.path.getmtime) if dosyalar else None


def gemini_dosyasi(proje):
    # Gemini kayıtları projeye göre ayrılmaz; en yeni oturumlardan bu projenin yolunu içeren ilkini seç.
    dosyalar = sorted(glob.glob(GEMINI_KAYITLARI), key=os.path.getmtime, reverse=True)
    surucu, geri = os.path.splitdrive(proje)
    parcalar = [re.escape(p) for p in re.split(r"[\\/]+", geri) if p]
    # Ayırıcı: kayıtta \, \\ (JSON kaçışı) veya / olabilir. Tek karakter sınıfı (geri izleme patlaması olmasın).
    desen = re.compile(re.escape(surucu.rstrip(":")) + r":?[\\/]+" +
                       r"[\\/]+".join(parcalar) + r"(?![A-Za-z0-9_\-])", re.IGNORECASE)
    for dosya in dosyalar[:GEMINI_TARAMA]:
        try:
            with open(dosya, encoding="utf-8", errors="replace") as f:
                if desen.search(f.read()):
                    return dosya
        except Exception:
            continue
    return None


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
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ("gemini", "claude"):
        print("Kullanım: python C:\\kopru\\son_mesajlar.py gemini|claude [proje_klasoru]")
        return
    kim = sys.argv[1].lower()
    proje = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.getcwd()).rstrip("\\/")

    dosya = gemini_dosyasi(proje) if kim == "gemini" else claude_dosyasi(proje)
    if not dosya:
        return

    ortak = os.path.join(proje, ".ortak")
    os.makedirs(ortak, exist_ok=True)
    durum_yolu = os.path.join(ortak, f"durum_{kim}.json")
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
