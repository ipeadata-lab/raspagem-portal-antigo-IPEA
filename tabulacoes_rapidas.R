library(tidyverse)
library(data.table)


d <- fread('dados_publicacoes_completo.csv')
names(d)
d[, num_pdf := stringr::str_count(`PDF Links`, fixed(".pdf", ignore_case = TRUE))-1]
a <- d[,.N,num_pdf][order(num_pdf)]
a[,pct_tot_num_pdf:=round(N/nrow(d),2)]
d[ num_pdf==0]
d[ pct_tot_num_pdf==0]
d[,.N,Tipo][order(Tipo)] %>% View
