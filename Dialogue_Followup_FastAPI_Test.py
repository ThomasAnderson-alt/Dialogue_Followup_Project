import requests
from typing import List, Dict, Any, Optional

class LocalDialogueClient:
    """HTTP client for interacting with the dialogue processing API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30
    
    def check_health(self) -> Dict[str, Any]:
        """Check if the API server is running and healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Failed to connect to API server: {e}")
            raise
    
    def process_dialogue(self, question: str, options: List[Dict[str, str]], user_answer: str,
                        question_type: str = "single", api_key: Optional[str] = None,
                        model: Optional[str] = None) -> Dict[str, Any]:
        """Send dialogue data to API for processing and return results"""
        payload = {"question": question, "options": options, "user_answer": user_answer, "question_type": question_type}
        if api_key: payload["api_key"] = api_key
        if model: payload["model"] = model
        
        try:
            response = requests.post(f"{self.base_url}/process-dialogue", json=payload,
                                   headers={"Content-Type": "application/json"}, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Failed to process dialogue: {e}")
            raise

def display_result(result: Dict[str, Any]) -> None:
    """Display API response in a formatted, readable format"""
    print(f"\n{'='*50}\nDIALOGUE PROCESSING RESULT\n{'='*50}")
    print(f"Success: {result['success']}\nQuestion: {result['question']}\nUser Answer: {result['user_answer']}")
    
    if result['success'] and result.get('match_result'):
        match = result['match_result']
        if isinstance(match, list):
            print(f"\n[MATCHES FOUND] ({len(match)} options selected)")
            for i, m in enumerate(match, 1):
                print(f"{i}. Option: {m['option_code']} - {m['option_content']}")
                if m.get('reasoning'): print(f"   Reasoning: {m['reasoning']}")
        else:
            print(f"\n[MATCH FOUND]\nOption: {match['option_code']} - {match['option_content']}")
            if match.get('reasoning'): print(f"Reasoning: {match['reasoning']}")
    elif not result['success']:
        print(f"\n[ERROR] {result.get('error_message', 'Unknown error occurred')}")

def main():
    """Interactive testing function for the dialogue processing API"""
    print("Local FastAPI Dialogue Client\n" + "="*30)
    
    client = LocalDialogueClient()
    
    # Check server health
    try:
        client.check_health()
        print("[SUCCESS] API server is healthy!")
    except Exception:
        print("[ERROR] Cannot connect to API server!\n[INFO] Please start your FastAPI server: python main.py")
        return
    
    # Question configurations
    questions = {
        "1": {
            "type": "single", 
            "question": "How often do you exercise?",
            "options": [{"opt_code": "1", "opt_content": "Daily"}, {"opt_code": "2", "opt_content": "Weekly"}, 
                       {"opt_code": "3", "opt_content": "Monthly"}, {"opt_code": "4", "opt_content": "Rarely"}],
            "example": "I exercise every day' or 'Almost never"
        },
        "2": {
            "type": "multiple",
            "question": "What activities do you enjoy doing in your free time?", 
            "options": [{"opt_code": "A", "opt_content": "Reading books"}, {"opt_code": "B", "opt_content": "Playing sports"},
                       {"opt_code": "C", "opt_content": "Watching movies"}, {"opt_code": "D", "opt_content": "Cooking"},
                       {"opt_code": "E", "opt_content": "Traveling"}],
            "example": "I like reading and watching movies' or 'Sports and cooking are my favorites"
        }
    }
    
    # Get user choice and setup question
    print("\nChoose question type:\n1. Single Choice Question\n2. Multiple Choice Question")
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice not in questions:
        print("[ERROR] Invalid choice! Please run the program again and choose 1 or 2.")
        return
    
    q = questions[choice]
    print(f"\n{q['type'].title()} Choice Question: {q['question']}")
    print(f"Options ({'select one' if q['type'] == 'single' else 'you can select multiple'}):")
    for option in q['options']:
        print(f"  {option['opt_code']}. {option['opt_content']}")
    
    # Get user input and process
    print(f"\nEnter your answer in natural language:\n(Example: '{q['example']}')")
    user_answer = input("Your answer: ").strip()
    
    if not user_answer:
        print("[ERROR] Answer cannot be empty!")
        return
    
    print(f"\n[PROCESSING] You answered: '{user_answer}'\n[INFO] Processing as {q['type']} choice question...\n[INFO] Sending to API for processing...")
    
    try:
        result = client.process_dialogue(q['question'], q['options'], user_answer, q['type'])
        display_result(result)
    except Exception as e:
        print(f"[ERROR] Processing failed: {e}\n[INFO] Make sure the FastAPI server is running properly.")

if __name__ == "__main__":
    main()
