from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_TOP_LEVEL = {
    ".github",
    ".gitignore",
    "NOTICE.md",
    "README.md",
    "assets",
    "docs",
    "tests",
}

ALLOWED_FILES = {
    ".github/workflows/public-boundary.yml",
    ".gitignore",
    "NOTICE.md",
    "README.md",
    "assets/motor-imagery-boxing-preview.png",
    "assets/system-overview.svg",
    "docs/DISCLOSURE_BOUNDARY.md",
    "tests/test_public_boundary.py",
}

PROHIBITED_SUFFIXES = {
    ".bdf",
    ".csv",
    ".docx",
    ".edf",
    ".eeg",
    ".fif",
    ".gz",
    ".h5",
    ".hdf5",
    ".joblib",
    ".json",
    ".jsonl",
    ".mat",
    ".npy",
    ".npz",
    ".pdf",
    ".pickle",
    ".pkl",
    ".set",
    ".tar",
    ".tsv",
    ".vhdr",
    ".vmrk",
    ".zip",
}

TEXT_SUFFIXES = {".css", ".html", ".js", ".md", ".py", ".svg", ".txt", ".yml", ".yaml"}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTML_RESOURCE = re.compile(r"(?:src|href)=\"([^\"]+)\"")

PRIVATE_DISCLOSURE_PATTERNS = {
    "macOS user path": re.compile(r"/Users/[^/\s]+/"),
    "OneDrive path": re.compile(r"OneDrive", re.IGNORECASE),
    "known private p value": re.compile(r"0\.001953"),
    "known private effect value": re.compile(r"0\.0675"),
    "known private result pair": re.compile(r"31\.2%.*38\.0%"),
    "live participant label": re.compile(r"Live recording B\d+", re.IGNORECASE),
}


class PublicBoundaryTests(unittest.TestCase):
    def test_only_approved_top_level_paths_exist(self) -> None:
        found = {path.name for path in ROOT.iterdir() if path.name != ".git"}
        self.assertEqual(set(), found - ALLOWED_TOP_LEVEL)

    def test_only_approved_public_files_exist(self) -> None:
        found = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.relative_to(ROOT).parts
            and "__pycache__" not in path.relative_to(ROOT).parts
        }
        self.assertEqual(ALLOWED_FILES, found)

    def test_research_and_participant_file_types_are_absent(self) -> None:
        found = [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*")
            if path.is_file() and path.suffix.lower() in PROHIBITED_SUFFIXES
        ]
        self.assertEqual([], found)

    def test_known_private_details_are_absent(self) -> None:
        findings: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for label, pattern in PRIVATE_DISCLOSURE_PATTERNS.items():
                if pattern.search(text):
                    findings.append(f"{path.relative_to(ROOT)}: {label}")
        self.assertEqual([], findings)

    def test_no_large_files(self) -> None:
        limit = 5 * 1024 * 1024
        found = [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*")
            if path.is_file() and path.stat().st_size > limit
        ]
        self.assertEqual([], found)

    def test_local_markdown_links_resolve(self) -> None:
        missing: list[str] = []
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for raw_target in MARKDOWN_LINK.findall(text):
                target = raw_target.strip().split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (path.parent / target).resolve().exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {raw_target}")
        self.assertEqual([], missing)

    def test_local_html_resources_resolve(self) -> None:
        missing: list[str] = []
        for path in [*ROOT.rglob("*.html"), *ROOT.rglob("*.md")]:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for raw_target in HTML_RESOURCE.findall(text):
                target = raw_target.strip().split("#", 1)[0]
                if not target or target.startswith(("data:", "http://", "https://", "mailto:")):
                    continue
                if not (path.parent / target).resolve().exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {raw_target}")
        self.assertEqual([], missing)

    def test_no_runnable_public_demo(self) -> None:
        self.assertFalse((ROOT / "demo").exists())

    def test_actual_interface_screenshot_is_present(self) -> None:
        screenshot = ROOT / "assets" / "motor-imagery-boxing-preview.png"
        self.assertTrue(screenshot.is_file())
        self.assertGreater(screenshot.stat().st_size, 50_000)
        self.assertEqual(b"\x89PNG\r\n\x1a\n", screenshot.read_bytes()[:8])


if __name__ == "__main__":
    unittest.main()
