# Importando as bibliotecas necessárias
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Criando um conjunto de dados fictício
# Suponha que estamos tentando prever o tipo de flor com base no comprimento e largura da pétala
# X representa as características (comprimento e largura da pétala)
# y representa as classes (tipo de flor)
X = np.array([[5.1, 3.5], [4.9, 3.0], [6.0, 2.7], [5.8, 2.8], [5.5, 2.3]])
y = np.array([0, 0, 1, 1, 1])  # 0 para uma classe de flor, 1 para outra

# Dividindo o conjunto de dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Criando o modelo Naive Bayes
model = GaussianNB()

# Treinando o modelo com os dados de treino
model.fit(X_train, y_train)

# Fazendo previsões com os dados de teste
y_pred = model.predict(X_test)

# Avaliando a precisão do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy * 100:.2f}%")