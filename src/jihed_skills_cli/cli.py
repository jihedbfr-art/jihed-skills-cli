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

def split_frontmatter(content: str):
    """Splits a SKILL.md into its frontmatter fields and its body.

    Rendering the raw file collapses the YAML block into an unreadable paragraph, so the
    metadata is pulled out and shown as a header instead. Only top-level scalar keys are read
    - enough for the header, and no YAML dependency for a tool that just prints documents.
    """
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    block, body = content[3:end], content[end + 4:]
    fields = {}
    for line in block.splitlines():
        if line.startswith((" ", "-")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, body.lstrip("\n")


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
        console.print(
            "[yellow]No domains returned.[/yellow] The GitHub API is used unauthenticated here "
            "(60 requests per hour per IP), so this is usually a rate limit."
        )
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
        console.print(f"[yellow]Nothing found under '{args.domain}'.[/yellow]")
    else:
        console.print(table)
        console.print(
            f"Use [bold cyan]jihed-skills read {args.domain}/<name>[/bold cyan] to view one. "
            "A domain may group its skills one level deeper, in which case list that entry too."
        )

def cmd_read(args):
    """Read the SKILL.md of a specific skill."""
    clean = args.path.strip("/")
    if "/" not in clean:
        console.print(
            "[bold red]Error:[/bold red] path must be <domain>/<skill>, "
            "or deeper if the domain nests its skills."
        )
        sys.exit(1)

    path = f"{clean}/SKILL.md"
    
    with console.status(f"[bold green]Downloading {clean}..."):
        content = fetch_raw_skill(path)
        
    if not content:
        console.print(f"[bold red]No SKILL.md at:[/bold red] {clean}")
        sys.exit(1)
        
    fields, body = split_frontmatter(content)
    title = fields.get("title") or fields.get("name") or clean
    header = f"[bold]{title}[/bold]"
    if fields.get("description"):
        header += f"\n{fields['description']}"
    if fields.get("updated"):
        header += f"\n[dim]updated {fields['updated']}[/dim]"

    console.print(Panel.fit(header, border_style="green"))
    console.print(Markdown(body))

def main():
    parser = argparse.ArgumentParser(
        description="Read the ai-skills engineering skill library from the terminal."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Subcommand: domains
    parser_domains = subparsers.add_parser("domains", help="List all available skill domains.")
    parser_domains.set_defaults(func=cmd_domains)
    
    # Subcommand: list
    parser_list = subparsers.add_parser("list", help="List skills in a specific domain.")
    parser_list.add_argument("domain", help="Domain name, e.g. '05-mcp-protocol-and-tools'")
    parser_list.set_defaults(func=cmd_list)
    
    # Subcommand: read
    parser_read = subparsers.add_parser("read", help="Read a specific skill's documentation.")
    parser_read.add_argument(
        "path",
        help="Skill path, e.g. '05-mcp-protocol-and-tools/mcp-server-stdio-tool-schema'",
    )
    parser_read.set_defaults(func=cmd_read)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
