import state

COMMANDS = {}

def command(name, description=""):
    def decorator(fn):
        COMMANDS[name] = {"fn": fn, "description": description}
        return fn
    return decorator

def handle_command(user_input: str) -> str | None:
    """Returns output string if input was a command, None otherwise."""
    if not user_input.startswith("/"):
        return None
    parts = user_input[1:].split()
    name, args = parts[0].lower(), parts[1:]
    if name not in COMMANDS:
        return f"Unknown command: /{name}. Type /help to see available commands."
    
    lines = []
    COMMANDS[name]["fn"](*args, _out=lines.append)
    return "\n".join(lines) if lines else ""


@command("switch", "Switch game context. Usage: /switch <jwe2|jwe3>")
def cmd_switch(*args, _out=print, game=None):
    game = args[0] if args else game
    if game not in state.NAME_MAP:
        _out(f"Valid games: {list(state.NAME_MAP.keys())}")
        return
    state.GAME = game
    state.reset_history()
    _out(f"Switched to {state.NAME_MAP[state.GAME]}. History cleared.")

@command("game", "Show the current active game.")
def cmd_game(*args, _out=print):
    _out(f"Current game: {state.NAME_MAP[state.GAME]}")

@command("clear", "Clear conversation history.")
def cmd_clear(*args, _out=print):
    state.reset_history()
    _out("History cleared.")

@command("history", "Show current conversation length.")
def cmd_history(*args, _out=print):
    _out(f"{len(state.history) - 1} messages in history.")

@command("help", "List all available commands.")
def cmd_help(*args, _out=print):
    for name, entry in COMMANDS.items():
        _out(f"  /{name} — {entry['description']}")