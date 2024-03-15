library(tidyverse)
library(data.table)


d <- fread('dados_publicacoes_completo.csv')
t1 <- fread('dados_1a_tabela.csv')

#combine them
d %>% setnames(c('Link','Tipo'     ),
               c('link','tipo_orig'))
d[,.(dups=.N),link][,.N,dups] #unique
t1[,.(dups=.N),link][,.N,dups] #unique
d <- t1[d,on='link'] 
d %>% str

d[, num_pdf := stringr::str_count(`PDF Links`, fixed(".pdf", ignore_case = TRUE))-1]
d[num_pdf!=0,.(mean_num_pdf=mean(num_pdf),median_num_pdf=median(num_pdf),
               min_num_pdf=min(num_pdf),max_num_pdf=max(num_pdf)),tipo]
a <- d[,.N,num_pdf][order(num_pdf)]
a[,pct_tot_num_pdf:=round(N/nrow(d),2)]
d[ num_pdf==0]
d[ pct_tot_num_pdf==0]



t1[,.N,tipo][order(tipo)] %>% View
t1[,.N,titulo]
t1[,.N,fonte]
t1[,.N,data_publicacao][order(data_publicacao)]
t1 %>% str
t1[,data_publicacao:=data_publicacao %>% dmy]


