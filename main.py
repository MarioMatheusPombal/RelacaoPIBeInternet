import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import linregress


gdp = pd.read_excel('E:\Artigo\gdp.xls')
internet = pd.read_excel('E:\Artigo\internet.xls')

print('Tratando Dados')
gdp.fillna(0)
internet.fillna(0)

print("Valores ausentes em gdp:")
print(gdp.isnull().sum())

#fazer uma verificação se em algum campo tem algum valor nulo

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
merged_dataS = merged_dataS.dropna(subset=['DadosUtilizados_GDP', 'DadosUtilizados_Internet'])

pd.DataFrame(merged_dataS).to_excel('E:\Artigo\merged_data.xlsx')