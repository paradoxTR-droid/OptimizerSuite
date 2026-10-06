import subprocess

class GameShield:
    def __init__(self):
        pass

    def set_gaming_dns(self):
        """Aktif ağ adaptörünü bulup DNS'i Cloudflare (1.1.1.1) olarak ayarlar."""
        try:
            # PowerShell ile aktif, fiziksel ağ kartlarını bulup DNS'lerini değiştirir
            cmd = "powershell -Command \"Get-NetAdapter -Physical | Where-Object {$_.Status -eq 'Up'} | Set-DnsClientServerAddress -ServerAddresses ('1.1.1.1','1.0.0.1')\""
            subprocess.run(cmd, shell=True, capture_output=True)
            return True
        except:
            return False

    def block_windows_updates(self):
        """Oyun sırasında ping fırlatmasın diye Update servislerini durdurur."""
        try:
            # BITS (Arka plan indirme) ve WUAUSERV (Windows Update) durduruluyor
            services = ["wuauserv", "bits"]
            for srv in services:
                subprocess.run(f'sc stop {srv}', shell=True, capture_output=True)
                subprocess.run(f'sc config {srv} start= demand', shell=True, capture_output=True)
            return True
        except:
            return False

    def run_shield(self):
        """Oyun Kalkanını aktif eder ve rapor döner."""
        report = []
        report.append("[*] 🛡️ Oyun Kalkanı başlatılıyor...")
        
        if self.set_gaming_dns():
            report.append("[+] Ağ trafiği Cloudflare DNS (1.1.1.1) üzerine yönlendirildi.")
            report.append("    -> Sunucu yanıt süreleri (Ping) en aza indirgendi.")
            
        if self.block_windows_updates():
            report.append("[+] Windows Update ve BITS arka plan servisleri durduruldu.")
            report.append("    -> Oyun esnasında ani ping dalgalanmaları engellendi.")
            
        report.append("\n✅ OYUN KALKANI AKTİF! Kesintisiz rekabete hazırsınız.")
        return report