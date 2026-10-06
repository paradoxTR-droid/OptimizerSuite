import psutil
import ctypes

class GameBooster:
    def __init__(self):
        # Kaynak tüketen, kapatıldığında sisteme zarar vermeyecek uygulamalar
        self.bloat_processes = [
            "OneDrive.exe",
            "Skype.exe",
            "Cortana.exe",
            "Spotify.exe",
            "msedge.exe",
            "EpicGamesLauncher.exe",
            "Steamwebhelper.exe",  # Steam'in web arayüzü RAM sömürür, oyunları etkilemez
            "YourPhone.exe",
            "Widgets.exe",
            "Discord.exe"          # Eğer oyun sırasında Discord kullanılmıyorsa
        ]

    def free_ram(self):
        """
        Win32 API (EmptyWorkingSet) kullanarak aktif çalışan programların 
        kullanmadığı bellek bloklarını zorla boşaltır.
        """
        freed_count = 0
        psapi = ctypes.windll.psapi
        kernel32 = ctypes.windll.kernel32
        
        # PROCESS_QUERY_INFORMATION (0x0400) | PROCESS_SET_QUOTA (0x0100)
        access_flags = 0x0400 | 0x0100 
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                # İşlemi kısıtlı yetkiyle aç (Güvenlik yazılımlarına takılmamak için)
                handle = kernel32.OpenProcess(access_flags, False, pid)
                if handle:
                    # Çalışma kümesini (Working Set) boşalt
                    if psapi.EmptyWorkingSet(handle):
                        freed_count += 1
                    kernel32.CloseHandle(handle)
            except Exception:
                # Sistem (NT Authority) işlemlerine erişim reddedilir, atlıyoruz.
                pass
                
        return freed_count

    def kill_background_apps(self):
        """Listedeki gereksiz uygulamaları zorla kapatır ve kazanılan RAM'i hesaplar."""
        killed_apps = 0
        freed_memory_mb = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                proc_name = proc.info['name']
                if proc_name and proc_name.lower() in [p.lower() for p in self.bloat_processes]:
                    mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    proc.kill()  # Acımasız kapatma (Terminate yerine Kill)
                    killed_apps += 1
                    freed_memory_mb += mem_mb
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return killed_apps, freed_memory_mb

    def set_high_priority(self, target_process_name):
        """Belirtilen uygulamaya (örn: csgo.exe, valorant.exe) Yüksek Öncelik atar."""
        success_count = 0
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == target_process_name.lower():
                    # psutil.HIGH_PRIORITY_CLASS eşdeğeri
                    proc.nice(psutil.HIGH_PRIORITY_CLASS)
                    success_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return success_count

    def run_boost(self):
        """Tüm güçlendirme işlemlerini sırayla çalıştırır ve rapor döner."""
        report = []
        
        # İşlem öncesi RAM
        ram_before = psutil.virtual_memory().percent
        
        # 1. Uygulama Kapatma
        killed_count, saved_mb = self.kill_background_apps()
        
        # 2. RAM Sıkıştırma (Geriye kalan tüm programlar için)
        optimized_procs = self.free_ram()
        
        # İşlem sonrası RAM
        ram_after = psutil.virtual_memory().percent
        
        report.append(f"[*] Arka Plan: {killed_count} gereksiz işlem öldürüldü (Kazanım: {saved_mb:.1f} MB).")
        report.append(f"[*] RAM Optimizasyonu: {optimized_procs} farklı işlemin belleği sıkıştırıldı.")
        report.append(f"\n--- TURBO BOOST ÖZETİ ---")
        
        if ram_after < ram_before:
            report.append(f"Sistem Bellek Yükü: %{ram_before} ➔ %{ram_after} (HAFİFLEDİ)")
        else:
            report.append(f"Sistem Bellek Yükü: %{ram_after} (Zaten optimum seviyede)")
            
        return report