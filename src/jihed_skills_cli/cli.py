import argparse
import sys
import httpx
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

GITHUB_API_BASE = "https://api.github.com/repos/jihedbfr-art/ai-skills/contents/skills"
RAW_BASE_URL = "https://raw.githubusercontent.com/jihedbfr-art/ai-skills/main/skills"

def fetch_contents(path: str = "") -> list:
    url = f"{GITHUB_API_BASE}/{path}".strip("/")
    try:
        response = httpx.get(url, headers={"Accept": "application/vnd.github.v3+json"})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError:
        console.print(f"[bold red]Error:[/bold red] Could not reach GitHub API for path '{path}'. Rate limits may apply.")
        sys.exit(1)

def fetch_raw_skill(path: str) -> str:
    url = f"{RAW_BASE_URL}/{path}"
    try:
        response = httpx.get(url)
        if response.status_code == 404:
            return ""
        response.raise_for_status()
        return response.text
    except httpx.HTTPError:
        console.print(f"[bold red]Error:[/bold red] Failed to download skill content.")
        sys.exit(1)

def cmd_domains(args):
    """List all available skill domains."""
    with console.status("[bold green]Fetching domains from JihedAiLabs..."):
        contents = fetch_contents("")
    
    table = Table(title="Available Engineering Domains")
    table.add_column("Domain", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    
    count = 0
    for item in contents:
        if item['type'] == 'dir':
            table.add_row(item['name'], "Domain")
            count += 1
            
    if count == 0:
        console.print("[yellow]No domains found.[/yellow]")
    else:
        console.print(table)
        console.print(f"Use [bold cyan]jihed-skills list <domain>[/bold cyan] to see available skills.")

def cmd_list(args):
    """List skills within a specific domain."""
    with console.status(f"[bold green]Fetching skills in {args.domain}..."):
        contents = fetch_contents(args.domain)
        
    table = Table(title=f"Skills in {args.domain}")
    table.add_column("Skill Name", style="cyan", no_wrap=True)
    
    count = 0
    for item in contents:
        if item['type'] == 'dir':
            table.add_row(item['name'])
            count += 1
            
    if count == 0:
        console.print(f"[yellow]No skills found in '{args.domain}'.[/yellow]")
    else:
        console.print(table)
        console.print(f"Use [bold cyan]jihed-skills read {args.domain}/{item['name']}[/bold cyan] to view the skill.")

def cmd_read(args):
    """Read the SKILL.md of a specific skill."""
    # Assuming user inputs domain/skill_name
    parts = args.path.split('/')
    if len(parts) < 2:
        console.print("[bold red]Error:[/bold red] Path must be in format <domain>/<skill_name>")
        sys.exit(1)
        
    path = f"{args.path}/SKILL.md"
    
    with console.status(f"[bold green]Downloading {args.path}..."):
        content = fetch_raw_skill(path)
        
    if not content:
        console.print(f"[bold red]Skill not found:[/bold red] {args.path}/SKILL.md")
        sys.exit(1)
        
    md = Markdown(content)
    console.print(Panel.fit("JihedAiLabs Agent-Ready Skill", border_style="green"))
    console.print(md)

def main():
    parser = argparse.ArgumentParser(
        description="JihedAiLabs CLI - Search and discover production-grade AI & Engineering skills.",
        epilog="Architected for the autonomous enterprise."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Subcommand: domains
    parser_domains = subparsers.add_parser("domains", help="List all available skill domains.")
    parser_domains.set_defaults(func=cmd_domains)
    
    # Subcommand: list
    parser_list = subparsers.add_parser("list", help="List skills in a specific domain.")
    parser_list.add_argument("domain", help="The domain name (e.g., '16-ai-platforms')")
    parser_list.set_defaults(func=cmd_list)
    
    # Subcommand: read
    parser_read = subparsers.add_parser("read", help="Read a specific skill's documentation.")
    parser_read.add_argument("path", help="The skill path (e.g., '16-ai-platforms/openai-spring-sdk')")
    parser_read.set_defaults(func=cmd_read)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
