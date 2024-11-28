'''with open("2024.csv", "r") as file:
    content = file.read().replace(",", ";")  # Substituir ',' por ';'

# Salvar o conteúdo padronizado
with open("2024_padronizado.csv", "w") as file:
    file.write(content)'''
# Abrir o arquivo para identificar linhas inconsistentes

import csv
import pandas as pd

with open("dados/2022.csv", "r", encoding="utf-8") as file:
    linhas = file.readlines()

# Identificar o número de colunas em cada linha
for i, linha in enumerate(linhas):
    colunas = linha.split(",")
    if len(colunas) != 30:  # Substitua 30 pelo número correto de colunas esperadas
        print(f"Linha {i + 1} tem {len(colunas)} colunas: {linha}")


# Reprocessar o arquivo corrigindo problemas
with open("dados/2022.csv", "r", encoding="utf-8") as infile, open("2022_corrigido.csv", "w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile, delimiter=",", quotechar='"', skipinitialspace=True)
    writer = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for row in reader:
        # Corrigir linhas com problemas ou remover colunas extras
        if len(row) != 30:  # Ajuste o número conforme o esperado
            print(f"Linha corrigida ou ignorada: {row}")
            continue  # Pule ou ajuste essas linhas
        writer.writerow(row)

# Carregar o arquivo corrigido no pandas
dados_2022 = pd.read_csv("dados/2022_corrigido.csv", delimiter=",", quotechar='"')
print(dados_2022.info())