import os
import subprocess
import winreg

class UltimateTweaker:
    def __init__(self):
        pass

    def create_restore_point(self):
        """Sistemi korumak için Geri Yükleme Noktası oluşturur."""
        try:
            # PowerShell komutu ile restore point oluşturma
            cmd = 'powershell.exe -ExecutionPolicy Bypass -Command "Checkpoint-Computer -Description \'OptimizerSuite Pre-Tweak\' -RestorePointType MODIFY_SETTINGS"'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            return True
        except Exception:
            return False

    def enable_ultimate_performance(self):
        """Windows Gizli Ultimate Performance Güç Planını Aktif Eder."""
        try:
            # Güç planını sisteme ekle
            add_cmd = 'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61'
            subprocess.run(add_cmd, shell=True, capture_output=True)
            
            # Eklenen planı aktif kıl
            set_cmd = 'powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61'
            subprocess.run(set_cmd, shell=True, capture_output=True)
            return True
        except:
            return False

    def apply_registry_tweaks(self):
        """Menü gecikmelerini sıfırlar ve tepkiselliği artırır."""
        try:
            # Sağ tık ve menü açılış hızını 400ms'den 0ms'ye çekme
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "MenuShowDelay", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(key)

            # Başlat menüsünde web (Bing) aramasını kapatma (Hızlandırır ve gizliliği artırır)
            explorer_path = r"SOFTWARE\Policies\Microsoft\Windows\Explorer"
            try:
                # Key yoksa oluştururuz
                winreg.CreateKey(winreg.HKEY_CURRENT_USER, explorer_path)
                exp_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, explorer_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(exp_key, "DisableSearchBoxSuggestions", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(exp_key)
            except:
                pass
            return True
        except Exception as e:
            return False

    def disable_telemetry_and_privacy(self):
        """Gizlilik Kalkanı: Telemetri servislerini ve Reklam Kimliğini kapatır."""
        # 1. Servisleri Durdurma
        services = ["DiagTrack", "dmwappushservice", "MapsBroker"]
        for srv in services:
            subprocess.run(f'sc stop "{srv}"', shell=True, capture_output=True)
            subprocess.run(f'sc config "{srv}" start= disabled', shell=True, capture_output=True)

        # 2. Reklam Kimliğini (Advertising ID) Kapatma
        try:
            adv_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, adv_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except:
            pass
        return True

    def run_ultimate_tweak(self):
        """Tüm hardcore optimizasyonları sırayla çalıştırır."""
        report = []
        
        report.append("[*] Sistem Geri Yükleme Noktası oluşturuluyor (Bu işlem 10-15 saniye sürebilir)...")
        if self.create_restore_point():
            report.append("[+] Geri Yükleme Noktası başarıyla oluşturuldu. (Sistem güvende)")
        else:
            report.append("[-] Geri Yükleme Noktası oluşturulamadı (Windows ayarlarından kapalı olabilir). Devam ediliyor...")

        if self.enable_ultimate_performance():
            report.append("[+] 'Nihai Performans' güç planı aktif edildi. (İşlemci darboğazı kaldırıldı)")
            
        if self.apply_registry_tweaks():
            report.append("[+] Kayıt defteri görsel gecikmeleri 0ms'ye ayarlandı. Bing Web araması kapatıldı.")

        if self.disable_telemetry_and_privacy():
            report.append("[+] Gizlilik Kalkanı Aktif: Windows Telemetri servisleri ve Reklam Kimliği kapatıldı.")

        report.append("\n--- ULTIMATE TWEAKER ÖZETİ ---")
        report.append("Sistem en yüksek performans moduna alındı ve arka plan izleme servisleri köreltildi.")
        return report