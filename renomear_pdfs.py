import os
import re
import pdfplumber
import warnings
import json

# Ignora avisos do pdfplumber sobre CropBox
warnings.filterwarnings("ignore", message="CropBox missing from /Page")

# Carrega a pasta do config.json
def carregar_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config.get('pasta_pdfs', '')  # Retorna o caminho ou string vazia
    except:
        return None  # Se o arquivo não existir ou for inválido

def extrair_identificacao(caminho_pdf):
    # Abre o PDF e busca a identificação em tabelas ou texto
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            # Primeiro tenta extrair de tabelas
            for tabela in pagina.extract_tables():
                for linha in tabela:
                    for i, celula in enumerate(linha):
                        if celula and "Identificação da Amostra" in str(celula):
                            if i + 1 < len(linha):
                                return linha[i + 1].strip()
            
            # Fallback para extração de texto bruto
            texto = pagina.extract_text()
            busca = re.search(r"Identificação da Amostra:\s*([^\n]+)", texto)
            if busca:
                return busca.group(1).strip()
    return None

def gerar_nome_unico(pasta, nome_base, arquivo_origem):
    # Remove caracteres inválidos para nome de arquivo
    nome_seguro = re.sub(r'[\\/*?:"<>|]', "_", nome_base).strip()
    caminho_base = os.path.join(pasta, f"{nome_seguro}.pdf")
    
    # Verifica se nome já existe e não é o próprio arquivo
    if not os.path.exists(caminho_base) or os.path.abspath(caminho_base) == os.path.abspath(arquivo_origem):
        return nome_seguro
    
    # Adiciona sufixo numérico (_2, _3...) se nome existir
    contador = 2
    while True:
        novo_nome = f"{nome_seguro}_{contador}"
        novo_caminho = os.path.join(pasta, f"{novo_nome}.pdf")
        if not os.path.exists(novo_caminho):
            return novo_nome
        contador += 1

def renomear_pdfs(pasta):
    # Processa todos os PDFs na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith('.pdf'):
            caminho_antigo = os.path.join(pasta, arquivo)
            try:
                identificacao = extrair_identificacao(caminho_antigo)
                if identificacao:
                    # Gera nome único e renomeia
                    nome_final = gerar_nome_unico(pasta, identificacao, caminho_antigo)
                    novo_caminho = os.path.join(pasta, f"{nome_final}.pdf")
                    os.rename(caminho_antigo, novo_caminho)
                    print(f"✅ Renomeado: {arquivo} -> {nome_final}.pdf")
                else:
                    print(f"❌ Identificação não encontrada em: {arquivo}")
            except Exception as e:
                print(f"⚠️ Erro em {arquivo}: {str(e)}")

# Configuração da pasta contendo os PDFs
config = carregar_config()
pasta_dos_pdfs = config if config else r"C:\\Users\\arthur.beiral\\Desktop\\PDFscript"  # Fallback

if __name__ == "__main__":
    if not os.path.exists(pasta_dos_pdfs):
        print(f"❌ Pasta não encontrada: {pasta_dos_pdfs}")
    else:
        renomear_pdfs(pasta_dos_pdfs)