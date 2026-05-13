import customtkinter as ctk
import psutil
import cpuinfo
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from py3nvml.py3nvml import *
import threading
import time

# Importação condicional do WMI (Apenas Windows)
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
ctk.set_default_color_theme("blue")

ACCENT_CYAN = "#00f2ff"
ACCENT_MAGENTA = "#ff00e5"
BG_COLOR = "#0b0e14"
CARD_BG = "#151921"
BORDER_COLOR = "#232936"

# ==========================================
# APP PRINCIPAL
# ==========================================
class SystemMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HEATCORE v2.0")
        self.geometry("1150x800")
        self.configure(fg_color=BG_COLOR)

        # Inicializar Hardware
        self.init_hardware()
        
        self.cpu_history = [0] * 50
        self.gpu_history = [0] * 50

        self.setup_ui()
        self.update_stats()

    def init_hardware(self):
        print("Iniciando motores...")
        # GPU
        try:
            nvmlInit()
            self.has_gpu = True
        except:
            self.has_gpu = False

        # WMI (Apenas Windows)
        try:
            if IS_WINDOWS and wmi:
                self.w_obj = wmi.WMI(namespace="root\\wmi")
            else:
                self.w_obj = None
        except:
            self.w_obj = None

        # Network
        self.last_net_recv = psutil.net_io_counters().bytes_recv
        self.last_net_sent = psutil.net_io_counters().bytes_sent
        self.last_net_time = time.time()

        # CPU Name
        self.cpu_name = cpuinfo.get_cpu_info().get("brand_raw", "Processador")

    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color=CARD_BG, height=60, corner_radius=0)
        self.header.pack(fill="x", side="top", pady=(0, 20))
        
        self.logo_label = ctk.CTkLabel(self.header, text="🔥 HEATCORE SYSTEM MONITOR", font=("Orbitron", 18, "bold"), text_color=ACCENT_CYAN)
        self.logo_label.pack(side="left", padx=30)

        self.os_label = ctk.CTkLabel(self.header, text=f"{platform.system()} | {platform.release()}", font=("Rajdhani", 12), text_color="gray")
        self.os_label.pack(side="right", padx=30)

        # Container Principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=0)

        # Grid: 2 Colunas para Cards e 1 para Lateral
        self.main_container.grid_columnconfigure((0, 1), weight=2)
        self.main_container.grid_columnconfigure(2, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # --- COLUNA 1: CPU ---
        self.cpu_frame = self.create_card(self.main_container, 0, 0, "PROCESSADOR CENTRAL", ACCENT_CYAN)
        self.cpu_usage_val = ctk.CTkLabel(self.cpu_frame, text="0%", font=("Orbitron", 48, "bold"), text_color=ACCENT_CYAN)
        self.cpu_usage_val.pack(pady=(10, 0))
        
        self.cpu_subtext = ctk.CTkLabel(self.cpu_frame, text=self.cpu_name, font=("Rajdhani", 14), text_color="gray")
        self.cpu_subtext.pack()

        self.cpu_metrics = ctk.CTkLabel(self.cpu_frame, text="TEMP: -- | CLOCK: --", font=("Rajdhani", 13, "bold"))
        self.cpu_metrics.pack(pady=10)

        self.cpu_canvas = self.create_chart(self.cpu_frame, self.cpu_history, ACCENT_CYAN, "cpu")
        self.cpu_canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=10)

        # --- COLUNA 2: GPU ---
        self.gpu_frame = self.create_card(self.main_container, 0, 1, "PLACA DE VÍDEO (GPU)", ACCENT_MAGENTA)
        self.gpu_usage_val = ctk.CTkLabel(self.gpu_frame, text="0%", font=("Orbitron", 48, "bold"), text_color=ACCENT_MAGENTA)
        self.gpu_usage_val.pack(pady=(10, 0))

        self.gpu_subtext = ctk.CTkLabel(self.gpu_frame, text="GPU NVIDIA", font=("Rajdhani", 14), text_color="gray")
        self.gpu_subtext.pack()

        self.gpu_metrics = ctk.CTkLabel(self.gpu_frame, text="TEMP: -- | VRAM: --", font=("Rajdhani", 13, "bold"))
        self.gpu_metrics.pack(pady=10)

        self.gpu_canvas = self.create_chart(self.gpu_frame, self.gpu_history, ACCENT_MAGENTA, "gpu")
        self.gpu_canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=10)

        # --- COLUNA 3: LATERAL ---
        self.side_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.side_panel.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        # RAM Card
        self.ram_card = self.create_side_card(self.side_panel, "MEMÓRIA RAM", "💾")
        self.ram_usage_label = ctk.CTkLabel(self.ram_card, text="0%", font=("Orbitron", 22, "bold"))
        self.ram_usage_label.pack()
        self.ram_bar = ctk.CTkProgressBar(self.ram_card, progress_color=ACCENT_CYAN, height=10)
        self.ram_bar.set(0)
        self.ram_bar.pack(fill="x", padx=15, pady=10)
        self.ram_details = ctk.CTkLabel(self.ram_card, text="-- / -- GB", font=("Rajdhani", 12), text_color="gray")
        self.ram_details.pack()

        # Net Card
        self.net_card = self.create_side_card(self.side_panel, "REDE / WIFI", "📶")
        self.net_down = ctk.CTkLabel(self.net_card, text="⬇ 0.00 MB/s", font=("Rajdhani", 16, "bold"), text_color=ACCENT_CYAN)
        self.net_down.pack(pady=2)
        self.net_up = ctk.CTkLabel(self.net_card, text="⬆ 0.00 MB/s", font=("Rajdhani", 16, "bold"), text_color=ACCENT_MAGENTA)
        self.net_up.pack(pady=2)

        # Disk Card
        self.disk_card = self.create_side_card(self.side_panel, "DISCO / SSD", "📀")
        self.disk_usage = ctk.CTkLabel(self.disk_card, text="0%", font=("Orbitron", 18, "bold"))
        self.disk_usage.pack()
        self.disk_bar = ctk.CTkProgressBar(self.disk_card, progress_color=ACCENT_CYAN, height=8)
        self.disk_bar.set(0)
        self.disk_bar.pack(fill="x", padx=15, pady=8)

        # Footer Status
        self.footer = ctk.CTkLabel(self, text="● SISTEMA ATIVO | Intervalo: 1s", font=("Rajdhani", 11), text_color="#44dd88")
        self.footer.pack(side="bottom", pady=10)

    def create_card(self, parent, row, col, title, accent):
        frame = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=20, border_width=1, border_color=BORDER_COLOR)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        lbl = ctk.CTkLabel(frame, text=title, font=("Orbitron", 11, "bold"), text_color="gray")
        lbl.pack(anchor="nw", padx=20, pady=15)
        
        # Linha decorativa
        line = ctk.CTkFrame(frame, fg_color=accent, height=2, width=40)
        line.pack(anchor="nw", padx=20)
        
        return frame

    def create_side_card(self, parent, title, icon):
        frame = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        frame.pack(fill="x", pady=(0, 15))
        
        title_frame = ctk.CTkFrame(frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(title_frame, text=icon, font=("Rajdhani", 16)).pack(side="left")
        ctk.CTkLabel(title_frame, text=title, font=("Orbitron", 10, "bold"), text_color="gray").pack(side="left", padx=10)
        
        return frame

    def create_chart(self, parent, data, color, chart_type):
        fig, ax = plt.subplots(figsize=(5, 3), dpi=90)
        fig.patch.set_facecolor(CARD_BG)
        ax.set_facecolor(CARD_BG)
        
        line, = ax.plot(data, color=color, linewidth=2.5)
        fill = ax.fill_between(range(len(data)), data, color=color, alpha=0.15)
        
        ax.set_ylim(0, 105)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        
        if chart_type == "cpu":
            self.cpu_line = line
            self.cpu_fill = fill
            self.cpu_canvas = canvas
            self.cpu_ax = ax
        else:
            self.gpu_line = line
            self.gpu_fill = fill
            self.gpu_canvas = canvas
            self.gpu_ax = ax
            
        return canvas

    def get_cpu_temp(self):
        try:
            # 1. Psutil (Busca em todos os sensores disponíveis)
            t = psutil.sensors_temperatures()
            if t:
                for name, entries in t.items():
                    for entry in entries:
                        if entry.current and entry.current > 0:
                            return f"{entry.current:.0f}°C"
            
            # 2. Específico Windows (WMI/PowerShell)
            if IS_WINDOWS:
                if self.w_obj:
                    res = self.w_obj.MSAcpi_ThermalZoneTemperature()
                    if res: return f"{(res[0].CurrentTemperature - 2732) / 10:.0f}°C"
                
                import subprocess
                cmd = "Get-CimInstance -Namespace root/wmi -ClassName MsAcpi_ThermalZoneTemperature | Select-Object -ExpandProperty CurrentTemperature"
                
                # Só usar CREATE_NO_WINDOW no Windows
                kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if IS_WINDOWS else {}
                
                proc = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, **kwargs)
                out, _ = proc.communicate(timeout=0.5)
                if out.strip(): return f"{(int(out.strip()) - 2732) / 10:.0f}°C"

            # 3. Específico macOS (Requer osx-cpu-temp instalado via brew)
            elif platform.system() == "Darwin":
                import subprocess
                try:
                    out = subprocess.check_output(["osx-cpu-temp"], text=True)
                    if out: return out.strip()
                except: pass
        except:
            pass
        return "N/A"

    def update_stats(self):
        # --- CPU ---
        cpu_usage = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq()
        temp = self.get_cpu_temp()
        
        self.cpu_usage_val.configure(text=f"{cpu_usage}%")
        self.cpu_metrics.configure(text=f"TEMP: {temp} | CLOCK: {cpu_freq.current:.0f} MHz" if cpu_freq else f"TEMP: {temp}")
        
        self.cpu_history.append(cpu_usage)
        self.cpu_history.pop(0)
        self.cpu_line.set_ydata(self.cpu_history)
        self.cpu_canvas.draw_idle()

        # --- GPU ---
        if self.has_gpu:
            try:
                h = nvmlDeviceGetHandleByIndex(0)
                name = nvmlDeviceGetName(h)
                if isinstance(name, bytes): name = name.decode()
                util = nvmlDeviceGetUtilizationRates(h)
                mem = nvmlDeviceGetMemoryInfo(h)
                gtmp = nvmlDeviceGetTemperature(h, NVML_TEMPERATURE_GPU)
                
                self.gpu_usage_val.configure(text=f"{util.gpu}%")
                self.gpu_subtext.configure(text=name)
                self.gpu_metrics.configure(text=f"TEMP: {gtmp}°C | VRAM: {mem.used//1024**2}/{mem.total//1024**2} MB")
                self.gpu_history.append(util.gpu)
            except:
                self.gpu_history.append(0)
        else:
            self.gpu_history.append(0)

        self.gpu_history.pop(0)
        self.gpu_line.set_ydata(self.gpu_history)
        self.gpu_canvas.draw_idle()

        # --- RAM ---
        m = psutil.virtual_memory()
        self.ram_usage_label.configure(text=f"{m.percent}%")
        self.ram_bar.set(m.percent / 100)
        self.ram_details.configure(text=f"{m.used/1024**3:.1f} / {m.total/1024**3:.1f} GB")

        # --- DISK ---
        d = psutil.disk_usage("/")
        self.disk_usage.configure(text=f"{d.percent}%")
        self.disk_bar.set(d.percent / 100)

        # --- NET ---
        net_io = psutil.net_io_counters()
        now = time.time()
        dt = now - self.last_net_time
        down = (net_io.bytes_recv - self.last_net_recv) / (1024 * 1024 * dt)
        up = (net_io.bytes_sent - self.last_net_sent) / (1024 * 1024 * dt)
        
        self.net_down.configure(text=f"⬇ {down:.2f} MB/s")
        self.net_up.configure(text=f"⬆ {up:.2f} MB/s")
        
        self.last_net_recv, self.last_net_sent, self.last_net_time = net_io.bytes_recv, net_io.bytes_sent, now

        # Loop
        self.after(1000, self.update_stats)

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()