from __future__ import annotations
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.datasets import mnist
import matplotlib.pyplot as plt
import os
import math


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
WEIGHTS_FILE = 'weights.h5'


class MyModel(Sequential):
    """Модель"""

    def __init__(self, train: bool = True):
        """Конструктор"""

        super().__init__()

        if train:
            (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()  # распаковываем массив

            self.x_train = self.x_train / 255  # нормализуем
            self.x_test = self.x_test / 255

            self.y_train_vec = keras.utils.to_categorical(self.y_train, 10)  # векторизируем
            self.y_test_vec = keras.utils.to_categorical(self.y_test, 10)

            self.add(Flatten(input_shape=(28, 28, 1)))
            self.add(Dense(128, activation='relu'))
            self.add(Dense(10, activation='softmax'))

            self.compile(optimizer='adam',
                         loss='categorical_crossentropy',
                         metrics=['accuracy'])

            self.train_model()
            return

        self.add(Flatten(input_shape=(28, 28, 1)))
        self.add(Dense(128, activation='relu'))
        self.add(Dense(10, activation='softmax'))

        self.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])

        self.load_weights()

    def train_model(self) -> None:
        """Тренировка модели"""

        self.fit(self.x_train, self.y_train_vec, batch_size=32, epochs=5, validation_split=0.2)
        self.save_weights(WEIGHTS_FILE)

    def test_model_with_statistics(self) -> None:
        """Тест модели"""

        self.evaluate(self.x_test, self.y_test_vec)

    def load_weights(self, **kwargs) -> None:
        """Загрузка весов"""

        super().load_weights(WEIGHTS_FILE)

    def test_model_by_index(self, index: int) -> None:
        """Тестрирует модель на определенном примере из массива x_test по индексу index"""

        res = self.predict(np.expand_dims(self.x_test[index], axis=0))
        print(np.argmax(res))
        plt.imshow(self.x_test[index], cmap='binary')
        plt.show()

    def use_model(self, image: np.ndarray) -> np.ndarray[int]:
        """Использование нейросети"""

        return self.predict(np.expand_dims(image, axis=0), verbose=None)

    @staticmethod
    def convert_image(image: np.ndarray) -> np.ndarray:
        """Конвертирует картинку под MNIST датасет картинка должна подаваться сырым массивом & shape = (28, 28) """

        image = 255 - image  # инвертирую

        w, h = image.shape
        xmask = np.array([np.any(image[:, y] != 0.0) for y in range(w)])  # обрезаем пустые строки и столбцы
        ymask = np.array([np.any(image[x, :] != 0.0) for x in range(h)])
        xmask = np.where(xmask)[0]
        ymask = np.where(ymask)[0]
        xmin = xmask.min()
        xmax = xmask.max() + 1
        ymin = ymask.min()
        ymax = ymask.max() + 1
        image = image[ymin: ymax, xmin: xmax]
        w, h = image.shape

        h_padding = int(math.ceil((28 - h) / 2.0)), int(math.floor((28 - h) / 2.0))  # заполняем пустыми пикселями для восстановления размера 28x28 px
        w_padding = int(math.ceil((28 - w) / 2.0)), int(math.floor((28 - w) / 2.0))
        image = np.lib.pad(image, (w_padding, h_padding), 'constant')

        image = image / 255  # нормализую

        return image
