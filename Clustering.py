# Importar bibliotecas necessárias
import numpy as np
from sklearn.datasets import load_digits
from time import time
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Carregar o conjunto de dados
data, labels = load_digits(return_X_y=True)
(n_samples, n_features), n_digits = data.shape, np.unique(labels).size

# Imprimir informações sobre o conjunto de dados
print(f"# digits: {n_digits}; # samples: {n_samples}; # features {n_features}")

# Definir a função de avaliação
def bench_k_means(kmeans, name, data, labels):
    """
    Benchmark para avaliar os métodos de inicialização do KMeans.

    Parâmetros
    ----------
    kmeans : KMeans instance
        Uma instância de KMeans com a inicialização já definida.
    name : str
        Nome dado à estratégia. Será usado para mostrar os resultados em uma tabela.
    data : ndarray de forma (n_samples, n_features)
        Os dados a serem agrupados.
    labels : ndarray de forma (n_samples,)
        As labels usadas para calcular as métricas de agrupamento que requerem supervisão.
    """
    t0 = time()
    estimator = make_pipeline(StandardScaler(), kmeans).fit(data)
    fit_time = time() - t0
    results = [name, fit_time, estimator[-1].inertia_]

    # Definir as métricas que requerem apenas as labels verdadeiras e as labels estimadas
    clustering_metrics = [
        metrics.homogeneity_score,
        metrics.completeness_score,
        metrics.v_measure_score,
        metrics.adjusted_rand_score,
        metrics.adjusted_mutual_info_score,
    ]
    results += [m(labels, estimator[-1].labels_) for m in clustering_metrics]

    # A métrica de silhueta requer o conjunto de dados completo
    results += [
        metrics.silhouette_score(
            data,
            estimator[-1].labels_,
            metric="euclidean",
            sample_size=300,
        )
    ]

    # Mostrar os resultados
    formatter_result = (
        "{:9s}\t{:.3f}s\t{:.0f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}"
    )
    print(formatter_result.format(*results))

# Executar o benchmark
print(82 * "_")
print("init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette")

kmeans = KMeans(init="k-means++", n_clusters=n_digits, n_init=4, random_state=0)
bench_k_means(kmeans=kmeans, name="k-means++", data=data, labels=labels)

kmeans = KMeans(init="random", n_clusters=n_digits, n_init=4, random_state=0)
bench_k_means(kmeans=kmeans, name="random", data=data, labels=labels)

pca = PCA(n_components=n_digits).fit(data)
kmeans = KMeans(init=pca.components_, n_clusters=n_digits, n_init=1)
bench_k_means(kmeans=kmeans, name="PCA-based", data=data, labels=labels)

print(82 * "_")

# Visualizar os resultados em um espaço reduzido por PCA
reduced_data = PCA(n_components=2).fit_transform(data)
kmeans = KMeans(init="k-means++", n_clusters=n_digits, n_init=4)
kmeans.fit(reduced_data)

# Tamanho da malha. Diminuir para aumentar a qualidade da VQ.
h = 0.02  # ponto na malha [x_min, x_max]x[y_min, y_max].

# Plotar a fronteira de decisão. Para isso, atribuiremos uma cor a cada
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obter labels para cada ponto na malha. Usar o último modelo treinado.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Colocar o resultado em um plot de cores
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(
    Z,
    interpolation="nearest",
    extent=(xx.min(), xx.max(), yy.min(), yy.max()),
    cmap=plt.cm.Paired,
    aspect="auto",
    origin="lower",
)

plt.plot(reduced_data[:, 0], reduced_data[:, 1], "k.", markersize=2)
# Plotar os centroides como um X branco
centroids = kmeans.cluster_centers_
plt.scatter(
    centroids[:, 0],
    centroids[:, 1],
    marker="x",
    s=169,
    linewidths=3,
    color="w",
    zorder=10,
)
plt.title(
    "Agrupamento K-means no conjunto de dados de dígitos (dados reduzidos por PCA)\n"
    "Centroides são marcados com um X branco"
)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()