### Agenda Federativa ####
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

    # Encontra o link para o PDF
    pdf_link = soup.find('a', string='Acesse o PDF (1 MB)')['href'] if soup.find('a', string='Acesse o PDF (1 MB)') else None


    # Verifica se encontrou o link
    if pdf_link:
        # Retorna as informações extraídas com o link do artigo
        return {
            'Título do Artigo': title_of_article,
            'Autor': author,
            'Palavras-chave': keywords,
            'Resumo': abstract,
            'Link para o Artigo': url,
            'Link para o PDF': fix_link(pdf_link)
        }
    else:
        print(f"Erro ao extrair link do PDF da URL {url}")
        return None
if __name__ == '__main__':
    # Substitua df_pub pelo seu DataFrame contendo as URLs
      # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)

    # Cria um DataFrame vazio para armazenar as informações extraídas
    df_td = pd.DataFrame()

    # Substitua df_links_tipos pelo seu DataFrame contendo as URLs
    df_links_tipos_td = df_links_tipos[df_links_tipos['Tipo 2'] == 'Publicações -Temas relevantes da agenda federativa']

    # Garante que há pelo menos 5 URLs no DataFrame
    if len(df_links_tipos_td) >= 5:
        # Seleciona aleatoriamente 5 URLs
        random_urls_td = df_links_tipos_td['Link']
        # Cria um DataFrame vazio para armazenar as informações extraídas
        df_td = pd.DataFrame()

        # Itera sobre as URLs selecionadas aleatoriamente
        for url in random_urls_td:
            try:
                # Realiza a requisição HTTP para a URL atual
                response = requests.get(url)

                # Verifica se a resposta contém HTML
                if 'text/html' not in response.headers['Content-Type']:
                    print(f"Ignorando URL {url} - Conteúdo não é HTML.")
                    continue

                # Verifica se a requisição foi bem-sucedida
                if response.status_code == 200:
                    # Chama a função para extrair as informações da página
                    result = extract_information(url)

                    # Adiciona as informações extraídas ao DataFrame principal
                    df_td = pd.concat([df_td, pd.DataFrame([result])], ignore_index=True)

                    # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
                    time.sleep(1)
                else:
                    print(f"Erro na requisição para {url}. Código de status: {response.status_code}")
            except Exception as e:
                print(f"Erro ao processar {url}: {e}")
