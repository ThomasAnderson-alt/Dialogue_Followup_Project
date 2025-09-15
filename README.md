# 🗣️ DialogueFlow Project

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/Framework-FastAPI-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A comprehensive suite of Python tools for advanced dialogue follow-up processing. This project leverages Large Language Models (LLMs) through FastAPI and LangGraph to intelligently match user responses to predefined options for both single and multiple-choice questions.

## ✨ Features

- **🧠 Intelligent Dialogue Matching**: Utilizes LLMs to accurately map natural language user answers to structured options.
- **🚀 Robust API & CLI Tools**: Includes a FastAPI service for web-based interaction, standalone clients for direct API calls, and LangGraph-powered workflow orchestrations.
- **🧩 Modular & Extensible**: Built with a clear separation of concerns, allowing for easy extension and integration.
- **🔄 Single & Multiple-Choice Support**: Flexibly handles both single-answer and multiple-answer question formats.
- **📚 Extensive Documentation**: Each major script is paired with a detailed Markdown file explaining its purpose, logic, and usage.

## ⚙️ System Architecture

This project is composed of several key components that can be used independently or together:

- **`main.py`**: 🌐 A FastAPI service that exposes endpoints for dialogue processing. It takes a question, options, and a user's answer, then uses an external LLM API to find the best match.
- **`Dialogue_Followup_APIClient.py`**: 💻 A standalone command-line client for interacting directly with the LLM API, demonstrating the core prompt engineering and API communication.
- **`Dialogue_Followup_FastAPI_Test.py`**: 🧪 An interactive local client used to test the `main.py` FastAPI service. It provides a simple interface to send requests and view formatted responses.
- **`Dialogue_Followup_Langgraph.py`**: 🔗 A script that implements a dialogue workflow using the `LangGraph` library. It orchestrates the steps of a conversation from asking a question to processing the answer.
- **`Dialogue_Followup_Langgraph_FastAPI.py`**: ⚡ Combines the power of `LangGraph` workflows with a FastAPI server, creating a more stateful and orchestrated dialogue processing service.

## 🚀 Getting Started

Follow these steps to set up and run the project.

### 1. Prerequisites

- Python 3.9+
- A virtual environment tool (like `venv`)

### 2. Setup & Installation

First, clone the repository to your local machine.

1. **Create and activate the virtual environment**:

   ```sh
   # Create the virtual environment
   python -m venv NewVitual.venv

   # On Windows (PowerShell)
   .\NewVitual.venv\Scripts\Activate.ps1

   # On macOS/Linux
   source NewVitual.venv/bin/activate
   ```

2. **Install dependencies**:

   The required packages are listed in `requirements.txt`.

   ```sh
   pip install -r requirements.txt
   ```

## 🏃‍♀️ Running the Applications

You can run different components of the project depending on your needs.

### Running the FastAPI Server

To start the main API service:

```sh
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`. You can view the interactive API documentation at `http://localhost:8000/docs`.

### Testing the FastAPI Server

Once the FastAPI server is running, you can use the local test client:

```sh
python Dialogue_Followup_FastAPI_Test.py
```

This script will guide you through testing the API with predefined questions.

### Running the Standalone Clients

- **Direct API Client**: To test the direct communication with the LLM API:

  ```sh
  python Dialogue_Followup_APIClient.py
  ```

- **LangGraph Workflow**: To run the dialogue workflow orchestrated by LangGraph:

  ```sh
  python Dialogue_Followup_Langgraph.py
  ```

- **LangGraph with FastAPI**: To run the combined LangGraph and FastAPI server:

  ```sh
  uvicorn Dialogue_Followup_Langgraph_FastAPI:app --reload
  ```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
