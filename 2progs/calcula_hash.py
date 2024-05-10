# -*- coding: utf-8 -*-
"""
Created on Thu May  9 21:39:26 2024

@author: Luiz Mario
"""

import pandas as pd
import hashlib

# Função para calcular o hash MD5 de uma string
def calcular_hash_md5(string):
    hasher = hashlib.md5()
    hasher.update(string.encode('utf-8'))
    return hasher.hexdigest()

# Ler o arquivo Excel
excel_file_path = r'C:\Users\B03531855158\Downloads\Tabela2_com_caminhos.xlsx'
df = pd.read_excel(excel_file_path)

# Calcular hash MD5 para cada PDF
hashes_md5 = []
for link_pdf in df['PDF Links']:
    # Converter para string antes de calcular o hash
    link_pdf_str = str(link_pdf)
    hash_md5 = calcular_hash_md5(link_pdf_str)
    hashes_md5.append(hash_md5)

# Adicionar os hashes MD5 ao DataFrame
df['Hash MD5'] = hashes_md5

# Salvar o DataFrame em um arquivo Excel
excel_output_path = r'C:\Users\B03531855158\Downloads\Tabela2_caminhos_hash.xlsx'
df.to_excel(excel_output_path, index=False)

# Indicar que o programa terminou
print("Programa terminou.")
