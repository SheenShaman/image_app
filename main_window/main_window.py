import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import constants


class MainWindow(QMainWindow):
    """
    Главное Окно
    """

    def __init__(self):
        super().__init__()
        self.current_dir: str | None = None
        self.original_pixmap: QPixmap | None = None
        self.initUI()

    def initUI(self):
        """
        Интерфейс программы
        """

        # центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # добавление панелей
        main_layout.addLayout(self.create_left_layout(), 1)
        main_layout.addLayout(self.create_right_layout(), 3)

        self.setWindowTitle("PhotoShelf")
        self.resize(900, 600)
        self.show()

    def create_left_layout(self) -> QVBoxLayout:
        """
        Левая панель
        Выбор папки и список изображений
        """
        # создание кнопки и подключение сигнала
        self.select_dir_btn = QPushButton("Выбрать папку")
        self.select_dir_btn.clicked.connect(self.select_directory)

        # создание кнопки и подключение сигнала
        self.files_list = QListWidget()
        self.files_list.itemClicked.connect(self.on_file_selected)

        layout = QVBoxLayout()
        layout.addWidget(self.select_dir_btn)
        layout.addWidget(self.files_list)

        return layout

    def on_file_selected(self, item: QListWidget):
        """
        Обработка файла
        """
        if not item or not self.current_dir:
            return

        image_path = os.path.join(self.current_dir, item.text())
        self.load_image(image_path)

    def load_image(self, image_path: str):
        """
        Загрузка изображения
        """
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Не удалось загрузить изображение: ", image_path)
            return
        self.original_pixmap = pixmap
        self.update_pixmap()

    def update_pixmap(self):
        """
        Изменение размеров изображение вместе с окном
        """
        if not self.original_pixmap or not hasattr(self, "image_label"):
            return

        scaled = self.original_pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)

    def select_directory(self):
        """
        Выбор папки с изображениями
        """
        directory = QFileDialog.getExistingDirectory(
            self, "Выберите папку с изображениями"
        )
        if not directory:
            return
        self.current_dir = directory
        self.fill_file_list(directory)

    def fill_file_list(self, directory: str):
        """
        Заполняет files_list изображениями из папки
        """
        self.files_list.clear()
        files = os.listdir(directory)

        image_files = [
            file
            for file in files
            if file.lower().endswith(constants.IMAGE_FORMATS)
        ]
        for file in image_files:
            self.files_list.addItem(file)

    def create_right_layout(self) -> QVBoxLayout:
        """
        Правая панель
        Область изображения + кнопки изменений
        """
        # область изображения
        self.image_label = QLabel("Изображение")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        # добавление кнопок
        for button in constants.IMAGE_BUTTONS:
            layout.addWidget(QPushButton(button))

        return layout

    def resizeEvent(self, event: QResizeEvent):
        """
        Вызывается при изменении размера окна
        """
        super().resizeEvent(event)
        self.update_pixmap()
