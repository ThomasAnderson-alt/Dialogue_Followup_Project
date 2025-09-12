# Import necessary modules for the application
import json  # For parsing and creating JSON data structures
import time  # For time-related operations like sleep delays
from typing import Any, Dict, List, TypedDict  # Type hints for better code documentation
import requests  # For making HTTP API requests
from langgraph.graph import StateGraph, END  # LangGraph components for workflow management

# Configuration constants
API_TIMEOUT = 30  # Timeout value in seconds for API requests
SILICON_FLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"  # Base URL for the Silicon Flow API
MODEL_NAME = "Qwen/Qwen3-30B-A3B-Instruct-2507"  # Default AI model name to use


class DialogueState(TypedDict):  # TypedDict class defining the structure of dialogue state
    question: str  # The current question being asked
    options: List[Dict[str, str]]  # List of answer options with codes and content
    question_type: str  # Type of question (single-choice, multiple-choice, etc.)
    user_answer: str  # The user's response to the question
    api_response: Dict[str, Any]  # Raw response from the API call
    parsed_result: Dict[str, Any]  # Parsed and structured result from API
    error_message: str  # Any error messages that occur during processing
    step_status: str  # Current status of the workflow step


class LanggraphVoiceFollowUp:  # Main class for handling voice follow-up dialogues using LangGraph
    def __init__(self, api_key: str, model: str = MODEL_NAME):  # Constructor to initialize the dialogue system
        self.api_key, self.model, self.api_endpoint = api_key, model, SILICON_FLOW_BASE_URL  # Store configuration
        self.workflow = self._build_workflow()  # Build and store the LangGraph workflow
        
    def _build_workflow(self):  # Private method to construct the LangGraph workflow
        workflow = StateGraph(DialogueState)  # Create a new StateGraph with DialogueState structure
        # Add nodes and set up workflow connections
        for node_name, node_func in [("display_question", self._display_question_node),  # Define node-function pairs
                                     ("collect_input", self._collect_input_node),  # Input collection node
                                     ("process_api", self._process_api_node),  # API processing node
                                     ("display_result", self._display_result_node)]:  # Result display node
            workflow.add_node(node_name, node_func)  # Add each node to the workflow graph
        
        workflow.set_entry_point("display_question")  # Set the starting point of the workflow
        # Create sequential workflow edges
        edges = [("display_question", "collect_input"), ("collect_input", "process_api"),  # Define workflow transitions
                ("process_api", "display_result"), ("display_result", END)]  # END terminates the workflow
        for from_node, to_node in edges:  # Iterate through edge definitions
            workflow.add_edge(from_node, to_node)  # Connect nodes in sequence
        
        return workflow.compile()  # Compile and return the workflow
    
    def _display_question_node(self, state: DialogueState) -> DialogueState:  # Node function to display question and options
        print(f"\n{state['question_type'].title()}-Choice Question: {state['question']}")  # Print formatted question header
        print("Options:")  # Print options header
        for option in state['options']:  # Iterate through each available option
            print(f"  {option['opt_code']}. {option['opt_content']}")  # Print option code and content
        return state  # Return updated state
    
    def _collect_input_node(self, state: DialogueState) -> DialogueState:  # Node function to collect user input
        state["user_answer"] = input("\nYour answer: ").strip()  # Get user input and store in state
        return state  # Return updated state
    
    def _process_api_node(self, state: DialogueState) -> DialogueState:  # Node function to process API request
        print("[PROCESSING] Processing your answer...")  # Inform user that processing has started
        
        # Make API request with consolidated operations
        response = requests.post(  # Send POST request to the API endpoint
            self.api_endpoint,  # Target API URL
            headers={"Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {self.api_key}"},  # HTTP headers with content type and auth
            json=self._build_api_payload(state["question"], state["options"], state["user_answer"], state["question_type"]),  # Request payload
            timeout=API_TIMEOUT  # Request timeout in seconds
        )
        
        result = response.json()  # Parse the JSON response
        state.update({  # Update state with results using dict update method
            "api_response": result,  # Store complete API response for debugging
            "parsed_result": json.loads(result['choices'][0]['message']['content'])  # Extract and parse AI response content
        })
        return state  # Return updated state
    
    def _display_result_node(self, state: DialogueState) -> DialogueState:  # Node function to display processing results
        data = state["parsed_result"]  # Get the parsed result data
        print(f"\n{'='*20} RESULTS {'='*20}")  # Print results header with formatting
        print(f"[MATCH] Match Found!\nOption: {data['option_code']} - {data['option_content']}")  # Display matched option
        if data.get('reasoning'):  # Check if reasoning is provided
            print(f"[REASONING] {data['reasoning']}")  # Display the reasoning
        return state  # Return updated state
    
    def _build_api_payload(self, question: str, options: List[Dict[str, str]], answer: str, question_type: str) -> Dict[str, Any]:  # Method to build API request payload
        options_str = "\n".join(f"{opt['opt_code']}. {opt['opt_content']}" for opt in options)  # Format options as string with newlines
        
        return {  # Return the complete API payload dictionary
            "model": self.model,  # Specify which AI model to use
            "messages": [  # Array of conversation messages
                {"role": "system", "content": f"""You are an expert at matching user answers to predefined options.
Given a {question_type}-choice question and the user's natural language answer, identify which option(s) best matches the user's response.

Return your response as a JSON object with this structure:
{{"option_code": "1", "option_content": "Option text", "confidence": 0.95, "reasoning": "Brief explanation of why this option matches"}}

For multiple options, use comma-separated values like "1,2,3"."""},  # System prompt defining AI behavior and expected output format
                {"role": "user", "content": f"""Question: {question}
Available options:
{options_str}
User's answer: "{answer}"

Please match the user's answer to the most appropriate option(s) and return the result in JSON format."""}  # User prompt with specific question, options, and answer to match
            ],
            "temperature": 0.1, "max_tokens": 500  # Low temperature for consistent responses, token limit for response length
        }
    
    def process_question(self, question: str, options: List[Dict[str, str]], question_type: str):  # Main method to process a single question
        return self.workflow.invoke(DialogueState(  # Execute workflow with initial state and return final state
            question=question, options=options, question_type=question_type,  # Set question data
            user_answer="", api_response={}, parsed_result={}, error_message="", step_status=""  # Initialize empty fields
        ))


