from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from consistency import run_consistency_checks


def _write_root_governance(root: Path) -> None:
    context_dir = root / ".context"
    context_dir.mkdir()
    (context_dir / "MILESTONES.md").write_text(
        "# Milestones\n\nCurrent: M1 - Program Milestone\n",
        encoding="utf-8",
    )
    (context_dir / "TENSIONS_OPEN.md").write_text(
        "# Tensions - OPEN\n",
        encoding="utf-8",
    )


class TestMonorepoGovernanceConsistency(unittest.TestCase):
    def test_errors_on_nested_context_milestones(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_root_governance(root)
            nested = root / "plugins" / "lab" / ".context"
            nested.mkdir(parents=True)
            (nested / "MILESTONES.md").write_text(
                "# Local Milestones\n\nCurrent: Lab Local\n",
                encoding="utf-8",
            )

            errors, warnings = run_consistency_checks(root)

            self.assertEqual(warnings, [])
            self.assertTrue(any("Nested governance milestone files" in e for e in errors))
            self.assertTrue(any("plugins/lab/.context/MILESTONES.md" in e for e in errors))

    def test_errors_on_nested_context_tension_files(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_root_governance(root)
            nested = root / "apps" / "web" / ".context"
            nested.mkdir(parents=True)
            (nested / "TENSIONS_OPEN.md").write_text(
                "# Local Tensions\n",
                encoding="utf-8",
            )

            errors, warnings = run_consistency_checks(root)

            self.assertEqual(warnings, [])
            self.assertTrue(any("Nested governance tension files" in e for e in errors))
            self.assertTrue(any("apps/web/.context/TENSIONS_OPEN.md" in e for e in errors))

    def test_warns_on_plugin_local_milestones_file(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_root_governance(root)
            nested = root / "packages" / "api"
            nested.mkdir(parents=True)
            (nested / "MILESTONES.md").write_text(
                "# Package Milestones\n",
                encoding="utf-8",
            )

            errors, warnings = run_consistency_checks(root)

            self.assertEqual(errors, [])
            self.assertTrue(any("Nested local milestone files" in w for w in warnings))
            self.assertTrue(any("packages/api/MILESTONES.md" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
