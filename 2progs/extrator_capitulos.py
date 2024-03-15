import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes
def extrair_informacoes_capitulos(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    capitulos = []
    titulos_capitulo = []
    autores = []
    links_capitulos = []

    # Encontrar todos os elementos 'p' com a classe 'linha_fina'
    for p_element in soup.find_all('p'):
        # Verificar se o elemento possui um link (indicando um capítulo)
        link_capitulo_element = p_element.find('a', href=True)
        if link_capitulo_element:
            # Extrair informações do capítulo
            capitulo_element = p_element.find('strong')
            capitulo = capitulo_element.text.strip() if capitulo_element else ''
            link_capitulo = link_capitulo_element['href']
            links_capitulos.append(link_capitulo)

            # Extrair informações sobre os autores
            autores_element = p_element.find_all_next('br')
            autores_text = ', '.join([br_element.find_next(string=True).strip() for br_element in autores_element[1:] if br_element.find_next(string=True)])
            autores.append(autores_text)

            # Extrair título do capítulo
            titulo_capitulo_element = autores_element[0].find_next('strong') if autores_element else None
            titulo_capitulo = titulo_capitulo_element.text.strip() if titulo_capitulo_element else ''
            titulos_capitulo.append(titulo_capitulo)

            # Adicionar informações do capítulo à lista
            capitulos.append(capitulo)

    # Criar um DataFrame com as informações dos capítulos
    df_capitulos = pd.DataFrame({
        'Capítulo': capitulos,
        'Título do Capítulo': titulos_capitulo,
        'Autores': autores,
        'Link do Capítulo': links_capitulos
    })

    return df_capitulos
if __name__ == "__main__":
    # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)
# Pega 5 links aleatórios da coluna 'Link'
random_links = df_links_tipos[df_links_tipos['Tipo 2'] == 'Publicações - Livros (todos os anos)']['Link']

# Cria um DataFrame vazio para armazenar as informações extraídas
df_capitulos = pd.DataFrame()

# Itera sobre os links aleatórios
for link in random_links:
    # Realiza a requisição HTTP para o link atual
    response = requests.get(link)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Chama a função para extrair as informações da página
        df_page = extrair_informacoes_capitulos(response.text)

        # Adiciona as informações extraídas ao DataFrame principal
        if df_page is not None:
            df_capitulos = pd.concat([df_capitulos, df_page], ignore_index=True)

        # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
        time.sleep(1)
    else:
        print(f"Erro na requisição para {link}. Código de status: {response.status_code}")

# Mostra o DataFrame com todas as informações extraídas
print(df_capitulos)
