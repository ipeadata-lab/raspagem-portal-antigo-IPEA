import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes
def fix_link(link):
    if link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link
def extrair_informacoes_notas_presidencia(url):
    # Realiza a requisição HTTP
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra a tabela com a classe 'contentpaneopen'
        table = soup.find('table', class_='contentpaneopen')

        # Extrai as informações desejadas
        created_date = table.find('td', class_='createdate').get_text(strip=True) if table.find('td', class_='createdate') else None

        # Modificação para extrair o conteúdo de <p class="linha_fina"> como título e o título original como Nota Técnica
        linha_fina_element = table.find('p', class_='linha_fina')
        nota_tecnica = linha_fina_element.get_text(strip=True) if linha_fina_element else None

        # Procura por uma tag 'span' dentro da classe 'titulo_artigo'
        title_element = table.find('span', class_='titulo_artigo')

        # Verifica se a tag 'span' foi encontrada e extrai o texto
        title = title_element.get_text(strip=True) if title_element else None

        # Procura por uma tag 'p' dentro da classe 'linha_fina'
        author_element = table.find('p', class_='linha_fina', string=lambda text: text and 'Autor' in text)

        # Verifica se a tag 'p' foi encontrada e extrai o texto
        author = author_element.get_text(strip=True) if author_element else None

        pdf_link = table.find('a', href=True)['href'] if table.find('a', href=True) else None

        # Cria um DataFrame com as informações
        data = {'Data de Criação': [created_date],
                'Nota Técnica': [title],  # 'Título' agora é a Nota Técnica
                'Título': [nota_tecnica],  # 'Nota Técnica' contém o conteúdo de <p class="linha_fina">
                'Autor': [author],
                'Link do PDF': [fix_link(pdf_link)]}

        df = pd.DataFrame(data)

        return df

    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")
        return None
if __name__ == "__main__":
    # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)
# Lê o DataFrame original do arquivo CSV
df_links_tipos = df
# DataFrame para armazenar as informações extraídas de "Publicações - Notas da Presidência"
df_notas_tecnicas_extraido = pd.DataFrame(columns=['Data de Criação', 'Título', 'Autor', 'Link do PDF'])

# Filtra as linhas do DataFrame original com tipo "Publicações - Notas Técnicas"
df_notas_tecnicas = df_links_tipos[df_links_tipos['Tipo 2'] == 'Publicações - Notas Técnicas']

# Pega 5 links aleatórios
links_aleatorios = df_notas_tecnicas['Link'] # random_state para reprodutibilidade

# Itera sobre os links aleatórios
for link in links_aleatorios:
    # Chama a função para extrair as informações da página
    df_page = extrair_informacoes_notas_presidencia(link)

    # Adiciona as informações extraídas ao DataFrame principal
    df_notas_tecnicas_extraido = pd.concat([df_notas_tecnicas_extraido, df_page], ignore_index=True)

    # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
    time.sleep(1)

# Mostra o DataFrame com todas as informações extraídas
print(df_notas_tecnicas_extraido)    
