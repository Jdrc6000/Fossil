import state

COMMANDS = {}

def command(name, description=""):
    def decorator(fn):
        COMMANDS[name] = {"fn": fn, "description": description}
        return fn
    return decorator

def handle_command(user_input: str) -> bool:
    """Returns True if input was a command, False otherwise."""
    if not user_input.startswith("/"):
        return False
    parts = user_input[1:].split()
    name, args = parts[0].lower(), parts[1:]
    if name not in COMMANDS:
        print(f"Unknown command: /{name}. Type /help to see available commands.")
        return True
    COMMANDS[name]["fn"](*args)
    return True


@command("switch", "Switch game context. Usage: /switch <jwe2|jwe3>")
def cmd_switch(game=None):
    if game not in state.NAME_MAP:
        print(f"Valid games: {list(state.NAME_MAP.keys())}")
        return
    state.GAME = game
    state.reset_history()
    print(f"Switched to {state.NAME_MAP[state.GAME]}. History cleared.")

@command("game", "Show the current active game.")
def cmd_game():
    print(f"Current game: {state.NAME_MAP[state.GAME]}")

@command("clear", "Clear conversation history.")
def cmd_clear():
    state.reset_history()
    print("History cleared.")

@command("history", "Show current conversation length.")
def cmd_history():
    print(f"{len(state.history) - 1} messages in history.")

@command("help", "List all available commands.")
def cmd_help():
    for name, entry in COMMANDS.items():
        print(f"  /{name} — {entry['description']}")