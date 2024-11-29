
# Análise de Acidentes de Trânsito no Brasil (2021-2024)

Este projeto realiza a análise de dados de acidentes de trânsito no Brasil dos anos 2021 a 2024. O objetivo é processar, limpar, consolidar e explorar os dados para identificar padrões, realizar análises e gerar insights úteis.

## Estrutura do Projeto

### 1. Configuração do Ambiente

Foi configurado um ambiente Python para garantir a reprodutibilidade do projeto:

1. Criar um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```
2. Instalar as dependências:
   ```bash
   pip install pandas matplotlib
   ```
3. Salvar as dependências:
   ```bash
   pip freeze > requirements.txt
   ```

---

### 2. Tratamento dos Arquivos

#### **Padronização**
Substituímos delimitadores inconsistentes (`','` para `';'`) nos arquivos CSV para garantir a leitura correta:

```python
# Substituir ',' por ';' e salvar o arquivo padronizado
with open("dados/2022_corrigido.csv", "r") as file:
    content = file.read().replace(",", ";")

with open("dados/2022_padronizado.csv", "w") as file:
    file.write(content)
```

#### **Eliminação de Colunas Desnecessárias**
Mantivemos apenas as primeiras 30 colunas relevantes para a análise:

```python
dados = pd.read_csv("dados/2022_padronizado.csv", delimiter=";")
dados = dados.iloc[:, :30]
dados.to_csv("dados/2022_atualizados.csv", sep=";", index=False)
```

---

### 3. Consolidação dos Dados

Os arquivos de 2021 a 2024 foram carregados e consolidados em um único DataFrame:

```python
dados_2021 = pd.read_csv("dados/2021.csv", delimiter=';', encoding='latin1')
dados_2022 = pd.read_csv("dados/2022_atualizados.csv", delimiter=';', encoding='latin1')
dados_2023 = pd.read_csv("dados/2023.csv", delimiter=';', encoding='latin1')
dados_2024 = pd.read_csv("dados/2024_atualizados.csv", delimiter=';', encoding='latin1')

dados_consolidados = pd.concat([dados_2021, dados_2022, dados_2023, dados_2024], ignore_index=True)
dados_consolidados.to_csv("dados/dados_consolidados.csv", index=False)
```

---

### 4. Limpeza e Validação dos Dados

#### **Tratamento de Valores Nulos**
- Para colunas numéricas, substituímos valores nulos pela média:
  ```python
  for col in dados.select_dtypes(include='number'):
      dados[col].fillna(dados[col].mean(), inplace=True)
  ```

- Para colunas categóricas, usamos a moda:
  ```python
  for col in dados.select_dtypes(include='object'):
      dados[col].fillna(dados[col].mode()[0], inplace=True)
  ```

#### **Ajuste de Colunas Numéricas**
Substituímos vírgulas por pontos em valores numéricos para permitir a conversão para `float`:

```python
colunas_para_corrigir = ['km', 'latitude', 'longitude']
for coluna in colunas_para_corrigir:
    dados[coluna] = dados[coluna].str.replace(',', '.', regex=True)
    dados[coluna] = pd.to_numeric(dados[coluna], errors='coerce')
```

#### **Remoção de Valores Inválidos**
Removemos linhas com datas inválidas:

```python
dados['data_inversa'] = pd.to_datetime(dados['data_inversa'], dayfirst=True, errors='coerce')
dados.dropna(subset=['data_inversa'], inplace=True)
```

---

### 5. Engenharia de Atributos

Criamos novos atributos para enriquecer a análise:

- **Informações Derivadas de Datas**:
  ```python
  dados['mes'] = dados['data_inversa'].dt.month
  dados['ano'] = dados['data_inversa'].dt.year
  ```

- **Classificação de Períodos do Dia**:
  ```python
  def periodo_do_dia(hora):
      if 0 <= hora < 6:
          return 'MADRUGADA'
      elif 6 <= hora < 12:
          return 'MANHÃ'
      elif 12 <= hora < 18:
          return 'TARDE'
      else:
          return 'NOITE'

  dados['periodo_dia'] = dados['horario'].str[:2].astype(int).apply(periodo_do_dia)
  ```

- **Cálculo do Total de Feridos**:
  ```python
  dados['total_feridos'] = dados['feridos_leves'] + dados['feridos_graves']
  ```

### 6. Análise Exploratória

#### **Exemplo: Total de Feridos por Tipo de Acidente**
Agrupamos os dados por tipo de acidente e visualizamos os feridos:

```python
import matplotlib.pyplot as plt

feridos_por_tipo = dados.groupby('tipo_acidente')['total_feridos'].sum().sort_values()

plt.figure(figsize=(10, 6))
feridos_por_tipo.plot(kind='bar', color='skyblue', title='Total de Feridos por Tipo de Acidente')
plt.xlabel('Tipo de Acidente')
plt.ylabel('Total de Feridos')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### 7. Resultados

- **Dados Limpos e Consolidados**: Os arquivos foram unificados e tratados, eliminando inconsistências como valores nulos, duplicados e formatos incorretos.
- **Novos Atributos**: Atributos como `mes`, `ano`, `periodo_dia` e `total_feridos` foram adicionados para enriquecer a análise.
- **Gráficos e Insights**: Gráficos foram gerados para explorar padrões nos dados, como o impacto de diferentes tipos de acidentes.


### Como Reproduzir

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   ```
2. Ative o ambiente virtual e instale as dependências:
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. Execute os scripts para carregar, limpar e analisar os dados.

### Execução do Aplicativo:

No terminal, execute o comando

```bash
streamlit run app.py
   ```
Use o menu lateral para navegar entre as diferentes páginas e análises.


