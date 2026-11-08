import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import kruskal, norm, rankdata, spearmanr
from matplotlib.lines import Line2D  # Necessário para criar a legenda didática

arquivoDados = "dados.csv"
arquivoSpearman = "spearman_heatmap.png"
arquivoKruskalBox = "kruskal_boxplot.png" 
arquivoKruskalDunn = "kruskal_dunn_heatmap.png"


class Cor:
    RESET = "\033[0m"
    VERMELHO = "\033[31m"
    VERDE = "\033[32m"


# Lendo o CSV
try:
    df = pd.read_csv(arquivoDados, sep=",", encoding="utf-8")
except OSError as erro:
    print(
        f"{Cor.VERMELHO}[ERRO]{Cor.RESET} Não foi possível abrir {arquivoDados}: {erro}"
    )
    os._exit(1)

colunas = (
    "2) Qual é o seu vínculo empregatício atual?",
    "4) Quanto tempo após a conclusão do curso você conseguiu seu primeiro emprego na área de computação?",
)
vinculo, emprego = colunas[0], colunas[1]
df = df.filter(items=colunas)

# Removendo o caso "Ainda não consegui"
df = df[df[emprego] != "e) Ainda não consegui"].reset_index(drop=True)

# Mantém linhas que iniciam com letra seguida de ')'
for col in colunas:
    df = df[
        df[col].astype(str).str.contains(r"^\s*[a-zA-Z]\s*\)", na=False)
    ].reset_index(drop=True)

dfSpearman = df.copy()
dfSpearman.columns = ("v", "t")

# Extrai a primeira letra e converte para minúscula
for col in dfSpearman.columns:
    dfSpearman[col] = dfSpearman[col].astype(str).str.strip().str[0].str.lower()

mapaTempo = {"a": 0, "b": 1, "c": 2, "d": 3}
mapaVinculo = {"c": 1, "d": 2, "e": 3, "a": 4, "b": 5}

dfSpearman["t"] = dfSpearman["t"].map(mapaTempo)
dfSpearman["v"] = dfSpearman["v"].map(mapaVinculo)

# Remove nulos gerados por mapeamentos não encontrados
dfSpearman = dfSpearman.dropna(subset=["t", "v"]).reset_index(drop=True)

# Cálculo de Spearman
rho, p = spearmanr(dfSpearman["t"], dfSpearman["v"])
tabelaSpearman = pd.crosstab(dfSpearman["t"], dfSpearman["v"]).reindex(
    index=[0, 1, 2, 3], columns=[1, 2, 3, 4, 5], fill_value=0
)

nomesVinculo = {
    1: "Autônomo",
    2: "PJ",
    3: "Estrangeira",
    4: "CLT",
    5: "Servidor",
}
nomesTempo = {0: "Antes da\nformatura", 1: "Até 6m\napós", 2: "6m a 1a\napós", 3: "1 a 10a\napós"}
tabelaSpearman = tabelaSpearman.rename(index=nomesTempo, columns=nomesVinculo)

# Plot Spearman
plt.figure(figsize=(7, 4))
sns.heatmap(
    tabelaSpearman,
    annot=True,
    fmt="d",
    cmap="coolwarm",
    cbar_kws={"label": "Nº de egressos"},
)
plt.xlabel("Vínculo atual")
plt.ylabel("Momento do 1º emprego\n(em relação à formatura)")
plt.yticks(rotation=0)
plt.title(
    f"Vínculo atual × momento do 1º emprego (n = {len(dfSpearman)})\nSpearman: rho = {rho:.2f}, p = {p:.3f}"
)
plt.tight_layout()

try:
    plt.savefig(arquivoSpearman, dpi=200)
    print(
        f"{Cor.VERDE}[OK]{Cor.RESET} Heatmap de Spearman salvo em {arquivoSpearman}"
    )
except OSError as erro:
    print(
        f"{Cor.VERMELHO}[ERRO]{Cor.RESET} Não foi possível salvar {arquivoSpearman}: {erro}"
    )

plt.close()

# =====================================================================
# KRUSKAL-WALLIS
# =====================================================================
dfKW = dfSpearman.copy()
dfKW["vinculo"] = dfKW["v"].map(nomesVinculo)

ordemVinculo = [nomesVinculo[k] for k in sorted(nomesVinculo)]
grupos = {
    g: dfKW.loc[dfKW["vinculo"] == g, "t"].to_numpy() for g in ordemVinculo
}
grupos = {g: v for g, v in grupos.items() if len(v) > 0}

if len(grupos) < 2:
    print(
        f"{Cor.VERMELHO}[ERRO]{Cor.RESET} Kruskal-Wallis precisa de pelo menos 2 grupos com dados válidos."
    )
    os._exit(1)

H, pKW = kruskal(*grupos.values())
N = len(dfKW)
k = len(grupos)
epsilon2 = H / (N - 1) if N > 1 else 0

efeito = (
    "desprezível"
    if epsilon2 < 0.01
    else "pequeno"
    if epsilon2 < 0.08
    else "moderado"
    if epsilon2 < 0.26
    else "grande"
)

descritiva = (
    dfKW.groupby("vinculo")["t"]
    .agg(n="count", mediana="median", media="mean")
    .reindex([g for g in ordemVinculo if g in grupos])
)

print(f"\n{Cor.VERDE}[Kruskal-Wallis]{Cor.RESET} Momento do 1º emprego por vínculo atual")
print(descritiva.round(2).to_string())
print(
    f"\nH({k - 1}) = {H:.3f} | p = {pKW:.4f} | n = {N} | ε² = {epsilon2:.3f} ({efeito})"
)

