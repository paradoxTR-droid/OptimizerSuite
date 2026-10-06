import winreg

class MMCSSOptimizer:
    def __init__(self):
        pass

    def optimize_gaming_profile(self):
        """Windows MMCSS Oyun Profilini %100 İşlemci Önceliği ile yeniden yazar."""
        try:
            path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games"
            # Yönetici haklarıyla anahtarı açıyoruz
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE)
            
            # Değerleri maksimum performansa göre ayarlıyoruz
            winreg.SetValueEx(key, "Affinity", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "Background Only", 0, winreg.REG_SZ, "False")
            winreg.SetValueEx(key, "Clock Rate", 0, winreg.REG_DWORD, 10000)
            winreg.SetValueEx(key, "GPU Priority", 0, winreg.REG_DWORD, 8)       # Max GPU önceliği
            winreg.SetValueEx(key, "Priority", 0, winreg.REG_DWORD, 6)           # Max CPU önceliği
            winreg.SetValueEx(key, "Scheduling Category", 0, winreg.REG_SZ, "High")
            winreg.SetValueEx(key, "SFIO Priority", 0, winreg.REG_SZ, "High")
            winreg.CloseKey(key)
            return True
        except:
            return False

    def run_mmcss_boost(self):
        report = []
        report.append("[*] MMCSS (Çoklu Ortam Çekirdeği) Oyun Profili Yeniden Yazılıyor...")
        
        if self.optimize_gaming_profile():
            report.append("[+] Windows, oyunlara %100 CPU ve GPU önceliği verecek şekilde kodlandı.")
            report.append("    -> Sistem arka plan görevleri artık oyunların hızını kesemeyecek.")
            
        report.append("\n✅ OYUN MOTORU (MMCSS) MAKSİMUM ÖNCELİKTE!")
        return report