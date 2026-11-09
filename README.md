# Projeto Egressos CIC-UESC

Projeto de extensão **Avaliação de Egressos do Curso de Ciência da Computação da UESC**, desenvolvido no contexto do **Projeto Extensionista Integrador I – PEI I (2026.2)**.

O projeto analisa respostas de egressos do curso por meio de técnicas estatísticas não paramétricas (**correlação de Spearman**, **teste de Kruskal-Wallis** e **post-hoc de Dunn**) para identificar relações entre aspectos da formação acadêmica e da trajetória profissional dos participantes.

## Objetivo

Avaliar, de forma estatística, **quando** os egressos conseguem o primeiro emprego na área de computação **em relação à formatura** (questão 4: antes da formatura, até 6 meses, de 6 meses a 1 ano ou de 1 a 10 anos após) e se esse momento se relaciona com o **vínculo atual** do egresso (questão 2: Autônomo, PJ, Empresa estrangeira, CLT ou Servidor). O vínculo é o de hoje, e não necessariamente o do primeiro emprego. Também são verificadas a significância estatística e produzidos gráficos e uma interpretação textual dos resultados.

## Base de dados

O arquivo [`dados.csv`](dados.csv) contém as respostas do formulário aplicado aos egressos:

- **63 respostas** (além do cabeçalho);
- **16 questões**;
- Perguntas sobre vínculo empregatício, ocupação, tempo até o primeiro emprego, satisfação com a trajetória, avaliação da formação, pós-graduação, vínculo com IES, relevância dos conteúdos, recomendação do curso, desenvolvimento pessoal, dedicação aos estudos, envolvimento em atividades, conceito do curso e dos professores, e componentes curriculares ausentes.

## Estrutura do projeto

```
Projeto-Egressos/
├── main.py                    # análise: Spearman, Kruskal-Wallis e Dunn
├── dados.csv                  # respostas do formulário
├── requirements.txt           # dependências Python
├── README.md                  # este arquivo
├── spearman_heatmap.png       # gerado pela execução
├── kruskal_boxplot.png        # gerado pela execução
└── kruskal_dunn_heatmap.png   # gerado pela execução
```

## Como executar

### Pré-requisitos

- Python 3.9 ou superior;
- `pip`;
- Ambiente virtual (recomendado);
- Arquivo `dados.csv` na mesma pasta do `main.py`.

### Passo a passo

1. Clone o repositório e acesse o diretório:

```bash
git clone https://github.com/CarvDev/Projeto-Egressos
cd Projeto-Egressos
```

2. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Instale as dependências (`pandas`, `numpy`, `scipy`, `matplotlib` e `seaborn`, listadas em `requirements.txt`):

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
python main.py
```

O arquivo `main.py` é o ponto de entrada da análise. Ele carrega `dados.csv`, formata as respostas selecionadas, calcula a correlação de Spearman, o teste de Kruskal-Wallis e o post-hoc de Dunn, imprime as estatísticas no terminal e salva os gráficos na pasta do projeto.

### Arquivos gerados

| Arquivo | Conteúdo |
| --- | --- |
| `spearman_heatmap.png` | Heatmap de contagem de egressos (vínculo atual × momento do 1º emprego), com rho e p-valor |
| `kruskal_boxplot.png` | Boxplot com pontos individuais, mediana e média do momento do 1º emprego por vínculo atual |
| `kruskal_dunn_heatmap.png` | Heatmap dos p-valores ajustados (Bonferroni) das comparações par a par de Dunn entre vínculos atuais |

## Metodologia

### Tratamento dos dados

1. Seleção das questões 2 (vínculo atual) e 4 (momento do 1º emprego em relação à formatura);
2. Exclusão dos egressos que responderam **"Ainda não consegui"** (4 respostas) e das respostas que não seguem o formato de alternativa (`a)`, `b)`, ...), resultando em **n = 59**;
3. Conversão das alternativas em valores numéricos:

| Momento do 1º emprego (em relação à formatura) | Código | Vínculo atual | Código |
| --- | --- | --- | --- |
| Antes da formatura | 0 | Autônomo / Freelancer | 1 |
| Até 6 meses após | 1 | PJ (empreendedor) | 2 |
| Entre 6 meses e 1 ano após | 2 | Empresa estrangeira | 3 |
| Entre 1 e 10 anos após | 3 | CLT | 4 |
| | | Servidor público | 5 |

> A ordenação dos vínculos atuais é uma **suposição** do pesquisador, necessária para o Spearman. Por isso o Kruskal-Wallis, que não depende dessa ordem, é usado como complemento.

Caso as questões escolhidas não sejam correlacionáveis por Spearman, deve-se utilizar outra técnica estatística adequada, como **Pearson**, **Kendall** ou **Kappa**, justificando a escolha.

### Por que usar mais de um teste?

As variáveis são ordinais/categóricas, com muitos empates e grupos pequenos, o que inviabiliza testes paramétricos. Foram usados testes baseados em postos, que respondem a perguntas complementares:

- **Correlação de Spearman:** mede a existência, a direção e a força de uma tendência monotônica entre as duas variáveis, assumindo uma ordem para os vínculos;
- **Kruskal-Wallis:** trata o vínculo como categoria nominal (sem ordem) e testa se ao menos um grupo difere dos demais quanto ao momento do 1º emprego. O tamanho de efeito é dado por ε² = H / (N − 1);
- **Post-hoc de Dunn (correção de Bonferroni):** indica quais pares de vínculos diferem entre si, com correção de empates. É interpretado como análise exploratória quando o Kruskal-Wallis não é significativo.

### Correlação de Spearman

A **correlação de Spearman (rho)** é uma medida estatística não paramétrica que avalia a força e a direção da relação entre duas variáveis ordinais, discretas ou contínuas. O coeficiente varia de **-1 a +1**:

| Intervalo do coeficiente | Força da relação |
| --- | --- |
| 0,00 a 0,29 | Muito fraca / desprezível |
| 0,30 a 0,49 | Fraca |
| 0,50 a 0,69 | Moderada |
| 0,70 a 0,89 | Forte |
| 0,90 a 1,00 | Muito forte / perfeita |

Direção da relação:

- **+1,0**: correlação positiva perfeita;
- **+0,1 a +0,9**: correlação positiva;
- **0,0**: ausência de correlação;
- **-0,1 a -0,9**: correlação negativa;
- **-1,0**: correlação negativa perfeita.

### Tamanho de efeito (ε²)

| ε² | Interpretação |
| --- | --- |
| < 0,01 | Desprezível |
| 0,01 a 0,08 | Pequeno |
| 0,08 a 0,26 | Moderado |
| ≥ 0,26 | Grande |

### Significância estatística

A significância é avaliada pelo **p-valor**:

- **p ≤ 0,05**: rejeita-se a hipótese nula (H₀); o resultado é estatisticamente significativo;
- **p > 0,05**: não há evidências suficientes para rejeitar H₀; o resultado pode ter ocorrido por acaso.

### Ferramentas

A análise é realizada em **Python**, utilizando:

- `pandas` e `numpy`: leitura e manipulação dos dados;
- `scipy`: Spearman, Kruskal-Wallis, postos e distribuição normal (Dunn);
- `seaborn`: heatmaps, boxplot e stripplot;
- `matplotlib`: personalização e exportação dos gráficos.

As versões mínimas de cada biblioteca estão em [`requirements.txt`](requirements.txt).

## Resultados esperados

A execução da análise deve produzir:

- Coeficiente de correlação (rho) e p-valor de Spearman para o par de questões analisado (vínculo atual × momento do 1º emprego em relação à formatura);
- Mapa de calor (heatmap) de contagem de egressos entre as duas variáveis (`spearman_heatmap.png`);
- Estatística descritiva (n, mediana e média) do momento do 1º emprego por vínculo atual;
- Resultado do teste de Kruskal-Wallis (H, p-valor e ε²) e boxplot por vínculo (`kruskal_boxplot.png`);
- Heatmap dos p-valores ajustados do post-hoc de Dunn (`kruskal_dunn_heatmap.png`);
- Texto interpretativo dos gráficos, dados e tabelas, com aproximadamente duas páginas.

## Autores

* [CarvDev](https://github.com/CarvDev)
* [4mandaCardoso](https://github.com/4mandaCardoso)