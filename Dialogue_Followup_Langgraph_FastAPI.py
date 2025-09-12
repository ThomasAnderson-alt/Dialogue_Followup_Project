# ============================================================================
# IMPORTS AND CONFIGURATION
# ============================================================================
# Core libraries for JSON handling, HTTP requests, workflow management, and type hints

import json
import time
from typing import Any, Dict, List, TypedDict
import requests
from langgraph.graph import StateGraph, END

API_TIMEOUT = 30
SILICON_FLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL_NAME = "Qwen/Qwen3-30B-A3B-Instruct-2507"


# ============================================================================
# STATE MANAGEMENT DATA STRUCTURE
# ============================================================================
# TypedDict that defines the data structure passed between workflow nodes

class DialogueState(TypedDict):
    question: str
    options: List[Dict[str, str]]
    question_type: str
    user_answer: str
    api_response: Dict[str, Any]
    parsed_result: Dict[str, Any]
    error_message: str
    step_status: str


# ============================================================================
# MAIN DIALOGUE PROCESSING CLASS
# ============================================================================
# This class manages the entire dialogue workflow using LangGraph for orchestration.
# It handles question display, user input collection, AI processing, and result display.

class LanggraphVoiceFollowUp:
    def __init__(self, api_key: str, model: str = MODEL_NAME):
        self.api_key, self.model, self.api_endpoint = api_key, model, SILICON_FLOW_BASE_URL
        self.workflow = self._build_workflow()
        
    # ------------------------------------------------------------------------
    # WORKFLOW CONSTRUCTION
    # ------------------------------------------------------------------------
    # Builds the LangGraph workflow with nodes and connections
    
    def _build_workflow(self):
        workflow = StateGraph(DialogueState)
        
        for node_name, node_func in [("display_question", self._display_question_node),
                                     ("collect_input", self._collect_input_node),
                                     ("process_api", self._process_api_node),
                                     ("display_result", self._display_result_node)]:
            workflow.add_node(node_name, node_func)
        
        workflow.set_entry_point("display_question")
        
        edges = [("display_question", "collect_input"), ("collect_input", "process_api"),
                ("process_api", "display_result"), ("display_result", END)]
        for from_node, to_node in edges:
            workflow.add_edge(from_node, to_node)
        
        return workflow.compile()
    
    # ------------------------------------------------------------------------
    # WORKFLOW NODE FUNCTIONS
    # ------------------------------------------------------------------------
    # Individual functions that handle each step of the dialogue process
    
    def _display_question_node(self, state: DialogueState) -> DialogueState:
        print(f"\n{state['question_type'].title()}-Choice Question: {state['question']}")
        print("Options:")
        for option in state['options']:
            print(f"  {option['opt_code']}. {option['opt_content']}")
        return state
    
    def _collect_input_node(self, state: DialogueState) -> DialogueState:
        state["user_answer"] = input("\nYour answer: ").strip()
        return state
    
    def _process_api_node(self, state: DialogueState) -> DialogueState:
        print("[PROCESSING] Processing your answer...")
        
        response = requests.post(
            self.api_endpoint,
            headers={"Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {self.api_key}"},
            json=self._build_api_payload(state["question"], state["options"], state["user_answer"], state["question_type"]),
            timeout=API_TIMEOUT
        )
        
        result = response.json()
        state.update({
            "api_response": result,
            "parsed_result": json.loads(result['choices'][0]['message']['content'])
        })
        return state
    
    def _display_result_node(self, state: DialogueState) -> DialogueState:
        data = state["parsed_result"]
        print(f"\n{'='*20} RESULTS {'='*20}")
        print(f"[MATCH] Match Found!\nOption: {data['option_code']} - {data['option_content']}")
        if data.get('reasoning'):
            print(f"[REASONING] {data['reasoning']}")
        return state
    
    # ------------------------------------------------------------------------
    # API PAYLOAD CONSTRUCTION
    # ------------------------------------------------------------------------
    # Builds the request payload for the AI API with proper formatting
    
    def _build_api_payload(self, question: str, options: List[Dict[str, str]], answer: str, question_type: str) -> Dict[str, Any]:
        options_str = "\n".join(f"{opt['opt_code']}. {opt['opt_content']}" for opt in options)
        
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": f"""You are an expert at matching user answers to predefined options.
Given a {question_type}-choice question and the user's natural language answer, identify which option(s) best matches the user's response.

Return your response as a JSON object with this structure:
{{"option_code": "1", "option_content": "Option text", "confidence": 0.95, "reasoning": "Brief explanation of why this option matches"}}

For multiple options, use comma-separated values like "1,2,3"."""},
                {"role": "user", "content": f"""Question: {question}
Available options:
{options_str}
User's answer: "{answer}"

Please match the user's answer to the most appropriate option(s) and return the result in JSON format."""}
            ],
            "temperature": 0.1, "max_tokens": 500
        }
    
    # ------------------------------------------------------------------------
    # PUBLIC INTERFACE
    # ------------------------------------------------------------------------
    # Main method to execute the dialogue workflow
    
    def process_question(self, question: str, options: List[Dict[str, str]], question_type: str):
        return self.workflow.invoke(DialogueState(
            question=question, options=options, question_type=question_type,
            user_answer="", api_response={}, parsed_result={}, error_message="", step_status=""
        ))


# ============================================================================
# DEMO FUNCTION
# ============================================================================
# Interactive demonstration that shows the dialogue system in action with
# predefined examples for both single-choice and multiple-choice questions

def run_demo():
    API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"
    dialogue_client = LanggraphVoiceFollowUp(API_KEY)
    
    print("\n[EXAMPLES] Running example questions using LangGraph...")
    
    print("\n[EXAMPLE 1] Single-choice question")
    dialogue_client.process_question(
        "Do you drink alcohol regularly?",
        [{"opt_code": "1", "opt_content": "Frequently"}, {"opt_code": "2", "opt_content": "Occasionally"}, {"opt_code": "3", "opt_content": "Never"}],
        "single"
    )
    
    print(f"\n{'='*80}\n[PAUSE] Waiting 10 seconds before the next question...")
    time.sleep(10)
    
    print("\n[EXAMPLE 2] Multiple-choice question")
    dialogue_client.process_question(
        "What are your symptoms?",
        [{"opt_code": str(i+1), "opt_content": symptom} for i, symptom in enumerate([
            "Headache", "Dizziness", "Blurred vision", "Sore throat", "Sneezing",
            "Runny nose", "Nasal congestion", "Chest tightness", "General weakness"
        ])],
        "multiple"
    )
    
    print("\n[COMPLETE] LangGraph demo completed! Thank you for using Voice Follow-Up API.")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
# Executes the demo when script is run directly

if __name__ == "__main__":
    run_demo()
