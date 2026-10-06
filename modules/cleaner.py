import os
import shutil
import ctypes

class DeepCleaner:
    def __init__(self):
        # Hedef klasör yollarını çevre değişkenlerinden (Environment Variables) alıyoruz
        self.windir = os.environ.get('WINDIR', 'C:\\Windows')
        self.user_temp = os.environ.get('TEMP')
        self.windows_temp = os.path.join(self.windir, 'Temp')
        self.prefetch = os.path.join(self.windir, 'Prefetch')
        self.software_dist = os.path.join(self.windir, 'SoftwareDistribution', 'Download')

    def get_dir_size(self, path):
        """Silinecek klasörün boyutunu hesaplar."""
        total = 0
        try:
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
        except Exception:
            pass
        return total

    def clean_directory(self, folder_path):
        """Klasördeki dosyaları zorla siler, kullanımda olanları atlar."""
        freed_space = 0
        deleted_files = 0
        
        if not folder_path or not os.path.exists(folder_path):
            return freed_space, deleted_files

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                size = 0
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    size = self.get_dir_size(item_path)
                    shutil.rmtree(item_path)
                
                freed_space += size
                deleted_files += 1
            except Exception:
                # Dosya şu an başka bir program tarafından kullanılıyorsa hatayı yoksay (Crash engelleme)
                pass
        
        return freed_space, deleted_files

    def empty_recycle_bin(self):
        """Win32 API ile çöp kutusunu sessizce boşaltır."""
        # API Bayrakları: 1 = Onay sorma, 2 = Arayüz gösterme, 4 = Ses çıkarma -> 1|2|4 = 7
        try:
            result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            return True if result == 0 else False
        except Exception:
            return False

    def run_full_cleanup(self):
        """Tüm temizlik işlemini başlatır ve bir rapor döndürür."""
        targets = {
            "Kullanıcı Temp": self.user_temp,
            "Windows Temp": self.windows_temp,
            "Prefetch": self.prefetch,
            "Windows Update Kalıntıları": self.software_dist
        }
        
        total_freed_bytes = 0
        total_deleted_items = 0
        report = []

        for name, path in targets.items():
            freed, count = self.clean_directory(path)
            total_freed_bytes += freed
            total_deleted_items += count
            
            freed_mb = freed / (1024 * 1024)
            report.append(f"[*] {name}: {count} öğe silindi, {freed_mb:.2f} MB yer açıldı.")
        
        # Çöp Kutusu İşlemi
        if self.empty_recycle_bin():
            report.append("[*] Çöp Kutusu: Başarıyla boşaltıldı.")
        else:
            report.append("[*] Çöp Kutusu: Zaten boş veya erişim yok.")

        total_freed_mb = total_freed_bytes / (1024 * 1024)
        report.append(f"\n--- ÖZET ---\nToplam {total_deleted_items} öğe silindi ve {total_freed_mb:.2f} MB alan kazanıldı.")
        
        return total_freed_mb, report