# Importa as bibliotecas necessárias
# svm: para criar o modelo de Support Vector Machine
# datasets: para carregar conjuntos de dados pré-existentes
from sklearn import svm, datasets

# Carrega o conjunto de dados de dígitos (números de 0 a 9)
# Este conjunto de dados contém imagens de dígitos escritos à mão
digits = datasets.load_digits()

# Cria um classificador de Support Vector Machine (SVC)
# gamma e C são hiperparâmetros que controlam o comportamento do modelo
clf = svm.SVC(gamma=0.001, C=100)

# Define o conjunto de treinamento
# x: dados de entrada (imagens dos dígitos)
# y: rótulos (números correspondentes às imagens)
# [:-1] exclui o último elemento para usar como conjunto de treinamento
x, y = digits.data[:-1], digits.target[:-1]

# Treina o modelo usando os dados de treinamento
clf.fit(x, y)

# Faz uma previsão usando o último elemento do conjunto de dados
# digits.data[-1] é a última imagem do conjunto de dados
y_pred = clf.predict([digits.data[-1]])

# Obtém o rótulo verdadeiro do último elemento do conjunto de dados
y_true = digits.target[-1]

# Exibe a previsão feita pelo modelo
print(y_pred)

# Exibe o rótulo verdadeiro para comparação
print(y_true)