# Importação das bibliotecas necessárias
import tensorflow as tf  # Para construir e treinar o modelo
import torch  # Para pré-processamento dos dados
from torchtext.data import get_tokenizer  # Para tokenização do texto
from torchtext.vocab import build_vocab_from_iterator  # Para criar o vocabulário

# Exemplo de dados de treino (substitua por seus dados reais)
train_data = ["I love this movie!", "This film is terrible.", "What a great experience!", "I hated every second of it."]
labels = [1, 0, 1, 0]  # 1 para positivo, 0 para negativo

# 1. Pré-processamento dos dados (com PyTorch)

# Tokenização: Divide o texto em palavras individuais
tokenizer = get_tokenizer('basic_english')  # Tokenizador básico para inglês

# Aplica o tokenizador aos dados de treino
train_it = map(tokenizer, train_data)

# Criação do vocabulário: Mapeia cada palavra para um índice numérico
vocab = build_vocab_from_iterator(train_it, specials=['<unk>'])  # '<unk>' para palavras desconhecidas
vocab.set_default_index(vocab['<unk>'])  # Define o índice padrão para palavras fora do vocabulário

# Função para converter texto em tensor
def text_to_tensor(text):
    tokens = tokenizer(text)  # Tokeniza o texto
    indexed = [vocab[token] for token in tokens]  # Converte tokens em índices numéricos
    tensor = torch.LongTensor(indexed)  # Cria um tensor do PyTorch
    return tensor

# Prepara os dados de treino (X_train e y_train)
X_train = [text_to_tensor(text) for text in train_data]  # Converte textos em tensores
y_train = labels  # Rótulos correspondentes

# 2. Criação do modelo (com TensorFlow)

# Tamanho do vocabulário e dimensão do embedding
vocab_size = len(vocab)  # Número de palavras no vocabulário
embedding_dim = 16  # Dimensão dos vetores de embedding

# Define o modelo sequencial
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim),  # Camada de embedding
    tf.keras.layers.GlobalAveragePooling1D(),  # Reduz a dimensionalidade
    tf.keras.layers.Dense(1, activation='sigmoid')  # Camada de saída para classificação binária
])

# 3. Treinamento do modelo

# Compila o modelo
model.compile(loss='binary_crossentropy',  # Função de perda para classificação binária
              optimizer='adam',  # Otimizador
              metrics=['accuracy'])  # Métrica de avaliação

# Converte os tensores do PyTorch para arrays do NumPy (compatível com TensorFlow)
import numpy as np
X_train_np = [tensor.numpy() for tensor in X_train]
X_train_padded = tf.keras.preprocessing.sequence.pad_sequences(X_train_np, padding='post')  # Padding para igualar tamanhos

# Treina o modelo
model.fit(X_train_padded, np.array(y_train), epochs=10)  # 10 épocas de treinamento

# 4. Avaliação do modelo

# Exemplo de dados de teste (substitua por seus dados reais)
test_data = ["This is amazing!", "I didn't like it at all."]
test_labels = [1, 0]

# Prepara os dados de teste
X_test = [text_to_tensor(text) for text in test_data]
X_test_np = [tensor.numpy() for tensor in X_test]
X_test_padded = tf.keras.preprocessing.sequence.pad_sequences(X_test_np, padding='post')

# Avalia o modelo
loss, accuracy = model.evaluate(X_test_padded, np.array(test_labels))
print(f"Loss: {loss}, Accuracy: {accuracy}")

# 5. Exemplo de uso do modelo

# Função para prever o sentimento de um texto
def predict_sentiment(text):
    tensor = text_to_tensor(text)  # Converte o texto em tensor
    tensor_np = tensor.numpy().reshape(1, -1)  # Redimension ```python
    # Redimensiona para compatibilidade com o modelo
    tensor_padded = tf.keras.preprocessing.sequence.pad_sequences(tensor_np, padding='post')  # Padding
    prediction = model.predict(tensor_padded)  # Faz a previsão
    return prediction[0][0]  # Retorna a probabilidade

# Exemplo de uso
text = "I love this movie!"  # Texto a ser analisado
prediction = predict_sentiment(text)  # Previsão do sentimento
print(f"Predição para '{text}': {'Positivo' if prediction > 0.5 else 'Negativo'} com probabilidade {prediction:.2f}")