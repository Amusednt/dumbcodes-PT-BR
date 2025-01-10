# Importando as bibliotecas necessárias
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Carregando um conjunto de dados de exemplo (Iris dataset)
data = load_iris()
X = data.data  # Características (4 variáveis)
y = data.target  # Classes (3 tipos de flores)

# Dividindo o conjunto de dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Aplicando PCA para reduzir a dimensionalidade
# Reduzindo de 4 variáveis para 2 componentes principais
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Criando um modelo de classificação (Random Forest) para testar a redução dimensional
model = RandomForestClassifier(random_state=42)

# Treinando o modelo com os dados reduzidos
model.fit(X_train_pca, y_train)

# Fazendo previsões com os dados de teste reduzidos
y_pred = model.predict(X_test_pca)

# Avaliando a precisão do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo após redução dimensional: {accuracy * 100:.2f}%")