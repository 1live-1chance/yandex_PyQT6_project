"""Работа с ML моделью для распознавания цифр"""

import os
import numpy as np
import tensorflow as tf


class ModelHandler:
    """Класс для работы с предобученной моделью MNIST"""
    
    def __init__(self, model_path="mnist_model"):
        """
        Инициализация обработчика модели
        
        Args:
            model_path: путь к директории с моделью
        """
        self.model = None
        self.model_path = model_path
        self.is_loaded = False
        
        try:
            self.load_model()
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            self.is_loaded = False
    
    def load_model(self):
        """Загрузка SavedModel"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Директория модели не найдена: {self.model_path}")
            
            # Проверяем наличие необходимых файлов
            required_files = [
                os.path.join(self.model_path, "saved_model.pb"),
                os.path.join(self.model_path, "variables")
            ]
            
            for file_path in required_files:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Не найден необходимый файл: {file_path}")
            
            # Загружаем модель
            self.model = tf.saved_model.load(self.model_path)
            
            # Проверяем, есть ли у модели метод __call__
            if not hasattr(self.model, '__call__'):
                raise RuntimeError("Модель не содержит callable метода")
            
            self.is_loaded = True
            print("Модель успешно загружена")
            print(f"Тип модели: {type(self.model)}")
            
        except Exception as e:
            print(f"Ошибка при загрузке модели из {self.model_path}: {e}")
            self.is_loaded = False
            raise
    
    def predict(self, image_array):
        """
        Выполнение предсказания для изображения
        
        Args:
            image_array: numpy array с изображением
            
        Returns:
            список вероятностей для каждой цифры (0-9)
        """
        try:
            if not self.is_loaded:
                raise RuntimeError("Модель не загружена")
            
            if image_array is None:
                raise ValueError("Пустое изображение")
            
            # Выполняем предсказание напрямую через модель
            prediction = self.model(tf.constant(image_array))
            
            # Обрабатываем разные форматы возвращаемых значений
            if isinstance(prediction, dict):
                # Если результат - словарь, пробуем извлечь значения
                output_keys = list(prediction.keys())
                print(f"Ключи выходных данных: {output_keys}")
                
                # Берем первый доступный ключ
                if output_keys:
                    logits = prediction[output_keys[0]]
                else:
                    raise RuntimeError("Пустой словарь результатов")
            else:
                # Если результат - тензор
                logits = prediction
            
            # Конвертируем в numpy
            if hasattr(logits, 'numpy'):
                logits_array = logits.numpy()
            else:
                logits_array = np.array(logits)
            
            print(f"Форма выходного тензора: {logits_array.shape}")
            
            # Обрабатываем различные формы тензора
            if len(logits_array.shape) == 2 and logits_array.shape[0] == 1 and logits_array.shape[1] == 10:
                # Форма (1, 10) - логиты для батча из 1 элемента
                flat_logits = logits_array[0]
            elif len(logits_array.shape) == 1 and logits_array.shape[0] == 10:
                # Форма (10,) - логиты
                flat_logits = logits_array
            elif len(logits_array.shape) > 1:
                # Многомерный тензор - пытаемся преобразовать
                flat_logits = logits_array.flatten()
                if len(flat_logits) != 10:
                    # Берем первые 10 элементов если их больше
                    if len(flat_logits) > 10:
                        flat_logits = flat_logits[:10]
                    else:
                        raise ValueError(f"Неправильное количество выходов: {len(flat_logits)}")
            else:
                raise ValueError(f"Неподдерживаемая форма тензора: {logits_array.shape}")
            
            # Применяем softmax для получения вероятностей
            probabilities = tf.nn.softmax(flat_logits).numpy()
            
            return probabilities.tolist()
            
        except Exception as e:
            print(f"Ошибка при выполнении предсказания: {e}")
            import traceback
            traceback.print_exc()
            # Возвращаем равномерные вероятности в случае ошибки
            return [0.1] * 10
    
    def get_prediction_result(self, probabilities):
        """
        Получение результата предсказания (цифра с наибольшей вероятностью)
        
        Args:
            probabilities: список вероятностей
            
        Returns:
            индекс цифры с максимальной вероятностью
        """
        try:
            if not probabilities:
                return -1
            return int(np.argmax(probabilities))
        except Exception as e:
            print(f"Ошибка при определении результата: {e}")
            return -1
