import json
import re
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

def strip_thinking(content: str) -> str:
    if not content:
        return content
    result = content
    while True:
        start = result.lower().find("<tool_call>think>")
        if start == -1:
            break
        end = result.lower().find("</think>", start)
        if end == -1:
            break
        result = result[:start] + result[end + len("</think>"):]
    return result.strip()

from app.prompt import SYSTEM_PROMPT
from app.memory import store, Session
from app.tools import TOOLS, simulate_booking
from app.llm import chat, extract_analytics

app = FastAPI(title="Northstar One AI Sales Agent")

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str

class EndSessionRequest(BaseModel):
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session = store.get_or_create(request.session_id)
    
    session.history.append({"role": "user", "content": request.message})
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_message = {
        "role": "system",
        "content": f"{SYSTEM_PROMPT}\nToday's date is {current_date}.",
    }
    
    messages = [system_message] + session.history
    
    response = chat(messages=messages, tools=TOOLS, tool_choice="auto")
    assistant_message = response.choices[0].message
    
    if assistant_message.tool_calls:
        session.history.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": assistant_message.tool_calls,
        })
    else:
        session.history.append({
            "role": "assistant",
            "content": assistant_message.content,
        })
    
    if not assistant_message.tool_calls:
        return ChatResponse(reply=strip_thinking(assistant_message.content), session_id=request.session_id)
    
    tool_results = []
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if function_name == "book_site_visit":
            result = simulate_booking(arguments["date"], arguments["time"])
            if result["status"] == "confirmed":
                session.flags.site_visit_status = "confirmed"
                session.flags.site_visit_datetime = f"{arguments['date']} {arguments['time']}"
            else:
                session.flags.site_visit_status = "unavailable_alternative_offered"
        
        elif function_name == "escalate_to_human":
            session.flags.escalated_to_human = True
            session.flags.escalation_reason = arguments.get("reason", "")
            result = {"status": "escalated", "reason": arguments.get("reason", "")}
        
        elif function_name == "mark_do_not_contact":
            session.flags.do_not_contact = True
            result = {"status": "do_not_contact_set"}
        
        elif function_name == "schedule_followup":
            session.flags.follow_up_required = True
            session.flags.follow_up_preferred_time = arguments.get("preferred_time", "")
            result = {"status": "followup_scheduled", "preferred_time": arguments.get("preferred_time", "")}
        
        else:
            result = {"status": "unknown_function"}
        
        tool_results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": json.dumps(result),
        })
    
    session.history.extend(tool_results)
    
    follow_up_messages = [system_message] + session.history
    follow_up_response = chat(messages=follow_up_messages)
    follow_up_content = strip_thinking(follow_up_response.choices[0].message.content)
    
    session.history.append({"role": "assistant", "content": follow_up_content})
    
    return ChatResponse(reply=follow_up_content, session_id=request.session_id)

@app.post("/end-session")
async def end_session(request: EndSessionRequest):
    session = store.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    flags = session.flags
    
    analytics_result = extract_analytics(session.history)
    
    result = {
        "session_id": request.session_id,
        "language_used": analytics_result.get("language_used", "Unknown"),
        "configuration_interest": analytics_result.get("configuration_interest", "Not discussed"),
        "purpose": analytics_result.get("purpose", "Unknown"),
        "budget_fit": analytics_result.get("budget_fit", "Not discussed"),
        "timeline": analytics_result.get("timeline", "Unknown"),
        "interest_level": analytics_result.get("interest_level", "Cold"),
        "objections_raised": analytics_result.get("objections_raised", []),
        "site_visit_status": flags.site_visit_status,
        "site_visit_datetime": flags.site_visit_datetime,
        "follow_up_required": flags.follow_up_required,
        "follow_up_preferred_time": flags.follow_up_preferred_time,
        "escalated_to_human": flags.escalated_to_human,
        "escalation_reason": flags.escalation_reason,
        "do_not_contact": flags.do_not_contact,
        "conversation_summary": analytics_result.get("conversation_summary", ""),
    }
    
    store.delete(request.session_id)
    
    return JSONResponse(content=result)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
