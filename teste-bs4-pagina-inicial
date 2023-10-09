import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página que você deseja raspar
url = 'https://portalantigo.ipea.gov.br/portal/index.php?option=com_alphacontent&view=alphacontent&Itemid=357'

# Fazer uma requisição HTTP para obter o conteúdo da página
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parsear o conteúdo HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todas as ocorrências das tags com as informações desejadas
    titles = soup.find_all('span', class_='_alphatitle')
    types = soup.find_all('div', class_='small')
    dates = soup.find_all('div', id=lambda x: x and x.startswith('features'))

    # Criar listas vazias para armazenar os dados
    title_list = []
    type_list = []
    date_list = []

    # Iterar pelas ocorrências das tags e extrair os dados
    for title, type, date in zip(titles, types, dates):
        title_text = title.text.strip()
        type_text = type.text.strip()
        date_text = date.text.strip()
        
        title_list.append(title_text)
        type_list.append(type_text)
        date_list.append(date_text)

    # Criar um DataFrame pandas com os dados extraídos
    data = {
        'Título': title_list,
        'Tipo de Publicação': type_list,
        'Data': date_list
    }

    df = pd.DataFrame(data)

    # Exibir o DataFrame
    print(df)

else:
    print('Falha ao acessar a página.')
