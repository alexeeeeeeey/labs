import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score


def relu(x):
    return np.maximum(0, x)


def relu_d(x):
    return np.where(x > 0, 1, 0)


def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def forward_propagation(self, X):
        self.hidden_input = np.dot(X, self.w1) + self.b1
        self.hidden_output = relu(self.hidden_input)
        self.output_input = np.dot(self.hidden_output, self.w2) + self.b2
        self.output_output = softmax(self.output_input)
        return self.output_output

    def back_propagation(self, X, y, learning_rate):
        m = y.shape[0]
        d_output = (self.output_output - y) / m
        d_w2 = np.dot(self.hidden_output.T, d_output)
        d_b2 = np.sum(d_output, axis=0, keepdims=True)
        d_hidden = np.dot(d_output, self.w2.T) * relu_d(self.hidden_input)
        d_w1 = np.dot(X.T, d_hidden)
        d_b1 = np.sum(d_hidden, axis=0, keepdims=True)
        self.w2 -= learning_rate * d_w2
        self.b2 -= learning_rate * d_b2
        self.w1 -= learning_rate * d_w1
        self.b1 -= learning_rate * d_b1

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            self.forward_propagation(X)
            self.back_propagation(X, y, learning_rate)
            if epoch % 50 == 0:
                print(f"Эпоха: {epoch}")

    def predict(self, X):
        output = self.forward_propagation(X)
        return np.argmax(output, axis=1)


# Загружаем набор данных и подготавливаем его
digits = load_digits()
X = digits.data
y = digits.target

# Преобразуем метки в формат one-hot
encoder = OneHotEncoder(sparse_output=False)
y_one_hot = encoder.fit_transform(y.reshape(-1, 1))

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X, y_one_hot, test_size=0.1
)

# Параметры модели
input_size = X_train.shape[1]  # Количество входных данных (пикселей)
hidden_size = 64  # Количество нейронов в скрытом слое
output_size = y_one_hot.shape[1]  # Количество классов

# Создаем и обучаем нейронную сеть
nn = NeuralNetwork(input_size, hidden_size, output_size)
nn.train(X_train, y_train, epochs=1000, learning_rate=0.01)

# Оцениваем качество на тестовой выборке
predictions = nn.predict(X_test)
accuracy = accuracy_score(y_test.argmax(axis=1), predictions)

print(f"Точность предсказания: {accuracy:.4f}")
