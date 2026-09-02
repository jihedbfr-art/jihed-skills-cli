# jihed-skills

<p align="center">
  <b>Read the <a href="https://github.com/jihedbfr-art/ai-skills">ai-skills</a> engineering skill library from the terminal.</b>
</p>

<p align="center">
  <a href="README.fr.md">🇫🇷 Lire en Français</a>
</p>

---

## What it does

Three commands, reading the library from GitHub at call time — so what prints is the current
version of a skill, not a copy vendored into this package.

```bash
jihed-skills domains                                              # what exists
jihed-skills list 05-mcp-protocol-and-tools                       # what's in a domain
jihed-skills read 05-mcp-protocol-and-tools/mcp-server-stdio-tool-schema
```

`read` pulls the YAML frontmatter out into a header — title, description, last update — and renders
the body as markdown, instead of printing the metadata block as a wall of text.

A domain may group its skills one level deeper. When `list` shows an entry that turns out not to be
a skill, list that entry too and read the full path.

## Install

Not published to PyPI. Install from source, `pipx` recommended so it lands on your PATH without
touching your environment:

```bash
git clone https://github.com/jihedbfr-art/jihed-skills-cli.git
cd jihed-skills-cli
pipx install .
```

## Note on rate limits

The GitHub API is used unauthenticated, which allows 60 requests per hour per IP. An empty result
is usually that limit rather than an empty library, and the tool says so instead of reporting
nothing found.

## See also

[`jihed-skills-mcp`](https://github.com/jihedbfr-art/jihed-skills-mcp) serves the same library to
agents over MCP. This one is for humans.

## License

MIT — see [LICENSE](LICENSE).
