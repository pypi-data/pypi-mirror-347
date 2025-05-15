from pathlib import Path

from .fs import ascii_tree, estimate_tokens


def assemble(root: Path, files: list[Path], instructions: str) -> tuple[str, int]:
    tree_block = f"<file_map>\n{ascii_tree(files, root)}\n</file_map>\n"
    parts = [tree_block]
    token_total = 0
    for p in files:
        try:
            txt = p.read_text("utf-8", errors="replace")
        except Exception:
            txt = ""
        token_total += estimate_tokens(p)
        parts.append(f'<file_contents filename="{p}">\n{txt}\n</file_contents>\n')
    parts.append(f"<user_instructions>\n{instructions}\n</user_instructions>\n")
    payload = "".join(parts)
    return payload, token_total
