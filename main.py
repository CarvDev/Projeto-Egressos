import pandas as pd
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Lendo o CSV e montando um dataframe com Pandas
arquivo = "dados.csv"
try:
    df = pd.read_csv(
        arquivo,
        sep=",",            
        encoding="utf-8"
    )
except OSError as erro:
    print(f"Não foi possível abrir {arquivo}: {erro}")
    os._exit(1)

# Filtrando só as colunas necessárias
colunas = ("2) Qual é o seu vínculo empregatício atual?", "4) Quanto tempo após a conclusão do curso você conseguiu seu primeiro emprego na área de computação?")
vinculo = colunas[0]
emprego = colunas[1]
df = df.filter(items=colunas)

# Removendo o caso "Ainda não consegui"
df = df[df[emprego] != "e) Ainda não consegui"].reset_index(drop=True)

# Removendo respostas abertas. O regex mantém apenas linhas que se inciam com uma
# letra minúscula e são seguidas de um ')', ignorando espaços em branco
for col in colunas:
    df = df[df[col].str.contains(r"^\s*[a-z]\s*\)", na=False)].reset_index(drop=True)

# Imprimindo para demonstrar a nova base de dados
print(df)