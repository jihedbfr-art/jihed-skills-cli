# jihed-skills

<p align="center">
  <b>Lire la bibliothèque <a href="https://github.com/jihedbfr-art/ai-skills">ai-skills</a> depuis le terminal.</b>
</p>

<p align="center">
  <a href="README.md">🇬🇧 Read in English</a>
</p>

---

## Ce que ça fait

Trois commandes, qui lisent la bibliothèque sur GitHub au moment de l'appel — ce qui s'affiche est
donc la version courante d'un skill, pas une copie figée dans le paquet.

```bash
jihed-skills domains                                              # ce qui existe
jihed-skills list 05-mcp-protocol-and-tools                       # le contenu d'un domaine
jihed-skills read 05-mcp-protocol-and-tools/mcp-server-stdio-tool-schema
```

`read` extrait le frontmatter YAML dans un en-tête — titre, description, date de mise à jour — et
rend le corps en markdown, au lieu d'imprimer le bloc de métadonnées en pavé illisible.

Un domaine peut regrouper ses skills un niveau plus bas. Quand `list` affiche une entrée qui n'est
pas un skill, lister cette entrée à son tour et lire le chemin complet.

## Installation

Pas publié sur PyPI. Installation depuis les sources, `pipx` recommandé pour l'avoir dans le PATH
sans toucher à l'environnement :

```bash
git clone https://github.com/jihedbfr-art/jihed-skills-cli.git
cd jihed-skills-cli
pipx install .
```

## À propos des limites de débit

L'API GitHub est utilisée sans authentification, soit 60 requêtes par heure et par IP. Un résultat
vide vient généralement de cette limite, pas d'une bibliothèque vide — l'outil le dit plutôt que
d'annoncer « rien trouvé ».

## Voir aussi

[`jihed-skills-mcp`](https://github.com/jihedbfr-art/jihed-skills-mcp) sert la même bibliothèque
aux agents via MCP. Celui-ci est pour les humains.

## Licence

MIT — voir [LICENSE](LICENSE).

## Validation

Le build déclare explicitement `src/jihed_skills_cli` : le nom du paquet distribué, `jihed-skills`, diffère de celui du module. La CI construit l’archive source et le wheel, installe le wheel et exécute sept tests hors réseau sur Ubuntu/Windows avec Python 3.9 et 3.12. Les appels HTTP des tests sont simulés ; ils ne prouvent pas la disponibilité de GitHub.

```bash
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
python -m unittest discover -s tests
```

---

<div align="center">
  <img src="https://raw.githubusercontent.com/jihedbfr-art/jihedbfr-art/main/assets/brand/jihedailabs-logo.svg" alt="JihedAiLabs" width="120"/>
  <br/>
  <sub>Un projet <a href="https://github.com/jihedbfr-art"><b>JihedAiLabs</b></a></sub>
</div>
