
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt

# AEON Theme
aeon_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green",
    "aeon_text": "white",
    "user_text": "grey70"
})

console = Console(theme=aeon_theme)

def output(text: str):
    """Outputs text in AEON's calm, authoritative style."""
    console.print(f"[aeon_text]{text}[/aeon_text]")

def error(text: str):
    """Outputs error messages."""
    console.print(f"[error]Error: {text}[/error]")

def confirm(text: str, default: bool = False) -> bool:
    """Explicit confirmation for risky actions."""
    return Prompt.ask(f"[warning]{text}[/warning]", choices=["y", "n"], default="y" if default else "n") == "y"

def user_input(prompt_text: str = "") -> str:
    """Gets user input."""
    return console.input(f"[user_text]{prompt_text} > [/user_text]")
