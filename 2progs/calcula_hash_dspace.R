library(readxl)
library(openxlsx)
library(tools)

# Função para calcular o hash MD5 de um arquivo usando md5sum
calcular_hash_md5 <- function(arquivo) {
  hash_md5 <- md5sum(arquivo)
  return(hash_md5)
}

# Caminho para o arquivo Excel
excel_path <- "//storage6/usuarios/CGDTI/IpeaDataLab/projetos/repo_conhecimento_Ipea/dados/20240506_arquivos_dspace.xlsx"

# Lê o arquivo Excel
d <- read_excel(excel_path)
d$full_path <- gsub("\\\\", "/", d$caminho_absoluto_windows)

# Filtra os arquivos que existem
d <- d[file.exists(d$full_path), ]

# Calcula o hash MD5 e armazena em uma nova coluna
d$HASH_MD5 <- sapply(d$full_path, calcular_hash_md5)

# Salva os dados em um novo arquivo Excel
output_excel_path <- "//storage6/usuarios/CGDTI/IpeaDataLab/projetos/repo_conhecimento_Ipea/dados/20240506_arquivos_dspace_com_hash.xlsx"
write.xlsx(d, output_excel_path, rowNames = FALSE)

cat("Processo concluído. Arquivo salvo em:", output_excel_path)
