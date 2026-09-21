"""Exercise the public CLI and portability boundaries without opening a browser."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "skills/implementation-progress/scripts/progress.py"
spec = importlib.util.spec_from_file_location("progress", SCRIPT)
progress = importlib.util.module_from_spec(spec)
spec.loader.exec_module(progress)


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="progress test ")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / "panel ü"

    def cli(self, command, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), command, "--dir", str(self.directory), *args],
            capture_output=True, text=True, encoding="utf-8",
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
        return result

    def init(self):
        self.cli("init", "--title", "Feature ü 🚀", "--phase", "Plan::Explore",
                 "--phase", "Build", "--now", "Starting")

    def state(self):
        return json.loads((self.directory / "progress.json").read_text(encoding="utf-8"))

    def test_full_workflow_and_serialization(self):
        self.init()
        self.assertEqual([p["state"] for p in self.state()["phases"]], ["active", "pending"])
        self.cli("phase", "1", "done")
        self.cli("step", "bu", "Handle ü", "active")
        self.assertEqual(self.state()["phases"][1]["state"], "active")
        self.cli("step", "2", "HANDLE Ü", "done")
        self.cli("step", "2", "Credentials", "blocked")
        self.cli("phase", "2", "done", "--detail", "Waiting on credentials")
        steps = self.state()["phases"][1]["steps"]
        self.assertEqual([s["state"] for s in steps], ["done", "blocked"])
        activity = 'Checking "quotes", </script>, and Unicode: ü 🚀\u2028'
        self.cli("now", activity)
        data = self.state()
        self.assertEqual(data["now"], activity)
        self.assertIn("updated", data)
        js = (self.directory / "progress.js").read_text(encoding="utf-8")
        prefix = "window.IMPLEMENTATION_PROGRESS = "
        self.assertTrue(js.startswith(prefix))
        self.assertEqual(json.loads(js[len(prefix):-2]), data)
        self.assertIn("Feature ü 🚀", self.cli("show").stdout)
        self.assertIn("IMPLEMENTATION_PROGRESS", (self.directory / "index.html").read_text())
        self.assertEqual({p.name for p in self.directory.iterdir()},
                         {"index.html", "progress.json", "progress.js"})

    def test_existing_panel_requires_explicit_reset(self):
        self.init()
        before = self.state()
        self.cli("init", "--title", "Replacement", "--phase", "New", success=False)
        self.assertEqual(before, self.state())
        self.cli("init", "--force", "--title", "Replacement", "--phase", "New")
        self.assertEqual(self.state()["title"], "Replacement")

    def test_invalid_commands_do_not_modify_progress(self):
        self.init()
        before = self.state()
        for args in [("phase", "0", "done"), ("phase", "missing", "done"),
                     ("phase", "1", "invalid"), ("step", "2", "New", "invalid")]:
            self.cli(*args, success=False)
            self.assertEqual(before, self.state())

    def test_missing_panel_and_invalid_init(self):
        for command in ("show", "open"):
            self.assertIn("run init", self.cli(command, success=False).stderr)
        self.cli("init", "--title", "Missing phases", success=False)
        self.cli("init", "--title", "Empty phase", "--phase", " ::detail", success=False)
        self.assertFalse(self.directory.exists())

    def test_ambiguous_prefix(self):
        self.cli("init", "--title", "Test", "--phase", "Build API", "--phase", "Build UI")
        self.assertIn("matched 2 phases", self.cli("phase", "Build", "done", success=False).stderr)

    def test_directory_defaults_and_precedence(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(tempfile, "gettempdir", return_value=self.temp.name):
            with patch.object(Path, "cwd", return_value=Path(self.temp.name) / "one/project"):
                first = progress.default_dir()
                self.assertEqual(first, progress.default_dir())
            with patch.object(Path, "cwd", return_value=Path(self.temp.name) / "two/project"):
                second = progress.default_dir()
            self.assertNotEqual(first, second)
            self.assertEqual(Path(first).parent, Path(self.temp.name) / "implementation-progress")
        with patch.dict(os.environ, {"PROGRESS_DIR": str(self.directory / "unused")}):
            self.assertEqual(progress.default_dir(), str(self.directory / "unused"))
            self.init()  # Explicit --dir takes priority over the inherited variable.
            self.assertFalse((self.directory / "unused").exists())
            result = subprocess.run([sys.executable, str(SCRIPT), "show"],
                                    env={**os.environ, "PROGRESS_DIR": str(self.directory)},
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_browser_uri_and_headless_fallback(self):
        self.init()
        args = SimpleNamespace(dir=str(self.directory))
        with patch.object(progress.webbrowser, "open", return_value=True) as launch:
            progress.cmd_open(args)
            launch.assert_called_once_with((self.directory / "index.html").resolve().as_uri())
        for behavior in ({"return_value": False}, {"side_effect": OSError("no browser")}):
            with patch.object(progress.webbrowser, "open", **behavior), contextlib.redirect_stderr(io.StringIO()) as errors:
                progress.cmd_open(args)
            self.assertIn("Open this file manually: file://", errors.getvalue())

    def test_failed_atomic_replace_preserves_previous_file(self):
        self.init()
        path = self.directory / "progress.json"
        original = path.read_bytes()
        with patch.object(progress.os, "replace", side_effect=OSError("cannot replace")):
            with self.assertRaises(OSError):
                progress.atomic_write(path, "new state")
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(len(list(self.directory.iterdir())), 3)


if __name__ == "__main__":
    unittest.main()
