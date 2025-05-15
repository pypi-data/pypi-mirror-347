import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi import HTTPException, Request, status
from fastapi.responses import HTMLResponse

from . import app, templates
from .fs import build_tree, flatten_selected
from .models import CopyRequest, CopyResponse, TreeNode
from .payload import assemble

executor = ThreadPoolExecutor()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/tree", response_model=TreeNode)
async def api_tree(root: str = "."):
    root_path = Path(root).expanduser().resolve()
    loop = asyncio.get_event_loop()
    tree_node = await loop.run_in_executor(executor, build_tree, root_path)
    return tree_node


@app.post("/api/copy", response_model=CopyResponse)
async def api_copy(req: CopyRequest):
    root_path = Path(req.root).expanduser().resolve()
    loop = asyncio.get_event_loop()
    files: list[Path] = await loop.run_in_executor(executor, flatten_selected, root_path, req.selected)
    if not files:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No files selected")
    payload, token_total = await loop.run_in_executor(executor, assemble, root_path, files, req.instructions)
    return CopyResponse(payload=payload, char_count=len(payload), token_count=token_total)
