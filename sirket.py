"""Ücretsiz "ajan şirketi": ekip.json'daki ajanları sırayla çalıştırır, günlük rapor yazar.
Yalnızca standart Python kütüphanesi kullanır (kurulum gerekmez)."""
import datetime
import json
import os
import time
import urllib.error
import urllib.request

URL = "https://models.github.ai/inference/chat/completions"
BEKLE = 8          # saniye: dakika başına istek limitine takılmamak için
MAX_ONCEKI = 6000  # sonraki ajana aktarılacak en fazla karakter


def sor(model, sistem, kullanici):
    govde = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": sistem},
            {"role": "user", "content": kullanici},
        ],
        "max_tokens": 900,
    }).encode()
    istek = urllib.request.Request(URL, govde, {
        "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "sirket-bot",
    })
    try:
        with urllib.request.urlopen(istek, timeout=120) as r:
            durum = r.status
            tur = r.headers.get("Content-Type", "")
            son_url = r.geturl()
            ham = r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %s: %s" % (e.code, e.read().decode("utf-8", errors="replace")[:500]))
    finally:
        time.sleep(BEKLE)
    try:
        return json.loads(ham)["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise RuntimeError("Beklenmeyen cevap (durum %s, tur %s, adres %s): %r" % (durum, tur, son_url, ham[:500]))


def main():
    with open("ekip.json", encoding="utf-8") as f:
        ekip = json.load(f)
    with open("konular.txt", encoding="utf-8") as f:
        konular = [s.strip() for s in f if s.strip() and not s.startswith("#")]
    if not konular:
        raise SystemExit("konular.txt boş")

    bugun = datetime.date.today()
    konu = konular[bugun.toordinal() % len(konular)]  # her gün sıradaki konu
    rapor = ["# %s - Konu: %s\n" % (bugun, konu)]
    onceki = ""

    for ajan in ekip["ajanlar"]:
        girdi = ajan["gorev"].format(konu=konu, onceki=onceki[-MAX_ONCEKI:])
        try:
            cikti = sor(ajan["model"], ekip["kurallar"] + "\n" + ajan["rol"], girdi)
        except Exception as e:  # limit veya model hatası: dur, hatayı rapora yaz
            rapor.append("## %s\nÇalışamadı: %s\n" % (ajan["ad"], e))
            break
        rapor.append("## %s (%s)\n%s\n" % (ajan["ad"], ajan["model"], cikti))
        onceki += "\n--- %s ---\n%s\n" % (ajan["ad"], cikti)

    os.makedirs("raporlar", exist_ok=True)
    with open("raporlar/%s.md" % bugun, "w", encoding="utf-8") as f:
        f.write("\n".join(rapor))


if __name__ == "__main__":
    main()
