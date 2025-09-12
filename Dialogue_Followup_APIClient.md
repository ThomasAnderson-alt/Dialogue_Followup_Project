# Dialogue_Followup_APIClient.md

## Overview

This file documents the code in `Dialogue_Followup_APIClient.py`, which provides a class for interacting with the external AI API for dialogue follow-up tasks. It demonstrates how to build requests, send user answers, and process the AI's response.

## Step-by-Step Code Explanation

### 1. Imports and Configuration

- Imports standard libraries (`json`, `time`, etc.), `requests` for HTTP calls.
- Sets constants for API timeout, model name, and the external API endpoint.

### 2. API Client Class

- `VoiceFollowUpAPI`:
  - **Initialization**: Stores API credentials and endpoint.
  - **call_api**: Builds the request payload, sends it to the external AI API, and parses the response. Handles errors and connection issues.
  - **\_build_payload**: Formats the prompt and options for the AI API.
  - **\_parse_silicon_flow_response**: Parses the AI's JSON response and attaches it to the result.

### 3. Question Processing Function

- `process_question`: Presents a question and options, collects user input, calls the API, and displays the result.

### 4. Result Display Function

- `_display_result`: Prints the matched option and reasoning from the AI's response.

### 5. Main Demo Function

- `main`: Demonstrates the API client with example single-choice and multiple-choice questions, including a pause between examples.

### 6. Application Entry Point

- If run as a script, executes the main function.

## How the Program Achieves Its Goal

- The program provides a reusable class for sending dialogue questions and user answers to an external LLM API.
- It demonstrates how to format prompts, handle responses, and display results, making it easy to integrate AI-powered matching into other applications.

## Usage

- Run the script: `python Dialogue_Followup_APIClient.py`
- The program will prompt you with example questions and process your answers using the external AI API.
