import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Configurar o driver do Selenium (certifique-se de especificar o caminho para o ChromeDriver)
driver_service = Service('C:/Users/B04106944103/chromedriver.exe')
driver = webdriver.Chrome(service=driver_service)

# URL da página da web inicial
base_url = "https://portalantigo.ipea.gov.br/portal/index.php?option=com_alphacontent&view=alphacontent&Itemid=357"

# Criar listas para armazenar todos os dados coletados
all_links = []
all_titles = []
all_types = []
all_dates = []
all_pdf_links = []  # Lista para armazenar os links que terminam com ".pdf"

# Função para atualizar links que começam com '/portal'
def fix_link(link):
    if link.startswith('/portal'):
        return 'https://portalantigo.ipea.gov.br' + link
    return link

# Coletar links de todas as páginas
for page_number in range(1, 268):
    # Construir a URL com base no número da página
    page_url = f"{base_url}&limitstart={20 * (page_number - 1)}"

    # Abrir a página da web
    driver.get(page_url)

    # Aguardar um curto período de tempo para que a página seja carregada completamente
    time.sleep(5)

    # Encontrar todas as tags <span> com class "_alphatitle" para os links
    title_elements = driver.find_elements(By.CLASS_NAME, "_alphatitle")

    # Coletar os links, títulos, tipos e datas
    for index, title_element in enumerate(title_elements, start=1):
        try:
            # Obter o link
            link = fix_link(title_element.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            all_links.append(link)

            # Obter o título
            title = title_element.text.strip()
            all_titles.append(title)

            # Construir o seletor XPath para o elemento de tipo com base no índice
            type_selector = f'//*[@id="article{20 * (page_number - 1) + index}"]/div[2]'
            type_element = driver.find_element(By.XPATH, type_selector)
            type = type_element.text.strip()
            all_types.append(type)

            # Construir o seletor XPath para o elemento de data com base no índice
            date_selector = f'//*[@id="features{20 * (page_number - 1) + index}"]/span'
            date_element = driver.find_element(By.XPATH, date_selector)
            date = date_element.text.strip()
            all_dates.append(date)
        except NoSuchElementException:
            # Lidar com o caso em que o elemento não foi encontrado
            all_links.append('')
            all_titles.append('')
            all_types.append('')
            all_dates.append('')

# Coletar links PDF de cada página
for link in all_links:
    driver.get(link)
    pdf_links = [fix_link(a.get_attribute('href')) for a in driver.find_elements(By.TAG_NAME, 'a') if a.get_attribute('href').endswith('.pdf')]
    all_pdf_links.append(pdf_links)

# Criar um DataFrame Pandas com as colunas "Título", "Link", "Tipo", "Data da Publicação" e "PDF Links"
df = pd.DataFrame({'Título': all_titles, 'Link': all_links, 'Tipo': all_types, 'Data da Publicação': all_dates, 'PDF Links': all_pdf_links})

# Imprimir o DataFrame
print(df)

# Salvar os dados em um arquivo CSV
df.to_csv('C:/Users/B04106944103/Documents/csvs_joao/dados_publicacoes_completos_primeiras_cinco_paginas.csv', index=False)

# Fechar o navegador
driver.quit()
