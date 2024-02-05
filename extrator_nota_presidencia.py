import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes
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
        title = table.find('span', class_='titulo_artigo').get_text(strip=True) if table.find('span', class_='titulo_artigo') else None

        # Procura por uma tag 'p' dentro da classe 'linha_fina'
        author_element = table.find('p', class_='linha_fina', string=lambda text: text and 'Autor' in text)

        # Verifica se a tag 'p' foi encontrada e extrai o texto
        author = author_element.get_text(strip=True) if author_element else None

        pdf_link = table.find('a', href=True)['href'] if table.find('a', href=True) else None

        # Cria um DataFrame com as informações
        data = {'Data de Criação': [created_date],
                'Título': [title],
                'Autor': [author],
                'Link do PDF': [pdf_link]}

        df = pd.DataFrame(data)

        return df

    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")
        return None
if __name__ == "__main__":
    # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)
# DataFrame para armazenar as informações extraídas de "Publicações - Notas da Presidência"
df_notas_presidencia_extraido = pd.DataFrame(columns=['Data de Criação', 'Título', 'Autor', 'Link do PDF'])

# Itera sobre as linhas do DataFrame original
for index, row in df_links_tipos.iterrows():
    # Verifica se o tipo é "Publicações - Notas da Presidência"
    if row['Tipo 2'] == 'Publicações - Notas da Presidência':
        # Chama a função para extrair as informações da página
        df_page = extrair_informacoes_notas_presidencia(row['Link'])

        # Adiciona as informações extraídas ao DataFrame principal
        df_notas_presidencia_extraido = pd.concat([df_notas_presidencia_extraido, df_page], ignore_index=True)

        # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
        time.sleep(1)

# Mostra o DataFrame com todas as informações extraídas
print(df_notas_presidencia_extraido)
