import typer
from .timer_utils import start_timer
from .banner_utils import show_banner

app = typer.Typer()

@app.command()
def start(minutes: int):
    """Start a focus timer for the given minutes."""
    show_banner()
    start_timer(minutes)

if __name__ == "__main__":
    app()
