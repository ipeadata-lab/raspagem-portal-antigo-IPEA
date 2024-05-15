library(openxlsx)
library(readxl)
library(tools)

# Função para calcular o hash MD5 de um arquivo e verificar a existência do arquivo
calcular_hash_md5 <- function(arquivo) {
  tryCatch(
    {
      # Check if the file exists
      if (!file.exists(arquivo)) {
        # If the file doesn't exist, return "Não Encontrado" and mark Arquivo_Existe as "Não Encontrado"
        return(list(HASH_MD5 = 'Não Encontrado', Arquivo_Existe = 'Não Encontrado'))
      }
      
      # Calculate MD5 hash
      hash_md5 <- md5sum(arquivo)
      
      return(list(HASH_MD5 = hash_md5, Arquivo_Existe = 'Existe'))
    },
    error = function(e) {
      message(paste("Erro ao calcular o hash para o arquivo:", arquivo))
      return(list(HASH_MD5 = 'Erro ao calcular o hash', Arquivo_Existe = 'Erro'))
    }
  )
}

# Caminho para o arquivo Excel
excel_path <- "C:/Users/B03531855158/Desktop/Tabela2_file_names.xlsx"

# Lê o arquivo Excel
d <- read_excel(excel_path)


# Aplica a função calcular_hash_md5 para cada caminho
hashes <- lapply(d$Caminho, calcular_hash_md5)

# Extrai os valores de hash_md5 e Arquivo_Existe
hash_md5 <- sapply(hashes, function(x) x$HASH_MD5)
arquivo_existe <- sapply(hashes, function(x) x$Arquivo_Existe)

# Adiciona as colunas HASH_MD5 e Arquivo_Existe ao dataframe
d$HASH_MD5 <- hash_md5
d$Arquivo_Existe <- arquivo_existe

# Salva os dados em um novo arquivo Excel
output_excel_path <- "//storage6/usuarios/CGDTI/IpeaDataLab/projetos/repo_conhecimento_Ipea/dados/20240506_arquivos_tabela2_hash_v1.xlsx"
write.xlsx(d, output_excel_path, rowNames = FALSE)

cat("Processo concluído. Arquivo salvo em:", output_excel_path)