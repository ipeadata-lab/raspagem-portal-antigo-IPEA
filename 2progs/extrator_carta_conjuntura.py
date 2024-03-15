#### CARTA CONJUNTURA ######
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from main import processar_publicacoes
# Função para atualizar links que começam com '/portal'
def fix_link(link):
    if link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link

def extract_information(url):
    # Realiza a requisição HTTP
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra a tabela com a classe 'contentpaneopen'
        table = soup.find('table', class_='contentpaneopen')

        # Obtém o título da carta
        title_of_article_elem = soup.find('p', class_='titulo_artigo')
        title_of_article = title_of_article_elem.get_text(strip=True) if title_of_article_elem else None

        # Extrai as informações desejadas
        data = []

        # Procura por todas as âncoras dentro da tabela
        anchors = table.find_all('a', href=True)

        for anchor in anchors:
            article_title = anchor.get_text(strip=True)
            pdf_link = fix_link(anchor['href'])

            # Encontra o autor
            author_elem = anchor.find_next('br').find_next('br')
            author = author_elem.get_text(strip=True) if author_elem else None

            # Adiciona os dados à lista
            data.append({'Título da Carta': title_of_article,
                         'Título do Artigo': article_title,
                         'Autor': author,
                         'Link para o PDF': pdf_link,
                         'Link': url})

        # Cria um DataFrame com as informações extraídas
        df = pd.DataFrame(data)
        return df

    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")
        return None
if __name__ == "__main__":
    # Lê o DataFrame original do arquivo CSV
      # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)

    # DataFrame para armazenar as informações extraídas de todas as páginas
    df_carta_conj = pd.DataFrame(columns=['Link PDF Extraído', 'Título', 'Autores', 'Data Publicação', 'Publicação Mãe'])

    # Tipos de publicações desejados
    tipos_de_publicacao_desejados = ['Publicações - Carta de Conjuntura']

    # Itera sobre as linhas do DataFrame original
    for index, row in df_links_tipos.iterrows():
        # Verifica se o tipo está entre os desejados
        if row['Tipo 2'] in tipos_de_publicacao_desejados:
            # Realiza a requisição HTTP para a URL da linha atual
            response = requests.get(row['Link'])

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                # Chama a função para extrair as informações da página
                df_page = extract_information(response.text)

                # Adiciona o link usado para extrair as informações como uma nova coluna 'Link'
                df_page['Link'] = row['Link']

                # Adiciona as informações extraídas ao DataFrame principal
                df_carta_conj = pd.concat([df_carta_conj, df_page], ignore_index=True)

                # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
                time.sleep(1)
            else:
                print(f"Erro na requisição para {row['Link']}. Código de status: {response.status_code}")

    # Mostra o DataFrame com todas as informações extraídas
    print(df_carta_conj)
