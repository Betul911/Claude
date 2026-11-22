# Ajan Şirketi (ücretsiz sürüm)

Her sabah GitHub kendi sunucusunda 5 ajanı çalıştırır (Araştırmacı, Öğretmen, Soru Yazarı,
Eleştirmen, Koordinatör) ve sonucu `raporlar/` klasörüne yazar.
Ajanlar GitHub Models'in ücretsiz, limitli katmanını kullanır.

## Kurulum (10 dakika)
1. github.com'da **Private** yeni bir depo aç (ör. `sirket`).
2. Bu klasördeki tüm dosyaları (gizli `.github` klasörü dahil) depoya yükle.
3. Depoda Settings > Actions > General > Workflow permissions: **Read and write** seç.
4. Actions sekmesi > `sirket` > **Run workflow** ile ilk çalıştırmayı elle başlat.
5. Bitince `raporlar/` içindeki dosyayı aç. Hata varsa raporun içinde yazar.

## Ayarlar
- `konular.txt`: Konuları kendi ünitelerine göre düzenle.
- `ekip.json`: Ajanların rolü ve modeli. Model adı hata verirse github.com/marketplace/models
  sayfasındaki güncel adı yaz.
- `sirket.yml` içindeki `cron`: Saati değiştirir (UTC).

## Claude ile analiz
Raporu bana yapıştır; ben Eleştirmen ile Öğretmen arasındaki çelişkileri ve [DOĞRULA]
işaretlerini kaynaktan kontrol edip konuyu seninle çalışırım.
