# FastAPI Dialogue Processing Service
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# Configuration
API_TIMEOUT = 30
SILICON_FLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL_NAME = "Qwen/Qwen3-30B-A3B-Instruct-2507"
DEFAULT_API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"

# FastAPI setup
app = FastAPI(title="Dialogue Follow-Up API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Data Models
class Option(BaseModel):
    opt_code: str = Field(..., description="Option code")
    opt_content: str = Field(..., description="Option content")

class DialogueRequest(BaseModel):
    question: str = Field(..., description="The question to be asked")
    options: List[Option] = Field(..., description="List of answer options")
    user_answer: str = Field(..., description="User's natural language answer")
    question_type: str = Field("single", description="Type: 'single' or 'multiple'")
    api_key: Optional[str] = Field(None, description="Optional API key")
    model: str = Field(MODEL_NAME, description="AI model to use")

    @field_validator('question_type')
    @classmethod
    def validate_question_type(cls, v):
        return v.lower() if v.lower() in ['single', 'multiple'] else 'single'
    
    @field_validator('options')
    @classmethod
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError('At least 2 options required')
        return v

class MatchResult(BaseModel):
    option_code: str
    option_content: str
    confidence: Optional[float] = None
    reasoning: Optional[str] = None

class DialogueResponse(BaseModel):
    success: bool
    timestamp: str
    question: str
    user_answer: str
    question_type: str
    match_result: Optional[Any] = None
    error_message: Optional[str] = None
    processing_time_ms: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# AI Processing
def process_ai_request(question: str, options: List[Dict], user_answer: str, question_type: str, api_key: str, model: str) -> Dict[str, Any]:
    options_str = "\n".join(f"{opt['opt_code']}. {opt['opt_content']}" for opt in options)
    
    prompts = {
        "multiple": """You are an expert at matching user answers to predefined options for multiple-choice questions.
The user can select multiple options. Return your response as a JSON object with this structure:
- For multiple matches: {"matches": [{"option_code": "A", "option_content": "Option text", "confidence": 0.95, "reasoning": "Brief explanation"}, {"option_code": "D", "option_content": "Another option", "confidence": 0.90, "reasoning": "Another explanation"}]}
- For single match: {"matches": [{"option_code": "A", "option_content": "Option text", "confidence": 0.95, "reasoning": "Brief explanation"}]}

Analyze the user's answer carefully and identify ALL options that match their response.""",
        "single": """You are an expert at matching user answers to predefined options for single-choice questions.
Return your response as a JSON object with this structure:
{"option_code": "1", "option_content": "Option text", "confidence": 0.95, "reasoning": "Brief explanation of why this option matches"}

Select the ONE best matching option."""
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompts[question_type]},
            {"role": "user", "content": f"Question: {question}\nOptions:\n{options_str}\nUser's answer: \"{user_answer}\"\n\nPlease match the user's answer to the most appropriate option(s) and return the result in JSON format."}
        ],
        "temperature": 0.1,
        "max_tokens": 800
    }
    
    response = requests.post(SILICON_FLOW_BASE_URL, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, json=payload, timeout=API_TIMEOUT)
    response.raise_for_status()
    return json.loads(response.json()['choices'][0]['message']['content'])


# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", timestamp=datetime.now().isoformat(), version="1.0.0")

@app.post("/process-dialogue", response_model=DialogueResponse)
async def process_dialogue(request: DialogueRequest):
    start_time = datetime.now()
    
    try:
        if not request.question.strip() or not request.user_answer.strip():
            raise HTTPException(status_code=400, detail="Question and answer cannot be empty")
            
        api_key = request.api_key or DEFAULT_API_KEY
        options_dict = [{"opt_code": opt.opt_code, "opt_content": opt.opt_content} for opt in request.options]
        parsed_result = process_ai_request(request.question, options_dict, request.user_answer, request.question_type, api_key, request.model)
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Handle response format
        if request.question_type == "multiple":
            matches_data = parsed_result.get('matches', [])
            match_result = [MatchResult(option_code=m.get('option_code', ''), option_content=m.get('option_content', ''), 
                                      confidence=m.get('confidence'), reasoning=m.get('reasoning')) for m in matches_data] if matches_data else None
        else:
            match_result = MatchResult(option_code=parsed_result.get('option_code', ''), option_content=parsed_result.get('option_content', ''),
                                     confidence=parsed_result.get('confidence'), reasoning=parsed_result.get('reasoning'))
        
        return DialogueResponse(success=True, timestamp=datetime.now().isoformat(), question=request.question, 
                              user_answer=request.user_answer, question_type=request.question_type, 
                              match_result=match_result, processing_time_ms=processing_time)
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        return DialogueResponse(success=False, timestamp=datetime.now().isoformat(), question=request.question, 
                              user_answer=request.user_answer, question_type=request.question_type, 
                              error_message=str(e), processing_time_ms=processing_time)

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
