# -*- coding: utf-8 -*-
"""
Created on Thu May  9 21:39:26 2024

@author: Luiz Mario
"""

import pandas as pd
import os

# Diretório base onde as pastas estão localizadas
base_dir = r'\\storage6\usuarios\CGDTI\IpeaDataLab\projetos\repo_conhecimento_Ipea\dados\PDFs - Portal Antigo'

# Carregar o dataframe
# Carregar o DataFrame do Excel
xlsx_file_path = r'C:\Users\B03531855158\Downloads\Tabela2.xlsx'
df = pd.read_excel(xlsx_file_path)

# Função para criar o caminho completo de cada publicação
def criar_caminho(id_unico):
    return os.path.join(base_dir, str(id_unico))

# Adicionar a coluna 'Caminho' ao dataframe
df['Caminho'] = df['ID_Unico'].apply(criar_caminho)
#Mostra Df 
df

# Salvar o DataFrame em um arquivo Excel
excel_output_path = r'C:\Users\B03531855158\Downloads\Tabela2_com_caminhos.xlsx'
df.to_excel(excel_output_path, index=False)