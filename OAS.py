# Authors: The scikit-learn developers
# SPDX-License-Identifier: BSD-3-Clause

# Importando bibliotecas necessárias
import matplotlib.pyplot as plt
import numpy as np

# Importando classes e funções específicas do scikit-learn
from sklearn.covariance import OAS
from sklearn.datasets import make_blobs
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Definindo parâmetros para o experimento
n_train = 20  # número de amostras para treinamento
n_test = 200  # número de amostras para teste
n_averages = 50  # número de repetições para a classificação
n_features_max = 75  # número máximo de features
step = 4  # passo para o cálculo do número de features

# Função para gerar dados aleatórios com uma feature discriminativa e o restante como ruído
def generate_data(n_samples, n_features):
    """Generate random blob-ish data with noisy features.

    This returns an array of input data with shape `(n_samples, n_features)`
    and an array of `n_samples` target labels.

    Only one feature contains discriminative information, the other features
    contain only noise.
    """
    # Gerando dados com uma feature discriminativa
    X, y = make_blobs(n_samples=n_samples, n_features=1, centers=[[-2], [2]])

    # Adicionando features não discriminativas (ruído)
    if n_features > 1:
        X = np.hstack([X, np.random.randn(n_samples, n_features - 1)])
    return X, y

# Listas para armazenar a acurácia dos classificadores
acc_clf1, acc_clf2, acc_clf3 = [], [], []

# Loop sobre o número de features
n_features_range = range(1, n_features_max + 1, step)
for n_features in n_features_range:
    score_clf1, score_clf2, score_clf3 = 0, 0, 0
    # Repetindo a classificação várias vezes para obter uma média
    for _ in range(n_averages):
        X, y = generate_data(n_train, n_features)

        # Treinando três diferentes classificadores LDA
        clf1 = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=None).fit(X, y)
        clf2 = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(X, y)
        oa = OAS(store_precision=False, assume_centered=False)
        clf3 = LinearDiscriminantAnalysis(solver="lsqr", covariance_estimator=oa).fit(
            X, y
        )

        # Gerando dados de teste e calculando a acurácia
        X, y = generate_data(n_test, n_features)
        score_clf1 += clf1.score(X, y)
        score_clf2 += clf2.score(X, y)
        score_clf3 += clf3.score(X, y)

    # Armazenando a acurácia média para cada classificador
    acc_clf1.append(score_clf1 / n_averages)
    acc_clf2.append(score_clf2 / n_averages)
    acc_clf3.append(score_clf3 / n_averages)

# Calculando a razão entre o número de features e o número de amostras
features_samples_ratio = np.array(n_features_range) / n_train

# Plotando os resultados
plt.plot(
    features_samples_ratio,
    acc_clf1,
    linewidth=2,
    label="LDA",
    color="gold",
    linestyle="solid",
)
plt.plot(
    features_samples_ratio,
    acc_clf2,
    linewidth=2,
    label="LDA with Ledoit Wolf",
    color="navy",
    linestyle="dashed",
)
plt.plot(
    features_samples_ratio,
    acc_clf3,
    linewidth=2,
    label="LDA with OAS",
    color="red",
    linestyle="dotted",
)

# Configurando os eixos e a legenda do gráfico
plt.xlabel("n_features / n_samples")
plt.ylabel("Classification accuracy")

plt.legend(loc="lower left")
plt.ylim((0.65, 1.0))
plt.suptitle(
    "LDA (Linear Discriminant Analysis) vs. "
    + "\n"
    + "LDA with Ledoit Wolf vs. "
    + "\n"
 + "LDA with OAS (1 discriminative feature)"
)

# Exibindo o gráfico
plt.show()