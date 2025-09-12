# DialogueFlow Project

This repository contains a suite of Python tools and APIs for dialogue follow-up processing using large language models (LLMs), FastAPI, and LangGraph. The project enables matching user answers to predefined options for both single and multiple-choice questions, supporting both local and external API workflows.

## Project Structure

- **main.py**: FastAPI service for dialogue follow-up. Exposes endpoints for health checks and dialogue processing, leveraging an external LLM API to match user answers to options. Handles both single and multiple-choice questions.
- **main.md**: Documentation for `main.py`, including API design, endpoints, and usage instructions.
- **Dialogue_Followup_APIClient.py**: Standalone client for sending dialogue questions and user answers to an external LLM API. Demonstrates prompt formatting, API calls, and result parsing.
- **Dialogue_Followup_APIClient.md**: Documentation for the API client, with code explanations and usage notes.
- **Dialogue_Followup_FastAPI_Test.py**: Local client and interactive test harness for the FastAPI service. Allows users to test API endpoints by sending questions, options, and answers, and viewing results.
- **Dialogue_Followup_FastAPI_Test.md**: Documentation for the FastAPI test client, including step-by-step code explanations.
- **Dialogue_Followup_Langgraph.py**: Implements a dialogue workflow using the LangGraph library. Structures the process of presenting questions, collecting input, processing answers with an external AI API, and displaying results.
- **Dialogue_Followup_Langgraph.md**: Documentation for the LangGraph workflow implementation.
- **Dialogue_Followup_Langgraph_FastAPI.py**: Combines LangGraph workflow with FastAPI for orchestrated dialogue processing, supporting multi-step user interaction and AI matching.
- **Dialogue_Followup_Langgraph_FastAPI.md**: Documentation for the LangGraph FastAPI workflow.
- **0.2.27**: Requirements or dependency notes for the project (see file for details).
- **Program Results.pdf**: Example output or results from running the dialogue processing tools.
- **.vscode/**: VS Code workspace settings.
- **NewVitual.venv/**: Python virtual environment for dependencies.
- **__pycache__/**: Python bytecode cache (auto-generated).

## Key Features

- **Dialogue Matching**: Match user answers to predefined options using LLMs.
- **API & CLI Tools**: FastAPI service, standalone clients, and workflow orchestrations.
- **LangGraph Integration**: Modular workflow for dialogue processing.
- **Extensive Documentation**: Each major script is paired with a Markdown file explaining its logic and usage.

## Getting Started

1. **Set up the virtual environment**:
   ```sh
   # On Windows (PowerShell)
   .\NewVitual.venv\Scripts\Activate.ps1
   ```
2. **Install dependencies** (if not already installed):
   ```sh
   pip install -r 0.2.27
   ```
3. **Run the FastAPI server**:
   ```sh
   python main.py
   ```
4. **Test the API**:
   - Use `Dialogue_Followup_FastAPI_Test.py` for interactive CLI testing.
   - Use `Dialogue_Followup_APIClient.py` for direct API calls.
   - Use LangGraph scripts for workflow-based dialogue processing.

## License

This project is for research and educational purposes. See individual files for more details.
