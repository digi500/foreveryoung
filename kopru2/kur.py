# Bir projeye Claude <-> Gemini köprüsünü kurar. Tekrar çalıştırmak güvenlidir (var olanı bozmaz).
# Kullanım:  python C:\kopru\kur.py C:\proje_klasoru
import json, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOPRU = os.path.dirname(os.path.abspath(__file__))
BETIK = os.path.join(KOPRU, "son_mesajlar.py").replace("\\", "/")
ISARET = "<!-- kopru -->"

GEMINI_KURALI = f"""{ISARET}
# Claude ile ortak çalışma kuralı (C:\\kopru)

Kullanıcının her yeni mesajında, cevap vermeden önce şu komutu çalıştır:

```
python {BETIK} claude {{proje}}
```

- Komut hiçbir şey yazdırmazsa Claude yeni bir şey yazmamıştır; bundan bahsetme, normal devam et.
- Çıktı gelirse bu, Claude'un son kontrolden bu yana yazdığı yeni cevaplardır; dikkate al.
- Claude'un kayıt dosyalarını başka yolla okumaya çalışma; yalnızca bu komutu kullan.
- Çalışma düzeni ve kesin kurallar: `C:\\kopru\\bilgi.md` (oku ve uy).
- Görevlerin: `.ortak\\gorevler.md` · Raporun: `.ortak\\rapor.md` · Claude'un düzeltmeleri: `.ortak\\kontrol.md`
"""

ORTAK_DOSYALAR = {
    "gorevler.md": "# Gemini için görevler (Claude yazar)\n\n_Henüz görev yok._\n",
    "rapor.md": "# Gemini'nin raporu\n\n_Henüz rapor yok._\n",
    "kontrol.md": "# Claude'un kontrol sonucu\n\n_Henüz kontrol yok._\n",
}

GITIGNORE = ["# Claude-Gemini kopru (yerel)", ".ortak/", ".claude/", "GEMINI.md"]


def kur(proje):
    proje = os.path.abspath(proje).rstrip("\\/")
    if not os.path.isdir(proje):
        print(f"Klasör yok: {proje}")
        return
    yapilan = []

    ortak = os.path.join(proje, ".ortak")
    os.makedirs(ortak, exist_ok=True)
    for ad, icerik in ORTAK_DOSYALAR.items():
        yol = os.path.join(ortak, ad)
        if not os.path.exists(yol):
            with open(yol, "w", encoding="utf-8") as f:
                f.write(icerik)
            yapilan.append(f".ortak/{ad} oluşturuldu")

    # Claude tarafı: UserPromptSubmit hook
    ayar_yolu = os.path.join(proje, ".claude", "settings.json")
    os.makedirs(os.path.dirname(ayar_yolu), exist_ok=True)
    try:
        with open(ayar_yolu, encoding="utf-8") as f:
            ayar = json.load(f)
    except FileNotFoundError:
        ayar = {}
    komut = f'python "{BETIK}" gemini "{proje}"'
    liste = ayar.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
    if "son_mesajlar.py" not in json.dumps(liste):
        liste.append({"hooks": [{"type": "command", "command": komut}]})
        with open(ayar_yolu, "w", encoding="utf-8") as f:
            json.dump(ayar, f, ensure_ascii=False, indent=2)
        yapilan.append(".claude/settings.json hook eklendi")

    # Gemini tarafı: GEMINI.md kuralı
    gemini_yolu = os.path.join(proje, "GEMINI.md")
    mevcut = ""
    if os.path.exists(gemini_yolu):
        with open(gemini_yolu, encoding="utf-8") as f:
            mevcut = f.read()
    if ISARET not in mevcut:
        with open(gemini_yolu, "w", encoding="utf-8") as f:
            f.write(GEMINI_KURALI.replace("{proje}", proje) + ("\n" + mevcut if mevcut else ""))
        yapilan.append("GEMINI.md kuralı eklendi")

    # Yerel köprü dosyaları repoya girmesin
    if os.path.isdir(os.path.join(proje, ".git")):
        gi = os.path.join(proje, ".gitignore")
        satirlar = open(gi, encoding="utf-8").read().splitlines() if os.path.exists(gi) else []
        eksik = [s for s in GITIGNORE if s not in satirlar]
        if eksik:
            with open(gi, "a", encoding="utf-8") as f:
                f.write(("\n" if satirlar else "") + "\n".join(eksik) + "\n")
            yapilan.append(".gitignore güncellendi")

    # Başlangıç noktasını kaydet (eski konuşmalar aktarılmasın); kuruluysa okunmamış mesajlara dokunma
    for kim in ("gemini", "claude"):
        if os.path.exists(os.path.join(ortak, f"durum_{kim}.json")):
            continue
        os.system(f'python "{BETIK}" {kim} "{proje}" > NUL 2>&1' if os.name == "nt"
                  else f'python3 "{BETIK}" {kim} "{proje}" > /dev/null 2>&1')

    print(f"Köprü kuruldu: {proje}")
    for y in yapilan or ["(zaten kuruluydu, değişiklik yok)"]:
        print(" -", y)
    print("Claude'un hook'u bir sonraki mesajda / oturum yeniden açılınca devreye girer.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python C:\\kopru\\kur.py C:\\proje_klasoru")
    else:
        kur(sys.argv[1])
