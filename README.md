# 🗣️ DialogueFlow Project

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?style=for-the-badge&logo=fastapi)
![Langchain](https://img.shields.io/badge/Langchain-0.2+-orange?style=for-the-badge&logo=langchain)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.69-blueviolet?style=for-the-badge&logo=langgraph)

## 📖 About The Project

The **DialogueFlow Project** is a comprehensive suite of Python tools for advanced dialogue follow-up processing. It leverages Large Language Models (LLMs) through FastAPI and LangGraph to intelligently match user responses to predefined options for both single and multiple-choice questions.

## 🚀 Getting Started

Follow these steps to set up and run the project.

### Prerequisites

- Python 3.9+

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/ThomasAnderson-alt/DialogueFlow_Project.git
   ```

2. **Navigate to the project directory**

   ```sh
   cd DialogueFlow_Project
   ```

3. **Create and activate a virtual environment**

   ```sh
   python -m venv NewVitual.venv
   .\NewVitual.venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

## ⚙️ Usage

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

## 📂 Project Structure

```plaintext
DialogueFlow_Project/
├── Dialogue_Followup_APIClient.py          # Command-line client for LLM API
├── Dialogue_Followup_FastAPI_Test.py       # Local test client for FastAPI service
├── Dialogue_Followup_Langgraph.py          # LangGraph workflow for dialogue
├── Dialogue_Followup_Langgraph_FastAPI.py  # Combined LangGraph and FastAPI server
├── main.py                                 # FastAPI service entry point
├── requirements.txt                        # Project dependencies
├── README.md                               # Project documentation
```

## 🏗️ System Structure

The **DialogueFlow Project** is designed with a clear and modular architecture to facilitate extensibility and maintainability. Below is an overview of the system structure:

1. **API Module**: Implements the FastAPI service (`main.py`) to expose endpoints for dialogue processing.
2. **Client Module**: Provides standalone clients (`Dialogue_Followup_APIClient.py`, `Dialogue_Followup_FastAPI_Test.py`) for interacting with the API and testing.
3. **Workflow Module**: Contains LangGraph-powered workflows (`Dialogue_Followup_Langgraph.py`, `Dialogue_Followup_Langgraph_FastAPI.py`) for orchestrating dialogue processes.

This modular design ensures that each component can be developed, tested, and deployed independently.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

Project Link: [https://github.com/ThomasAnderson-alt/DialogueFlow_Project](https://github.com/ThomasAnderson-alt/DialogueFlow_Project)
