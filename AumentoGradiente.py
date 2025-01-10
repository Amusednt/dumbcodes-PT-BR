# Importando as bibliotecas necessárias
import xgboost as xgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Carregando um conjunto de dados de exemplo (Iris dataset)
data = load_iris()
X = data.data  # Características (4 variáveis)
y = data.target  # Classes (3 tipos de flores)

# Dividindo o conjunto de dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Criando o modelo XGBoost (Gradient Boosting)
model = xgb.XGBClassifier(objective='multi:softmax', num_class=3, random_state=42)

# Treinando o modelo com os dados de treino
model.fit(X_train, y_train)

# Fazendo previsões com os dados de teste
y_pred = model.predict(X_test)

# Avaliando a precisão do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo XGBoost: {accuracy * 100:.2f}%")