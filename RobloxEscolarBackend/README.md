# 🎮 RobloxEscolarBackend

API FastAPI para registro e visualização de provas escolares.

## 🗂️ Estrutura do projeto

```
RobloxEscolarBackend/
├── main.py                  # Rotas FastAPI
├── models.py                # Modelo Pydantic Trial
├── services.py              # Funções de negócio
├── config.py                # Gabarito, constantes e banco em memória
├── templates/
│   └── show_all.html        # Template Jinja2 (HTML puro)
├── static/
│   ├── style.css            # Estilos (CSS puro)
│   └── show_all.js          # Interatividade (JS puro)
└── requirements.txt
```

## 🚀 Instalação e execução

### 1. Criar o ambiente virtual

Um ambiente virtual isola as dependências do projeto (FastAPI, Uvicorn, Jinja2, etc.) do Python global do sistema, evitando conflitos de versão entre projetos diferentes.

```bash
python -m venv venv
```

Isso cria uma pasta `venv/` dentro do projeto com um Python isolado.

### 2. Ativar o ambiente virtual

No Linux/macOS:
```bash
source venv/bin/activate
```

No Windows (Prompt de Comando — cmd.exe):
```cmd
venv\Scripts\activate.bat
```

No Windows (PowerShell):
```powershell
venv\Scripts\activate
```

Após ativar, o terminal exibirá `(venv)` no início da linha.

#### ⚠️ Erro de segurança no PowerShell (Windows)

Por padrão, o PowerShell bloqueia a execução de scripts `.ps1`, o que impede a ativação do venv. Se aparecer o erro `não pode ser carregado porque a execução de scripts foi desabilitada`, use uma das soluções abaixo:

**Opção A — Liberar somente para a sessão atual (mais seguro, não persiste)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

A liberação some quando o terminal é fechado, sem alterar nada permanentemente no sistema.

**Opção B — Liberar permanentemente para o seu usuário (recomendado para desenvolvimento)**

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Resolve de vez para o seu usuário sem precisar repetir o comando a cada sessão. Scripts locais rodam livremente; scripts baixados da internet ainda exigem assinatura digital.

**Opção C — Usar o Prompt de Comando (cmd.exe) no lugar do PowerShell**

O CMD não tem essa restrição. Basta abrir o cmd.exe e usar `venv\Scripts\activate.bat` conforme mostrado acima.

---

#### 📋 Referência: valores de `-Scope` e `-ExecutionPolicy`

O parâmetro `-Scope` define **onde** a política se aplica:

| Scope | Descrição |
|---|---|
| `Process` | Só a sessão atual do PowerShell. Some ao fechar o terminal. |
| `CurrentUser` | Apenas o seu usuário do Windows. Persiste entre sessões. Não exige administrador. |
| `LocalMachine` | Todos os usuários do computador. Persiste e exige administrador. |
| `UserPolicy` | Definida via Group Policy para o usuário (uso corporativo). |
| `MachinePolicy` | Definida via Group Policy para a máquina inteira. Maior precedência. |

O parâmetro `-ExecutionPolicy` define **o que** é permitido executar:

| Política | Descrição |
|---|---|
| `Restricted` | Padrão do Windows. Nenhum script é permitido. |
| `AllSigned` | Apenas scripts assinados por editor confiável. |
| `RemoteSigned` | Scripts locais livres; scripts baixados exigem assinatura. |
| `Unrestricted` | Executa tudo, mas exibe aviso para scripts baixados. |
| `Bypass` | Executa tudo sem bloqueios e sem avisos. |
| `Undefined` | Remove a política do escopo, herdando a do escopo superior. |

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o servidor

```bash
uvicorn main:app --reload
```

### 5. Desativar o ambiente virtual (quando terminar)

```bash
deactivate
```

---

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Resultados: http://localhost:8000/trials/show-all

---

## 📌 Endpoints

### `POST /trials`
Envia a **prova completa** de um aluno de uma só vez.

**Payload:**
```json
{
  "nome": "Maria Silva",
  "respostas": {
    "1": "A",
    "2": "B",
    "3": "C",
    "5": "A",
    "8": "D"
  }
}
```
- `nome`: string não vazia
- `respostas`: objeto `{ "numero_questao": "alternativa" }` — pode ter quantas questões quiser
- Alternativas aceitas: A, B, C, D ou E (maiúsculo ou minúsculo)
- Questões não enviadas ficam como **em branco** (valem 0)
- Reenviar o mesmo nome **sobrescreve** a prova anterior

**Resposta:**
```json
{
  "status": "ok",
  "mensagem": "Prova de 'Maria Silva' registrada com sucesso.",
  "questoes_respondidas": 5,
  "questoes_em_branco": 5
}
```

### `GET /trials/show-all`
Página HTML com:
- Estatísticas da turma (alunos, média, aprovados, reprovados, maior nota)
- Ranking por nota com medalhas 🥇🥈🥉
- Acertos, erros e nota colorida por aluno
- Barra de progresso visual
- Painel expansível com detalhe de cada questão (acerto ✅ / erro ❌ / em branco)

---

## 📝 Gabarito (edite em `config.py`)

| Q  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|----|---|---|---|---|---|---|---|---|---|----|
|    | A | C | B | D | A | C | B | A | D | C  |

---

## 💡 Exemplos com curl

```bash
# Aluno 1 — responde todas as questões
curl -X POST http://localhost:8000/trials \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Ana Costa",
    "respostas": {"1":"A","2":"C","3":"B","4":"D","5":"A","6":"C","7":"B","8":"A","9":"D","10":"C"}
  }'

# Aluno 2 — responde só algumas
curl -X POST http://localhost:8000/trials \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Mendes",
    "respostas": {"1":"B","3":"B","5":"A","7":"C"}
  }'

# Ver resultados
curl http://localhost:8000/trials/show-all
```