# Post-hoc de Dunn
nomes = list(grupos.keys())
todos = np.concatenate([grupos[g] for g in nomes])
ranks = rankdata(todos)
rotulos = np.concatenate([[g] * len(grupos[g]) for g in nomes])
postoMedio = {g: ranks[rotulos == g].mean() for g in nomes}
nGrupo = {g: len(grupos[g]) for g in nomes}

_, contagens = np.unique(todos, return_counts=True)
correcaoEmpates = (
    (contagens**3 - contagens).sum() / (12 * (N - 1)) if N > 1 else 0
)
variancia = N * (N + 1) / 12 - correcaoEmpates

nComp = k * (k - 1) // 2
dunn = pd.DataFrame(1.0, index=nomes, columns=nomes)

for i, a in enumerate(nomes):
    for b in nomes[i + 1 :]:
        denom = np.sqrt(variancia * (1 / nGrupo[a] + 1 / nGrupo[b]))
        z = (postoMedio[a] - postoMedio[b]) / denom if denom != 0 else 0
        pAjust = min(2 * norm.sf(abs(z)) * nComp, 1.0)
        dunn.loc[a, b] = dunn.loc[b, a] = pAjust

# =====================================================================
# Gráfico 1: Boxplot 
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ordemPlot = [g for g in ordemVinculo if g in grupos]

# 1. Cria um leve espalhamento vertical para os pontos não formarem uma reta colada
np.random.seed(42) # Mantém as cores/posições estáveis ao rodar o script novamente
dfKW["t_jitter"] = dfKW["t"] + np.random.uniform(-0.15, 0.15, size=len(dfKW))

# 2. Desenha os pontos coloridos e semi-transparentes ao fundo
sns.stripplot(
    data=dfKW,
    x="vinculo",
    y="t_jitter",
    order=ordemPlot,
    hue="vinculo",
    palette="Set2",
    alpha=0.6,
    size=5,
    jitter=0.25,
    legend=False,
    ax=ax,
    zorder=1
)

# 3. Desenha o Boxplot "vazado" (translúcido) por cima
sns.boxplot(
    data=dfKW,
    x="vinculo",
    y="t",
    order=ordemPlot,
    color="white",
    width=0.45,
    showfliers=False,       # Esconde os outliers redundantes gerados pelo boxplot
    showmeans=True,         # Mostra a média
    meanprops={
        "marker": "D",
        "markerfacecolor": "yellow",
        "markeredgecolor": "black",
        "markersize": "7",
        "zorder": 3
    },
    medianprops={"color": "red", "linewidth": 2.5, "zorder": 3},
    boxprops={"alpha": 0.4, "edgecolor": "black", "linewidth": 1.2, "zorder": 2},
    whiskerprops={"linewidth": 1.2},
    capprops={"linewidth": 1.2},
    ax=ax
)

# Ajusta as escalas do eixo Y para dar "respiro" aos pontos
ax.set_ylim(-0.5, 3.5)
ax.set_yticks(sorted(nomesTempo))
ax.set_yticklabels([nomesTempo[i] for i in sorted(nomesTempo)])
ax.set_xticks(range(len(ordemPlot)))
ax.set_xticklabels([f"{g}\n(n={nGrupo[g]})" for g in ordemPlot])

ax.set_xlabel("Vínculo atual", fontweight="bold", labelpad=10)
ax.set_ylabel("Momento do 1º emprego\n(em relação à formatura)", fontweight="bold", labelpad=10)
ax.set_title(
    f"Distribuição do Momento do 1º Emprego (Boxplot)\nKruskal-Wallis: H({k - 1}) = {H:.2f}, p = {pKW:.3f}, ε² = {epsilon2:.2f}",
    pad=15
)

# 4. Adiciona a legenda explicativa customizada
elementos_legenda = [
    Line2D([0], [0], color='red', lw=3, label='Mediana (valor central)'),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='yellow', markeredgecolor='black', markersize=8, label='Média (tendência geral)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', alpha=0.6, markersize=8, label='Respostas individuais')
]
ax.legend(handles=elementos_legenda, loc='upper left', bbox_to_anchor=(1.02, 1), frameon=True, title="Legenda de Leitura:")

plt.tight_layout()

try:
    plt.savefig(arquivoKruskalBox, dpi=200)
    print(
        f"{Cor.VERDE}[OK]{Cor.RESET} Boxplot Didático salvo em {arquivoKruskalBox}"
    )
except OSError as erro:
    print(
        f"{Cor.VERMELHO}[ERRO]{Cor.RESET} Não foi possível salvar {arquivoKruskalBox}: {erro}"
    )
plt.close()

# Gráfico 2: Heatmap de Dunn
mascara = np.triu(np.ones_like(dunn, dtype=bool))
plt.figure(figsize=(6.5, 5))
sns.heatmap(
    dunn,
    mask=mascara,
    annot=True,
    fmt=".3f",
    cmap="viridis_r",
    vmin=0,
    vmax=1,
    cbar_kws={"label": "p ajustado (Bonferroni)"},
)
plt.title("Post-hoc de Dunn – vínculo atual (comparações pareadas)")
plt.tight_layout()

try:
    plt.savefig(arquivoKruskalDunn, dpi=200)
    print(
        f"{Cor.VERDE}[OK]{Cor.RESET} Heatmap de Dunn salvo em {arquivoKruskalDunn}"
    )
except OSError as erro:
    print(
        f"{Cor.VERMELHO}[ERRO]{Cor.RESET} Não foi possível salvar {arquivoKruskalDunn}: {erro}"
    )
plt.close()