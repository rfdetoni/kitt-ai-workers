# Manual do K.I.T.T. AI Workers (`kitt-ai-workers`)

> Serviços locais de IA do K.I.T.T.: STT com Whisper, worker NDJSON leve e workloads isolados de avaliação/evolução.

---

## 1. Visão Geral e Arquitetura

O **`kitt-ai-workers`** encapsula serviços pesados de Machine Learning que executam diretamente na máquina local ou em nós servidores dedicados da rede local.

### Principais Recursos:
- **`stt_server`**: Servidor HTTP local compatível com a API `/v1/audio/transcriptions` (utilizando OpenAI Whisper / Faster-Whisper localmente).
- **Proteção Anti-CSRF (R5)**: Bloqueio estrito de requisições disparadas por navegadores (`Origin` header presente retorna `403 Forbidden`) para evitar exploração de endpoints locais de processamento pesado.
- **Workers NDJSON**: runner leve sob demanda via `stdin`/`stdout`, atualmente com capabilities `health` e `echo`.

---

## 2. Requisitos de Sistema

- **Python**: 3.14+
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
pip install -e ".[stt]"

# O extra `stt` instala faster-whisper. O backend openai-whisper continua
# suportado como alternativa quando instalado manualmente.
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

## 0.1.42: privacidade e estabilidade

Evolution compartilha a classificação de processamento local do Agent CLI 0.83: um reverse proxy em loopback continua sendo processamento remoto. Erros na criação ou escrita do arquivo temporário do STT liberam o lock da transcrição e permitem novas requisições. Os pacotes seguem main; nenhum modelo Whisper foi baixado para validar estas fronteiras.
