"""Виджет для рисования цифр"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QImage, QPixmap, QColor
from PyQt6.QtCore import Qt, QPoint


class DrawingWidget(QWidget):
    """Виджет для рисования рукописных цифр"""
    
    def __init__(self):
        """Инициализация виджета рисования"""
        super().__init__()
        
        # Настройки рисования
        self.drawing = False
        self.brush_size = 20
        self.brush_color = Qt.GlobalColor.black
        
        # Создаем изображение для рисования
        self.image = QImage(
            self.width(), 
            self.height(), 
            QImage.Format.Format_RGB32
        )
        self.image.fill(Qt.GlobalColor.white)
        
        # Последняя точка для рисования
        self.last_point = QPoint()
        
        # Настройки виджета
        self.setMinimumSize(280, 280)
        self.resize(280, 280)
    
    def resizeEvent(self, event):
        """Обработка изменения размера виджета"""
        try:
            # Создаем новое изображение с новыми размерами
            new_image = QImage(
                self.width(),
                self.height(),
                QImage.Format.Format_RGB32
            )
            new_image.fill(Qt.GlobalColor.white)
            
            # Копируем старое изображение на новое
            painter = QPainter(new_image)
            painter.drawImage(QPoint(0, 0), self.image)
            painter.end()
            
            self.image = new_image
            
        except Exception as e:
            print(f"Ошибка при изменении размера: {e}")
        
        super().resizeEvent(event)
    
    def paintEvent(self, event):
        """Отрисовка содержимого виджета"""
        try:
            canvas_painter = QPainter(self)
            canvas_painter.drawImage(self.rect(), self.image, self.image.rect())
            canvas_painter.end()
        except Exception as e:
            print(f"Ошибка при отрисовке: {e}")
    
    def mousePressEvent(self, event):
        """Обработка нажатия кнопки мыши"""
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                self.drawing = True
                self.last_point = event.position().toPoint()
        except Exception as e:
            print(f"Ошибка при обработке нажатия мыши: {e}")
    
    def mouseMoveEvent(self, event):
        """Обработка движения мыши"""
        try:
            if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
                painter = QPainter(self.image)
                painter.setPen(QPen(
                    self.brush_color,
                    self.brush_size,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin
                ))
                
                # Рисуем линию от последней точки до текущей
                painter.drawLine(self.last_point, event.position().toPoint())
                painter.end()
                
                self.last_point = event.position().toPoint()
                self.update()
        except Exception as e:
            print(f"Ошибка при рисовании: {e}")
    
    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши"""
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                self.drawing = False
        except Exception as e:
            print(f"Ошибка при отпускании мыши: {e}")
    
    def clear_canvas(self):
        """Очистка холста"""
        try:
            self.image.fill(Qt.GlobalColor.white)
            self.update()
        except Exception as e:
            print(f"Ошибка при очистке холста: {e}")
    
    def get_image(self):
        """
        Получение текущего изображения
        
        Returns:
            QImage - текущее изображение с холста
        """
        try:
            return self.image
        except Exception as e:
            print(f"Ошибка при получении изображения: {e}")
            # Возвращаем пустое изображение в случае ошибки
            empty_image = QImage(
                self.width(),
                self.height(),
                QImage.Format.Format_RGB32
            )
            empty_image.fill(Qt.GlobalColor.white)
            return empty_image
