"""Вспомогательные функции для обработки изображений"""

import numpy as np
from PIL import Image, ImageOps


def preprocess_image_for_model(qt_image, target_size=28):
    """
    Предобработка изображения Qt для подачи в модель
    
    Args:
        qt_image: QImage для обработки
        target_size: целевой размер изображения
    
    Returns:
        numpy array с нормализованным изображением
    """
    try:
        # Конвертируем QImage в PIL Image
        byte_data = qt_image.bits().asstring(qt_image.width() * qt_image.height() * 4)
        pil_image = Image.frombuffer(
            "RGBA",
            (qt_image.width(), qt_image.height()),
            byte_data,
            "raw",
            "RGBA",
            0,
            1
        )
        
        # Конвертируем в grayscale
        pil_image = pil_image.convert('L')
        
        # Инвертируем цвета (MNIST использует белый фон, черные цифры)
        pil_image = ImageOps.invert(pil_image)
        
        # Изменяем размер до target_size x target_size
        pil_image = pil_image.resize((target_size, target_size), Image.Resampling.LANCZOS)
        
        # Конвертируем в numpy array
        image_array = np.array(pil_image)
        
        # Нормализуем значения пикселей в диапазон [0, 1]
        image_array = image_array.astype(np.float32) / 255.0
        
        # Добавляем размерности для батча и канала
        image_array = image_array.reshape(1, target_size, target_size, 1)
        
        return image_array
        
    except Exception as e:
        print(f"Ошибка при предобработке изображения: {e}")
        # Возвращаем нулевой массив в случае ошибки
        return np.zeros((1, target_size, target_size, 1), dtype=np.float32)