def run_demo():  # Main demo function to showcase the dialogue system
    API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"  # API key for authentication
    dialogue_client = LanggraphVoiceFollowUp(API_KEY)  # Create dialogue client instance
    
    print("\n[EXAMPLES] Running example questions using LangGraph...")  # Inform user demo is starting
    
    # Example 1: Single-choice question
    print("\n[EXAMPLE 1] Single-choice question")  # Header for first example
    dialogue_client.process_question(  # Process first question directly
        "Do you drink alcohol regularly?",  # Question text
        [{"opt_code": "1", "opt_content": "Frequently"}, {"opt_code": "2", "opt_content": "Occasionally"}, {"opt_code": "3", "opt_content": "Never"}],  # Answer options
        "single"  # Question type
    )
    
    print(f"\n{'='*80}\n[PAUSE] Waiting 10 seconds before the next question...")  # Inform about delay with separator
    time.sleep(10)  # Wait 10 seconds between questions
    
    # Example 2: Multiple-choice question  
    print("\n[EXAMPLE 2] Multiple-choice question")  # Header for second example
    dialogue_client.process_question(  # Process second question directly
        "What are your symptoms?",  # Question text
        [{"opt_code": str(i+1), "opt_content": symptom} for i, symptom in enumerate([  # Generate options with enumerated codes
            "Headache", "Dizziness", "Blurred vision", "Sore throat", "Sneezing",  # Symptoms list part 1
            "Runny nose", "Nasal congestion", "Chest tightness", "General weakness"  # Symptoms list part 2
        ])],  # List comprehension to create option dictionaries
        "multiple"  # Question type for multiple selection
    )
    
    print("\n[COMPLETE] LangGraph demo completed! Thank you for using Voice Follow-Up API.")  # Demo completion message


if __name__ == "__main__":  # Check if script is run directly (not imported)
    run_demo()  # Execute the demo function
