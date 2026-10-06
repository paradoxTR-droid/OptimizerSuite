import winreg
import subprocess
import ctypes

class FPSBooster:
    def __init__(self):
        pass

    def force_timer_resolution(self):
        """Windows çekirdek zamanlayıcısını 0.5ms (5000 nanosaniye) değerine kilitler."""
        try:
            ntdll = ctypes.windll.ntdll
            current_res = ctypes.c_ulong()
            # 5000 birim = 0.5 milisaniye. True = Set
            ntdll.NtSetTimerResolution(5000, True, ctypes.byref(current_res))
            return True
        except:
            return False

    def disable_hpet_and_ticks(self):
        """HPET'i ve Dinamik Tickleri kapatarak CPU gecikmesini düşürür."""
        try:
            subprocess.run("bcdedit /set useplatformclock false", shell=True, capture_output=True)
            subprocess.run("bcdedit /set disabledynamictick yes", shell=True, capture_output=True)
            return True
        except:
            return False

    def disable_game_bar_dvr(self):
        """FPS katili Xbox Game DVR'ı kökünden kapatır."""
        try:
            # 1. GameConfigStore
            path1 = r"System\GameConfigStore"
            key1 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path1, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key1, "GameDVR_Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key1)

            # 2. Windows Policies
            path2 = r"SOFTWARE\Policies\Microsoft\Windows\GameDVR"
            try:
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path2)
                key2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path2, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key2, "AllowGameDVR", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key2)
            except:
                pass
            return True
        except:
            return False

    def enable_hags(self):
        """Hardware Accelerated GPU Scheduling (HAGS) Aktif Eder."""
        try:
            path = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "HwSchMode", 0, winreg.REG_DWORD, 2) # 2 = Enabled
            winreg.CloseKey(key)
            return True
        except:
            return False

    def run_extreme_fps(self):
        report = []
        report.append("[*] EXTREME FPS VE MICRO-STUTTER KORUMASI BAŞLATILIYOR...")
        
        if self.force_timer_resolution():
            report.append("[+] Timer Resolution 0.5ms'ye zorlandı! (Uygulama açık kaldıkça akıcılık maksimumda olacak)")
            
        if self.disable_hpet_and_ticks():
            report.append("[+] HPET ve Dynamic Ticks kapatıldı. (İşlemci darboğazı azaltıldı)")
            
        if self.disable_game_bar_dvr():
            report.append("[+] Xbox Game DVR arka plan kayıtları tamamen yok edildi.")
            
        if self.enable_hags():
            report.append("[+] Donanım Hızlandırmalı GPU Zamanlaması (HAGS) açıldı.")

        report.append("\n✅ MAKSİMUM KARE HIZI (FPS) KİLİDİ AÇILDI! (Bazı ayarlar için yeniden başlatma gerekebilir)")
        return report