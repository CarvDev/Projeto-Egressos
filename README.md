# Projeto Egressos CIC-UESC

Projeto de extensão **Avaliação de Egressos do Curso de Ciência da Computação da UESC**, desenvolvido no contexto do **Projeto Extensionista Integrador I – PEI I (2026.2)**.

O projeto analisa respostas de egressos do curso por meio de técnicas estatísticas, com ênfase na **correlação de Spearman**, para identificar relações entre aspectos da formação acadêmica e da trajetória profissional dos participantes.

## Objetivo

Avaliar, de forma estatística, a correlação entre "tempo de graduação" e "atuação profissional na área da computação" a partir da base de dados disponível, então verificar a significância estatística e produzir gráficos e uma interpretação textual dos resultados.

## Base de dados

O arquivo [`dados.csv`](dados.csv) contém as respostas do formulário aplicado aos egressos:

- **63 respostas** (além do cabeçalho);
- **16 questões**;
- Perguntas sobre vínculo empregatício, ocupação, tempo até o primeiro emprego, satisfação com a trajetória, avaliação da formação, pós-graduação, vínculo com IES, relevância dos conteúdos, recomendação do curso, desenvolvimento pessoal, dedicação aos estudos, envolvimento em atividades, conceito do curso e dos professores, e componentes curriculares ausentes.

## Como executar

### Pré-requisitos

- Python 3.9 ou superior;
- `pip`;
- Ambiente virtual (recomendado).

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

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
python main.py
```

O arquivo `main.py` é o ponto de entrada da análise. Ele deve carregar `dados.csv`, formatar as respostas selecionadas, calcular a correlação de Spearman com o respectivo p-valor e gerar os gráficos e resultados da análise.

## Metodologia

### Correlação de Spearman

A **correlação de Spearman (rho)** é uma medida estatística não paramétrica que avalia a força e a direção da relação entre duas variáveis ordinais, discretas ou contínuas. É indicada para dados ordinais, como escalas de Likert (1 a 5) e ranqueamentos, e para respostas de opinião coletadas em questionários.

O coeficiente varia de **-1 a +1**:

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

### Significância estatística

A significância é avaliada pelo **p-valor**:

- **p ≤ 0,05**: rejeita-se a hipótese nula (H₀); a correlação é estatisticamente significativa;
- **p > 0,05**: não há evidências suficientes para rejeitar H₀; a correlação pode ter ocorrido por acaso.

### Tratamento dos dados

Respostas categóricas ou não ordinais devem ser formatadas para valores numéricos, por exemplo:

- `a)` → 1
- `b)` → 2
- `c)` → 3
- e assim por diante.

Caso as questões escolhidas não sejam correlacionáveis por Spearman, deve-se utilizar outra técnica estatística adequada, como **Pearson**, **Kendall** ou **Kappa**, justificando a escolha.

### Ferramentas

A análise é realizada em **Python**, utilizando:

- `pandas` — leitura e manipulação dos dados;
- `scipy` — cálculo da correlação e do p-valor;
- `seaborn` — construção de gráficos, como o mapa de calor da matriz de correlação;
- `matplotlib` — personalização e exibição dos gráficos.

## Resultados esperados

A execução da análise deve produzir:

- Matriz de correlação de Spearman entre as variáveis selecionadas;
- Mapa de calor (heatmap) da matriz de correlação;
- Coeficiente de correlação (rho) e p-valor para o par de questões analisado;
- Gráficos de convergência e/ou dispersão conforme as orientações do projeto;
- Texto interpretativo dos gráficos, dados e tabelas, com aproximadamente duas páginas.
