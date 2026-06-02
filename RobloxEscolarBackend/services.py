from typing import Dict, Any
from config import GABARITO, TOTAL_QUESTOES, respostas_alunos
from models import Trial


def registrar_prova(trial: Trial) -> Dict[str, Any]:
    """
    Substitui (ou cria) o conjunto de respostas de um aluno em memória.
    Cada chamada com o mesmo nome sobrescreve a entrega anterior.
    """
    respostas_alunos[trial.nome] = dict(trial.respostas)

    return {
        "status": "ok",
        "mensagem": f"Prova de '{trial.nome}' registrada com sucesso.",
        "questoes_respondidas": len(trial.respostas),
        "questoes_em_branco": TOTAL_QUESTOES - len(trial.respostas),
    }


def calcular_resultado(nome: str) -> Dict[str, Any]:
    """Computa acertos, erros e nota de um aluno com base no gabarito."""
    respostas = respostas_alunos.get(nome, {})
    acertos = 0
    erros = 0
    detalhes = []

    for questao in sorted(GABARITO.keys()):
        gabarito = GABARITO[questao]
        if questao in respostas:
            escolha = respostas[questao]
            correto = escolha == gabarito
            acertos += int(correto)
            erros   += int(not correto)
            detalhes.append({
                "questao":  questao,
                "escolha":  escolha,
                "gabarito": gabarito,
                "correto":  correto,
                "status":   "acerto" if correto else "erro",
            })
        else:
            detalhes.append({
                "questao":  questao,
                "escolha":  None,
                "gabarito": gabarito,
                "correto":  False,
                "status":   "em_branco",
            })

    nota = round((acertos / TOTAL_QUESTOES) * 10, 1)

    return {
        "nome":            nome,
        "acertos":         acertos,
        "erros":           erros,
        "respondidas":     len(respostas),
        "em_branco":       TOTAL_QUESTOES - len(respostas),
        "nota":            nota,
        "situacao":        "Aprovado" if nota >= 5 else "Reprovado",
        "detalhes":        detalhes,
    }


def obter_todos_resultados() -> list[Dict[str, Any]]:
    """Retorna resultados de todos os alunos, ordenados por nota (maior primeiro)."""
    resultados = [calcular_resultado(nome) for nome in respostas_alunos]
    resultados.sort(key=lambda r: r["nota"], reverse=True)
    return resultados


def calcular_estatisticas_turma(resultados: list[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula estatísticas gerais da turma."""
    if not resultados:
        return {"media": 0.0, "aprovados": 0, "reprovados": 0, "maior_nota": 0.0, "menor_nota": 0.0}

    notas = [r["nota"] for r in resultados]
    aprovados = sum(1 for n in notas if n >= 5)

    return {
        "media":      round(sum(notas) / len(notas), 1),
        "aprovados":  aprovados,
        "reprovados": len(resultados) - aprovados,
        "maior_nota": max(notas),
        "menor_nota": min(notas),
    }
