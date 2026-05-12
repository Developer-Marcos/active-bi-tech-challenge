# Analisador de Documentos com IA (Active BI)
###### Projeto desenvolvido como parte do **Desafio Técnico** para a vaga de estágio na **Active BI**.
Este projeto é uma ferramenta de linha de comando (CLI) desenvolvida para permitir que usuários realizem perguntas em linguagem natural sobre relatórios em PDF, obtendo respostas estruturadas e formatadas automaticamente via Inteligência Artificial.

### Arquitetura e Decisões Técnicas:
A aplicação foi construída focando em **escalabilidade**, **manutenibilidade** e **robustez**, seguindo princípios de separação de responsabilidades **(SOLID)**.

---

### Estrutura de Módulos:
- **`main.py`**: O orquestrador da pipeline e interface de linha de comando (CLI) desenvolvida com a biblioteca `argparse`.
- **`src/data_extractor.py`**: Módulo especializado na extração de texto de arquivos PDF utilizando `PyPDFLoader` (`langchain-community`).
- **`src/llm_service.py`**: Serviço responsável pela comunicação com a API da OpenAI, processamento do prompt e validação da saída estruturada.
- **`prompt.xml`**: Centralização da engenharia de prompt utilizando tags XML, persona de Analista de BI Sênior e técnica de *few-shot prompting*.
  
---

### Garantia de Estrutura (Pydantic):
Para cumprir o requisito obrigatório de saída em **JSON puro**, o projeto utiliza **Pydantic** integrado ao método `.with_structured_output()` do LangChain. 

Isso elimina o risco de "alucinações" de texto fora do objeto JSON e garante que o campo `suggestions` tenha sempre exatamente 3 itens, conforme exigido.

---

### Justificativa do Modelo *(GPT-4o-mini)*:
A escolha do modelo **`gpt-4o-mini`** foi estratégica para o cenário de Business Intelligence:
1. **Eficiência de Custo:** É significativamente mais barato que modelos como o GPT-4o original, mantendo uma alta performance para tarefas de extração.
2. **Janela de Contexto (128k):** Permite o processamento de documentos extensos sem a necessidade imediata de arquiteturas de RAG (Vector DBs) complexas para esta primeira versão.
3. **Structured Outputs:** Suporte nativo para garantir que a resposta seja estritamente o JSON solicitado.

---

### Estimativa de Custos (Monitoramento):

O projeto implementa o `get_openai_callback` do LangChain para monitorar o consumo de tokens e o custo em USD. <br>
Para manter a integridade da saída JSON (conforme regra do desafio), estas informações são enviadas para:

1. `sys.stderr`: Visível no terminal durante a execução, mas ignorado por pipes de dados
2. `custos_execucao.log`: Arquivo de log persistente que armazena o histórico de custos e tokens de cada consulta realizada.

---

### Configuração e Instalação:
#### Pré-requisitos:
- Python 3.9 ou superior
- Chave de API da OpenAI

#### 1. Clone e Acesse o Projeto
```bash
git clone https://github.com/Developer-Marcos/active-bi-tech-challenge
```
```bash
cd active-bi-tech-challenge
```

#### 2. Crie / Acesse o Ambiente Virtual e baixe as dependências:
```bash
# Criação do ambiente
python -m venv venv
```
```bash
# Ativação (Windows)
.\\\\venv\\\\Scripts\\\\activate
```
```bash
# Ativação (Linux/Mac)
source venv/bin/activate
```
```bash
# Instalação das dependências
pip install -r requirements.txt
```

#### 3. Crie um arquivo .env na raiz do projeto seguindo o modelo .env.example:
```python
OPENAI_API_KEY=sua-chave-aqui
```

---

### Uso da Ferramenta:
Para analisar um documento, execute o main.py passando o caminho do arquivo e a pergunta entre aspas:
```bash
python main.py "caminho/do/arquivo.pdf" "Sua pergunta aqui"
```
#### Exemplo de Saída (STDOUT):
```JSON
{
    "type": "text",
    "text": "### Resumo Financeiro\\nO relatório indica um crescimento de **15%**...",
    "source": "relatorio_mensal.pdf",
    "suggestions": [
        "Qual foi o lucro líquido?",
        "Quem são os principais clientes?",
        "Qual a projeção para o próximo mês?"
    ]
}
```
