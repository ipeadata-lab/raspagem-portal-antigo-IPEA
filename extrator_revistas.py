### REVISTAS #####
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes
# Função para atualizar links que começam com '/portal'
def fix_link(link):
    if link and isinstance(link, str) and link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link

# Função para extrair informações de uma página de Publicações - PPE
def extrair_informacoes(html_content, link):
    soup = BeautifulSoup(html_content, 'html.parser')
    publicacao_mae = soup.find('meta', {'name': 'title'})['content']

    titulos = []
    autores = []
    links_pdf = []

    for p_element in soup.find_all('p'):
        link_pdf = p_element.find('a', href=True)
        if link_pdf:
            links_pdf.append(fix_link(link_pdf['href']))

            # Extrai o título e os autores da âncora
            titulo_autores = link_pdf.get_text(strip=True)
            titulo, *autores_info = titulo_autores.split('<br />')
            titulos.append(titulo.upper())
            autores.append(', '.join(autores_info))

    # Certifica-se de que todas as listas tenham o mesmo comprimento
    max_len = max(len(links_pdf), len(titulos), len(autores))

    # Cria um DataFrame com as informações
    df = pd.DataFrame({
        'Publicação Mãe': [publicacao_mae] * max_len,  # Repete a informação para todas as linhas
        'PDF Links': links_pdf,
        'Título do Artigo': titulos,
        'Autores': autores,
        'Link': [link] * max_len  # Adiciona o link usado para todas as linhas
    })

    return df
if __name__ == "__main__":
    # Lê o DataFrame original do arquivo CSV
      # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)

    # DataFrame para armazenar as informações extraídas de todas as páginas
    df_publicacoes_extraido = pd.DataFrame(columns=['PDF Links', 'Título', 'Autores', 'Publicação Mãe', 'Link'])

    # Lista de tipos de publicações desejados
    tipos_de_publicacao_desejados = ['Publicações - PPP', 'Publicações - Tempo do Mundo', 'Publicações - Radar']

    # Itera sobre as linhas do DataFrame original
    for index, row in df_links_tipos.iterrows():
        # Verifica se o tipo está na lista de tipos de publicações desejados
        if row['Tipo 2'] in tipos_de_publicacao_desejados:
            # Realiza a requisição HTTP para a URL da linha atual
            response = requests.get(row['Link'])

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                # Chama a função para extrair as informações da página
                df_page = extrair_informacoes(response.text, row['Link'])

                # Adiciona as informações extraídas ao DataFrame principal
                df_publicacoes_extraido = pd.concat([df_publicacoes_extraido, df_page], ignore_index=True)

                # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
                time.sleep(1)
            else:
                print(f"Erro na requisição para {row['Link']}. Código de status: {response.status_code}")

    # Mostra o DataFrame com todas as informações extraídas
    df_publicacoes_extraido