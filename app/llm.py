import os
import json
from groq import Groq
from app.prompt import SYSTEM_PROMPT

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
PRIMARY_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
FALLBACK_MODELS = ["openai/gpt-oss-120b", "groq/compound"]

def chat(messages: list, tools: list = None, tool_choice: str = "auto") -> dict:
    models_to_try = [PRIMARY_MODEL] + [m for m in FALLBACK_MODELS if m != PRIMARY_MODEL]
    last_error = None
    
    for model in models_to_try:
        try:
            kwargs = {
                "model": model,
                "messages": messages,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = tool_choice
            
            response = client.chat.completions.create(**kwargs)
            return response
        except Exception as e:
            last_error = e
            continue
    
    raise last_error

def extract_analytics(transcript: list) -> dict:
    system_msg = """You will be given a transcript of a conversation between an AI sales agent and
a customer about Northstar One, a real-estate project. Output ONLY a JSON
object with exactly these fields: language_used, configuration_interest,
purpose, budget_fit, timeline, interest_level, objections_raised,
conversation_summary. Base every field only on what's explicitly evident in
the transcript. If something wasn't discussed, use "Not discussed" or
"Unknown" as appropriate — never guess. Output no text outside the JSON object."""
    
    messages = [{"role": "system", "content": system_msg}] + transcript
    
    models_to_try = [PRIMARY_MODEL] + [m for m in FALLBACK_MODELS if m != PRIMARY_MODEL]
    last_error = None
    
    for model in models_to_try:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            last_error = e
            continue
    
    raise last_error
