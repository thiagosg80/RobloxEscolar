from typing import List, Dict
from pydantic import BaseModel, model_validator

class Questao(BaseModel):
    enunciado: str
    alternativas: List[str]  # Lista com 5 enunciados de alternativas
    correta: int             # Índice da alternativa correta (0 a 4)

    @model_validator(mode="after")
    def validar_estrutura(self) -> "Questao":
        if len(self.alternativas) != 5:
            raise ValueError("Cada questão deve ter exatamente 5 alternativas.")
        if not (0 <= self.correta <= 4):
            raise ValueError("A alternativa correta deve ser um índice entre 0 e 4.")
        return self

class Prova(BaseModel):
    nome_prova: str
    questoes: List[Questao]

    @model_validator(mode="after")
    def validar_total(self) -> "Prova":
        if len(self.questoes) != 10:
            raise ValueError("A prova deve ter exatamente 10 questões.")
        return self

class Trial(BaseModel):
    nome: str
    respostas: Dict[int, str] # {1: "A", 2: "B"...} mapeado para o índice da alternativa