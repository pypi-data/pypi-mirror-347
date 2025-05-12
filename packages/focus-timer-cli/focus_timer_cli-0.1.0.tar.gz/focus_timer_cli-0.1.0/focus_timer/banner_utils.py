from rich.console import Console
from rich.panel import Panel

console = Console()

def show_banner():
    banner_text = r"""
   ______            _                 _             
  |  ____|          | |               | |            
  | |__  __  ___ __ | | ___   __ _  __| | ___  _ __  
  |  __| \ \/ / '_ \| |/ _ \ / _` |/ _` |/ _ \| '_ \ 
  | |____ >  <| |_) | | (_) | (_| | (_| | (_) | | | |
  |______/_/\_\ .__/|_|\___/ \__,_|\__,_|\___/|_| |_|
               | |                                   
               |_|                                   
    """
    console.print(Panel.fit(banner_text, title="FOCUS TIMER", style="bold green"))
