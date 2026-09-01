# JihedAiLabs Skills CLI (`jihed-skills`)

<p align="center">
  <b>The command-line distribution system for JihedAiLabs engineering skills.</b>
</p>

## Overview

As defined in the **JihedAiLabs Top 10 World Strategy**, the `ai-skills` repository is not just a Markdown library; it is a developer tool ecosystem. This CLI allows human developers to rapidly search, list, and read production-grade engineering patterns from the terminal.

It parses the `ai-skills` repository in real-time.

## Installation

You can install this tool globally using `pipx` (recommended):

```bash
git clone https://github.com/jihedbfr-art/jihed-skills-cli.git
cd jihed-skills-cli
pipx install .
```

## Usage

List all top-level engineering domains:
```bash
jihed-skills domains
```

List specific skills within a domain:
```bash
jihed-skills list 16-ai-platforms
```

Read and inject a skill directly into your terminal (renders Markdown beautifully via `Rich`):
```bash
jihed-skills read 16-ai-platforms/openai-spring-sdk
```

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*
