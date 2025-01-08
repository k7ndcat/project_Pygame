"""import sqlite3
def create_data_base(login, password, database='Login_Password.db'):
    conn = sqlite3.connect(database)
    cr = conn.cursor()
    cr.execute('''
        CREATE TABLE IF NOT EXISTS users (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT
       )
   ''')
    cr.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Password TEXT
            )
        ''')
    cr.execute('INSERT INTO Users (Name) VALUES (?)', (login,))
    cr.execute('INSERT INTO passwords (Password) VALUES (?)', (password,))
    conn.commit()
    conn.close()
create_data_base('Login.db')"""

import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtGui import QImage, QColor
from PyQt6.QtCore import Qt

class BinaryImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.binary_records = []  # Двойной список для хранения бинарных записей

    def initUI(self):
        self.setWindowTitle("Binary to Image")

        layout = QVBoxLayout()

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Введите бинарное число (12 символов)")
        layout.addWidget(self.input_field)

        self.submit_button = QPushButton("Создать изображение", self)
        self.submit_button.clicked.connect(self.create_image)
        layout.addWidget(self.submit_button)

        self.decode_button = QPushButton("Расшифровать записи", self)
        self.decode_button.clicked.connect(self.decode_records)
        layout.addWidget(self.decode_button)

        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def create_image(self):
        binary_input = self.input_field.text()

        if len(binary_input) != 12 or not all(c in '01' for c in binary_input):
            self.result_label.setText("Ошибка: Введите корректное бинарное число длиной 12 символов.")
            return

        # Добавляем бинарное число в двойной список
        self.binary_records.append(binary_input)

        # Разделение на 3 части по 4 символа
        parts = [binary_input[i:i + 4] for i in range(0, 12, 4)]

        # Создаем изображение 100x100 пикселей
        image = QImage(100, 100, QImage.Format.Format_RGB32)
        image.fill(QColor(255, 255, 255))  # Заполняем белым цветом

        for part in parts:
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            # Преобразуем бинарную строку в RGB цвет
            r = int(part[0]) * 255
            g = int(part[1]) * 255
            b = int(part[2]) * 255
            image.setPixel(x, y, QColor(r, g, b).rgb())

        # Сохраняем изображение
        image.save("output_image.png")
        self.result_label.setText("Изображение создано: output_image.png")

    def decode_records(self):
        if not self.binary_records:
            self.result_label.setText("Нет записей для расшифровки.")
            return

        decoded_output = "\n".join(self.binary_records)
        self.result_label.setText(f"Расшифрованные записи:\n{decoded_output}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = BinaryImageApp()
    ex.resize(300, 200)
    ex.show()
    sys.exit(app.exec())
