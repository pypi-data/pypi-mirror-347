from importlib import resources
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="Repo Prompt")


templates_dir = resources.files(__name__).joinpath("templates")
templates = Jinja2Templates(directory=str(templates_dir))
