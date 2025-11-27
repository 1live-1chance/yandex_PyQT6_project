"""Создание тестовой модели MNIST для проверки работы приложения"""

import tensorflow as tf
from tensorflow import keras
import os


def create_and_save_test_model():
    """Создание и сохранение простой тестовой модели"""
    
    # Создаем простую модель
    model = keras.Sequential([
        keras.layers.Input(shape=(28, 28, 1)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation='softmax')
    ])
    
    # Компилируем модель
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Создаем директорию для модели если её нет
    os.makedirs('mnist_model', exist_ok=True)
    
    # Сохраняем модель в формате SavedModel
    tf.saved_model.save(model, 'mnist_model')
    
    print("Тестовая модель создана и сохранена в mnist_model/")


if __name__ == "__main__":
    create_and_save_test_model()
