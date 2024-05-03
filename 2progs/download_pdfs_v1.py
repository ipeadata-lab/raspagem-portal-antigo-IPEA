# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:55:47 2024

@author: Luiz Mario 
"""

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Caminho para o diretório onde os PDFs serão salvos
output_directory = r"C:\Users\B03531855158\Documents\Links Falhos"

# Função para baixar o PDF de um URL e salvar no diretório especificado
def download_pdf(url, directory, filename):
    try:
        os.makedirs(directory, exist_ok=True)  # Certifica-se de que o diretório existe
        with open(os.path.join(directory, filename), 'wb') as f:
            response = requests.get(url)
            f.write(response.content)
        print(f"PDF baixado: {filename}")
        return True
    except Exception as e:
        print(f"Erro ao baixar o PDF de {url}: {e}")
        return False

# Carregar o DataFrame do Excel
csv_file_path = r'C:\Users\B03531855158\Downloads\Tabela2.csv'
df = pd.read_csv(csv_file_path)

# Iterar sobre as linhas do DataFrame
for idx, row in df.iterrows():
    pdf_link = row['PDF Links']
    main_link = row['Link']
    title = row['Título do Artigo']

    # Tenta baixar o PDF diretamente
    if pd.notna(pdf_link):
        pdf_filename = os.path.basename(pdf_link)  # Pega o nome do arquivo do link
        if download_pdf(pdf_link, output_directory, pdf_filename):
            # Pausa de 10 segundos entre os downloads
            time.sleep(0.05)
            continue  # Se o PDF foi baixado com sucesso, passa para a próxima linha

    # Se não puder baixar diretamente, tenta encontrar o PDF no link principal
    if pd.notna(main_link):
        try:
            main_response = requests.get(main_link)
            main_soup = BeautifulSoup(main_response.content, 'html.parser')

            # Procura por links que terminam com .pdf
            pdf_links = main_soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

            for link in pdf_links:
                pdf_url = urljoin(main_link, link.get('href'))
                pdf_filename = os.path.basename(pdf_url)  # Pega o nome do arquivo do link
                if download_pdf(pdf_url, output_directory, pdf_filename):
                    # Pausa de 10 segundos entre os downloads
                    time.sleep(0.05)
                    break  # Se encontrou e baixou o PDF, para a busca

        except Exception as e:
            print(f"Erro ao acessar {main_link}: {e}")

print("Todos os links foram verificados.")
