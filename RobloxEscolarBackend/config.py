from typing import Dict

# Gabarito oficial: questão (int) -> alternativa correta (str)
GABARITO: Dict[int, str] = {
    1:  "A",
    2:  "C",
    3:  "B",
    4:  "A",
    5:  "C",
    6:  "C",
    7:  "D",
    8:  "B",
    9:  "C",
    10: "C",
}

TOTAL_QUESTOES: int = len(GABARITO)

# Banco de dados em memória.
# Estrutura: { "Nome do Aluno": { numero_questao: alternativa_escolhida, ... } }
respostas_alunos: Dict[str, Dict[int, str]] = {}
