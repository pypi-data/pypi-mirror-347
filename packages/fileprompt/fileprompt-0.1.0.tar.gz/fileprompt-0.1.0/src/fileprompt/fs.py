import os
import re
from pathlib import Path

from .models import TreeNode

# Hard-coded regex patterns for files *or* directories that should be
# ignored when building or flattening the tree.  Edit this list as needed.
EXCLUDE_PATTERNS: list[str] = [
    r"^__pycache__$",  # compiled byte-code folders
    r".*\.pyc$",  # compiled python files
    r".*~$",  # editor swap/backup files
    r"^\.git$",  # git repository
    r"^\.venv$",  # virtual environment
    r"^.*\.egg-info$",
]


def _matches_exclude(path: Path) -> bool:
    """Return True when *path* should be excluded according to
    ``EXCLUDE_PATTERNS``.
    The match is performed against the *basename* only (``path.name``)."""
    return any(re.match(pattern, path.name) for pattern in EXCLUDE_PATTERNS)


def estimate_tokens_text(text: str) -> int:
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4


def estimate_tokens(path: Path) -> int:
    try:
        text = path.read_text("utf-8", errors="ignore")
    except Exception:
        text = ""
    return estimate_tokens_text(text)


def build_tree(root: Path) -> TreeNode:
    """Recursively walk *root* and build a :class:`TreeNode` tree.

    Files or directories whose *basename* matches any pattern in
    ``EXCLUDE_PATTERNS`` are silently skipped, in addition to the existing
    rule that hides dot-prefixed names.
    """
    root = root.resolve()

    def _recurse(path: Path) -> TreeNode:
        stat = path.stat()

        # Skip files/dirs matching exclusion patterns *except* the *root* itself
        if path != root and _matches_exclude(path):
            # Treat excluded paths as a zero-sized, zero-token leaf so that the
            # parent directory's aggregate sizes are correct.
            return TreeNode(
                path=str(path),
                name=path.name,
                is_dir=path.is_dir(),
                size=0,
                tokens=0,
                mtime=stat.st_mtime,
                children=[] if path.is_dir() else None,
            )

        if path.is_dir():
            children_nodes: list[TreeNode] = []
            tokens_sum = 0
            size_sum = 0
            for entry in sorted(path.iterdir(), key=lambda p: p.name.lower()):
                # Skip dot-files and excluded patterns
                if entry.name.startswith(".") or _matches_exclude(entry):
                    continue
                node = _recurse(entry)
                # Nodes that returned zero size/tokens were fully excluded.
                if node.size == 0 and node.tokens == 0 and not node.children:
                    continue
                children_nodes.append(node)
                tokens_sum += node.tokens
                size_sum += node.size
            return TreeNode(
                path=str(path),
                name=path.name,
                is_dir=True,
                size=size_sum,
                tokens=tokens_sum,
                mtime=stat.st_mtime,
                children=children_nodes,
            )
        else:
            size = stat.st_size
            tokens = estimate_tokens(path)
            return TreeNode(
                path=str(path),
                name=path.name,
                is_dir=False,
                size=size,
                tokens=tokens,
                mtime=stat.st_mtime,
                children=None,
            )

    return _recurse(root)


def flatten_selected(root: Path, selected: list[str]) -> list[Path]:
    """Return *selected* paths flattened into individual files, respecting
    ``EXCLUDE_PATTERNS``.
    """
    unique: list[Path] = []
    seen: set[Path] = set()
    root = root.resolve()
    for s in selected:
        p = Path(s).resolve()
        if root not in p.parents and p != root:
            continue
        if _matches_exclude(p):
            continue
        if p.is_dir():
            for dirpath, _dirnames, filenames in os.walk(p):
                dirpath_p = Path(dirpath)
                if _matches_exclude(dirpath_p):
                    # Skip whole directory tree if the directory itself is excluded
                    _dirnames[:] = []  # don't descend further
                    continue
                for fn in filenames:
                    fp = Path(dirpath) / fn
                    if _matches_exclude(fp):
                        continue
                    if fp not in seen:
                        unique.append(fp)
                        seen.add(fp)
        else:
            if p not in seen:
                unique.append(p)
                seen.add(p)
    return unique


def ascii_tree(paths: list[Path], root: Path) -> str:
    """Return a compact ASCII tree of *paths* relative to *root*.

    Consecutive entries that share directory prefixes are only shown once,
    giving an output similar to the Unix ``tree`` utility.
    """
    rel_paths = sorted(p.relative_to(root) for p in paths)

    lines: list[str] = []
    prev_parts: list[str] = []

    for rp in rel_paths:
        parts = list(rp.parts)

        # length of the common prefix with the previous path
        common = 0
        for a, b in zip(parts, prev_parts):
            if a == b:
                common += 1
            else:
                break

        indent = "    " * common
        for i, part in enumerate(parts[common:], start=common):
            is_last_component = i == len(parts) - 1
            connector = "└── " if is_last_component else "├── "
            lines.append(f"{indent}{connector}{part}")
            indent += "    "
        prev_parts = parts

    return "\n".join(lines)
