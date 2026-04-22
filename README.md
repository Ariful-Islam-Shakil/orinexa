# Orinexa 🤖

Orinexa is a sophisticated AI assistant built with Google's Gemini models. It leverages a modular tool system and a dual-memory architecture (short-term and long-term) to provide accurate, context-aware, and automated solutions.

---

## 🌟 Features

### 🛠️ Advanced Toolset
Orinexa can perform a wide range of tasks by autonomously calling integrated tools:
- **Computational Tools**: Perform arithmetic operations (sum, subtract, multiply, divide, percentage).
- **Automation**: Execute Python scripts locally and compile LaTeX code into PDF documents.
- **Information Retrieval**:
  - **Web Search**: Live search via DuckDuckGo.
  - **ArXiv Search**: Find research papers and summaries.
  - **YouTube Transcripts**: Extract text scripts from YouTube videos.
  - **Weather & Time**: Get real-time weather updates and current time across different timezones.
- **Communication**: Send emails with attachments via SMTP.
- **Visuals**: Display local images in a grid format using Matplotlib.

### 🧠 Dual Memory System
- **Short-Term Memory**: Maintains context of the current conversation session.
- **Long-Term Memory**: Uses **FAISS (Facebook AI Similarity Search)** and **Sentence Transformers** to store and retrieve past interactions and tool outputs, allowing the agent to "remember" previous tasks.

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher
- A Google Gemini API Key

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/Ariful-Islam-Shakil/orinexa.git
cd orinexa
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key
WEATHER_API=your_weather_api_key

# Email Settings (for send_email tool)
EMAIL=your_email@gmail.com
EMAIL_PASS=your_app_specific_password
```

---

## 📖 User Guide

### Running the Assistant
Start the interactive session by running:
```bash
python main.py
```

### Interaction Examples
Once the assistant is running, you can ask questions like:
- **General Inquiry**: "What is the weather in London right now?"
- **Research**: "Find 3 papers on 'Quantum Computing' from Arxiv."
- **Computation**: "Calculate the percentage of 500 from 1500."
- **Automation**: "Write a Python script to find the first 10 prime numbers and run it."
- **Memory**: "Do you remember what we discussed about AI earlier?"

### Commands
- Type `exit`, `quit`, or `bye` to end the conversation.

---

## 📂 Project Structure
- `main.py`: The entry point for the assistant.
- `components/`:
  - `agents.py`: Core logic for the Gemini-powered agent.
  - `tools.py`: Implementation of all external tools.
  - `vector_db.py`: Long-term memory management using FAISS.
  - `schema.py`: Data models for structured tool outputs.
- `output_dir/`: Default directory for generated outputs (like LaTeX PDFs).

---

