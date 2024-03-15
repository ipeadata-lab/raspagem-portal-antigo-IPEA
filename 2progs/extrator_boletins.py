### Robo Boletins ####
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from main import processar_publicacoes

# Função para atualizar links que começam com '/portal'
def fix_link(link):
    if link and link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link

def extrair_informacoes(html_content, link):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='contentpaneopen')
    links_pdf = []
    titulos = []
    autores = []
    datas_publicacao = []  # Adiciona uma lista para armazenar as datas de publicação
    publicacao_mae = soup.find('meta', {'name': 'title'})['content']

    for p_element in table.find_all('p', class_='linha_fina'):
        # Verifica se o elemento contém informações de data de publicação
        if 'Volume' in p_element.get_text():
            # Captura o conteúdo completo dentro do elemento <p class="linha_fina">
            data_publicacao = p_element.get_text(strip=True)
            datas_publicacao.append(data_publicacao)
        else:
            datas_publicacao.append(None)

    for p_element in table.find_all('p'):
        if p_element.find('a') and p_element.find('strong'):
            link_pdf = p_element.find('a')['href']
            links_pdf.append(link_pdf)

            titulo = p_element.find('a').get_text(strip=True).upper()
            titulos.append(titulo)

            autores_info = p_element.find('strong').find_next('br').next_siblings
            autores_text = ', '.join([autor.strip() for autor in autores_info if isinstance(autor, str)])
            autores.append(autores_text)

    # Certifica-se de que todas as listas tenham o mesmo comprimento
    max_len = max(len(links_pdf), len(titulos), len(autores), len(datas_publicacao))
    links_pdf += [None] * (max_len - len(links_pdf))
    titulos += [None] * (max_len - len(titulos))
    autores += [None] * (max_len - len(autores))
    datas_publicacao += [None] * (max_len - len(datas_publicacao))

     # Cria um DataFrame com as informações
    df = pd.DataFrame({
        'PDF Links': [fix_link(link) for link in links_pdf],
        'Título': titulos,
        'Autor': autores,
        'Data Publicação': datas_publicacao,
        'Publicação Mãe': [publicacao_mae] * max_len,  # Repete a informação para todas as linhas
        'Link': [link] * max_len  # Adiciona a coluna com o link de origem
    })

    return df
if __name__ == "__main__":
        # Lê o DataFrame original do arquivo CSV
      # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)
    # DataFrame para armazenar as informações extraídas de todas as páginas
    df_boletins_extraido = pd.DataFrame(columns=['Link', 'PDF Links', 'Título', 'Autores', 'Data Publicação', 'Publicação Mãe'])

    # Tipos de publicações desejados
    tipos_de_publicacao_desejados = ['Publicações - Boletim Regional',
                                    'Publicações - Mercado de Trabalho',
                                    'Publicações - Boletim Internacional',
                                    'Publicações - Análise Político-Institucional']

    # Itera sobre as linhas do DataFrame original
    for index, row in df_links_tipos.iterrows():
        # Verifica se o tipo está entre os desejados
        if row['Tipo 2'] in tipos_de_publicacao_desejados:
            # Realiza a requisição HTTP para a URL da linha atual
            response = requests.get(row['Link'])

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                # Chama a função para extrair as informações da página, passando o link da publicação mãe
                df_page = extrair_informacoes(response.text, row['Link'])

                # Adiciona as informações extraídas ao DataFrame principal
                df_boletins_extraido = pd.concat([df_boletins_extraido, df_page], ignore_index=True)

                # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
                time.sleep(1)
            else:
                print(f"Erro na requisição para {row['Link']}. Código de status: {response.status_code}")

    # Mostra o DataFrame com todas as informações extraídas
    print(df_boletins_extraido)
