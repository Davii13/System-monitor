# ⚡ HEATCORE TELEMETRY PRO

O **Heatcore Telemetry Pro** é um dashboard de monitoramento de sistema de alta performance, desenvolvido em Python. Ele oferece uma interface moderna e futurista, inspirada em painéis de telemetria profissional, permitindo acompanhar em tempo real o estado do seu hardware.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

## 📸 Demonstração

| Dashboard Principal | Modo Widget | Conectividade |
| :---: | :---: | :---: |
| <img src="https://github.com/user-attachments/assets/3c0145eb-f783-473e-aa71-b66ab6f51db6" width="400" /> | <img src="https://github.com/user-attachments/assets/2c5f4bf7-64af-4390-8144-b7dcdbba229c" width="400" /> | <img src="https://github.com/user-attachments/assets/7610d906-87ad-47d2-a3e5-328e2adc014f" width="400" /> |

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
-   **Pythonnet (clr)**: Biblioteca de ponte para carregar código .NET/C# no Python.

---

## 🌡️ Monitoramento de Temperatura & DLLs

Para extrair com precisão a temperatura do processador (CPU) no Windows, este projeto utiliza a biblioteca oficial do **[LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor)**. Como o Python não possui acesso nativo de baixo nível a esses sensores diretamente no Windows, a integração é feita através de DLLs compiladas em C# (.NET) importadas dinamicamente.

### 📁 Estrutura da pasta `dll/`

No diretório `dll/` do projeto, você encontrará os seguintes arquivos:

1. **`LibreHardwareMonitorLib.dll`**: É a biblioteca principal do LibreHardwareMonitor. Ela contém toda a lógica de detecção de hardware, controle de drivers em nível de kernel (Ring 0) e leitura de sensores de temperatura, carga e clock.
2. **`System.Memory.dll`**: Uma dependência do .NET necessária para manipulação eficiente de buffers e memória pelo LibreHardwareMonitor.
3. **`System.Runtime.CompilerServices.Unsafe.dll`**: Uma biblioteca de suporte necessária para operações de ponteiro e código "unsafe" (não seguro) usadas nas chamadas de baixo nível dos drivers.

### 📥 Download e Atualização das DLLs

As DLLs utilizadas neste projeto foram extraídas da versão oficial do LibreHardwareMonitor. Se você deseja atualizá-las ou baixá-las manualmente, siga os passos abaixo:

1. Acesse a página oficial de lançamentos: **[LibreHardwareMonitor Releases](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases)**.
2. Baixe o arquivo `.zip` da versão estável mais recente (ex: `LibreHardwareMonitor.zip`).
3. Extraia o conteúdo e copie os arquivos `LibreHardwareMonitorLib.dll`, `System.Memory.dll` e `System.Runtime.CompilerServices.Unsafe.dll` para a pasta `dll/` do projeto.

### ⚠️ Importante: Permissões de Administrador

Para que o LibreHardwareMonitor consiga inicializar o driver de kernel necessário para ler os sensores de temperatura da CPU, **o script Python deve ser executado com privilégios de Administrador**. 

* Se você executar como usuário comum, a temperatura da CPU será exibida como **N/A** (Não Disponível).
* **Como rodar como Administrador:** Abra o Prompt de Comando (cmd) ou PowerShell como Administrador e execute:
  ```bash
  python monitor.py
  ```

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
