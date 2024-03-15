import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from main import processar_publicacoes
def extrair_informacoes_livro(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Inicializa listas para armazenar as informações
    titulos_livro = []
    categorias = []
    organizadores = []

    # Encontra todos os elementos 'p' com a classe 'titulo_artigo'
    for p_element in soup.find_all('p', class_='titulo_artigo'):
        # Extrai a categoria e o título do livro
        categoria_titulo_text = p_element.get_text(strip=True).strip()
        categoria, _, titulo = categoria_titulo_text.partition('-')
        categorias.append(categoria.strip())
        titulos_livro.append(titulo.strip())

    # Encontra o elemento <p> com a classe "linha_fina"
    linha_fina_element = soup.find('p', class_='linha_fina')

    # Verifica se o elemento foi encontrado
    if linha_fina_element:
        # Extrai os organizadores do livro
        organizadores_info = linha_fina_element.find_next('p', class_='linha_fina')

        # Verifica se a próxima linha é encontrada
        if organizadores_info:
            # Extrai os organizadores e remove a palavra "Organizadores:"
            organizadores_text = organizadores_info.text.replace('Organizadores:', '').strip()
            organizadores.append(organizadores_text)
        else:
            # A próxima linha não foi encontrada
            organizadores.append(None)
    else:
        # O elemento não foi encontrado
        organizadores.append(None)

    # Encontra todos os elementos 'td' com a classe 'createdate'
    created_date_element = soup.find('td', class_='createdate')
    created_date_text = created_date_element.get_text(strip=True) if created_date_element else ''

    # Encontra o primeiro elemento 'a' dentro da classe 'contentpaneopen'
    table_element = soup.find('table', class_='contentpaneopen')
    pdf_link_text = None
    if table_element:
        pdf_link_element = table_element.find('a', href=True)
        pdf_link_text = pdf_link_element['href'] if pdf_link_element else ''

    # Garante que todas as listas tenham o mesmo comprimento
    max_len = max(len(titulos_livro), len(categorias), len(organizadores))
    titulos_livro += [None] * (max_len - len(titulos_livro))
    categorias += [None] * (max_len - len(categorias))
    organizadores += [None] * (max_len - len(organizadores))

    # Cria um DataFrame com as informações
    df = pd.DataFrame({
        'Data de Criação': [created_date_text] * max_len,
        'Título do Livro': titulos_livro,
        'Categoria': categorias,
        'Organizadores': organizadores,
        'Link do PDF': [pdf_link_text] * max_len
    })

    return df
if __name__ == "__main__":
    # Chama a função do main para obter o DataFrame
    df_links_tipos = processar_publicacoes(caminho_do_csv)
# DataFrame para armazenar as informações extraídas de "Publicações - Livros (todos os anos)"
df_livros = pd.DataFrame(columns=['Data de Criação', 'Título do Livro', 'Categoria', 'Organizadores', 'Link do PDF'])

# Itera sobre as linhas do DataFrame original
for index, row in df_links_tipos.iterrows():
    # Verifica se o tipo é "Publicações - Livros (todos os anos)"
    if row['Tipo 2'] == 'Publicações - Livros (todos os anos)':
        # Realiza a requisição HTTP para a URL da linha atual
        response = requests.get(row['Link'])

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Chama a função para extrair as informações da página
            df_page = extrair_informacoes_livro(response.text)

            # Adiciona as informações extraídas ao DataFrame principal
            if df_page is not None:
                df_livros = pd.concat([df_livros, df_page], ignore_index=True)

            # Aguarda um intervalo de tempo (opcional, para evitar sobrecarga no servidor)
            time.sleep(1)
        else:
            print(f"Erro na requisição para {row['Link']}. Código de status: {response.status_code}")

# Mostra o DataFrame com todas as informações extraídas
print(df_livros)
