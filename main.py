import sys
import ctypes
import psutil
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QPushButton, QHBoxLayout, QStackedWidget, 
                             QListWidget, QProgressBar, QTextEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# --- 14 DEV MODÜLÜMÜZ ---
from modules.cleaner import DeepCleaner
from modules.booster import GameBooster 
from modules.network import NetworkOptimizer
from modules.startup import StartupManager
from modules.shield import GameShield
from modules.visuals import VisualOptimizer
from modules.inputlag import InputOptimizer
from modules.fps import FPSBooster
from modules.gpu import GPUOptimizer
from modules.ssd import SSDOptimizer
from modules.esports import EsportsOptimizer
from modules.nuke import AnnoyanceNuker
from modules.mmcss import MMCSSOptimizer
from modules.nic import NICOptimizer
from modules.tweaker import UltimateTweaker

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class OptimizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexus Optimizer - QUANTUM SINGULARITY EDITION")
        self.resize(1350, 950)
        self.init_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_stats)
        self.timer.start(1000)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. SOL MENÜ (15 Sekme)
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(310)
        self.sidebar.addItems([
            "🏠 Dashboard (Ana Panel)", 
            "🧹 Derin Temizlik", 
            "🚀 RAM & İşlem", 
            "🌐 Ağ & Ping", 
            "⏱ Açılış Hızı", 
            "🛡️ Oyun Kalkanı", 
            "📉 Düşük Sistem (Görsel)", 
            "⚡ Input Lag Sıfırlayıcı",
            "🔥 EXTREME FPS BOOST",
            "🎮 GPU Shader Temizleyici",
            "💽 SSD Overdrive (TRIM)",
            "🎯 Esports Aim & FSO",
            "☢️ Prangaları Kır (Nuke)",
            "⚙️ MMCSS Oyun Motoru",
            "📡 Derin NIC (Ağ Kartı)",
            "⚠️ Ultimate Tweak"
        ])
        self.sidebar.currentRowChanged.connect(self.change_page)
        
        # 2. İÇERİK ALANI
        self.pages = QStackedWidget()
        
        self.page_dashboard = self.create_dashboard_page()
        self.page_cleaner = self.create_module_page("Derin Sistem Temizliği", "Gereksiz dosyaları ve önbellekleri siler.", "#e63946", self.run_cleaner)
        self.page_booster = self.create_module_page("RAM ve Oyun Modu", "Arka plan işlemlerini kapatıp RAM sıkıştırır.", "#fca311", self.run_booster)
        self.page_network = self.create_module_page("Ağ ve Ping Optimizasyonu", "TCP/IP yığınını ve Nagle Algoritmasını sıfırlar.", "#4361ee", self.run_network)
        self.page_startup = self.create_module_page("Başlangıç Hızlandırıcısı", "Windows açılışını yavaşlatan programları kapatır.", "#ff006e", self.run_startup)
        self.page_shield = self.create_module_page("Oyun Kalkanı (Game Shield)", "Pingi düşürmek için DNS değiştirir, Update'leri durdurur.", "#00b4d8", self.run_shield)
        self.page_visuals = self.create_module_page("Düşük Sistem Kurtarıcısı", "Diski sömüren servisleri ve Windows animasyonlarını kapatır.", "#f15bb5", self.run_visuals)
        self.page_input = self.create_module_page("Input Lag Optimizasyonu", "Klavye ve fare tepki süresini minimuma indirir.", "#9b5de5", self.run_input)
        self.page_fps = self.create_module_page("Extreme FPS & Anti-Stutter", "Timer Resolution'ı 0.5ms yapar, Game DVR ve HPET'i öldürür.", "#ff5400", self.run_fps)
        self.page_gpu = self.create_module_page("GPU Shader Cache Temizleyici", "Ekran kartı kalıntılarını silerek oyunlardaki anlık dropları çözer.", "#00ff7f", self.run_gpu)
        self.page_ssd = self.create_module_page("SSD & NTFS Overdrive", "Diski zorla TRIM'ler ve Windows'un disk yoran kayıtlarını kapatır.", "#f72585", self.run_ssd)
        self.page_esports = self.create_module_page("Esports Aim Optimizasyonu", "Mouse İvmesini (Acceleration) ve FSO'yu global kapatır.", "#ffd166", self.run_esports)
        self.page_nuke = self.create_module_page("Windows Prangalarını Kır", "Windows reklamlarını, bloat yazılımları ve SmartScreen'i yok eder.", "#d90429", self.run_nuke)
        self.page_mmcss = self.create_module_page("MMCSS Oyun Motoru", "Windows'un oyunlara %100 CPU/GPU ayırmasını sağlar.", "#8338ec", self.run_mmcss)
        self.page_nic = self.create_module_page("Derin Ağ Kartı Optimizasyonu", "LSO ve Checksum özelliklerini kapatarak paket kaybını önler.", "#3a0ca3", self.run_nic)
        self.page_tweaker = self.create_module_page("Nihai Sistem Tweaker", "Telemetriyi kapatır, güç ayarlarını zorlar.", "#7209b7", self.run_tweaker)

        self.pages.addWidget(self.page_dashboard)
        self.pages.addWidget(self.page_cleaner)
        self.pages.addWidget(self.page_booster)
        self.pages.addWidget(self.page_network)
        self.pages.addWidget(self.page_startup)
        self.pages.addWidget(self.page_shield)
        self.pages.addWidget(self.page_visuals)
        self.pages.addWidget(self.page_input)
        self.pages.addWidget(self.page_fps)
        self.pages.addWidget(self.page_gpu)
        self.pages.addWidget(self.page_ssd)
        self.pages.addWidget(self.page_esports)
        self.pages.addWidget(self.page_nuke)
        self.pages.addWidget(self.page_mmcss)
        self.pages.addWidget(self.page_nic)
        self.pages.addWidget(self.page_tweaker)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)
        self.apply_theme()

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("QUANTUM SINGULARITY CORE")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        
        self.cpu_label = QLabel("CPU Kullanımı: %0")
        self.cpu_label.setStyleSheet("color: #aeb4c0; font-size: 16px;")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setFixedHeight(14)
        
        self.ram_label = QLabel("RAM Kullanımı: %0")
        self.ram_label.setStyleSheet("color: #aeb4c0; font-size: 16px;")
        self.ram_bar = QProgressBar()
        self.ram_bar.setTextVisible(False)
        self.ram_bar.setFixedHeight(14)

        self.btn_turbo = QPushButton("🌌 NİHAİ QUANTUM BOOST (14 MODÜL)")
        self.btn_turbo.setFixedHeight(90)
        self.btn_turbo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.btn_turbo.setStyleSheet("""
            QPushButton { background-color: #00ffcc; color: #121212; border-radius: 12px; }
            QPushButton:hover { background-color: #00cca3; }
        """)
        self.btn_turbo.clicked.connect(self.run_all_modules)

        self.dash_log = QTextEdit()
        self.dash_log.setReadOnly(True)
        self.dash_log.setStyleSheet("background-color: #020202; color: #00ffcc; font-family: Consolas; border-radius: 8px; padding: 15px; font-size: 15px;")

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addSpacing(10)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)
        layout.addSpacing(40)
        layout.addWidget(self.btn_turbo)
        layout.addSpacing(20)
        layout.addWidget(self.dash_log)
        
        return page

    def create_module_page(self, title_text, desc_text, color, function_to_call):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel(title_text)
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {color};")
        
        desc = QLabel(desc_text)
        desc.setStyleSheet("color: #aeb4c0; font-size: 15px;")

        btn = QPushButton(f"{title_text.split()[0]} Başlat")
        btn.setFixedHeight(55)
        btn.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; font-weight: bold; font-size: 17px; border-radius: 8px; }} QPushButton:hover {{ opacity: 0.8; }}")
        
        log_screen = QTextEdit()
        log_screen.setReadOnly(True)
        log_screen.setStyleSheet("background-color: #020202; color: #aeb4c0; font-family: Consolas; border-radius: 8px; padding: 15px; font-size: 15px;")
        
        btn.clicked.connect(lambda: function_to_call(log_screen, btn))

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(20)
        layout.addWidget(btn)
        layout.addSpacing(20)
        layout.addWidget(log_screen)

        return page

    def change_page(self, index):
        self.pages.setCurrentIndex(index)

    def update_system_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.cpu_label.setText(f"İşlemci (CPU) Yükü: %{cpu}")
        self.cpu_bar.setValue(int(cpu))
        self.ram_label.setText(f"Bellek (RAM) Yükü: %{ram}")
        self.ram_bar.setValue(int(ram))

    def log_msg(self, log_widget, msg):
        log_widget.append(msg)
        scroll_bar = log_widget.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        QApplication.processEvents() 

    def run_cleaner(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "🧹 Temizlik başlatıldı...")
        _, report = DeepCleaner().run_full_cleanup()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_booster(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "🚀 RAM sıkıştırılıyor...")
        report = GameBooster().run_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_network(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "🌐 Ağ yapılandırması sıfırlanıyor...")
        report = NetworkOptimizer().run_network_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)
        
    def run_startup(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "⏱️ Başlangıç hızlandırılıyor...")
        report = StartupManager().run_startup_optimizer()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_shield(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "🛡️ Oyun kalkanı başlatılıyor...")
        report = GameShield().run_shield()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_visuals(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "📉 Düşük sistem koruması aktif ediliyor...")
        report = VisualOptimizer().run_visual_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_input(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "⚡ Giriş gecikmesi optimize ediliyor...")
        report = InputOptimizer().run_input_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_fps(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "🔥 Extreme FPS yükleniyor...")
        report = FPSBooster().run_extreme_fps()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_gpu(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "🎮 GPU Shader önbelleği temizleniyor...")
        report = GPUOptimizer().run_gpu_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_ssd(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "💽 SSD TRIM ve NTFS optimizasyonu yapılıyor...")
        report = SSDOptimizer().run_ssd_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_esports(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "🎯 Mouse Acceleration ve FSO kapatılıyor...")
        report = EsportsOptimizer().run_esports_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_nuke(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "☢️️ Windows prangaları kırılıyor...")
        report = AnnoyanceNuker().run_nuke()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_mmcss(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "⚙️ MMCSS Oyun motoru devreye alınıyor...")
        report = MMCSSOptimizer().run_mmcss_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_nic(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "📡 Ağ Kartı donanım özellikleri kapatılıyor...")
        report = NICOptimizer().run_nic_boost()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def run_tweaker(self, log_widget, btn):
        btn.setEnabled(False)
        self.log_msg(log_widget, "⚠️ Geri yükleme noktası alınıyor (Donmalar olabilir)...")
        report = UltimateTweaker().run_ultimate_tweak()
        self.log_msg(log_widget, "\n".join(report))
        btn.setEnabled(True)

    def force_reboot(self):
        """Tüm işlemler bittikten sonra sistemi 15 saniye içinde zorla yeniden başlatır."""
        self.log_msg(self.dash_log, "\n[⚠️] UYARI: Değişikliklerin çekirdek seviyesinde uygulanması için sistem YENİDEN BAŞLATILIYOR!")
        self.log_msg(self.dash_log, "[!] Lütfen açık olan çalışmalarınızı hemen kaydedin. (15 Saniye...)")
        subprocess.run('shutdown /r /f /t 15 /c "Nexus Optimizer: Sistem maksimum performans moduna geciyor. Bilgisayar yeniden baslatiliyor..."', shell=True)

    def run_all_modules(self):
        self.btn_turbo.setEnabled(False)
        self.btn_turbo.setText("QUANTUM SENTEZİ DEVREDE...")
        self.dash_log.clear()
        
        self.log_msg(self.dash_log, ">>> NİHAİ QUANTUM BOOST BAŞLATILDI <<<\n")
        
        modules = [
            ("[1/14] RAM & İşlem Optimizasyonu...", GameBooster().run_boost),
            ("[2/14] Derin Temizlik...", lambda: DeepCleaner().run_full_cleanup()[1]),
            ("[3/14] Ping ve Ağ Ayarları...", NetworkOptimizer().run_network_boost),
            ("[4/14] Başlangıç Hızlandırıcısı...", StartupManager().run_startup_optimizer),
            ("[5/14] Oyun Kalkanı (DNS/Update)...", GameShield().run_shield),
            ("[6/14] Düşük Sistem Optimizasyonu...", VisualOptimizer().run_visual_boost),
            ("[7/14] Input Lag Sıfırlayıcı...", InputOptimizer().run_input_boost),
            ("[8/14] EXTREME FPS & 0.5ms Timer...", FPSBooster().run_extreme_fps),
            ("[9/14] GPU Shader Temizleyici...", GPUOptimizer().run_gpu_boost),
            ("[10/14] SSD Overdrive (TRIM)...", SSDOptimizer().run_ssd_boost),
            ("[11/14] Esports Aim (Mouse/FSO)...", EsportsOptimizer().run_esports_boost),
            ("[12/14] Windows Prangalarını Kır...", AnnoyanceNuker().run_nuke),
            ("[13/14] MMCSS Oyun Motoru Enjeksiyonu...", MMCSSOptimizer().run_mmcss_boost),
            ("[14/14] Derin NIC (Ağ Kartı) Gecikme Önleyici...", NICOptimizer().run_nic_boost)
        ]

        for title, func in modules:
            self.log_msg(self.dash_log, title)
            try:
                report_lines = func()
                self.log_msg(self.dash_log, "\n".join(report_lines) + "\n")
            except Exception as e:
                self.log_msg(self.dash_log, f"[!] Hata oluştu: {str(e)}\n")

        self.log_msg(self.dash_log, "\n✅ İŞLETİM SİSTEMİ TAMAMEN SİZE İTAAT EDİYOR. OYUN BAŞLASIN!")
        self.btn_turbo.setText("🌌 NİHAİ QUANTUM BOOST (14 MODÜL)")
        self.btn_turbo.setEnabled(True)
        
        # Sistemi yeniden başlat
        self.force_reboot()

    def apply_theme(self):
        style = """
        QMainWindow { background-color: #030303; }
        QListWidget { background-color: #0a0a0a; color: #a6adc8; border: none; font-size: 15px; font-weight: bold; padding-top: 15px; }
        QListWidget::item { padding: 12px 15px; border-radius: 5px; margin: 4px 10px; }
        QListWidget::item:selected { background-color: #00ffcc; color: #030303; }
        QListWidget::item:hover { background-color: #1e293b; }
        QProgressBar { border: none; background-color: #1e293b; border-radius: 5px; text-align: center; color: white; }
        QProgressBar::chunk { background-color: #b185db; border-radius: 5px; }
        """
        self.setStyleSheet(style)

if __name__ == "__main__":
    if is_admin():
        app = QApplication(sys.argv)
        window = OptimizerApp()
        window.show()
        sys.exit(app.exec())
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)