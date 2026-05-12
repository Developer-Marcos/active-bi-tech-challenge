import os
from langchain_community.document_loaders import PyPDFLoader

def extrair_pdf(arquivo_caminho: str) -> str:
      if not os.path.exists(arquivo_caminho):
            raise FileNotFoundError(f"Arquivo PDF não encontrado no caminho: {arquivo_caminho}")
      
      loader = PyPDFLoader(file_path=arquivo_caminho)
      paginas = loader.load()

      texto_completo = "\n".join([pagina.page_content for pagina in paginas])

      if not texto_completo.strip():
            raise ValueError("O PDF está vazio ou contém apenas imagens não legíveis")
      
      return texto_completo