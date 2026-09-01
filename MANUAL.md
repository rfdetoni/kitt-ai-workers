# Manual do K.I.T.T. AI Workers (`kitt-ai-workers`)

> Serviços de Inteligência Artificial locais: Servidor STT (Speech-to-Text) com Whisper, processamento de áudio, visão e workers de execução em lote.

---

## 1. Visão Geral e Arquitetura

O **`kitt-ai-workers`** encapsula serviços pesados de Machine Learning que executam diretamente na máquina local ou em nós servidores dedicados da rede local.

### Principais Recursos:
- **`stt_server`**: Servidor HTTP local compatível com a API `/v1/audio/transcriptions` (utilizando OpenAI Whisper / Faster-Whisper localmente).
- **Proteção Anti-CSRF (R5)**: Bloqueio estrito de requisições disparadas por navegadores (`Origin` header presente retorna `403 Forbidden`) para evitar exploração de endpoints locais de processamento pesado.
- **Workers NDJSON**: Executores de visão computacional e OCR sob demanda através de pipes padrão `stdin`/`stdout`.

---

## 2. Requisitos de Sistema

- **Python**: 3.12, 3.13 ou 3.14
- **FFmpeg**: Necessário para decodificação e processamento de formatos de áudio (MP3, WAV, OGG, FLAC, M4A).
- **Dispositivo**: CPU x86_64/ARM64 ou GPU com aceleração CUDA/MPS.

---

## 3. Instalação Passo a Passo por Sistema Operacional

### 🐧 A. LINUX (Ubuntu/Debian)

```bash
# 1. Instalar FFmpeg
sudo apt-get update && sudo apt-get install -y ffmpeg

# 2. Criar ambiente virtual Python e instalar
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# 3. (Opcional) Instalar suporte completo ao modelo Whisper
pip install openai-whisper soundfile
```

### 🍏 B. macOS

```bash
# 1. Instalar FFmpeg via Homebrew
brew install ffmpeg

# 2. Criar ambiente virtual e instalar
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# 3. (Opcional) Suporte ao Whisper com aceleração Apple Silicon Metal (MPS)
pip install openai-whisper soundfile
```

### 🪟 C. WINDOWS (PowerShell)

```powershell
# 1. Instalar FFmpeg via winget (ou Chocolatey)
winget install Gyan.FFmpeg

# 2. Criar ambiente virtual e instalar
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .

# 3. (Opcional) Instalar Whisper
pip install openai-whisper soundfile
```

---

## 4. Configuração e Inicialização do Servidor STT

### Variáveis de Ambiente Suportadas:
```bash
# Porta do servidor (Padrão: 8000)
export KITT_STT_PORT=8000

# Host do servidor (Padrão: 127.0.0.1)
export KITT_STT_HOST=127.0.0.1

# Modelo Whisper (tiny, base, small, medium, large-v3)
export KITT_WHISPER_MODEL="base"
```

### Inicializando o Servidor STT:
```bash
python3 -m kitt_workers.stt_server
```
*O servidor estará ouvindo em: `http://127.0.0.1:8000`.*

---

## 5. Guia de Uso da API de Transcrição

### Exemplo de Transcrição via `curl` (Linha de Comando):
```bash
curl -X POST http://127.0.0.1:8000/v1/audio/transcriptions \
  -F "file=@/caminho/do/audio.wav" \
  -F "model=whisper-1" \
  -F "language=pt"
```

*Resposta JSON:*
```json
{
  "text": "Olá, KITT. Qual é o status do sistema?"
}
```

### Exemplo de Integração em Python:
```python
import urllib.request
import json

# Enviar requisição para o servidor local
# (Nota: Comunicações entre processos CLI/Daemon não enviam header Origin)
```

---

## 6. Validação e Testes
```bash
python3 -m unittest discover tests -v
```
