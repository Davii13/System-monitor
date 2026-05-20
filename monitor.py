import customtkinter as ctk
import psutil
import cpuinfo
import platform
import threading
import time
import speedtest
from py3nvml.py3nvml import *
import psutil
import platform
import os
import clr
_DLL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dll",
    "LibreHardwareMonitorLib.dll"
)
clr.AddReference(_DLL_PATH)
from LibreHardwareMonitor.Hardware import Computer

IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    try:
        import wmi
    except ImportError:
        wmi = None
else:
    wmi = None

# ==========================================
# DESIGN SYSTEM
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG_COLOR = "#0a0a0c"
CARD_BG = "#121418"
BORDER_COLOR = "#2a2d35"

ACCENT_CYAN = "#00f2ff"
COLOR_SAFE = "#00e676"   
COLOR_WARN = "#ffea00"   
COLOR_DANGER = "#ff1744" 
TEXT_GRAY = "#8a93a6"

# ==========================================
# GAUGE CUSTOMIZADO
# ==========================================
class TelemetryGauge(ctk.CTkCanvas):
    def __init__(self, parent, size=240, title=""):
        super().__init__(parent, width=size, height=size, bg=CARD_BG, highlightthickness=0)
        self.size = size
        self.title = title
        self.value = 0
        self.text_val = "0%"
        self.draw_gauge()

    def get_color(self):
        if self.value < 60: return COLOR_SAFE
        elif self.value < 85: return COLOR_WARN
        else: return COLOR_DANGER

    def set_value(self, value, text_val=None):
        self.value = max(0, min(100, value))
        self.text_val = text_val if text_val else f"{int(self.value)}%"
        self.draw_gauge()

    def draw_gauge(self):
        self.delete("all")
        current_color = self.get_color()
        padding = 20
        coord = padding, padding, self.size - padding, self.size - padding
        
        self.create_arc(coord, start=225, extent=-270, style="arc", outline="#1e222b", width=18)
        
        extent = -(270 * (self.value / 100))
        if extent != 0:
            self.create_arc(coord, start=225, extent=extent, style="arc", outline=current_color, width=18)
        
        self.create_oval(padding+12, padding+12, self.size-padding-12, self.size-padding-12, outline="#16191f", width=2)
        self.create_text(self.size / 2, self.size / 2 - 10, text=self.text_val, fill="white", font=("Orbitron", 36, "bold"))
        self.create_text(self.size / 2, self.size / 2 + 35, text=self.title, fill=TEXT_GRAY, font=("Rajdhani", 12, "bold"))

