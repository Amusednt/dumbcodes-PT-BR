import time
import numpy as np
from sklearn.datasets import make_classification
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import FixedThresholdClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier

# Geração de dados
X, y = make_classification(n_samples=1000, random_state=0)

# Treinamento do classificador
start = time.time()
classifier = SGDClassifier().fit(X, y)
print(f"Fitting the classifier took {(time.time() - start) * 1_000:.2f} milliseconds")

# Treinamento do classificador com threshold
start = time.time()
threshold_classifier = FixedThresholdClassifier(
    estimator=FrozenEstimator(classifier), threshold=0.9
).fit(X, y)
print(
    f"Fitting the threshold classifier took {(time.time() - start) * 1_000:.2f} "
    "milliseconds"
)

# Separação de dados para validação
X_val = X[:200]
y_val = y[:200]
X = X[200:]
y = y[200:]

# Busca de parâmetros com GridSearchCV
from sklearn.base import BaseEstimator
class EstimatorWithValidationSet(BaseEstimator):
    def __init__(self, param_to_optimize):
        self.param_to_optimize = param_to_optimize

    def fit(self, X, y, X_val=None, y_val=None):
        # Simula o treinamento com os dados de validação
        if X_val is not None and y_val is not None:
            print(f"Treinando com X_val={X_val.shape} e y_val={y_val.shape}")
        return self

    def predict(self, X):
        return np.zeros(X.shape[0])

est_gs = GridSearchCV(
    Pipeline(
        (
            StandardScaler(),
            EstimatorWithValidationSet(0).set_fit_request(X_val=True, y_val=True),
        ),
        # telling pipeline to transform these inputs up to the step which is
        # requesting them.
        transform_input=["X_val"],
    ),
    param_grid={"estimatorwithvalidationset__param_to_optimize": list(range(5))},
    cv=5,
).fit(X, y, X_val=X_val, y_val=y_val)

# Treinamento do classificador ExtraTrees
X = np.array([0, 1, 6, np.nan]).reshape(-1, 1)
y = [0, 0, 1, 1]

forest = ExtraTreesClassifier(random_state=0).fit(X, y)
forest.predict(X)