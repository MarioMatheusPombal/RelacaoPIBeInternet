import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
from scipy.stats import pearsonr

# Carregando os dados do GDP e da Internet
gdp_per_capita = pd.read_excel('E:\Artigo\gdp.xls')
individuos_usando_internet = pd.read_excel('E:\Artigo\internet.xls')

# Preenchendo valores ausentes com 0
gdp_per_capita.fillna(0, inplace=True)
individuos_usando_internet.fillna(0, inplace=True)

# Mesclando os DataFrames
merged_data = pd.merge(gdp_per_capita[['Data Source', 'DadosUtilizados']],
                       individuos_usando_internet[['Data Source', 'DadosUtilizados']],
                       on='Data Source', how='inner')

# Renomeando as colunas
merged_data.rename(
    columns={'DadosUtilizados_x': 'DadosUtilizados_GDP', 'DadosUtilizados_y': 'DadosUtilizados_Internet'}, inplace=True)

# Ordenando os dados
merged_dataS = merged_data.sort_values(by=['DadosUtilizados_GDP', 'DadosUtilizados_Internet'])

# Filtrar os dados em 'DadosUtilizados_Internet' que são menores ou iguais a 100
merged_dataS = merged_dataS[merged_dataS['DadosUtilizados_Internet'] <= 100]

# Salvando os dados mesclados em um arquivo Excel
merged_dataS.to_excel('E:\Artigo\merged_data.xlsx', index=False)

# Salvar a tabela filtrada em um novo arquivo Excel (opcional)
merged_dataS.to_excel('E:\Artigo\merged_data_filtered.xlsx', index=False)

# Normalização linear para o intervalo de 0 a 100
min_value = merged_dataS['DadosUtilizados_GDP'].min()
max_value = merged_dataS['DadosUtilizados_GDP'].max()
merged_dataS['DadosUtilizados_GDP_Normalizado'] = ((merged_dataS['DadosUtilizados_GDP'] - min_value) / (
        max_value - min_value)) * 100
min_value = merged_dataS['DadosUtilizados_Internet'].min()
max_value = merged_dataS['DadosUtilizados_Internet'].max()
merged_dataS['DadosUtilizados_Internet_Normalizado'] = ((merged_dataS['DadosUtilizados_Internet'] - min_value) / (
        max_value - min_value)) * 100

# Arredondar para dígitos após o ponto decimal
merged_dataS['DadosUtilizados_GDP_Normalizado'] = merged_dataS['DadosUtilizados_GDP_Normalizado'].round(2)
merged_dataS['DadosUtilizados_Internet_Normalizado'] = merged_dataS['DadosUtilizados_Internet_Normalizado'].round(2)

merged_dataS.to_excel('E:\Artigo\merged_data_normalized.xlsx', index=False)

# Realizando a regressão linear
slope, intercept, r_value, p_value, std_err = linregress(merged_dataS['DadosUtilizados_GDP'],
                                                         merged_dataS['DadosUtilizados_Internet'])

# Lista dos países de primeiro mundo e Brasil
countries_to_label = ['Brazil', 'United States', 'French', 'Canada', 'Japan', 'Spsain',
                      'Norway', 'Italy', 'Luxembourg', 'Liechtenstein', 'Ireland', 'Monaco',
                      'India', 'Bangladesh', 'Uganda', 'Nigeria', 'Kenya', 'Ghana', 'Zimbabwe',
                      'Egypt', 'Korea, Rep.', 'North Korea', 'China', 'Russia']

# Plotando o gráfico de dispersão e a linha de regressão
plt.figure(figsize=(10, 5))

# Filtrando apenas os países com dados diferentes de zero em ambas as tabelas
filtered_data = merged_dataS[(merged_dataS['DadosUtilizados_GDP_Normalizado'] > 0) &
                             (merged_dataS['DadosUtilizados_Internet'] > 0)]

plt.scatter(filtered_data['DadosUtilizados_GDP_Normalizado'], filtered_data['DadosUtilizados_Internet'],
            label='Dados originais')
plt.plot(filtered_data['DadosUtilizados_GDP_Normalizado'], intercept + slope * filtered_data['DadosUtilizados_GDP'],
         'r',
         label='Linha de regressão')

# Adicionando os nomes dos países selecionados
for i, country in enumerate(merged_dataS['Data Source']):
    if country in countries_to_label:
        plt.annotate(country,
                     (merged_dataS['DadosUtilizados_GDP_Normalizado'].iloc[i],
                      merged_dataS['DadosUtilizados_Internet'].iloc[i]))

# Adicionando os nomes dos países com menos de 40% de acesso à internet
for i, country in enumerate(merged_dataS['Data Source']):
    if country in countries_to_label and merged_dataS['DadosUtilizados_Internet'].iloc[i] < 40:
        plt.annotate(country,
                     (merged_dataS['DadosUtilizados_GDP_Normalizado'].iloc[i],
                      merged_dataS['DadosUtilizados_Internet'].iloc[i]))

# Limitando o eixo Y para variar de 0 a 100
plt.ylim(0, 110)

# Calculando o coeficiente de Pearson
correlation, _ = pearsonr(filtered_data['DadosUtilizados_GDP_Normalizado'], filtered_data['DadosUtilizados_Internet'])
print('Coeficiente de Pearson: %.3f' % correlation)

# Realizando a regressão linear
slope, intercept, r_value, p_value, std_err = linregress(filtered_data['DadosUtilizados_GDP_Normalizado'],
                                                         filtered_data['DadosUtilizados_Internet'])

# Imprimindo os resultados da regressão linear
print('Regressão Linear:', 'y =', slope.round(2), 'x +', intercept.round(2))
print('Inclinação (slope):', slope)
print('Interceptação (intercept):', intercept)
print('Coeficiente de determinação (r-squared):', r_value**2)
print('Valor p:', p_value)
print('Erro padrão:', std_err)

plt.xlabel('PIB per capita Normalizado (0-100)')
plt.ylabel('Usuários de Internet (%)')
plt.title('PIB per capita Normalizado vs. Usuários de Internet (%)')
plt.legend()
plt.show()
