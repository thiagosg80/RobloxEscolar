from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import TOTAL_QUESTOES
from models import Trial
from services import (
    registrar_prova,
    obter_todos_resultados,
    calcular_estatisticas_turma,
)

app = FastAPI(title="RobloxEscolarBackend", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/trials", summary="Registrar prova completa de um aluno")
def post_trial(trial: Trial):
    return registrar_prova(trial)


@app.get("/trials/show-all", response_class=HTMLResponse, summary="Exibir resultados de todos os alunos")
def show_all(request: Request):
    resultados  = obter_todos_resultados()
    estatisticas = calcular_estatisticas_turma(resultados)

    return templates.TemplateResponse(
        request=request,
        name="show_all.html",
        context={
            "resultados":    resultados,
            "total_alunos":  len(resultados),
            "total_questoes": TOTAL_QUESTOES,
            "stats":         estatisticas,
        },
    )
