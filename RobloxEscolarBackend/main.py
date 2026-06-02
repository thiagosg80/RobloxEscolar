from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Prova, Trial
from services import (
    registrar_nova_prova, registrar_respostas_aluno, obter_resultados, 
    calcular_estatisticas_turma, obter_prova_ativa
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/prova/criar")
def criar_prova(prova: Prova):
    registrar_nova_prova(prova)
    return {"status": "ok"}

@app.post("/trials")
def post_trial(trial: Trial):
    return registrar_respostas_aluno(trial)

@app.get("/prova/nova", response_class=HTMLResponse)
def get_form_prova(request: Request):
    return templates.TemplateResponse(request=request, name="form_prova.html")

@app.get("/prova/editar", response_class=HTMLResponse)
def editar_prova_get(request: Request):
    return templates.TemplateResponse(request=request, name="form_prova.html", context={"prova": obter_prova_ativa()})

@app.get("/trials/show-all", response_class=HTMLResponse)
def show_all(request: Request):
    resultados = obter_resultados()
    return templates.TemplateResponse(
        request=request,
        name="show_all.html", 
        context={
            "resultados": resultados, 
            "total_alunos": len(resultados),
            "total_questoes": 10,
            "stats": calcular_estatisticas_turma(resultados)
        }
    )