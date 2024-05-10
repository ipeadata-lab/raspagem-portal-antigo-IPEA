import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Caminho para o diretório onde os arquivos serão salvos
output_directory = 'F:\\Luiz - Repo IPEA\\PDFS 3'

# Função para baixar o arquivo de um URL e salvar no diretório especificado
def download_arquivo(url, directory, filename):
    try:
        os.makedirs(directory, exist_ok=True)  # Certifica-se de que o diretório existe
        with open(os.path.join(directory, filename), 'wb') as f:
            response = requests.get(url)
            f.write(response.content)
        print(f"Arquivo baixado: {filename}")
        return True
    except Exception as e:
        print(f"Erro ao baixar o arquivo de {url}: {e}")
        return False

# Função para limpar o nome do arquivo removendo caracteres inválidos
def limpar_nome_arquivo(nome_arquivo):
    # Caracteres inválidos no Windows
    caracteres_invalidos = '\\/:*?"<>|'

    # Substituir caracteres inválidos por sublinhados
    for char in caracteres_invalidos:
        nome_arquivo = nome_arquivo.replace(char, '_')

    return nome_arquivo

# Carregar o DataFrame do Excel
xlsx_file_path = r'C:\Users\B03531855158\Downloads\Tabela2.xlsx'
df = pd.read_excel(xlsx_file_path)

# Lista para armazenar os caminhos de download
caminhos_download = []

# Iterar sobre as linhas do DataFrame
for idx, row in df.iterrows():
    pdf_link = row['PDF Links']
    main_link = row['Link']
    title = row['Título do Artigo']
    id_unico = row['ID_Unico']

    # Diretório para salvar o arquivo baseado no ID_Unico
    output_directory_id = os.path.join(output_directory, str(id_unico))

    # Tenta baixar o arquivo diretamente
    if pd.notna(pdf_link):
        filename = limpar_nome_arquivo(os.path.basename(pdf_link))
        if download_arquivo(pdf_link, output_directory_id, filename):
            caminhos_download.append(output_directory_id)
            # Pausa de 0.5 segundos entre os downloads
            time.sleep(0.5)
            continue

    # Se não puder baixar diretamente, tenta encontrar o arquivo no link principal
    if pd.notna(main_link):
        try:
            main_response = requests.get(main_link)
            main_soup = BeautifulSoup(main_response.content, 'html.parser')

            # Procura por links que terminam com .pdf, .epub ou .xlsx
            for extensao in ['.pdf', '.epub', '.xlsx']:
                links = main_soup.find_all('a', href=lambda href: href and href.endswith(extensao))

                for link in links:
                    url = urljoin(main_link, link.get('href'))
                    filename = limpar_nome_arquivo(os.path.basename(url))
                    if download_arquivo(url, output_directory_id, filename):
                        caminhos_download.append(output_directory_id)
                        # Pausa de 0.5 segundos entre os downloads
                        time.sleep(0.5)
                        break

        except Exception as e:
            print(f"Erro ao acessar {main_link}: {e}")

# Verificar se o comprimento de 'caminhos_download' corresponde ao número de linhas no DataFrame
if len(caminhos_download) == len(df):
    # Adicionar a coluna "Caminho_Download" ao DataFrame
    df['Caminho_Download'] = caminhos_download

    # Salvar o DataFrame em um arquivo Excel
    excel_output_path = r'C:\Users\B03531855158\Downloads\Tabela2_atualizado.xlsx'
    df.to_excel(excel_output_path, index=False)

    print("Todos os links foram verificados e o DataFrame foi salvo em um arquivo Excel.")
else:
    print("O número de caminhos de download não corresponde ao número de linhas no DataFrame. Verifique os links e tente novamente.")
