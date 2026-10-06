import winreg

class StartupManager:
    def __init__(self):
        # Başlangıçta çalışması gereksiz olan ve sistemi yavaşlatan yaygın uygulamalar
        self.heavy_startup_apps = [
            "OneDrive", 
            "Spotify", 
            "Skype", 
            "Discord", 
            "EpicGamesLauncher",
            "Steam",
            "GogGalaxy",
            "Origin",
            "WebCompanion"
        ]

    def optimize_startup(self):
        """Kayıt defterindeki başlangıç (Run) uygulamalarını tarar ve gereksizleri kapatır."""
        disabled_count = 0
        optimized_apps = []

        # İşletim sistemindeki kullanıcı başlangıç uygulamalarının olduğu kayıt defteri yolu
        run_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        
        try:
            # Okuma ve Yazma yetkisiyle açıyoruz
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_path, 0, winreg.KEY_ALL_ACCESS)
            
            # Kayıt defterindeki kaç tane başlangıç öğesi olduğunu bulalım
            num_values = winreg.QueryInfoKey(key)[1]
            
            # Tersten döngü yapıyoruz çünkü silme işlemi yaparken index kayabilir
            for i in range(num_values - 1, -1, -1):
                try:
                    val_name, val_data, val_type = winreg.EnumValue(key, i)
                    
                    # Eğer listedeki ağır uygulamalardan biri başlangıçta varsa
                    for app in self.heavy_startup_apps:
                        if app.lower() in val_name.lower() or app.lower() in val_data.lower():
                            # Başlangıçtan sil!
                            winreg.DeleteValue(key, val_name)
                            optimized_apps.append(val_name)
                            disabled_count += 1
                            break # Bir eşleşme yeterli
                except Exception:
                    continue
            
            winreg.CloseKey(key)
        except Exception as e:
            pass
            
        return disabled_count, optimized_apps

    def run_startup_optimizer(self):
        report = []
        report.append("[*] Windows Başlangıç (Boot) analiz ediliyor...")
        
        count, apps = self.optimize_startup()
        
        if count > 0:
            report.append(f"[+] Başlangıcı yavaşlatan {count} uygulama devre dışı bırakıldı!")
            for app in apps:
                report.append(f"  - Kapatıldı: {app}")
            report.append("\n[*] Bilgisayarınız bir sonraki yeniden başlatmada daha hızlı açılacaktır.")
        else:
            report.append("[+] Başlangıç dizini zaten temiz. Ekstra bir yavaşlatıcı bulunamadı.")
            
        return report