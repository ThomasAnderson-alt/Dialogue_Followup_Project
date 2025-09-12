# Dialogue_Followup_Langgraph.md

## Overview

This file documents the code in `Dialogue_Followup_Langgraph.py`, which implements a dialogue workflow using the LangGraph library. The code structures the process of presenting questions, collecting user input, processing answers with an external AI API, and displaying results.

## Step-by-Step Code Explanation

### 1. Imports and Configuration

- Imports standard libraries (`json`, `time`, etc.), `requests` for HTTP calls, and LangGraph for workflow management.
- Sets constants for API timeout, model name, and the external API endpoint.

### 2. State Management

- Defines a `DialogueState` TypedDict to structure the data passed between workflow nodes, including question, options, user answer, API responses, and error messages.

### 3. Main Dialogue Processing Class

- `LanggraphVoiceFollowUp` manages the dialogue workflow:
  - **Initialization**: Stores API credentials and builds the workflow.
  - **Workflow Construction**: Uses LangGraph to define nodes for displaying the question, collecting input, processing the API call, and displaying results. Nodes are connected in sequence.
  - **Node Functions**:
    - `_display_question_node`: Prints the question and options.
    - `_collect_input_node`: Prompts the user for an answer.
    - `_process_api_node`: Sends the user's answer to the external AI API and parses the response.
    - `_display_result_node`: Prints the matched option and reasoning.
  - **API Payload Construction**: Formats the prompt and options for the AI API.
  - **Public Interface**: `process_question` runs the workflow for a given question and options.

### 4. Demo Function

- `run_demo` demonstrates the workflow with example single-choice and multiple-choice questions, including a pause between examples.

### 5. Application Entry Point

- If run as a script, executes the demo function.

## How the Program Achieves Its Goal

- The program uses LangGraph to structure a dialogue workflow as a series of steps (nodes).
- It collects user input, sends it to an external LLM for matching, and displays the result.
- The workflow is modular, making it easy to extend or modify steps.

## Usage

- Run the script: `python Dialogue_Followup_Langgraph.py`
- The program will prompt you with example questions and process your answers using the external AI API.
