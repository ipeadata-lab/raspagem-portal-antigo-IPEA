## ROBO TDS CEPAL #######
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes

def fix_link(link):
    if link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link

def extract_information(url, link):
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

    # Encontra a tabela com a classe "contentpaneopen"
    table_elem = soup.find('table', class_='contentpaneopen')

    if table_elem:
        # Obtém os autores do artigo
        authors_elem = table_elem.find_all('span', class_='linha_fina')
        authors = ", ".join([author.get_text(strip=True) for author in authors_elem]) if authors_elem else None

        # Obtém o link do PDF
        pdf_link_elem = table_elem.find('a', href=True)
        pdf_link = fix_link(pdf_link_elem['href']) if pdf_link_elem else None

        # Verifica se encontrou todas as informações necessárias
        if title_of_article and authors and pdf_link:
            # Retorna as informações extraídas com o link fornecido
            return {
                'Título do Artigo': title_of_article,
                'Autores': authors,
                'Link para o PDF': pdf_link,
                'Link': link  # Adiciona o link fornecido ao DataFrame
            }
        else:
            print(f"Algumas informações não puderam ser encontradas na URL {url}")
            return None
    else:
        print(f"Tabela com a classe 'contentpaneopen' não encontrada na URL {url}")
        return None

if __name__ == "__main__":
    # Exemplo de uso
    caminho_do_csv = 'C:\\Users\\B03531855158\\Downloads\\dados_publicacoes_completo.csv'
    df_links_tipos = processar_publicacoes(caminho_do_csv)
    
    # Cria um DataFrame vazio para armazenar as informações extraídas
    df_td_cepal = pd.DataFrame()
    
    # Substitua df_links_tipos pelo seu DataFrame contendo as URLs
    df_links_tipos_td = df_links_tipos[df_links_tipos['Tipo 2'] == 'Publicações - TDs Ipea']
    
    # Garante que há pelo menos 5 URLs no DataFrame
    if len(df_links_tipos_td) >= 5:
        # Seleciona aleatoriamente 5 URLs
        random_urls_td = df_links_tipos_td['Link'].sample(5)
        
        # Itera sobre as URLs selecionadas aleatoriamente
        for url, link in zip(random_urls_td, df_links_tipos_td['Link']):
            try:
                result = extract_information(url, link)
                if result:
                    df_td_cepal = pd.concat([df_td_cepal, pd.DataFrame([result])], ignore_index=True)
                    time.sleep(1)
            except Exception as e:
                print(f"Erro ao processar {url}: {e}")

        # Mostra o DataFrame com todas as informações extraídas
        print(df_td_cepal)
        # df_td_cepal.to_csv('TD_CEPAL.csv')
    else:
        print("Não há pelo menos 5 URLs que atendem ao filtro.")
