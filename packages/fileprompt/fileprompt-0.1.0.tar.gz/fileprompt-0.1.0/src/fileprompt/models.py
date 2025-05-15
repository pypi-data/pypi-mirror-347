from __future__ import annotations

from pydantic import BaseModel


class TreeNode(BaseModel):
    path: str
    name: str
    is_dir: bool
    size: int
    tokens: int
    mtime: float
    children: list[TreeNode] | None = None


class CopyRequest(BaseModel):
    root: str
    selected: list[str]
    instructions: str


class CopyResponse(BaseModel):
    payload: str
    char_count: int
    token_count: int
