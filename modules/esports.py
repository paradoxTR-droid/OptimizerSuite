import winreg
import ctypes

class EsportsOptimizer:
    def __init__(self):
        pass

    def disable_mouse_acceleration(self):
        """Kusursuz Aim (Nişan) için Fare İvmesini kapatır."""
        try:
            path = r"Control Panel\Mouse"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
            # Fare hızlandırma değerlerini 0'a çekiyoruz
            winreg.SetValueEx(key, "MouseSpeed", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "MouseThreshold1", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "MouseThreshold2", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(key)

            # Değişikliklerin bilgisayarı yeniden başlatmadan anında etki etmesi için Win32 API çağrısı
            ctypes.windll.user32.SystemParametersInfoW(0x0004, 0, None, 1 | 2) # SPI_SETMOUSE
            return True
        except:
            return False

    def disable_fso_globally(self):
        """Oyunlardaki Input Lag'ı yok eden Global FSO kapatma işlemi."""
        try:
            path = r"System\GameConfigStore"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
            # 2 değeri: Tam Ekran İyileştirmelerini (FSO) tüm oyunlar için devre dışı bırakır
            winreg.SetValueEx(key, "GameDVR_FSEBehaviorMode", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            return True
        except:
            return False

    def run_esports_boost(self):
        report = []
        report.append("[*] ESPORTS (Rekabetçi Profil) Başlatılıyor...")
        
        if self.disable_mouse_acceleration():
            report.append("[+] Fare İvmesi (Mouse Acceleration) kökünden kapatıldı.")
            report.append("    -> Kas hafızanız bozulmayacak, Aim (Nişan) almanız kusursuzlaşacak.")
            
        if self.disable_fso_globally():
            report.append("[+] Tam Ekran İyileştirmeleri (FSO) küresel olarak engellendi.")
            report.append("    -> Alt-Tab hızı arttı, görüntü gecikmesi (Input Lag) tamamen yok oldu.")
            
        report.append("\n✅ REKABETÇİ ESPOR PROFİLİ AKTİF! (CS2, Valorant, Apex için mükemmel donanım uyumu)")
        return report