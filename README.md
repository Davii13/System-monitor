# ⚡ HEATCORE TELEMETRY PRO

O **Heatcore Telemetry Pro** é um dashboard de monitoramento de sistema de alta performance, desenvolvido em Python. Ele oferece uma interface moderna e futurista, inspirada em painéis de telemetria profissional, permitindo acompanhar em tempo real o estado do seu hardware.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

## 📸 Demonstração

| Dashboard Principal | Modo Widget | Conectividade |
| :---: | :---: | :---: |
| ![Dashboard](<img width="1919" height="1013" alt="image" src="https://github.com/user-attachments/assets/3c0145eb-f783-473e-aa71-b66ab6f51db6" />
) | ![Widget](<img width="857" height="434" alt="image" src="https://github.com/user-attachments/assets/2c5f4bf7-64af-4390-8144-b7dcdbba229c" />
) | ![Network](<img width="1915" height="1018" alt="image" src="https://github.com/user-attachments/assets/7610d906-87ad-47d2-a3e5-328e2adc014f" />) |

---

## ✨ Funcionalidades

-   📊 **Dashboard em Tempo Real**: Monitoramento de carga e performance.
-   🔥 **CPU Core**: Frequência, carga e temperatura (quando disponível).
-   🎮 **GPU Engine**: Uso de GPU, VRAM e temperatura (suporte para NVIDIA via NVML).
-   🧠 **System Memory**: Uso detalhado da memória RAM.
-   📀 **Armazenamento**: Monitoramento de espaço em disco em tempo real.
-   📶 **Conectividade**: Monitor de tráfego de rede (Download/Upload) ao vivo.
-   🚀 **Speedtest Integrado**: Teste de velocidade de internet oficial direto no app.
-   📌 **Modo Widget**: Janela flutuante minimalista para manter o monitoramento sobre outras janelas.
-   🎨 **Interface Premium**: Design dark-mode com animações e gauges customizados.

---

## 🛠️ Tecnologias Utilizadas

-   **Python**: Linguagem base.
-   **CustomTkinter**: Interface moderna e responsiva.
-   **Psutil**: Coleta de dados do sistema e processos.
-   **Py-cpuinfo**: Detecção detalhada do processador.
-   **Speedtest-cli**: Integração de testes de velocidade.
-   **Py3nvml**: Monitoramento de GPUs NVIDIA.
-   **WMI**: Integração avançada com sensores Windows.

---

## 🚀 Como Instalar

### Pré-requisitos
Certifique-se de ter o **Python 3.10 ou superior** instalado em sua máquina.

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/Davii13/System-monitor.git
cd System-monitor
```

### Passo 2: Instalar as dependências
Recomendamos o uso de um ambiente virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Instalar pacotes
pip install -r requirements.txt
```

---

## 💻 Como Usar

Para iniciar o monitoramento, basta executar o arquivo principal:

```bash
python monitor.py
```

-   Use a **Sidebar** para navegar entre o Dashboard e as métricas de Conectividade.
-   Clique em **MODO WIDGET** para alternar para a janela compacta e flutuante.
-   No Modo Widget, você pode arrastar a janela clicando na barra superior.

---

## 👥 Autores

Desenvolvido por:
-   **Davi Nunes Carvalho** ([Davii13](https://github.com/Davii13))
-   **João Paulo Aramuni**  ([joaopauloaramuni](https://github.com/joaopauloaramuni))

---

## 🤝 Contribuição

Este projeto está aberto para contribuições! Se você tem ideias para novos widgets, melhorias na performance ou correções de bugs:

1. Faça um **Fork** do projeto.
2. Crie uma **Branch** para sua feature (`git checkout -b feature/nova-feature`).
3. Dê um **Commit** nas suas alterações (`git commit -m 'Adicionando nova funcionalidade'`).
4. Faça um **Push** para a Branch (`git push origin feature/nova-feature`).
5. Abra um **Pull Request**.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
*Developed for hardware enthusiasts.*
