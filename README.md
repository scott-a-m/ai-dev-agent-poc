# 🧠 AI Dev Agent (POC)

A lightweight, AI dev agent for reviewing and refactoring source code using local LLMs via [Ollama](https://ollama.com). This CLI-based assistant reads your code, detects bugs and performance issues, proposes fixes, and optionally overwrites the original file. It offers user-driven refinement and multiturn logic until the code meets your requirements.

**⚠️ Please note that this is a proof of concept and is not production ready.**

---

## 🚀 Features

- Multi-language support (Python, JavaScript, C++, Java, etc.)
- Streaming LLM responses for real-time feedback
- File backup and overwrite with user confirmation
- Multiturn conversation loop for iterative refinement
- Environment interaction: reads, edits, and backs up files
- Model-agnostic architecture (supports Mistral, Deepseek, etc.)
- Verbose mode for HTTP diagnostics and payload inspection

---

## 🧩 How It Works

1. Prompts the user for a file path  
2. Detects the language based on file extension  
3. Sends a structured prompt to a local LLM via Ollama  
4. Streams the model's response token-by-token  
5. Extracts proposed code changes and asks for confirmation  
6. Backs up and overwrites the file if approved  
7. Supports follow-up questions and iterative refinement  

---

## 🛠️ Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running locally
- A supported model pulled via Ollama (e.g. `ollama pull mistral`)

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/codechecker-agent.git
cd dev-ai-agent
```

## 🛠️ Local Development
Set up a Python virtual environment and install dependencies:

```python
#Create and activate virtual environment
py -m venv .venv
venv\Scripts\activate
pip install requests

## Run agent
python main.py

# optional flags to run http diagnostics: 
python main.py --verbose
```

## 🧠 Supported Models
This agent is model-agnostic. It works with any Ollama-compatible chat model.

## 📂 File Structure

ai-dev-agent/
├── main.py
├── ai_dev_agent_helpers.py
└── README.md     

## Agentic Architecture

This project is a proof-of-concept AI agent, it demonstrates:

- Goal-oriented behavior (code review and improvement)
- Environment interaction (file I/O and backup)
- Context tracking (message history and follow-ups)
- Adaptive flow (user-driven refinement and multiturn logic)