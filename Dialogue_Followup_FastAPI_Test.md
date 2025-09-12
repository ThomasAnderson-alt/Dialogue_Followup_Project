# Dialogue_Followup_FastAPI_Test.md

## Overview

This file documents the code in `Dialogue_Followup_FastAPI_Test.py`, which provides a local client and interactive test harness for the FastAPI dialogue processing service. It allows users to test the API endpoints by sending questions, options, and answers, and viewing the results.

## Step-by-Step Code Explanation

### 1. Imports and Client Class

- Imports `requests` for HTTP calls and typing utilities.
- Defines `LocalDialogueClient`, an HTTP client for interacting with the FastAPI service:
  - `__init__`: Sets the base URL and timeout.
  - `check_health`: Checks if the API server is running.
  - `process_dialogue`: Sends a question, options, and user answer to the API and returns the result.

### 2. Result Display Function

- `display_result`: Nicely formats and prints the API response, including matched options and reasoning.

### 3. Main Interactive Test Function

- `main`: Provides an interactive CLI for testing the API:
  - Checks server health.
  - Presents two example questions (single and multiple choice).
  - Prompts the user to select a question and enter a natural language answer.
  - Sends the data to the API and displays the result.

### 4. Application Entry Point

- If run as a script, executes the main function.

## How the Program Achieves Its Goal

- The program allows users to interactively test the FastAPI dialogue service.
- It sends user input to the API and displays the AI's matching results, making it easy to verify and debug the backend service.

## Usage

- Start the FastAPI server (`python main.py`).
- Run this script: `python Dialogue_Followup_FastAPI_Test.py`
- Follow the prompts to test single and multiple-choice questions.