# ==========================================
# APP PRINCIPAL
# ==========================================
class SystemMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HEATCORE TELEMETRY PRO")
        self.geometry("1280x720")
        self.configure(fg_color=BG_COLOR)

        self.init_hardware()
        
        self.net_history_down = [0, 0, 0]
        self.net_history_up = [0, 0, 0]
        self.is_widget_mode = False

        self.setup_ui()
        self.update_stats()

    def init_hardware(self):
        try:
            nvmlInit()
            self.has_gpu = True
        except:
            self.has_gpu = False

        try:
            self.w_obj = wmi.WMI(namespace="root\\wmi") if (IS_WINDOWS and wmi) else None
        except:
            self.w_obj = None

        self.last_net_recv = psutil.net_io_counters().bytes_recv
        self.last_net_sent = psutil.net_io_counters().bytes_sent
        self.last_net_time = time.time()
        self.cpu_name = cpuinfo.get_cpu_info().get("brand_raw", "Processador")

    # ==========================================
    # ESTRUTURA DA INTERFACE
    # ==========================================
    def setup_ui(self):
        # Container do Modo Normal (Sidebar + Conteúdo)
        self.normal_container = ctk.CTkFrame(self, fg_color="transparent")
        self.normal_container.pack(fill="both", expand=True)

        # Container do Modo Widget (Inicia oculto)
        self.widget_container = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=10, border_width=2, border_color=BORDER_COLOR)
        
        self.build_sidebar()
        self.build_pages()
        self.build_widget_ui()
        
        # Inicia na página Dashboard
        self.navigate_to("dashboard")

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.normal_container, width=220, corner_radius=0, fg_color=CARD_BG)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", pady=30, padx=20)
        ctk.CTkLabel(logo_frame, text="HEATCORE", font=("Orbitron", 22, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="TELEMETRY PRO", font=("Rajdhani", 12), text_color=ACCENT_CYAN).pack(anchor="w")

        # Botões de Navegação
        self.nav_buttons = {}
        
        self.btn_dash = self.create_nav_button("📊  DASHBOARD", "dashboard")
        self.btn_net = self.create_nav_button("📶  CONECTIVIDADE", "network")
        
        # Botão Modo Widget fica lá embaixo
        self.btn_widget = ctk.CTkButton(self.sidebar, text="📌 MODO WIDGET", font=("Rajdhani", 14, "bold"), 
                                        fg_color="#1e222b", text_color="white", hover_color=BORDER_COLOR, 
                                        height=45, command=self.enable_widget_mode)
        self.btn_widget.pack(side="bottom", fill="x", padx=20, pady=30)

    def create_nav_button(self, text, page_name):
        btn = ctk.CTkButton(self.sidebar, text=text, font=("Rajdhani", 15, "bold"), height=50,
                            fg_color="transparent", text_color=TEXT_GRAY, hover_color="#1a1d24", anchor="w",
                            command=lambda: self.navigate_to(page_name))
        btn.pack(fill="x", padx=15, pady=5)
        self.nav_buttons[page_name] = btn
        return btn

    def navigate_to(self, page_name):
        # Atualiza Estado Visual do Menu (Destaque do ativo)
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(fg_color="#1e222b", text_color=ACCENT_CYAN) # Estado Ativo
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_GRAY) # Inativo

        # Alterna as páginas
        if page_name == "dashboard":
            self.page_network.pack_forget()
            self.page_dashboard.pack(fill="both", expand=True, padx=25, pady=25)
        elif page_name == "network":
            self.page_dashboard.pack_forget()
            self.page_network.pack(fill="both", expand=True, padx=25, pady=25)

    def build_pages(self):
        self.content_area = ctk.CTkFrame(self.normal_container, fg_color="transparent")
        self.content_area.pack(side="left", fill="both", expand=True)

        # --- PÁGINA 1: DASHBOARD ---
        self.page_dashboard = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.page_dashboard.grid_columnconfigure((0, 1, 2), weight=1)
        self.page_dashboard.grid_rowconfigure(0, weight=2)
        self.page_dashboard.grid_rowconfigure(1, weight=1)

        
       # CPU

        self.cpu_frame = self.create_card(self.page_dashboard, 0, 0)

        ctk.CTkLabel(self.cpu_frame, text="CPU CORE", font=("Orbitron", 14, "bold"), text_color="white").pack(pady=(15, 0))

        self.cpu_gauge = TelemetryGauge(self.cpu_frame, size=240, title="LOAD")

        self.cpu_gauge.pack(pady=10, expand=True)

        self.cpu_temp_label = ctk.CTkLabel(self.cpu_frame, text="🌡 --°C",

                                            font=("Orbitron", 22, "bold"),

                                            text_color=COLOR_SAFE)

        self.cpu_temp_label.pack(pady=(0, 2))

        self.cpu_metrics = ctk.CTkLabel(self.cpu_frame, text="CLK: -- MHz",

                                         font=("Rajdhani", 13),

                                         text_color=TEXT_GRAY)

        self.cpu_metrics.pack(pady=(0, 15))
 

        # GPU
        self.gpu_frame = self.create_card(self.page_dashboard, 0, 1)
        ctk.CTkLabel(self.gpu_frame, text="GPU ENGINE", font=("Orbitron", 14, "bold"), text_color="white").pack(pady=(15, 0))
        self.gpu_gauge = TelemetryGauge(self.gpu_frame, size=240, title="LOAD")
        self.gpu_gauge.pack(pady=10, expand=True)
        self.gpu_metrics = ctk.CTkLabel(self.gpu_frame, text="TEMP: -- | VRAM: --", font=("Rajdhani", 14, "bold"), text_color="white")
        self.gpu_metrics.pack(pady=(0, 15))

        # RAM
        self.ram_frame = self.create_card(self.page_dashboard, 0, 2)
        ctk.CTkLabel(self.ram_frame, text="SYSTEM MEMORY", font=("Orbitron", 14, "bold"), text_color="white").pack(pady=(15, 0))
        self.ram_gauge = TelemetryGauge(self.ram_frame, size=240, title="USAGE")
        self.ram_gauge.pack(pady=10, expand=True)
        self.ram_metrics = ctk.CTkLabel(self.ram_frame, text="USED: -- / -- GB", font=("Rajdhani", 14, "bold"), text_color="white")
        self.ram_metrics.pack(pady=(0, 15))

        # DISCO
        self.disk_frame = self.create_card(self.page_dashboard, 1, 0, colspan=3)
        ctk.CTkLabel(self.disk_frame, text="📀 ARMAZENAMENTO (C:)", font=("Orbitron", 12, "bold"), text_color="white").pack(anchor="nw", padx=20, pady=(15, 5))
        self.disk_usage = ctk.CTkLabel(self.disk_frame, text="0%", font=("Orbitron", 24, "bold"), text_color="white")
        self.disk_usage.pack(pady=(5, 0))
        self.disk_bar = ctk.CTkProgressBar(self.disk_frame, progress_color=COLOR_SAFE, fg_color="#1e222b", height=12)
        self.disk_bar.set(0)
        self.disk_bar.pack(fill="x", padx=40, pady=10)

        # --- PÁGINA 2: CONECTIVIDADE ---
        self.page_network = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.page_network.grid_columnconfigure((0, 1), weight=1)
        self.page_network.grid_rowconfigure(0, weight=1)

        # Rede Ao Vivo
        self.net_live_frame = self.create_card(self.page_network, 0, 0)
        ctk.CTkLabel(self.net_live_frame, text="📶 TRÁFEGO AO VIVO", font=("Orbitron", 16, "bold"), text_color="white").pack(pady=30)
        self.net_down_mbps = ctk.CTkLabel(self.net_live_frame, text="⬇ 0.00 Mbps", font=("Orbitron", 40, "bold"), text_color=COLOR_SAFE)
        self.net_down_mbps.pack(pady=20)
        self.net_up_mbps = ctk.CTkLabel(self.net_live_frame, text="⬆ 0.00 Mbps", font=("Orbitron", 40, "bold"), text_color="#00b0ff")
        self.net_up_mbps.pack(pady=20)

        # Speedtest
        self.net_st_frame = self.create_card(self.page_network, 0, 1)
        ctk.CTkLabel(self.net_st_frame, text="🚀 SPEEDTEST OFICIAL", font=("Orbitron", 16, "bold"), text_color="white").pack(pady=30)
        self.btn_speedtest = ctk.CTkButton(self.net_st_frame, text="INICIAR TESTE MÁXIMO", font=("Rajdhani", 16, "bold"), height=50, fg_color=BORDER_COLOR, hover_color="#3a3d45", command=self.start_speedtest)
        self.btn_speedtest.pack(pady=20)
        self.lbl_st_results = ctk.CTkLabel(self.net_st_frame, text="Teste não realizado.", font=("Rajdhani", 16), text_color=TEXT_GRAY)
        self.lbl_st_results.pack(pady=20)

    def create_card(self, parent, row, col, colspan=1):
        frame = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        frame.grid(row=row, column=col, columnspan=colspan, padx=10, pady=10, sticky="nsew")
        return frame

    # ==========================================
    # LÓGICA DO MODO WIDGET
    # ==========================================
    def build_widget_ui(self):
        # Barra de arrastar superior
        self.drag_bar = ctk.CTkFrame(self.widget_container, height=25, fg_color="#1e222b", corner_radius=10)
        self.drag_bar.pack(fill="x", side="top")
        
        # Eventos para arrastar a janela sem bordas
        self.drag_bar.bind("<ButtonPress-1>", self.start_move)
        self.drag_bar.bind("<B1-Motion>", self.do_move)
        
        ctk.CTkLabel(self.drag_bar, text="HEATCORE", font=("Orbitron", 10, "bold")).pack(side="left", padx=10)
        
        # Botão para voltar ao normal
        btn_close_widget = ctk.CTkButton(self.drag_bar, text="⛶", width=25, height=20, fg_color="transparent", hover_color=BORDER_COLOR, command=self.disable_widget_mode)
        btn_close_widget.pack(side="right", padx=5)

        # Conteúdo do Widget
        content = ctk.CTkFrame(self.widget_container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.wdg_cpu = ctk.CTkLabel(content, text="CPU: 0%", font=("Orbitron", 14, "bold"), text_color=COLOR_SAFE)
        self.wdg_cpu.pack(side="left", expand=True)
        self.wdg_gpu = ctk.CTkLabel(content, text="GPU: 0%", font=("Orbitron", 14, "bold"), text_color=COLOR_WARN)
        self.wdg_gpu.pack(side="left", expand=True)
        self.wdg_ram = ctk.CTkLabel(content, text="RAM: 0%", font=("Orbitron", 14, "bold"), text_color=ACCENT_CYAN)
        self.wdg_ram.pack(side="left", expand=True)

    def enable_widget_mode(self):
        self.is_widget_mode = True
        self.normal_container.pack_forget()
        self.widget_container.pack(fill="both", expand=True)
        
        self.overrideredirect(True) # Remove bordas do SO
        self.attributes("-topmost", True) # Trava por cima de tudo
        self.geometry("320x80") # Fica pequeno

    def disable_widget_mode(self):
        self.is_widget_mode = False
        self.widget_container.pack_forget()
        self.normal_container.pack(fill="both", expand=True)
        
        self.overrideredirect(False)
        self.attributes("-topmost", False)
        self.geometry("1280x720")

    # Funções para mover a janela no modo Widget
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    # ==========================================
    # COLETA DE DADOS (Mantida e otimizada)
    # ==========================================
    def get_cpu_temp(self):

        try:

            if not hasattr(self, "_lhm_computer"):

                print("[DEBUG] Inicializando LHM Computer...")

                self._lhm_computer = Computer()

                self._lhm_computer.IsCpuEnabled = True

                self._lhm_computer.Open()

                print("[DEBUG] LHM Computer aberto.")
    
            for hw in self._lhm_computer.Hardware:

                print(f"[DEBUG] Hardware encontrado: {hw.HardwareType} - {hw.Name}")

                if "Cpu" not in str(hw.HardwareType):

                    continue

                hw.Update()

                print(f"[DEBUG] Sensores da CPU:")

                for s in hw.Sensors:

                    print(f"  - [{s.SensorType}] {s.Name} = {s.Value}")

                temps = [

                    float(s.Value) for s in hw.Sensors

                    if str(s.SensorType) == "Temperature" and s.Value is not None

                ]

                if temps:

                    result = f"{max(temps):.0f}°C"

                    print(f"[DEBUG] Retornando: {result}")

                    return result

                else:

                    print("[DEBUG] Nenhum sensor de temperatura com valor!")

        except Exception as e:

            print(f"[DEBUG] EXCEÇÃO: {type(e).__name__}: {e}")

        return "N/A"
 
    
    def start_speedtest(self):
        self.btn_speedtest.configure(state="disabled", text="TESTANDO...")
        self.lbl_st_results.configure(text="Conectando... Aguarde cerca de 15s.")
        threading.Thread(target=self._run_speedtest_thread, daemon=True).start()

    def _run_speedtest_thread(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            down_max = st.download() / 1_000_000
            up_max = st.upload() / 1_000_000
            ping = st.results.ping
            self.lbl_st_results.configure(text=f"PING: {ping:.0f} ms | DOWN: {down_max:.1f} Mbps | UP: {up_max:.1f} Mbps", text_color=COLOR_SAFE)
        except Exception:
            self.lbl_st_results.configure(text="Falha. Verifique a rede.", text_color=COLOR_DANGER)
        finally:
            self.btn_speedtest.configure(state="normal", text="REFAZER TESTE")

    def update_stats(self):
        # Coleta
        cpu_usage = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq()
        temp = self.get_cpu_temp()
        m = psutil.virtual_memory()
        
        gpu_usage = 0
        if self.has_gpu:
            try:
                h = nvmlDeviceGetHandleByIndex(0)
                gpu_usage = nvmlDeviceGetUtilizationRates(h).gpu
                mem = nvmlDeviceGetMemoryInfo(h)
                gtmp = nvmlDeviceGetTemperature(h, NVML_TEMPERATURE_GPU)
            except: pass

        # Atualiza UI (Modo Normal)
        if not self.is_widget_mode:
            self.cpu_gauge.set_value(cpu_usage)
            # Temperatura com cor dinâmica
            temp_color = COLOR_SAFE
            if temp != "N/A":
                try:
                    tv = int(temp.replace("°C", ""))
                    if tv >= 80: temp_color = COLOR_DANGER
                    elif tv >= 65: temp_color = COLOR_WARN
                except ValueError:
                    pass
            self.cpu_temp_label.configure(text=f"🌡 {temp}", text_color=temp_color)
            self.cpu_metrics.configure(
                text=f"CLK: {cpu_freq.current:.0f} MHz" if cpu_freq else "CLK: --"
            )
            
            if self.has_gpu:
                self.gpu_gauge.set_value(gpu_usage)
                self.gpu_metrics.configure(text=f"TEMP: {gtmp}°C | VRAM: {mem.used//1024**2}/{mem.total//1024**2} MB")
                
            self.ram_gauge.set_value(m.percent)
            self.ram_metrics.configure(text=f"USED: {m.used/1024**3:.1f} / {m.total/1024**3:.1f} GB")

            d = psutil.disk_usage("/")
            self.disk_usage.configure(text=f"{d.percent}%")
            self.disk_bar.set(d.percent / 100)

            # Rede
            net_io = psutil.net_io_counters()
            now = time.time()
            dt = now - self.last_net_time
            if dt > 0:
                raw_down_bps = max(0, (net_io.bytes_recv - self.last_net_recv) / dt)
                raw_up_bps = max(0, (net_io.bytes_sent - self.last_net_sent) / dt)
                
                self.net_history_down.append(raw_down_bps)
                self.net_history_up.append(raw_up_bps)
                if len(self.net_history_down) > 4: self.net_history_down.pop(0)
                if len(self.net_history_up) > 4: self.net_history_up.pop(0)

                avg_down_bps = sum(self.net_history_down) / len(self.net_history_down)
                avg_up_bps = sum(self.net_history_up) / len(self.net_history_up)

                self.net_down_mbps.configure(text=f"⬇ {(avg_down_bps * 8) / 1_000_000:.1f} Mbps")
                self.net_up_mbps.configure(text=f"⬆ {(avg_up_bps * 8) / 1_000_000:.1f} Mbps")
                
                self.last_net_recv = net_io.bytes_recv
                self.last_net_sent = net_io.bytes_sent
                self.last_net_time = now

        # Atualiza UI (Modo Widget)
        else:
            self.wdg_cpu.configure(text=f"CPU: {cpu_usage:.0f}%", text_color=COLOR_DANGER if cpu_usage > 85 else COLOR_SAFE)
            self.wdg_gpu.configure(text=f"GPU: {gpu_usage:.0f}%", text_color=COLOR_DANGER if gpu_usage > 85 else COLOR_WARN)
            self.wdg_ram.configure(text=f"RAM: {m.percent:.0f}%", text_color=COLOR_DANGER if m.percent > 90 else ACCENT_CYAN)

        self.after(1000, self.update_stats)

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()