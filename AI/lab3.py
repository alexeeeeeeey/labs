import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score


class NeuralNetwork:
    def __init__(self, input_size, hidden_layer_size, output_size):
        # Инициализация весов и смещений
        self.weights_input_to_hidden = (
            np.random.randn(input_size, hidden_layer_size) * 0.01
        )
        self.bias_hidden = np.zeros((1, hidden_layer_size))
        self.weights_hidden_to_output = (
            np.random.randn(hidden_layer_size, output_size) * 0.01
        )
        self.bias_output = np.zeros((1, output_size))

        # Переменные для промежуточных вычислений
        self.input_data = None
        self.hidden_layer_activations = None
        self.output_layer_activations = None

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def relu_derivative(x):
        return np.where(x > 0, 1, 0)

    @staticmethod
    def softmax(x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, input_data):
        # Прямой проход
        self.input_data = input_data
        hidden_layer_input = (
            np.dot(self.input_data, self.weights_input_to_hidden)
            + self.bias_hidden
        )
        self.hidden_layer_activations = self.relu(hidden_layer_input)
        output_layer_input = (
            np.dot(
                self.hidden_layer_activations, self.weights_hidden_to_output
            )
            + self.bias_output
        )
        self.output_layer_activations = self.softmax(output_layer_input)
        return self.output_layer_activations

    def backward(self, target_labels, learning_rate):
        # Обратный проход
        num_samples = target_labels.shape[0]

        # Ошибка и градиенты для выходного слоя
        output_error = (
            self.output_layer_activations - target_labels
        ) / num_samples
        gradient_weights_hidden_to_output = np.dot(
            self.hidden_layer_activations.T, output_error
        )
        gradient_bias_output = np.sum(output_error, axis=0, keepdims=True)

        # Ошибка и градиенты для скрытого слоя
        hidden_error = np.dot(
            output_error, self.weights_hidden_to_output.T
        ) * self.relu_derivative(self.hidden_layer_activations)
        gradient_weights_input_to_hidden = np.dot(
            self.input_data.T, hidden_error
        )
        gradient_bias_hidden = np.sum(hidden_error, axis=0, keepdims=True)

        # Обновление весов и смещений
        self.weights_hidden_to_output -= (
            learning_rate * gradient_weights_hidden_to_output
        )
        self.bias_output -= learning_rate * gradient_bias_output
        self.weights_input_to_hidden -= (
            learning_rate * gradient_weights_input_to_hidden
        )
        self.bias_hidden -= learning_rate * gradient_bias_hidden

    def train(self, input_data, target_labels, epochs, learning_rate):
        for epoch in range(epochs):
            # Прямой и обратный проходы
            self.forward(input_data)
            self.backward(target_labels, learning_rate)

            # Лог потерь каждые 50 эпох
            if epoch % 50 == 0 or epoch == epochs - 1:
                loss = -np.mean(
                    target_labels
                    * np.log(self.output_layer_activations + 1e-9)
                )
                print(f"Эпоха: {epoch}, Потеря: {loss:.4f}")

    def predict(self, input_data):
        # Предсказание классов
        output_probabilities = self.forward(input_data)
        return np.argmax(output_probabilities, axis=1)


def main():
    # Загрузка набора данных
    digits = load_digits()
    features = digits.data
    labels = digits.target

    # Преобразование меток в формат one-hot
    encoder = OneHotEncoder(sparse_output=False)
    labels_one_hot = encoder.fit_transform(labels.reshape(-1, 1))

    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels_one_hot, test_size=0.1
    )

    # Параметры сети
    hidden_neurons = 64  # Количество нейронов в скрытом слое
    input_neurons = X_train.shape[1]
    output_neurons = y_train.shape[1]

    # Создание и обучение модели
    neural_net = NeuralNetwork(input_neurons, hidden_neurons, output_neurons)
    neural_net.train(X_train, y_train, epochs=1000, learning_rate=0.01)

    # Оценка качества модели
    test_predictions = neural_net.predict(X_test)
    test_accuracy = accuracy_score(y_test.argmax(axis=1), test_predictions)

    print(f"Точность на тестовой выборке: {test_accuracy:.4f}")


if __name__ == "__main__":
    main()
