# Importe as bibliotecas necessárias
from sklearn.datasets import load_boston  # Carrega o conjunto de dados de Boston
from sklearn.model_selection import train_test_split  # Divide o conjunto de dados em treinamento e teste
from sklearn.linear_model import LinearRegression  # Modelo de regressão linear
from sklearn.metrics import mean_squared_error  # Métrica de erro quadrático médio

# Carregue o conjunto de dados de Boston
boston = load_boston()

# Divida o conjunto de dados em treinamento e teste (80% para treinamento e 20% para teste)
X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(
    boston.data,  # Características do conjunto de dados
    boston.target,  # Variável resposta do conjunto de dados
    test_size=0.2,  # Tamanho da amostra de teste (20%)
    random_state=42  # Semente aleatória para garantir a reprodutibilidade
)

# Treine um modelo de regressão linear
modelo = LinearRegression()  # Instância do modelo de regressão linear
modelo.fit(X_treinamento, y_treinamento)  # Treine o modelo com os dados de treinamento

# Faça previsões com o modelo treinado
previsoes = modelo.predict(X_teste)  # Previsões do modelo para os dados de teste

# Avalie o modelo com a métrica de erro quadrático médio (MSE)
mse = mean_squared_error(y_teste, previsoes)  # Cálculo do MSE
print(f"MSE: {mse:.2f}")  # Exibe o resultado do MSE com duas casas decimais