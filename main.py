import argparse
import json
import sys
import os
from src.data_extractor import extrair_pdf
from src.llm_service import analisar_documento

def main():
      # 1. Configurando os argumentos de linha de comando
      parser = argparse.ArgumentParser(description="Analisador de Documentos com IA (Active BI)")
      parser.add_argument("pdf_path", type=str, help="Caminho para o arquivo PDF local")
      parser.add_argument("question", type=str, help="Sua pergunta sobre o documento")

      args = parser.parse_args()

      # 2. Extração de Dados
      try:
            conteudo_documento = extrair_pdf(args.pdf_path)
            nome_documento = os.path.basename(args.pdf_path)
      except Exception as e:
            print(json.dumps({"error": f"Erro na extração do PDF: {str(e)}"}))
            sys.exit(1)

      # 3. Análise com Inteligência Artificial
      try:
            print("Lendo o documento e consultando a IA... Isso pode levar alguns segundos.", file=sys.stderr)

            resposta_json, custo_info = analisar_documento(
                  nome_documento=nome_documento,
                  conteudo_documento=conteudo_documento,
                  usuario_pergunta=args.question
            )

            # 4. Output do script
            print(json.dumps(resposta_json, indent=4, ensure_ascii=False))

            # 5. Salva o custo em um arquivo de log
            with open("custos_execucao.log", "a", encoding="utf-8") as f:
                f.write(f"Arquivo: {nome_documento} | Pergunta: {args.question}\n")
                f.write(f"Tokens Entrada: {custo_info['prompt_tokens']} | Saída: {custo_info['completion_tokens']}\n")
                f.write(f"Custo Total (USD): ${custo_info['custo_total_usd']}\n")
                f.write("-" * 50 + "\n")
      
      except Exception as e:
            print(json.dumps({"error": f"Erro na análise da IA: {str(e)}"}))
            sys.exit(1)

if __name__ == "__main__":
      main()