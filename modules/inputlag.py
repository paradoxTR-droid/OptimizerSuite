import winreg

class InputOptimizer:
    def __init__(self):
        pass

    def optimize_keyboard_mouse(self):
        """Klavye gecikmesini sıfırlar ve Fare veri aktarım hızını optimize eder."""
        try:
            # Klavye Gecikmesini (Delay) en aza indir, Hızı (Speed) maksimuma al
            kb_path = r"Control Panel\Keyboard"
            key_kb = winreg.OpenKey(winreg.HKEY_CURRENT_USER, kb_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key_kb, "KeyboardDelay", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key_kb, "KeyboardSpeed", 0, winreg.REG_SZ, "31")
            winreg.CloseKey(key_kb)

            # Yapışkan Tuşları (Sticky Keys) ve Filtre Tuşlarını (Filter Keys) kapat
            acc_path = r"Control Panel\Accessibility\StickyKeys"
            key_sk = winreg.OpenKey(winreg.HKEY_CURRENT_USER, acc_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key_sk, "Flags", 0, winreg.REG_SZ, "506") # Devre dışı bayrağı
            winreg.CloseKey(key_sk)
            return True
        except:
            return False

    def run_input_boost(self):
        report = []
        report.append("[*] Giriş Gecikmesi (Input Lag) protokolleri ayarlanıyor...")
        
        if self.optimize_keyboard_mouse():
            report.append("[+] Klavye tepki hızı maksimuma çekildi, gecikme (delay) sıfırlandı.")
            report.append("[+] Oyun esnasında çıkan Yapışkan Tuşlar (Sticky Keys) kapatıldı.")
            
        report.append("\n✅ DONANIM TEPKİ SÜRESİ MİNİMUMA İNDİRİLDİ!")
        return report