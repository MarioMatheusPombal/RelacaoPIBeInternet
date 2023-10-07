import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import linregress
import seaborn as sns

# Leitura dos dados do arquivo Excel
merged_dataS = pd.read_excel('E:\Artigo\merged_data.xlsx')

# Calculando o coeficiente de Pearson
pearson_corr = merged_dataS['DadosUtilizados_GDP'].corr(merged_dataS['DadosUtilizados_Internet'])

# Calculando a regressão linear
slope, intercept, r_value, p_value, std_err = linregress(merged_dataS['DadosUtilizados_GDP'], merged_dataS['DadosUtilizados_Internet'])

# Plotando o gráfico de dispersão e a linha de regressão
plt.figure(figsize=(10, 6))
sns.scatterplot(x='DadosUtilizados_GDP', y='DadosUtilizados_Internet', data=merged_dataS)
plt.plot(merged_dataS['DadosUtilizados_GDP'], intercept + slope * merged_dataS['DadosUtilizados_GDP'], color='red', label='Linha de Regressão')
plt.title('Gráfico de Dispersão com Regressão Linear')
plt.xlabel('PIB')
plt.ylabel('% de acesso a internet')
plt.legend()
plt.grid(True)

# Exibindo o coeficiente de Pearson e os parâmetros da regressão
print(f'Coeficiente de Pearson: {pearson_corr}')
print(f'Regressão Linear: Y = {slope:.2f}X + {intercept:.2f}')
print(f'R-squared: {r_value**2:.2f}')
print(f'Valor p: {p_value:.4f}')
print(f'Erro padrão: {std_err:.2f}')

plt.show()
