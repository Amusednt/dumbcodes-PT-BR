# Autores: Os desenvolvedores do scikit-learn
# SPDX-License-Identifier: BSD-3-Clause

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from sklearn import datasets
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

# Carrega o conjunto de dados Iris
iris = datasets.load_iris()

# Seleciona apenas as duas primeiras características para visualização
X = iris.data[:, 0:2]
y = iris.target

# Obtém o número de características
n_features = X.shape[1]

# Define o valor de regularização para os classificadores
C = 10

# Define o kernel para o classificador Gaussian Process
kernel = 1.0 * RBF([1.0, 1.0])  # para GPC

# Cria diferentes classificadores
classifiers = {
    "L1 logístico": LogisticRegression(C=C, penalty="l1", solver="saga", max_iter=10000),
    "L2 logístico (Multinomial)": LogisticRegression(
        C=C, penalty="l2", solver="saga", max_iter=10000
    ),
    "L2 logístico (OvR)": OneVsRestClassifier(
        LogisticRegression(C=C, penalty="l2", solver="saga", max_iter=10000)
    ),
    "Linear SVC": SVC(kernel="linear", C=C, probability=True, random_state=0),
    "GPC": GaussianProcessClassifier(kernel),
}

# Obtém o número de classificadores
n_classifiers = len(classifiers)

# Cria uma figura com subplots para visualizar os resultados
fig, axes = plt.subplots(
    nrows=n_classifiers,
    ncols=len(iris.target_names),
    figsize=(3 * 2, n_classifiers * 2),
)

# Itera sobre os classificadores e plota os resultados
for classifier_idx, (name, classifier) in enumerate(classifiers.items()):
    # Treina o classificador e obtém as previsões
    y_pred = classifier.fit(X, y).predict(X)
    
    # Calcula a acurácia do classificador
    accuracy = accuracy_score(y, y_pred)
    print(f"Acurácia (treinamento) para {name}: {accuracy:0.1%}")
    
    # Plota a probabilidade estimada pelo classificador para cada classe
    for label in np.unique(y):
        disp = DecisionBoundaryDisplay.from_estimator(
            classifier,
            X,
            response_method="predict_proba",
            class_of_interest=label,
            ax=axes[classifier_idx, label],
            vmin=0,
            vmax=1,
        )
        axes[classifier_idx, label].set_title(f"Classe {label}")
        
        # Plota os dados previstos para pertencer à classe atual
        mask_y_pred = y_pred == label
        axes[classifier_idx, label].scatter(
            X[mask_y_pred, 0], X[mask_y_pred, 1], marker="o", c="w", edgecolor="k"
        )
        axes[classifier_idx, label].set(xticks=(), yticks=())
    
    # Define o título do eixo y para o classificador atual
    axes[classifier_idx, 0].set_ylabel(name)

# Cria uma barra de cores para a probabilidade
ax = plt.axes([0.15, 0.04, 0.7, 0.02])
plt.title("Probabilidade")
_ = plt.colorbar(
    cm.ScalarMappable(norm=None, cmap="viridis"), cax=ax, orientation="horizontal"
)

# Exibe a figura
plt.show()