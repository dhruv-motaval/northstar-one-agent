# Northstar One — AI Sales Agent (Huvo AI Assignment)

## Overview
A FastAPI-based chatbot that simulates an AI sales assistant for Northstar One, a fictional real-estate project in Gurugram. The agent handles lead qualification, objection handling, and site-visit booking.

## How to run
1. git clone <repo> && cd northstar-one-agent
2. python -m venv venv && source venv/bin/activate   (Windows: venv\Scripts\activate)
3. pip install -r requirements.txt
4. cp .env.example .env   → add your GROQ_API_KEY
5. uvicorn app.main:app --reload
6. open http://localhost:8000

## Project structure
```
northstar-one-agent/
├── app/
│   ├── __init__.py          # Package initializer
│   ├── main.py              # FastAPI app with /chat and /end-session routes
│   ├── prompt.py            # SYSTEM_PROMPT constant (loaded from PROMPT.md)
│   ├── tools.py             # Tool JSON schemas + simulate_booking()
│   ├── llm.py               # Groq client wrapper with model fallback
│   ├── memory.py            # In-memory session store
│   └── static/
│       └── index.html       # Chat UI (text-only)
├── tests/
│   └── test_cases.md        # Test scenarios with input/expected/actual output
├── PROMPT.md                # System prompt for Riya (AI sales assistant)
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── .gitignore               # Git ignore patterns
```

## Key assumptions
- Prices are fixed exactly as given in the assignment; no other project data
  (amenities, possession date, RERA, discounts) was provided, so the agent is
  built to never fabricate it.
- Site-visit booking is simulated with a fixed rule (see PROMPT.md / tools.py),
  not connected to a real scheduling system.
- The assignment's voice requirement is about prompt design, not live
  telephony — Part 2 is a text bot built from a prompt that's also written to
  work over voice.

## Known limitations
- Session memory is in-memory only and resets on server restart — fine for
  this take-home, not something to build around for real use.
- Analytics' softer fields (interest level, budget fit, etc.) come from an LLM
  read of the transcript, so occasional misclassification is possible; the
  booking/escalation/opt-out/follow-up fields are tracked directly by the
  backend and don't have this issue.
- No auth, no rate limiting — out of scope for a take-home demo.

## AI tools used
- **Kiro Extension**: Used for code generation and development assistance
- **OmniRoute**: Used for multi-provider LLM access and model routing (supports Groq, OpenAI, and other providers with automatic fallback)

## Test cases
See tests/test_cases.md
