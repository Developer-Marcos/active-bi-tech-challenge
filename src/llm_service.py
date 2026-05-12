import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks import get_openai_callback
from pydantic import BaseModel, Field
from typing import List


# 0. Inicializacao do ambiente
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: A variável de ambiente OPENAI_API_KEY não foi encontrada.")
    print("Por favor, crie um arquivo .env e adicione sua chave. Veja o .env.example.")
    sys.exit(1)

# 1. Schema de output que a LLM deve seguir
class RespostaLLM(BaseModel):
      type: str = Field(default="text", description="Sempre deve ser a palavra 'text'")
      text: str = Field(description="A resposta principal da pergunta em formato Markdown (pt-BR)")
      source: str = Field(description="O nome do documento consultado ou N/A")
      suggestions: List[str] = Field(
             description="Uma lista contendo EXATAMENTE 3 perguntas de acompanhamento relacionadas à resposta",
             min_length=3,
             max_length=3
      )

# 2. Inicializando a LLM junto com o output
llm = ChatOpenAI(
      model="gpt-4o-mini",
      temperature=0,
      openai_api_key=api_key
)
llm_estruturado = llm.with_structured_output(RespostaLLM) 

# 3. Carregando o prompt de sistema
try:
      with open("prompt.xml", "r", encoding="utf-8") as arquivo:
            prompt_sistema = arquivo.read()
except FileNotFoundError:
      raise Exception("Error: Arquivo prompt.xml não encontrado na raiz do projeto.")

prompt = ChatPromptTemplate.from_messages([
      ("system", prompt_sistema),
      ("human", "Document Name: {nome_documento}\n\nDocument Content: {conteudo_documento}\n\nUser Question: {usuario_pergunta}")
])

# 4. Criando a sequencia (prompt de sistema + LLM com o output)
chain = prompt | llm_estruturado 

# 5. Definindo a funcao que permite interagir com a LLM
def analisar_documento(nome_documento: str, conteudo_documento: str, usuario_pergunta: str) -> tuple[dict, dict]:
      try:
            with get_openai_callback() as cb:
                  resposta_pydantic = chain.invoke({
                        "nome_documento": nome_documento,
                        "conteudo_documento": conteudo_documento,
                        "usuario_pergunta": usuario_pergunta
                  })
            
                  custo_info = {
                        "tokens_totais": cb.total_tokens,
                        "prompt_tokens": cb.prompt_tokens,
                        "completion_tokens": cb.completion_tokens,
                        "custo_total_usd": round(cb.total_cost, 6)
                  }
      except Exception as e:
            raise RuntimeError(f"Falha ao comunicar com a API da OpenAI: {str(e)}")

      return resposta_pydantic.model_dump(), custo_info