import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# **Passo 1: Gerar dados de exemplo**
# Vamos criar um conjunto de dados fictício para agrupamento.
np.random.seed(42)
X = np.random.rand(100, 2)  # 100 pontos de dados em 2D

# **Passo 2: Definir o número de clusters (k)**
k = 3  # Número de clusters desejados

# **Passo 3: Inicializar e ajustar o modelo K-Means**
# O KMeans do sklearn faz todo o trabalho pesado: seleciona os centroides iniciais,
# atribui pontos aos clusters e recalcula os centroides até a convergência.
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)

# **Passo 4: Obter os rótulos dos clusters e os centroides**
labels = kmeans.labels_  # Rótulos dos clusters para cada ponto de dados
centroids = kmeans.cluster_centers_  # Coordenadas dos centroides finais

# **Passo 5: Visualizar os clusters e os centroides**
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, label='Centroides')
plt.title('Agrupamento com K-Means')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()