import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.stats import pearsonr

# Carregando os dados do GDP e da Internet
gdp_per_capita = pd.read_excel('E:\Artigo\gdp.xls')
individuos_usando_internet = pd.read_excel('E:\Artigo\internet.xls')

# Preenchendo valores ausentes com 0
gdp_per_capita.fillna(0, inplace=True)
individuos_usando_internet.fillna(0, inplace=True)

# Verificando valores ausentes
print("Valores ausentes em gdp:")
print(gdp_per_capita.isnull().sum())

print("Valores ausentes em internet:")
print(individuos_usando_internet.isnull().sum())

# Mesclando os DataFrames
merged_data = pd.merge(gdp_per_capita[['Data Source', 'DadosUtilizados']],
                       individuos_usando_internet[['Data Source', 'DadosUtilizados']],
                       on='Data Source', how='inner')

# Renomeando as colunas
merged_data.rename(
    columns={'DadosUtilizados_x': 'DadosUtilizados_GDP', 'DadosUtilizados_y': 'DadosUtilizados_Internet'}, inplace=True)

# Ordenando os dados
merged_dataS = merged_data.sort_values(by=['DadosUtilizados_GDP', 'DadosUtilizados_Internet'])

# Salvando os dados mesclados em um arquivo Excel
merged_dataS.to_excel('E:\Artigo\merged_data.xlsx', index=False)

# Filtrar os dados em 'DadosUtilizados_Internet' que são menores ou iguais a 100
merged_dataS = merged_dataS[merged_dataS['DadosUtilizados_Internet'] <= 100]

# Salvar a tabela filtrada em um novo arquivo Excel (opcional)
merged_dataS.to_excel('E:\Artigo\merged_data_filtered.xlsx', index=False)

# Calculando o coeficiente de Pearson
correlation, _ = pearsonr(merged_dataS['DadosUtilizados_GDP'], merged_dataS['DadosUtilizados_Internet'])
print('Coeficiente de Pearson: %.3f' % correlation)

# Realizando a regressão linear
slope, intercept, r_value, p_value, std_err = linregress(merged_dataS['DadosUtilizados_GDP'],
                                                         merged_dataS['DadosUtilizados_Internet'])

# Lista dos países de primeiro mundo e Brasil
countries_to_label = ['Brazil', 'United States', 'United Kingdom', 'French', 'Canada', 'Japan', 'Spsain',
                      'Norway', 'Italy', 'Cayman Islands', 'Luxembourg', 'Liechtenstein', 'Ireland', 'Monaco']

# Plotando o gráfico de dispersão e a linha de regressão
plt.figure(figsize=(10, 5))
plt.scatter(merged_dataS['DadosUtilizados_GDP'], merged_dataS['DadosUtilizados_Internet'], label='Dados originais')
plt.plot(merged_dataS['DadosUtilizados_GDP'], intercept + slope * merged_dataS['DadosUtilizados_GDP'], 'r',
         label='Linha de regressão')

# Adicionando os nomes dos países selecionados
for i, country in enumerate(merged_dataS['Data Source']):
    if country in countries_to_label:
        plt.annotate(country,
                     (merged_dataS['DadosUtilizados_GDP'].iloc[i], merged_dataS['DadosUtilizados_Internet'].iloc[i]))

plt.xlabel('PIB per capita')
plt.ylabel('Usuários de Internet (%)')
plt.title('PIB per capita vs. Usuários de Internet (%)')
plt.legend()
plt.show()
