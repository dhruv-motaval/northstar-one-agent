from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "PROMPT.md"

def load_system_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

SYSTEM_PROMPT = load_system_prompt()
