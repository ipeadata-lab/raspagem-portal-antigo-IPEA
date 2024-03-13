## Robo Publicacoes ###
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes
def fix_link(link):
    if link is not None and link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link

def extrair_informacoes_notas_presidencia(url):
    # Realiza a requisição HTTP
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrai as informações desejadas
        title = soup.find('meta', {'name': 'title'})['content']
        author = soup.find('meta', {'name': 'author'})['content']
        description = soup.find('meta', {'name': 'description'})['content']

        # Encontra o link do PDF
        pdf_link = None
        for link in soup.find_all('a'):
            if link.get('href', '').endswith('.pdf'):
                pdf_link = link.get('href')
                break

        # Cria um DataFrame com as informações
        data = {'Título': [title],
                'Autor': [author],
                'Descrição': [description],
                'PDF Links': [fix_link(pdf_link)]}

        df = pd.DataFrame(data)

        return df

    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")
        return None
if __name__ == "__main__":
    # Exemplo de uso
    caminho_do_csv = 'C:\\Users\\B03531855158\\Downloads\\dados_publicacoes_completo.csv'
    df_links_tipos = processar_publicacoes(caminho_do_csv)
    # Lê o DataFrame original do arquivo CSV
df_links_tipos = df_pub

# DataFrame para armazenar as informações extraídas de "Publicações - Notas da Presidência"
df_ps = pd.DataFrame(columns=['Data de Criação', 'Título', 'Autor', 'PDF Links', 'Link'])  # Adicionando a coluna 'Link'

# Filtra as linhas do DataFrame original com tipo "Publicações - Notas Técnicas"
df_notas_tecnicas = df_links_tipos[df_links_tipos['Tipo 2'] == 'Publicações']

# Pega 5 links aleatórios
links_aleatorios = df_notas_tecnicas['Link']  # random_state para reprodutibilidade

# Itera sobre os links aleatórios
for link in links_aleatorios:
    # Verifica se o link não é None
    if link is not None:
        # Chama a função para extrair as informações da página
        df_page = extrair_informacoes_notas_presidencia(link)

        # Adiciona o link usado para extrair as informações ao DataFrame df_page
        df_page['Link'] = link

        # Adiciona as informações extraídas ao DataFrame principal
        df_ps = pd.concat([df_ps, df_page], ignore_index=True)

        # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
        time.sleep(1)

# Mostra o DataFrame com todas as informações extraídas
print(df_ps)
  