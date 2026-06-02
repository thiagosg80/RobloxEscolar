from typing import Dict
from pydantic import BaseModel, field_validator, model_validator
from config import GABARITO


class Trial(BaseModel):
    """
    Representa a entrega completa de um aluno:
    um nome e um dicionário de { numero_questao: alternativa_escolhida }.

    Exemplo de payload:
    {
        "nome": "Maria Silva",
        "respostas": {
            "1": "A",
            "3": "B",
            "7": "C"
        }
    }
    """

    nome: str
    respostas: Dict[int, str]   # { numero_questao -> alternativa }

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("O nome do aluno não pode ser vazio.")
        return v

    @model_validator(mode="after")
    def validar_respostas(self) -> "Trial":
        questoes_invalidas = [q for q in self.respostas if q not in GABARITO]
        if questoes_invalidas:
            raise ValueError(
                f"Questões inválidas: {sorted(questoes_invalidas)}. "
                f"Questões aceitas: {sorted(GABARITO.keys())}"
            )

        alternativas_invalidas = {
            q: a
            for q, a in self.respostas.items()
            if a.strip().upper() not in ("A", "B", "C", "D", "E")
        }
        if alternativas_invalidas:
            raise ValueError(
                f"Alternativas inválidas: {alternativas_invalidas}. Use A, B, C, D ou E."
            )

        # Normaliza todas as alternativas para maiúsculo
        self.respostas = {q: a.strip().upper() for q, a in self.respostas.items()}
        return self
