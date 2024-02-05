import pandas as pd

def processar_publicacoes(caminho_csv):
    # Gerando Dataframe das Publicações (Tabela 1)
    df = pd.read_csv(caminho_csv)

    # Pré-processando a coluna 'Tipo' removendo "/yyyy"
    df['Tipo 2'] = df['Tipo'].str.replace(r'/\d{4}', '', regex=True)
    df['Tipo 2'] = df['Tipo 2'].str.split('/').str[0]

    # Criando um dataframe de segurança (Cópia)
    df_pub = df.copy()

    # Encontrando Publicações Extintas 
    titulos_publicacoes = [
        "Publicações - Revista Desafios",
        "Publicações - Comunicado do Ipea",
        "Publicações - Série Situação Social",
        "Publicações - Agenda Federativa",
        "Publicações - Conjuntura em Foco",
        "Publicações - Boletim de Conjuntura",
        "Publicações - Conjuntura Industrial",
        "Publicações - Desenvolvimento Fiscal",
        "Publicações - Fiscal Development",
        "Publicações - Sensor Econômico",
        "Publicações - Monitor Internacional",
        "Publicações - IQD",
        "Publicações - Economic Quarterly",
        "Publicações - Sistema de Indicadores e Percepção Social",
        "Publicações - Documentos de Política"
    ]

    # Verificar o match e alterar o tipo para "Publicação Extinta"
    df_pub.loc[df_pub['Tipo 2'].isin(titulos_publicacoes), 'Situação'] = 'Publicação Extinta'

    return df_pub

if __name__ == "__main__":
    # Exemplo de uso
    caminho_do_csv = 'D:\\Users\\B03531855158\\Downloads\\dados_publicacoes_completo.csv'
    resultado_processamento = processar_publicacoes(caminho_do_csv)
    print(resultado_processamento)
