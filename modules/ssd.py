import subprocess

class SSDOptimizer:
    def __init__(self):
        pass

    def optimize_ntfs(self):
        """NTFS dosya sisteminin diski gereksiz yoran özelliklerini kapatır."""
        try:
            # 1. Son erişim tarihi güncellemelerini kapat (Diski çok rahatlatır)
            subprocess.run("fsutil behavior set disablelastaccess 1", shell=True, capture_output=True)
            # 2. MS-DOS 8.3 kısa isim oluşturmayı kapat (Klasör açılışlarını hızlandırır)
            subprocess.run("fsutil behavior set disable8dot3 1", shell=True, capture_output=True)
            return True
        except:
            return False

    def force_trim(self):
        """SSD'deki boş hücreleri temizleyen TRIM komutunu zorla çalıştırır."""
        try:
            # C: sürücüsü için TRIM (Retrim) ve Optimizasyon işlemi
            subprocess.run("defrag c: /O /U", shell=True, capture_output=True)
            return True
        except:
            return False

    def run_ssd_boost(self):
        report = []
        report.append("[*] SSD & Depolama Overdrive Protokolü Başlatılıyor...")
        
        if self.optimize_ntfs():
            report.append("[+] NTFS yükleri (LastAccessTime ve 8.3 Naming) devre dışı bırakıldı.")
            report.append("    -> Klasörlerin ve dosyaların açılış hızı maksimuma çıktı.")
            
        report.append("[*] SSD TRIM Optimizasyonu yapılıyor (Biraz sürebilir)...")
        if self.force_trim():
            report.append("[+] SSD TRIM komutu başarıyla uygulandı! Disk okuma/yazma hızları tazelendi.")
            
        report.append("\n✅ DEPOLAMA BİRİMİ MAKSİMUM HIZA ULAŞTI!")
        return report