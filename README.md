# RenomeadorPDFs
Ferramenta Python que renomeia PDFs com base no campo "Identificação da Amostra", evitando duplicatas com sufixos (_2, _3). Ideal para laboratórios ou equipes que padronizam arquivos.

1. CONFIGURAÇÃO INICIAL:
   - Baixe os arquivos "RenomeadorPDFs.exe" e "config.json"
   - Edite o arquivo 'config.json' e coloque o caminho da sua pasta de PDFs (lembrando que o caminho deve conter uma barra "/" ou duas contrabarras "\\" para separação:
     Exemplo: "pasta_pdfs": "C:/Meus_Documentos/PDFs" ou "C:\\Meus_Documentos\\PDFs"

2. COMO USAR:
   - Execute 'RenomeadorPDFs.exe'
   - Os arquivos serão renomeados automaticamente
   - Arquivos com nomes repetidos ganharão _2, _3, etc.

3. SUPORTE:
   - Problemas? Contate: [arthur.beiral@mxns.com]
   - Erros comuns:
     * Pasta não encontrada → Verifique o caminho no config.json
     * PDF não renomeado → Verifique se contém "Identificação da Amostra"
