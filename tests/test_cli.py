import argparse
import io
import unittest
from unittest.mock import patch

import httpx
from rich.console import Console
from jihed_skills_cli import cli


class CliContractTests(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        self.console = patch.object(cli, "console", Console(file=self.output, force_terminal=False))
        self.console.start()
        self.addCleanup(self.console.stop)

    def test_frontmatter_keeps_body_and_top_level_scalars(self):
        fields, body = cli.split_frontmatter("---\ntitle: 'A skill'\nupdated: 2026-10-21\ntags:\n  - demo\n---\n\n# Body\n")
        self.assertEqual(fields["title"], "A skill")
        self.assertEqual(fields["updated"], "2026-10-21")
        self.assertEqual(body, "# Body\n")

    def test_unclosed_frontmatter_is_preserved(self):
        text = "---\ntitle: sample\n# Body"
        self.assertEqual(cli.split_frontmatter(text), ({}, text))

    def test_plain_markdown_is_preserved(self):
        self.assertEqual(cli.split_frontmatter("# Body"), ({}, "# Body"))

    @patch.object(cli, "fetch_raw_skill", return_value="---\ntitle: Nested skill\n---\n# Content")
    def test_nested_read_fetches_exact_skill_path(self, fetch):
        cli.cmd_read(argparse.Namespace(path="/domain/group/skill/"))
        fetch.assert_called_once_with("domain/group/skill/SKILL.md")
        self.assertIn("Nested skill", self.output.getvalue())

    @patch.object(cli, "fetch_raw_skill")
    def test_incomplete_path_does_not_request_network(self, fetch):
        with self.assertRaises(SystemExit) as failure:
            cli.cmd_read(argparse.Namespace(path="domain"))
        self.assertEqual(failure.exception.code, 1)
        fetch.assert_not_called()

    @patch.object(cli.httpx, "get")
    def test_missing_raw_file_returns_empty(self, get):
        get.return_value = httpx.Response(404, request=httpx.Request("GET", "https://example.invalid/skill"))
        self.assertEqual(cli.fetch_raw_skill("domain/skill/SKILL.md"), "")

    @patch.object(cli.httpx, "get")
    def test_api_failure_exits_with_error(self, get):
        get.side_effect = httpx.ConnectError("synthetic offline error")
        with self.assertRaises(SystemExit) as failure:
            cli.fetch_contents("domain")
        self.assertEqual(failure.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
