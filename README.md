# RanjithGPT | Private Edge-AI Chat Dashboard

RanjithGPT is a privacy-first, full-stack local AI chat application designed to mimic the premium user experience of ChatGPT and Gemini. Unlike cloud-based alternatives, ranjithgpt runs entirely on local hardware, ensuring that no user data or conversation history ever leaves the host machine.

---

## 🚀 Key Features

* **Local Inference:** Powered by Ollama and Llama 3 to process prompts 100% offline.
* **Real-Time Token Streaming:** Implements a streaming API architecture to reduce Time-To-First-Token (TTFT) and provide a snappy UI experience.
* **Multi-Session History:** A persistent sidebar that saves, loads, and manages multiple unique conversation threads.
* **Auto-Titling:** Automatically summarizes the first user message into a clean chat title for the history sidebar.
* **Dynamic Markdown Rendering:** Full support for rendering mathematical notations, bold prose, and code blocks using `Marked.js`.
* **Session Deletion:** A modern hover-and-delete functionality to cleanly purge chat records from local storage.

---

## 🛠️ The Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3 (Flexbox), Vanilla JS (ES6+) | Fully responsive user interface and async streaming handler. |
| **Markdown** | Marked.js | Parses structured LLM output (code blocks, lists) on the fly. |
| **Backend** | Python / Flask | Web server routing, stream generation, and API orchestration. |
| **AI Engine** | Ollama | Local model manager acting as the host infrastructure. |
| **LLM** | Llama 3 (Meta) | The core intelligence brain for natural language understanding. |
| **Database** | JSON File System (`Flat-file`) | Lightweight, zero-config local storage for message persistence. |

---

## 🏗️ Architecture Workflow

1. **Client (JS):** Captures user message, pushes it to the UI instantly, and triggers an asynchronous `POST` fetch request.
2. **Server (Flask):** Intercepts the request, fetches existing conversation history from the JSON file based on the `session_id`, and passes it to the AI controller.
3. **Engine (Ollama):** Fires up the local **Llama 3** weights to process the history + new prompt, streaming chunks of text back to Flask.
4. **Streaming Delivery:** Flask yields these text chunks sequentially to the browser via a readable stream, which updates the UI word-by-word.
5. **Persistence:** Once the response completes, the updated chat array is serialized back into the local JSON database.

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.8 or higher installed.
* [Ollama](https://ollama.com/) installed and running in the background.

### Step 1: Pull the Model
Open your terminal and ensure Llama 3 is downloaded locally:

    ollama run llama3

### Step 2: Clone & Install Dependencies
Navigate to the project root directory and install Flask and Ollama's Python library:

    Bash
    pip install flask ollama

### Step 3: Run the Application
Start your local Flask development server:

    Bash
    python app.py

### Open your browser and navigate to http://127.0.0.1:5000 to start chatting!
