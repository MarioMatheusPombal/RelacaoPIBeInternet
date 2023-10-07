import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

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
merged_data = pd.merge(gdp_per_capita[['Data Source', 'DadosUtilizados']], individuos_usando_internet[['Data Source', 'DadosUtilizados']],
                       on='Data Source', how='inner')

# Renomeando as colunas
merged_data.rename(columns={'DadosUtilizados_x': 'DadosUtilizados_GDP', 'DadosUtilizados_y': 'DadosUtilizados_Internet'}, inplace=True)

# Ordenando os dados
merged_dataS = merged_data.sort_values(by=['DadosUtilizados_GDP', 'DadosUtilizados_Internet'])

# Salvando os dados mesclados em um arquivo Excel
merged_dataS.to_excel('E:\Artigo\merged_data.xlsx', index=False)

# Filtrar os dados em 'DadosUtilizados_Internet' que são menores ou iguais a 100
merged_dataS = merged_dataS[merged_dataS['DadosUtilizados_Internet'] <= 100]

# Salvar a tabela filtrada em um novo arquivo Excel (opcional)
merged_dataS.to_excel('E:\Artigo\merged_data_filtered.xlsx', index=False)

# Calculando a regressão linear
slope, intercept, r_value, p_value, std_err = linregress(merged_dataS['DadosUtilizados_GDP'], merged_dataS['DadosUtilizados_Internet'])

# Exibindo o coeficiente de Pearson e os parâmetros da regressão
print(f'Coeficiente de Pearson: {r_value:.2f}')
print(f'Regressão Linear: Y = {slope:.2f}X + {intercept:.2f}')
print(f'R-squared: {r_value**2:.2f}')
print(f'Valor p: {p_value:.4f}')
print(f'Erro padrão: {std_err:.2f}')

# Plotando o gráfico de dispersão e a linha de regressão
plt.figure(figsize=(10, 6))
plt.scatter(merged_dataS['DadosUtilizados_GDP'], merged_dataS['DadosUtilizados_Internet'])
plt.plot(merged_dataS['DadosUtilizados_GDP'], intercept + slope * merged_dataS['DadosUtilizados_GDP'], color='red', label='Linha de Regressão')
plt.title('Gráfico de Dispersão com Regressão Linear')
plt.xlabel('GDP per Capita')
plt.ylabel('% de Indivíduos Usando Internet')
plt.legend()
plt.grid(True)

# Mostrando o gráfico
plt.show()
