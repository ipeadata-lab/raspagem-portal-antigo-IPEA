# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:19:11 2024

@author: Luiz Mario
"""

import pandas as pd
import openpyxl

# Caminho para o arquivo Excel
excel_path = "C:/Users/B03531855158/Desktop/Tabela2_caminhos_hash.xlsx"

# Ler o arquivo Excel
df = pd.read_excel(excel_path)

# Extrair o nome do arquivo da coluna "PDF Links"
def extract_file_name(link):
    if isinstance(link, str):
        return link.split('/')[-1]
    else:
        return ""

df['file_name'] = df['PDF Links'].apply(extract_file_name)
# Remove vírgulas e pontos e vírgulas da coluna "Caminho"
df['Caminho'] = df['Caminho'].str.replace("[,;]", "")

# Substituir os dados da coluna "Caminho" com os dados corretos
df['Caminho'] = '\\\\storage6\\usuarios\\CGDTI\\IpeaDataLab\\projetos\\repo_conhecimento_Ipea\\dados\\PDFs - Portal Antigo\\' + df['ID_Unico'].astype(str) + '\\' + df['file_name']

# Salvar o resultado em um novo arquivo Excel
output_excel_path = "C:/Users/B03531855158/Desktop/Tabela2_file_names.xlsx"
df.to_excel(output_excel_path, index=False, engine='openpyxl')

print("Processo concluído. Arquivo salvo em:", output_excel_path)