from typing import Dict, Any, List, Optional
from models import Prova, Trial

prova_ativa: Optional[Dict[str, Any]] = None
respostas_alunos: Dict[str, Dict[int, str]] = {}

def registrar_nova_prova(prova: Prova):
    global prova_ativa
    prova_ativa = prova.model_dump()
    respostas_alunos.clear()

def obter_prova_ativa() -> Optional[Dict[str, Any]]:
    return prova_ativa

def registrar_respostas_aluno(trial: Trial):
    respostas_alunos[trial.nome] = trial.respostas
    return {"status": "ok"}

def obter_resultados() -> List[Dict[str, Any]]:
    if not prova_ativa: return []
    mapa_letras = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    resultados = []
    for nome, respostas in respostas_alunos.items():
        acertos = 0
        detalhes = []
        for i, q in enumerate(prova_ativa['questoes']):
            escolha = respostas.get(i + 1)
            letra_correta = mapa_letras[q['correta']]
            correto = (escolha == letra_correta)
            if correto: acertos += 1
            detalhes.append({"questao": i+1, "status": "acerto" if correto else "erro", "escolha": escolha, "gabarito": letra_correta})
        resultados.append({"nome": nome, "nota": float(acertos), "detalhes": detalhes})
    return resultados

def calcular_estatisticas_turma(resultados: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not resultados: return {"media": 0.0, "maior_nota": 0.0}
    notas = [r["nota"] for r in resultados]
    return {"media": sum(notas) / len(notas), "maior_nota": max(notas)}