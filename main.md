# main.md

## Overview

This file documents the code in `main.py`, which implements a FastAPI-based service for processing dialogue follow-up questions using an external AI model. The API receives a question, options, and a user's answer, and returns the best-matching option(s) with reasoning, leveraging a large language model via HTTP API.

## Step-by-Step Code Explanation

### 1. Imports and Configuration

- Imports standard libraries (`json`, `datetime`, etc.), FastAPI, Pydantic, and `requests` for HTTP calls.
- Sets constants for API timeout, model name, and the external API endpoint.

### 2. FastAPI Setup

- Initializes a FastAPI app and configures CORS to allow all origins.

### 3. Data Models

- Defines Pydantic models for request and response validation:
  - `Option`: Represents an answer option.
  - `DialogueRequest`: The request body, including question, options, user answer, etc.
  - `MatchResult`, `DialogueResponse`, `HealthResponse`: For structured API responses.

### 4. AI Processing Function

- `process_ai_request`:
  - Formats the options and constructs a prompt for the AI model.
  - Sends a POST request to the external AI API with the prompt and user data.
  - Parses and returns the AI's JSON response.

### 5. API Endpoints

- `/health`: Returns a health check response.
- `/process-dialogue`: Main endpoint. Validates input, calls the AI processing function, and returns the result in a structured format. Handles both single and multiple-choice questions.

### 6. Running the Server

- If run as a script, starts the FastAPI server using Uvicorn.

## How the Program Achieves Its Goal

- The program exposes an HTTP API for dialogue follow-up tasks.
- It validates and structures user input, then crafts a prompt for an external LLM.
- The LLM matches the user's answer to the best option(s) and provides reasoning.
- The API returns this result in a clear, structured format for downstream use.

## Usage

- Start the server: `python main.py`
- Send POST requests to `/process-dialogue` with the required fields.
- The API responds with the best-matching option(s) and reasoning, powered by the external AI model.
