# Import necessary modules for the application
import json  # For parsing and creating JSON data structures
import time  # For time-related operations like sleep delays
from typing import Any, Dict, List  # Type hints for better code documentation
import requests  # For making HTTP API requests

# Configuration constants
API_TIMEOUT = 30  # Timeout value in seconds for API requests
SILICON_FLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"  # Base URL for the Silicon Flow API
MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct"  # Default AI model name to use

class VoiceFollowUpAPI:  # Main class for handling voice follow-up API interactions
    def __init__(self, api_key: str, model: str = MODEL_NAME):  # Constructor to initialize the API client
        self.api_key = api_key  # Store the API key for authentication
        self.model = model  # Store the AI model name to use
        self.api_endpoint = SILICON_FLOW_BASE_URL  # Store the API endpoint URL
        
    def call_api(self, question: str, options: List[Dict[str, str]],  # Method to make API calls
                 answer: str, question_type: str) -> Dict[str, Any]:  # Parameters and return type
        payload = self._build_payload(question, options, answer, question_type)  # Build request payload
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {self.api_key}"}  # Set HTTP headers
        
        print("[PROCESSING] Processing your answer...")  # Inform user that processing has started
        
        try:  # Begin error handling block
            response = requests.post(self.api_endpoint, headers=headers, json=payload, timeout=API_TIMEOUT)  # Make API request
            
            if response.status_code != 200:  # Check if request was not successful
                print(f"[DISCONNECTION] Lost connection to model! Status code: {response.status_code}")  # Show error status
                print("[INFO] Please check your internet connection or API key.")  # Provide troubleshooting tip
                raise Exception("Model disconnection detected")  # Raise exception for non-200 status
                
            result = response.json()  # Parse JSON response
            self._parse_silicon_flow_response(result)  # Parse the response content
            return result  # Return the processed result
            
        except requests.exceptions.RequestException as e:  # Catch network-related exceptions
            print("[DISCONNECTION] Lost connection to model!")  # Inform about connection loss
            print(f"[ERROR] Network error: {e}")  # Display specific error message
            print("[INFO] Please check your internet connection and try again.")  # Provide troubleshooting advice
            raise  # Re-raise the exception
    
    def _build_payload(self, question: str, options: List[Dict[str, str]],  # Private method to build API request payload
                      answer: str, question_type: str) -> Dict[str, Any]:  # Parameters and return type
        options_str = "\n".join([f"{opt['opt_code']}. {opt['opt_content']}" for opt in options])  # Format options as string
        
        system_prompt = f"""You are an expert at matching user answers to predefined options.   # System prompt for AI
Given a {question_type}-choice question and the user's natural language answer,   # Explain the task context
identify which option(s) best matches the user's response.  # Define the objective

Return your response as a JSON object with this structure:  # Specify response format
{{
    "option_code": "1",  # Expected JSON structure
    "option_content": "Option text",  # Option content field
    "confidence": 0.95,  # Confidence score field
    "reasoning": "Brief explanation of why this option matches"  # Reasoning field
}}

For multiple options, use comma-separated values like "1,2,3"."""  # Handle multiple selection case
        
        user_prompt = f"""Question: {question}  # Format the user prompt with question
Available options:  # List available options
{options_str}
User's answer: "{answer}"  # Include user's answer

Please match the user's answer to the most appropriate option(s) and return the result in JSON format."""  # Request JSON response
        
        return {  # Return the complete API payload
            "model": self.model,  # Specify the AI model to use
            "messages": [  # Define the conversation messages
                {"role": "system", "content": system_prompt},  # System message with instructions
                {"role": "user", "content": user_prompt}  # User message with question and answer
            ],
            "temperature": 0.1,  # Set low temperature for consistent responses
            "max_tokens": 500  # Limit response length
        }
    
    def _parse_silicon_flow_response(self, result: Dict[str, Any]) -> None:  # Private method to parse API response
        content = result['choices'][0]['message']['content']  # Extract content from response
        result['parsed_data'] = json.loads(content)  # Parse content as JSON and store in result

