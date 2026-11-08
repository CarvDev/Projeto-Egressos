import pandas as pd
from scipy.stats import spearmanr, kruskal
import seaborn as sns
import matplotlib.pyplot as plt
import os

arquivoDados = "dados.csv"
arquivoSpearman = "spearman_heatmap.png"

class Cor:
    RESET    = "\033[0m"
    VERMELHO = "\033[31m"
    VERDE    = "\033[32m"

# Lendo o CSV e montando um dataframe com Pandas
try:
    df = pd.read_csv(
        arquivoDados,
        sep=",",            
        encoding="utf-8"
    )
except OSError as erro:
    print(f"{Cor.VERMELHO}[ERRO]{Cor.RESET} Não foi possível abrir {arquivoDados}: {erro}")
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


# Criando um novo dataframe para a correlação de spearman:
# Primeiro, copia o dataframe original e renomeia as colunas:
# v para vínculo e t para tempo
dfSpearman = df.copy()
dfSpearman.columns = ("v", "t")

# Depois extrai somente a primeira letra de cada linha, removendo espaços
for col in dfSpearman.columns:
    dfSpearman[col] = dfSpearman[col].str.strip().str[0]

# Por fim mapeia as letras para dados numéricos: 
# Ordinal para tempo e por ordem de formalidade para vínculo 
mapaTempo = {"a": 0, "b": 1, "c": 2, "d": 3}
mapaVinculo = {"c": 1, "d": 2, "e": 3, "a": 4, "b": 5}
dfSpearman["t"] = dfSpearman["t"].map(mapaTempo)
dfSpearman["v"] = dfSpearman["v"].map(mapaVinculo)

# Calculando `rho` e `p` e gerando a tabela com os dados cruzados
rho, p = spearmanr(dfSpearman["t"], dfSpearman["v"])
tabelaSpearman = pd.crosstab(dfSpearman["t"], dfSpearman["v"]).reindex(
    index=[0, 1, 2, 3], columns=[1, 2, 3, 4, 5], fill_value=0)
nomesVinculo = {1: "Autônomo", 2: "PJ", 3: "Estrangeira", 4: "CLT", 5: "Servidor"}
nomesTempo = {0: "Antes", 1: "Até 6m", 2: "6m-1a", 3: "1-10a"}
tabelaSpearman = tabelaSpearman.rename(index=nomesTempo, columns=nomesVinculo)

# Gerando o heatmap de Spearman com a tabela
plt.figure(figsize=(7, 4))
sns.heatmap(tabelaSpearman, annot=True, fmt="d", cmap="coolwarm",
            cbar_kws={"label": "Nº de egressos"})
plt.xlabel("Vínculo")
plt.ylabel("Tempo até 1º emprego")
plt.title(f"Spearman: rho = {rho:.2f}, p = {p:.3f}")
plt.title(f"Vínculo × tempo até o 1º emprego (n = {len(dfSpearman)})\nSpearman: rho = {rho:.2f}, p = {p:.3f}")
plt.tight_layout()

# Salvando como arquivo png
try:
    plt.savefig(arquivoSpearman, dpi=200)
    print(f"{Cor.VERDE}[OK]{Cor.RESET} Heatmap de Spearman gerado e salvo em {arquivoSpearman}")
except OSError as erro:
    print(f"{Cor.VERMELHO}[ERRO]{Cor.RESET} Não foi possível salvar {arquivoSpearman}: {erro}")

plt.close()