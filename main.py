import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import linregress


gdp = pd.read_excel('E:\Artigo\gdp.xls')
internet = pd.read_excel('E:\Artigo\internet.xls')

print('Tratando Dados')

print("Valores ausentes em gdp:")
print(gdp.isnull().sum())

print("Valores ausentes em internet:")
print(internet.isnull().sum())

print('---------------------------')
columns_to_keep = ['Data Source', 'DadosUtilizados']
merged_data = pd.merge(gdp[['Data Source', 'DadosUtilizados']], internet[['Data Source', 'DadosUtilizados']],
                       on='Data Source', how='inner')
merged_data.rename(
    columns={'DadosUtilizados_x': 'DadosUtilizados_GDP', 'DadosUtilizados_y': 'DadosUtilizados_Internet'}, inplace=True)
merged_dataS = merged_data.sort_values(by=['DadosUtilizados_GDP', 'DadosUtilizados_Internet'])
for indice, linha in merged_dataS.iterrows():
    print(f'Índice: {indice}')
    for coluna, valor in linha.items():
        print(f'Coluna: {coluna}, Valor: {valor}')
    print('\n')
print('---------------------------')

merged_data = merged_data.dropna(subset=['DadosUtilizados_GDP', 'DadosUtilizados_Internet'])

print('---------------------------')
print('CALCULOS')
x = merged_data['DadosUtilizados_GDP']
y = merged_data['DadosUtilizados_Internet']

correlacao = x.corr(y)
print(f"Correlação entre as colunas: {correlacao}")

cInclinacao, cInterceptacao, cValorDeterminacao, p_value, std_err = linregress(x, y)
print(f"Coeficiente de inclinação (slope): {cInclinacao}")
print(f"Coeficiente de interceptação (intercept): {cInterceptacao}")
print(f"Coeficiente de determinação (r-squared): {cValorDeterminacao ** 2}")

plt.scatter(x, y, label='Dados')
plt.plot(x, cInclinacao * x + cInterceptacao, color='red', label='Regressão Linear')
plt.xlabel('DadosUtilizados_GDP')
plt.ylabel('DadosUtilizados_Internet')
plt.legend()
plt.show()
print('---------------------------')