def process_question(api_client: VoiceFollowUpAPI, question: str,  # Function to process a single question
                    options: List[Dict[str, str]], question_type: str) -> None:  # Parameters and return type
    print(f"\n{'='*20} QUESTION PROCESSING {'='*20}")  # Print processing header
    print(f"\n{question_type.title()}-Choice Question: {question}")  # Display the question with type
    print("Options:")  # Print options header
    for option in options:  # Iterate through each option
        print(f"  {option['opt_code']}. {option['opt_content']}")  # Display option code and content
    
    try:  # Begin error handling for input collection
        answer = input("\nYour answer: ").strip()  # Get user input and remove whitespace
        print(f"[INPUT] You answered: '{answer}'")  # Display what the user entered
                    
    except EOFError:  # Handle case where no input is provided
        print("\n[WARNING] No input provided. Skipping this question.")  # Inform user about skipping
        return  # Exit function early
    
    try:  # Begin error handling for API processing
        result = api_client.call_api(question, options, answer, question_type)  # Call the API with user's answer
        print(f"\n{'='*20} RESULTS {'='*20}")  # Print results header
        _display_result(result)  # Display the processing results
    except Exception as e:  # Catch any exceptions during API call
        print(f"\n{'='*20} CONNECTION ERROR {'='*20}")  # Print error header
        print("[FAILED] Could not process your answer due to connection issues.")  # Inform about failure
        print("[TIP] Please try again when your connection is restored.")  # Provide troubleshooting tip
        return  # Exit function


def _display_result(result: Dict[str, Any]) -> None:  # Private function to display API results
    data = result['parsed_data']  # Extract parsed data from result
    
    print("[MATCH] Match Found!")  # Indicate that a match was found
    print(f"Option: {data['option_code']} - {data['option_content']}")  # Display matched option
    
    if data.get('reasoning'):  # Check if reasoning is provided
        print(f"[REASONING] {data['reasoning']}")  # Display the reasoning


def main():  # Main function to run the demo
    API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"  # API key for authentication
    
    api_client = VoiceFollowUpAPI(API_KEY)  # Create instance of the API client
    
    print("\n[EXAMPLES] Running example questions...")  # Inform user that examples are starting
    
    print("\n[EXAMPLE 1] Single-choice question")  # Header for first example
    single_question = "Do you drink alcohol regularly?"  # Define single-choice question
    single_options = [  # Define options for single-choice question
        {"opt_code": "1", "opt_content": "Frequently"},  # Option 1
        {"opt_code": "2", "opt_content": "Occasionally"},  # Option 2
        {"opt_code": "3", "opt_content": "Never"}  # Option 3
    ]
    process_question(api_client, single_question, single_options, "single")  # Process the single-choice question
    
    print("\n" + "=" * 80)  # Print separator line
    print("\n[PAUSE] Waiting 10 seconds before the next question...")  # Inform about delay
    time.sleep(10)  # Wait 10 seconds between questions
    
    print("\n[EXAMPLE 2] Multiple-choice question")  # Header for second example
    multi_question = "What are your symptoms?"  # Define multiple-choice question
    multi_options = [  # Define options for multiple-choice question
        {"opt_code": "1", "opt_content": "Headache"},  # Option 1
        {"opt_code": "2", "opt_content": "Dizziness"},  # Option 2
        {"opt_code": "3", "opt_content": "Blurred vision"},  # Option 3
        {"opt_code": "4", "opt_content": "Sore throat"},  # Option 4
        {"opt_code": "5", "opt_content": "Sneezing"},  # Option 5
        {"opt_code": "6", "opt_content": "Runny nose"},  # Option 6
        {"opt_code": "7", "opt_content": "Nasal congestion"},  # Option 7
        {"opt_code": "8", "opt_content": "Chest tightness"},  # Option 8
        {"opt_code": "9", "opt_content": "General weakness"}  # Option 9
    ]
    process_question(api_client, multi_question, multi_options, "multiple")  # Process the multiple-choice question
    
    print("\n[COMPLETE] Demo completed! Thank you for using Voice Follow-Up API.")  # Demo completion message


if __name__ == "__main__":  # Check if script is run directly (not imported)
    main()  # Execute the main function
