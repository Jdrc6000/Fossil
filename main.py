from database_manager import is_dino_real, query_dino, list_all_dinos, list_all_guides, read_guide
import commands, state, ollama, json

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

MODEL = "gpt-oss:20b-cloud"

def get_tool_map():
    return {
        "is_dino_real": lambda args: str(is_dino_real(game=state.GAME, **args)),
        "query_dino": lambda args: json.dumps(query_dino(game=state.GAME, **args), indent=2),
        "list_all_dinos": lambda args: json.dumps(list_all_dinos(game=state.GAME)),
        "list_all_guides": lambda args: json.dumps(list_all_guides(game=state.GAME)),
        "read_guide": lambda args: read_guide(game=state.GAME, **args) or f"Guide '{args.get('guide_name')}' not found.",
    }

def run_agent(user_message: str) -> str:
    state.history.append({"role": "user", "content": user_message})
    tool_map = get_tool_map()
    while True:
        response = ollama.chat(model=MODEL, messages=state.history, tools=TOOLS)
        msg = response.message
        state.history.append(msg)
        if not msg.tool_calls:
            return msg.content
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = tc.function.arguments or {}
            print(f"  [tool] {fn_name}({fn_args})")
            result = tool_map[fn_name](fn_args) if fn_name in tool_map else f"Unknown tool: {fn_name}"
            state.history.append({"role": "tool", "content": result})

state.reset_history()
print(f"Fossil - model: {MODEL}  |  game: {state.NAME_MAP[state.GAME]}  |  type /help for commands")
print("Type 'quit' to exit.")

while True:
    try:
        user_input = input("User: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break
    if not user_input or user_input.lower() in {"quit", "exit"}:
        break
    if commands.handle_command(user_input):
        continue
    answer = run_agent(user_input)
    print(f"Fossil: {answer}")