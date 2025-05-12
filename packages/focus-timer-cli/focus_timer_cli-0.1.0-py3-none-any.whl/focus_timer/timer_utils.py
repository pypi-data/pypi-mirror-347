import time
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn

console = Console()

def start_timer(minutes: int):
    total_seconds = minutes * 60
    console.print(f"\n[bold green]Timer set for {minutes} minutes! Stay focused.[/bold green]\n")

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=None),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Focusing...", total=total_seconds)
        while not progress.finished:
            time.sleep(1)
            progress.update(task, advance=1)

    console.print("\n[bold cyan]⏰ Time's up! Great job staying focused![/bold cyan]\n")
