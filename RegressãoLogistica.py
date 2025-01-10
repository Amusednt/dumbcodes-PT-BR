# Importando as bibliotecas necessárias
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Criando um conjunto de dados fictício
# Suponha que estamos tentando prever se vai chover (1) ou não (0) com base em duas características (ex.: temperatura e umidade)
# X representa as características (temperatura e umidade)
# y representa as classes (0 para "não chove", 1 para "chove")
X = np.array([[25, 80], [30, 60], [15, 90], [20, 85], [10, 95]])
y = np.array([0, 0, 1, 1, 1])  # 0 para "não chove", 1 para "chove"

# Dividindo o conjunto de dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Criando o modelo de Regressão Logística
model = LogisticRegression()

# Treinando o modelo com os dados de treino
model.fit(X_train, y_train)

# Fazendo previsões com os dados de teste
y_pred = model.predict(X_test)

# Avaliando a precisão do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy * 100:.2f}%")