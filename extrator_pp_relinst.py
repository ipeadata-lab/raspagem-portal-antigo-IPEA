### PP E Relatorio Institucional ####
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes
def fix_link(link):
    if link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link

def extract_information(url):
    response = requests.get(url)

    # Verifica se a resposta contém HTML
    if 'text/html' not in response.headers['Content-Type']:
        print(f"Ignorando URL {url} - Conteúdo não é HTML.")
        return None

    html_code = response.text
    soup = BeautifulSoup(html_code, 'html.parser')

    # Obtém o título do artigo
    title_of_article_elem = soup.find('meta', {'name': 'title'})
    title_of_article = title_of_article_elem['content'] if title_of_article_elem else None

    # Obtém o autor do artigo
    author_elem = soup.find('meta', {'name': 'author'})
    author = author_elem['content'] if author_elem else None

    # Obtém outras informações como antes
    keywords_elem = soup.find('meta', {'name': 'keywords'})
    keywords = keywords_elem['content'] if keywords_elem else None

    abstract_elem = soup.find('meta', {'name': 'description'})
    abstract = abstract_elem['content'] if abstract_elem else None

    # Obtém o link para o artigo e para o sumário executivo
    article_link = None
    sumario_link = None
    pdf_links_elements = soup.find_all('a', href=True)
    for link_elem in pdf_links_elements:
        href = link_elem.get('href')
        if href and href.startswith('/portal/images/stories/PDFs/TDs/'):
            if "sumex" in href:
                sumario_link = fix_link(href)
            else:
                article_link = fix_link(href)

    # Verifica se encontrou os links
    if article_link:
        # Retorna as informações extraídas com o link do artigo
        return {
            'Título': title_of_article,
            'Autor': author,
            'Palavras-chave': keywords,
            'Resumo': abstract,
            'PDF Links': article_link,
            'Link para o Sumário Executivo': sumario_link
        }
    else:
        print(f"Erro ao extrair link do artigo da URL {url}")
        return None
if __name__ == "__main__":
    # Lê o DataFrame original do arquivo CSV
      # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)
    # DataFrame para armazenar as informações extraídas de "Publicações - Notas da Presidência"
    df_ppreliminar_RelInst = pd.DataFrame(columns=['Data de Criação', 'Título', 'Autor', 'PDF Links'])
    publicacoes_faltantes_nt =   ['Publicações - Relatório Institucional','Publicações - Publicação Preliminar']
    # Filtra as linhas do DataFrame original com tipo "Publicações - Notas Técnicas"
    df_notas_tecnicas = df_links_tipos[df_links_tipos['Tipo 2'].isin(publicacoes_faltantes_nt)]

    # Pega 5 links aleatórios
    links_aleatorios = df_notas_tecnicas['Link'] # random_state para reprodutibilidade

    # Itera sobre os links aleatórios
    for link in links_aleatorios:
        # Chama a função para extrair as informações da página
        df_page = extrair_informacoes_notas_presidencia(link)

        # Adiciona as informações extraídas ao DataFrame principal
        df_ppreliminar_RelInst = pd.concat([df_ppreliminar_RelInst, df_page], ignore_index=True)

        # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
        time.sleep(1)

    # Mostra o DataFrame com todas as informações extraídas
    print(df_ppreliminar_RelInst)