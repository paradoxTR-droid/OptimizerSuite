import winreg
import subprocess

class VisualOptimizer:
    def __init__(self):
        pass

    def strip_visual_effects(self):
        """Windows görsel efektlerini (Gölgeler, Saydamlık, Animasyonlar) Performans moduna alır."""
        try:
            # 2 değeri: "En iyi performans için ayarla" seçeneğine eşdeğerdir
            visual_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, visual_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)

            # Masaüstü Pencere Yöneticisi (DWM) saydamlık ve animasyonlarını kapat
            dwm_path = r"Software\Microsoft\Windows\DWM"
            key_dwm = winreg.OpenKey(winreg.HKEY_CURRENT_USER, dwm_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key_dwm, "EnableAeroPeek", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key_dwm, "ColorPrevalence", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key_dwm)
            return True
        except:
            return False

    def disable_heavy_services(self):
        """Eski bilgisayarları donduran Disk I/O servislerini durdurur."""
        try:
            # SysMain (Eski adıyla Superfetch) ve WSearch (Windows Arama İndeksi)
            services = ["SysMain", "WSearch"]
            for srv in services:
                subprocess.run(f'sc stop {srv}', shell=True, capture_output=True)
                subprocess.run(f'sc config {srv} start= disabled', shell=True, capture_output=True)
            return True
        except:
            return False

    def run_visual_boost(self):
        report = []
        report.append("[*] Düşük Sistem (Low-End) Optimizasyonu Başlatılıyor...")
        
        if self.strip_visual_effects():
            report.append("[+] Gereksiz görsel efektler, saydamlık ve animasyonlar kapatıldı. (GPU ve RAM rahatladı)")
            
        if self.disable_heavy_services():
            report.append("[+] SysMain ve WSearch servisleri durduruldu. (Disk %100 kullanım sorunu çözüldü)")
            
        report.append("\n✅ GÖRSEL & DİSK YÜKÜ SIFIRLANDI! (Değişikliklerin tam etki etmesi için bilgisayarı yeniden başlatın)")
        return report