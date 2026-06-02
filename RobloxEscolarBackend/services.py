from typing import Dict, Any, List, Optional
from models import Prova, Trial

prova_ativa: Optional[Dict[str, Any]] = None
respostas_alunos: Dict[str, Dict[int, str]] = {}

from typing import Dict, Any, List, Optional
from models import Prova

def carregar_prova_padrao():
    global prova_ativa
    # Criação da estrutura da prova de nível fácil
    dados_padrao = {
        "nome_prova": "Conhecimentos Gerais - Nível Fácil",
        "questoes": [
            {"enunciado": "Quanto é 2 + 2?", "alternativas": ["3", "4", "5", "6", "7"], "correta": 1},
            {"enunciado": "Qual a capital da França?", "alternativas": ["Londres", "Berlim", "Paris", "Madri", "Roma"], "correta": 2},
            {"enunciado": "Como se diz 'olá' em inglês?", "alternativas": ["Goodbye", "Hello", "Thanks", "Please", "Sorry"], "correta": 1},
            {"enunciado": "Qual a maior floresta tropical do mundo?", "alternativas": ["Mata Atlântica", "Taiga", "Amazônia", "Congo", "Valdiviana"], "correta": 2},
            {"enunciado": "Qual a raiz quadrada de 9?", "alternativas": ["1", "2", "3", "4", "5"], "correta": 2},
            {"enunciado": "Qual destes é um substantivo?", "alternativas": ["Correr", "Bonito", "Casa", "Rapidamente", "Muito"], "correta": 2},
            {"enunciado": "Em qual continente fica o Brasil?", "alternativas": ["Europa", "Ásia", "África", "América do Sul", "Oceania"], "correta": 3},
            {"enunciado": "Qual a tradução de 'Apple'?", "alternativas": ["Banana", "Uva", "Maçã", "Pera", "Laranja"], "correta": 2},
            {"enunciado": "Quem escreveu Dom Casmurro?", "alternativas": ["Machado de Assis", "Clarice Lispector", "Monteiro Lobato", "Jorge Amado", "Drummond"], "correta": 0},
            {"enunciado": "Qual o resultado de 10 dividido por 2?", "alternativas": ["2", "4", "5", "6", "8"], "correta": 2}
        ]
    }
    prova_ativa = dados_padrao

# Chama a função ao carregar o módulo
carregar_prova_padrao()

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