"""Главное окно приложения"""

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from src.drawing_widget import DrawingWidget
from src.prediction_display import PredictionDisplay
from src.model_handler import ModelHandler
from src.utils import preprocess_image_for_model
import config


class MainWindow(QMainWindow):
    """Главное окно приложения для распознавания рукописных цифр"""
    
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        
        # Инициализация компонентов
        self.drawing_widget = DrawingWidget()
        self.prediction_display = PredictionDisplay()
        self.model_handler = ModelHandler(config.MODEL_PATH)
        
        # Настройка интерфейса
        self.setup_ui()
        self.setup_connections()
        
        # Проверка загрузки модели
        self.check_model_status()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        try:
            # Основной виджет и layout
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            main_layout = QVBoxLayout()
            
            # Заголовок
            title_label = QLabel("Распознавание рукописных цифр")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
            main_layout.addWidget(title_label)
            
            # Основная область с холстом и результатами
            content_layout = QHBoxLayout()
            
            # Область рисования
            drawing_layout = QVBoxLayout()
            drawing_label = QLabel("Холст для рисования:")
            drawing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            drawing_layout.addWidget(drawing_label)
            drawing_layout.addWidget(self.drawing_widget)
            
            # Кнопки управления
            button_layout = QHBoxLayout()
            self.recognize_button = QPushButton("Распознать")
            self.clear_button = QPushButton("Очистить")
            button_layout.addWidget(self.recognize_button)
            button_layout.addWidget(self.clear_button)
            drawing_layout.addLayout(button_layout)
            
            content_layout.addLayout(drawing_layout)
            
            # Область результатов
            results_layout = QVBoxLayout()
            results_label = QLabel("Результаты распознавания:")
            results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            results_layout.addWidget(results_label)
            results_layout.addWidget(self.prediction_display)
            content_layout.addLayout(results_layout)
            
            main_layout.addLayout(content_layout)
            central_widget.setLayout(main_layout)
            
            # Настройки окна
            self.setWindowTitle("Распознавание рукописных цифр MNIST")
            self.setMinimumSize(800, 400)
            
        except Exception as e:
            print(f"Ошибка при настройке интерфейса: {e}")
            self.show_error_message("Ошибка интерфейса", f"Не удалось создать интерфейс: {e}")
    
    def setup_connections(self):
        """Настройка соединений сигналов и слотов"""
        try:
            self.recognize_button.clicked.connect(self.on_recognize_clicked)
            self.clear_button.clicked.connect(self.on_clear_clicked)
        except Exception as e:
            print(f"Ошибка при настройке соединений: {e}")
    
    def check_model_status(self):
        """Проверка статуса загрузки модели"""
        try:
            if not self.model_handler.is_loaded:
                QMessageBox.warning(
                    self,
                    "Предупреждение",
                    "Модель не загружена. Распознавание может не работать корректно."
                )
        except Exception as e:
            print(f"Ошибка при проверке статуса модели: {e}")
    
    def on_recognize_clicked(self):
        """Обработка нажатия кнопки 'Распознать'"""
        try:
            if not self.model_handler.is_loaded:
                self.show_error_message(
                    "Ошибка", 
                    "Модель не загружена. Проверьте наличие файлов модели."
                )
                return
            
            # Получаем изображение с холста
            image = self.drawing_widget.get_image()
            
            # Предобрабатываем изображение для модели
            processed_image = preprocess_image_for_model(
                image, 
                config.MODEL_IMAGE_SIZE
            )
            
            # Выполняем предсказание
            probabilities = self.model_handler.predict(processed_image)
            
            # Обновляем отображение результатов
            self.prediction_display.update_predictions(probabilities)
            
        except Exception as e:
            print(f"Ошибка при распознавании: {e}")
            self.show_error_message("Ошибка", f"Ошибка при распознавании: {e}")
    
    def on_clear_clicked(self):
        """Обработка нажатия кнопки 'Очистить'"""
        try:
            # Очищаем холст
            self.drawing_widget.clear_canvas()
            
            # Очищаем результаты
            self.prediction_display.clear_predictions()
            
        except Exception as e:
            print(f"Ошибка при очистке: {e}")
            self.show_error_message("Ошибка", f"Ошибка при очистке: {e}")
    
    def show_error_message(self, title, message):
        """
        Отображение сообщения об ошибке
        
        Args:
            title: заголовок сообщения
            message: текст сообщения
        """
        try:
            QMessageBox.critical(self, title, message)
        except Exception as e:
            print(f"Ошибка при отображении сообщения об ошибке: {e}")

