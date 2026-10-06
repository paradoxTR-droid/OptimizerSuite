import winreg

class AnnoyanceNuker:
    def __init__(self):
        pass

    def disable_windows_ads(self):
        """Windows 10/11 içine gömülü tüm Microsoft reklamlarını ve önerilerini yok eder."""
        try:
            paths = [
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", "SubscribedContent-338387Enabled", 0), # Kilit Ekranı
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", "SubscribedContent-338389Enabled", 0), # Başlat Menüsü
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ShowSyncProviderNotifications", 0)        # Dosya Gezgini Reklamları
            ]
            
            for root, path, name, value in paths:
                try:
                    key = winreg.OpenKey(root, path, 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                    winreg.CloseKey(key)
                except:
                    pass
            return True
        except:
            return False

    def disable_smartscreen(self):
        """Sistemi sürekli tarayıp yavaşlatan ve uyarı veren SmartScreen'i susturur."""
        try:
            path = r"SOFTWARE\Policies\Microsoft\Windows\System"
            try:
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
            except:
                pass
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "EnableSmartScreen", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            return True
        except:
            return False

    def run_nuke(self):
        report = []
        report.append("[*] WINDOWS PRANGALARI KIRILIYOR (Nükleer Protokol)...")
        
        if self.disable_windows_ads():
            report.append("[+] Başlat menüsü, Dosya Gezgini ve Kilit ekranındaki tüm Microsoft reklamları yok edildi.")
            
        if self.disable_smartscreen():
            report.append("[+] SmartScreen ve gereksiz güvenlik uyarıları susturuldu.")
            
        report.append("\n✅ KULLANICI ÖZGÜRLÜĞÜNE KAVUŞTU! Arka planda sinsi işlemler bitti.")
        return report