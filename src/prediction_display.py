"""Виджет для отображения результатов предсказания"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt


class PredictionDisplay(QWidget):
    """Виджет для отображения результатов распознавания"""
    
    def __init__(self):
        """Инициализация виджета отображения результатов"""
        super().__init__()
        
        # Список для хранения прогресс-баров для каждой цифры
        self.progress_bars = []
        self.digit_labels = []
        
        # Метка для отображения результата
        self.result_label = QLabel("Нарисуйте цифру и нажмите 'Распознать'")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Настройка интерфейса
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        try:
            layout = QVBoxLayout()
            layout.addWidget(self.result_label)
            
            # Создаем прогресс-бары для каждой цифры (0-9)
            for i in range(10):
                digit_layout = QHBoxLayout()
                
                # Метка с цифрой
                digit_label = QLabel(f"{i}:")
                digit_label.setFixedWidth(20)
                self.digit_labels.append(digit_label)
                
                # Прогресс-бар для вероятности
                progress_bar = QProgressBar()
                progress_bar.setRange(0, 100)
                progress_bar.setValue(0)
                progress_bar.setTextVisible(True)
                self.progress_bars.append(progress_bar)
                
                digit_layout.addWidget(digit_label)
                digit_layout.addWidget(progress_bar)
                layout.addLayout(digit_layout)
            
            self.setLayout(layout)
            
        except Exception as e:
            print(f"Ошибка при настройке интерфейса: {e}")
    
    def update_predictions(self, probabilities):
        """
        Обновление отображения результатов
        
        Args:
            probabilities: список вероятностей для каждой цифры
        """
        try:
            if not probabilities or len(probabilities) != 10:
                return
            
            # Обновляем прогресс-бары
            for i, (progress_bar, probability) in enumerate(zip(self.progress_bars, probabilities)):
                percentage = int(probability * 100)
                progress_bar.setValue(percentage)
                progress_bar.setFormat(f"{percentage}%")
            
            # Определяем цифру с максимальной вероятностью
            max_prob_index = probabilities.index(max(probabilities))
            max_probability = max(probabilities)
            
            # Обновляем метку результата
            self.result_label.setText(
                f"Результат: {max_prob_index} "
                f"(вероятность: {max_probability:.2%})"
            )
            
        except Exception as e:
            print(f"Ошибка при обновлении результатов: {e}")
            self.result_label.setText("Ошибка при распознавании")
    
    def clear_predictions(self):
        """Очистка отображения результатов"""
        try:
            # Сбрасываем все прогресс-бары
            for progress_bar in self.progress_bars:
                progress_bar.setValue(0)
                progress_bar.setFormat("0%")
            
            # Сбрасываем метку результата
            self.result_label.setText("Нарисуйте цифру и нажмите 'Распознать'")
            
        except Exception as e:
            print(f"Ошибка при очистке результатов: {e}")

