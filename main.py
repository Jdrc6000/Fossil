# NOTE
# Cheers, Paleo.gg for the full database of dinosaurs for JWE2

from database_manager import is_dino_real, query_dino, list_all_dinos, list_all_guides, read_guide
import ollama, json

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "is_dino_real",
            "description": "Check if a dinosaur exists in the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dino_name": {"type": "string", "description": "Name of the dinosaur to check."}
                },
                "required": ["dino_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_dino",
            "description": "Get all stored information about a specific dinosaur.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dino_name": {"type": "string", "description": "Name of the dinosaur to look up."}
                },
                "required": ["dino_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_all_dinos",
            "description": "List every dinosaur currently in the database.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_all_guides",
            "description": "List all available guide names. Call this when unsure what guides exist before reading one.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_guide",
            "description": "Read a guide by name. Use when the user asks a how-to question or needs help with a topic a guide might cover.",
            "parameters": {
                "type": "object",
                "properties": {
                    "guide_name": {"type": "string", "description": "Name of the guide to read (without .md extension)."}
                },
                "required": ["guide_name"],
            },
        },
    },
]

TOOL_MAP = {
    "is_dino_real": lambda args: str(is_dino_real(**args)),
    "query_dino": lambda args: json.dumps(query_dino(**args), indent=2),
    "list_all_dinos": lambda args: json.dumps(list_all_dinos()),
    "list_all_guides": lambda args: json.dumps(list_all_guides()),
    "read_guide": lambda args: read_guide(**args) or f"Guide '{args.get('guide_name')}' not found.",
}

MODEL = "gpt-oss:20b-cloud"
SYSTEM = """
You are a helpful assistant for the Fossil dinosaur database (Jurassic World Evolution 2).
You have access to tools that query the database and read guides. You MUST use these tools — never answer from your own knowledge.

Rules:
- If the user asks about a specific dinosaur's stats, behaviour, cohabitation, or hunting targets, use query_dino.
- Dinosaur records contain: stats (attack, defence, etc), social needs, cohab_like/cohab_dislike/cohab_neutral lists, and a reaction dict showing how they respond to each species (hunt or fight).
- If the user asks about a game mechanic or how something works, call list_all_guides first, then read the most relevant guide.
- Do NOT answer any game-related question from memory. Only use information returned by your tools.
- If no guide or database entry exists for the topic, say so honestly.
"""

def run_agent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_message},
    ]

    while True:
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        msg = response.message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = tc.function.arguments or {}
            print(f"  [tool] {fn_name}({fn_args})")

            if fn_name in TOOL_MAP:
                result = TOOL_MAP[fn_name](fn_args)
            else:
                result = f"Unknown tool: {fn_name}"

            messages.append({"role": "tool", "content": result})

print(f"Fossil - model: {MODEL}  |  tool count: {len(TOOL_MAP)}")
print("Type 'quit' to exit.")
while True:
    try:
        user_input = input("User: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break

    if not user_input or user_input.lower() in {"quit", "exit"}:
        break

    answer = run_agent(user_input)
    print(f"Fossil: {answer}")