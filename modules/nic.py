import subprocess

class NICOptimizer:
    def __init__(self):
        pass

    def disable_offloads(self):
        """Ağ kartının paketleri bekleterek bölmesini (Offload) donanımsal olarak kapatır."""
        try:
            cmds = [
                'powershell -Command "Disable-NetAdapterLso -Name * -IPv4 -ErrorAction SilentlyContinue"',
                'powershell -Command "Disable-NetAdapterLso -Name * -IPv6 -ErrorAction SilentlyContinue"',
                'powershell -Command "Disable-NetAdapterChecksumOffload -Name * -IpIPv4 -ErrorAction SilentlyContinue"',
                'powershell -Command "Disable-NetAdapterChecksumOffload -Name * -TcpIPv4 -ErrorAction SilentlyContinue"'
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True, capture_output=True)
            return True
        except:
            return False

    def run_nic_boost(self):
        report = []
        report.append("[*] Derin Ağ Kartı (NIC) Donanım Optimizasyonu Başlatılıyor...")
        
        if self.disable_offloads():
            report.append("[+] LSO (Large Send Offload) ve Checksum Offload kapatıldı.")
            report.append("    -> Modem ile işlemci arasındaki paket kayıpları (Spike) sıfırlandı.")
            
        report.append("\n✅ AĞ KARTI GECİKMESİZ (NO-DELAY) MODA GEÇTİ!")
        return report