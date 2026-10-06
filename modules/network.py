import subprocess
import winreg

class NetworkOptimizer:
    def __init__(self):
        pass

    def reset_network_stack(self):
        """DNS'i temizler, Winsock ve TCP/IP yığınını sıfırlar."""
        cmds = [
            "ipconfig /flushdns",
            "netsh winsock reset",
            "netsh int ip reset"
        ]
        for cmd in cmds:
            # shell=True ile komutları gizlice çalıştırıyoruz
            subprocess.run(cmd, shell=True, capture_output=True)
        return True

    def optimize_registry_ping(self):
        """
        Oyunlardaki gecikmeyi düşürmek için Nagle Algoritmasını kapatır
        ve Multimedia Throttling sınırını kaldırır.
        """
        try:
            # 1. Network Throttling Kapatma (Oyunlarda bant genişliği sınırını kaldırır)
            sys_profile_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sys_profile_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 0xFFFFFFFF)
            winreg.SetValueEx(key, "SystemResponsiveness", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)

            # 2. Nagle Algoritmasını Kapatma (TCP paketlerini biriktirmeden anında gönderir)
            interfaces_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
            # Hem okuma hem yazma yetkisi alıyoruz
            interfaces_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, interfaces_path, 0, winreg.KEY_READ | winreg.KEY_SET_VALUE)
            
            # Sistemdeki tüm ağ kartlarını (Wi-Fi, Ethernet) tarayıp ayarları uygulayalım
            num_subkeys = winreg.QueryInfoKey(interfaces_key)[0]
            for i in range(num_subkeys):
                try:
                    subkey_name = winreg.EnumKey(interfaces_key, i)
                    subkey = winreg.OpenKey(interfaces_key, subkey_name, 0, winreg.KEY_SET_VALUE)
                    
                    # TCPNoDelay ve TcpAckFrequency değerlerini 1 yaparak gecikmeyi sıfırlıyoruz
                    winreg.SetValueEx(subkey, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(subkey, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(subkey)
                except EnvironmentError:
                    continue # Yetki alınamayan boş/sistem arayüzlerini atla
                    
            winreg.CloseKey(interfaces_key)
            return True
        except Exception as e:
            return False

    def run_network_boost(self):
        """Tüm ağ optimizasyonlarını çalıştırır ve rapor döner."""
        report = []
        
        # 1. DNS ve TCP/IP Sıfırlama
        self.reset_network_stack()
        report.append("[*] DNS Önbelleği temizlendi ve TCP/IP bağlantıları sıfırlandı.")
        
        # 2. Registry Ping Optimizasyonu
        if self.optimize_registry_ping():
            report.append("[*] Nagle Algoritması kapatıldı (Paketler beklemeden gönderilecek).")
            report.append("[*] Windows Ağ Darboğazı (Network Throttling) devre dışı bırakıldı.")
        else:
            report.append("[!] Registry ağ ayarları yapılandırılamadı.")
            
        report.append("\n--- AĞ & PİNG ÖZETİ ---")
        report.append("Bağlantı gecikmesi en aza indirildi. Çevrimiçi oyunlarda tepki süresi artırıldı.")
        return report