from __future__ import annotations
from database_manager import is_dino_real, query_dino, list_all_dinos, list_all_guides, read_guide
import commands, state, ollama, json
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.widgets import Footer, Header, Input, RichLog, Static
from textual.reactive import reactive
from rich.text import Text
from rich.style import Style
from rich.padding import Padding
from rich.markdown import Markdown

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
            "description": "List all available guide names.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_guide",
            "description": "Read a guide by name.",
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

def run_agent_sync(user_message: str, on_tool_call) -> str:
    state.history.append({"role": "user", "content": user_message})
    tool_map = get_tool_map()

    while True:
        response = ollama.chat(model=MODEL, messages=state.history, tools=TOOLS)
        msg = response.message
        state.history.append(msg)
        if not msg.tool_calls:
            return msg.content or ""
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = tc.function.arguments or {}
            on_tool_call(fn_name, fn_args)
            result = (
                tool_map[fn_name](fn_args)
                if fn_name in tool_map
                else f"Unknown tool: {fn_name}"
            )
            state.history.append({"role": "tool", "content": result})

CSS = """
Screen {
    background: #0d0d0d;
}

StatusBar {
    height: 1;
    background: #111111;
    color: #555555;
    padding: 0 1;
    border-bottom: tall #1e1e1e;
}

#log-container {
    height: 1fr;
    padding: 0 1;
    overflow-y: auto;
}

RichLog {
    background: transparent;
    scrollbar-color: #2a2a2a #111111;
    scrollbar-size: 1 1;
}

#input-row {
    height: 3;
    background: #111111;
    border-top: tall #1e1e1e;
    padding: 0 1;
    align: left middle;
}

#prompt-label {
    width: auto;
    height: 1;
    color: #cc785c;
    margin-right: 1;
    text-style: bold;
}

#user-input {
    width: 1fr;
    height: 1;
    background: transparent;
    border: none;
    color: #d4d4d4;
    padding: 0;
}

#user-input:focus {
    border: none;
    background: transparent;
}

Footer {
    background: #0d0d0d;
    color: #3a3a3a;
    border-top: tall #1a1a1a;
}
"""

class StatusBar(Static):
    def on_mount(self):
        game_name = state.NAME_MAP.get(state.GAME, state.GAME)
        self.update(f" fossil  ~  {MODEL}  ~  {game_name}")

class FossilApp(App):
    CSS = CSS
    TITLE = "fossil"
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+r", "reset", "Reset history"),
        Binding("ctrl+l", "clear_log", "Clear"),
    ]

    _busy: reactive[bool] = reactive(False)

    def compose(self) -> ComposeResult:
        yield StatusBar()
        with Vertical(id="log-container"):
            yield RichLog(id="log", wrap=True, markup=False, highlight=False)
        with Horizontal(id="input-row"):
            yield Static(">", id="prompt-label")
            yield Input(placeholder="Ask about dinosaurs…", id="user-input")
        yield Footer()

    def on_mount(self):
        state.reset_history()
        self._print_welcome()
        self.query_one(Input).focus()
    
    # display helpers
    def _richlog(self) -> RichLog:
        return self.query_one(RichLog)

    def _print_welcome(self):
        self._richlog().write(Text(""))
        t = Text()
        t.append("  🦕 fossil", style=Style(color="#cc785c", bold=True))
        self._richlog().write(t)
        self._richlog().write(Text(
            f"  {MODEL}  ~  {state.NAME_MAP.get(state.GAME, state.GAME)}",
            style=Style(color="#555555"),
        ))
        self._richlog().write(Text(
            "  Type /help for commands. Ctrl+R resets history, Ctrl+C quits.",
            style=Style(color="#3a3a3a"),
        ))
        self._richlog().write(Text(""))

    def _append_user(self, text: str):
        self._richlog().write(Text(""))
        t = Text()
        t.append("  ▸ ", style=Style(color="#cc785c", bold=True))
        t.append(text, style=Style(color="#d4d4d4"))
        self._richlog().write(t)
        self._richlog().write(Text(""))

    def _append_assistant(self, text: str):
        t = Text()
        t.append("  fossil", style=Style(color="#7ab8a0", bold=True))
        self._richlog().write(t)
        self._richlog().write(Padding(Markdown(text, code_theme="monokai"), pad=(0, 0, 0, 2)))
        self._richlog().write(Text(""))

    def _append_tool(self, fn_name: str, fn_args: dict):
        args_str = ", ".join(f"{k}={v!r}" for k, v in fn_args.items())
        t = Text()
        t.append("  $ ", style=Style(color="#444444"))
        t.append(fn_name, style=Style(color="#6a6a6a", bold=True))
        t.append(f"({args_str})", style=Style(color="#444444"))
        self._richlog().write(t)

    def _append_error(self, text: str):
        t = Text()
        t.append("  x ", style=Style(color="#c05050"))
        t.append(text, style=Style(color="#a05050"))
        self._richlog().write(t)
        self._richlog().write(Text(""))

    def _append_info(self, text: str):
        t = Text()
        t.append("  ~ ", style=Style(color="#555555"))
        t.append(text, style=Style(color="#666666"))
        self._richlog().write(t)

    def _set_busy(self, busy: bool):
        self._busy = busy
        inp = self.query_one(Input)
        inp.disabled = busy
        prompt = self.query_one("#prompt-label", Static)
        prompt.update("  …" if busy else ">")
        if not busy:
            inp.focus()

    # input
    async def on_input_submitted(self, event: Input.Submitted):
        text = event.value.strip()
        if not text:
            return
        event.input.clear()

        if text.lower() in {"quit", "exit"}:
            self.exit()
            return

        result = commands.handle_command(text)
        if result is not None:
            self._append_user(text)
            if result:
                self._append_info(result)
            return

        self._append_user(text)
        self._set_busy(True)
        self.run_worker(lambda: self._agent_worker(text), thread=True)
    
    # worker
    def _agent_worker(self, text: str):
        try:
            result = run_agent_sync(
                text,
                on_tool_call=lambda fn, args: self.call_from_thread(
                    self._append_tool, fn, args
                ),
            )
            self.call_from_thread(self._append_assistant, result)
        except Exception as exc:
            self.call_from_thread(self._append_error, str(exc))
        finally:
            self.call_from_thread(self._set_busy, False)
    
    # action
    def action_reset(self):
        state.reset_history()
        self._richlog().clear()
        self._print_welcome()
        self._append_info("History reset.")

    def action_clear_log(self):
        self._richlog().clear()
        self._print_welcome()

FossilApp().run()