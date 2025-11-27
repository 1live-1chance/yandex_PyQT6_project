"""Точка входа в приложение"""

import sys
import os
from PyQt6.QtWidgets import QApplication

from src.main_window import MainWindow


def main():
    """Основная функция запуска приложения"""
    try:
        print("Запуск приложения распознавания рукописных цифр...")
        print(f"Текущая директория: {os.getcwd()}")
        print(f"Содержимое директории: {os.listdir('.')}")
        
        if os.path.exists('mnist_model'):
            print("Содержимое mnist_model:", os.listdir('mnist_model'))
            if os.path.exists('mnist_model/variables'):
                print("Содержимое mnist_model/variables:", os.listdir('mnist_model/variables'))
        
        # Создаем QApplication
        app = QApplication(sys.argv)
        
        # Создаем и показываем главное окно
        window = MainWindow()
        window.show()
        
        print("Приложение запущено успешно")
        
        # Запускаем event loop
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Критическая ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

