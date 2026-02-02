import os

from PIL.Image import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from list_model import ImageListModel
from managers import BatchManager


class MainWindow(QMainWindow):
    """
    Главное Окно
    """

    def __init__(self):
        super().__init__()
        self.batch_manager = BatchManager()
        self.list_model = ImageListModel()
        self.current_dir: str | None = None
        self.original_pixmap: QPixmap | None = None
        self.edit_buttons: list[QPushButton] = []
        self.initUI()

    def _has_image(self) -> bool:
        """
        Проверка наличия изображения
        """
        if len(self.batch_manager.images_managers) > 0:
            return True
        return False

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
        self.files_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.files_list.itemClicked.connect(self.on_file_selected)

        layout = QVBoxLayout()
        layout.addWidget(self.select_dir_btn)
        layout.addWidget(self.files_list)

        return layout

    def on_file_selected(self, item: QListWidgetItem):
        """
        Обработка файла
        """
        if not item or not self.current_dir:
            return

        selected_files = []
        for file in self.files_list.selectedItems():
            image_path = os.path.join(self.current_dir, file.text())
            selected_files.append(image_path)
        self.batch_manager.images_managers.clear()
        if not selected_files:
            self.set_edit_buttons_enabled(False)
            return
        self.load_images(selected_files)

    def load_images(self, image_paths: list[str]):
        """
        Загрузка изображения
        """
        try:
            self.batch_manager.load_images(image_paths)
        except Exception as e:  # ошибки связанные с загрузкой
            print(e)
            return
        # отображение изображения
        self.show_image(self.batch_manager.images_managers[-1].current_image)
        # включаем кнопки
        self.set_edit_buttons_enabled(True)

    def show_image(self, image: Image):
        """
        Отображение изображения
        """
        image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)

        pixmap = QPixmap.fromImage(qimage)
        self.original_pixmap = pixmap
        self.update_pixmap()

    def update_pixmap(self):
        """
        Изменение размеров изображение вместе с окном
        """
        if not self.original_pixmap or not hasattr(self, "image_label"):
            return
        # изменение размеров под изображение
        scaled = self.original_pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        # установка новых размеров
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

        try:
            self.list_model.scan_directory(directory)
        except Exception as e:
            print(e)
            return
        # обновление списка изображений
        self.update_file_list()
        # отключение кнопки
        self.set_edit_buttons_enabled(False)

    def update_file_list(self):
        """
        Заполняет files_list изображениями из папки
        """
        self.files_list.clear()
        for filename in self.list_model.get_files():
            self.files_list.addItem(filename)

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
        btn_save_image = QPushButton("Сохранить")
        btn_save_image.clicked.connect(self.save_image)

        btn_rotate_left = QPushButton("Поворот влево")
        btn_rotate_left.clicked.connect(self.rotate_left)

        btn_rotate_right = QPushButton("Поворот вправо")
        btn_rotate_right.clicked.connect(self.rotate_right)

        btn_flip_horizontal = QPushButton("Отзеркаливание по горизонтали")
        btn_flip_horizontal.clicked.connect(self.flip_horizontal)

        btn_to_grayscale = QPushButton("Ч/Б")
        btn_to_grayscale.clicked.connect(self.to_grayscale)

        btn_brighter = QPushButton("Ярче")
        btn_brighter.clicked.connect(lambda: self.change_brightness(130))

        btn_darker = QPushButton("Темнее")
        btn_darker.clicked.connect(lambda: self.change_brightness(70))

        btn_reset = QPushButton("Сброс изменений")
        btn_reset.clicked.connect(self.reset_image)

        for btn in [
            btn_save_image,
            btn_rotate_left,
            btn_rotate_right,
            btn_flip_horizontal,
            btn_to_grayscale,
            btn_brighter,
            btn_darker,
            btn_reset,
        ]:
            btn.setEnabled(False)
            self.edit_buttons.append(btn)
            layout.addWidget(btn)

        return layout

    def save_image(self):
        """
        Сохранение
        """
        if not self._has_image():
            return
        self.batch_manager.save_all()

    def rotate_left(self):
        """
        Поворот налево
        """
        if not self._has_image():
            return
        self.batch_manager.apply_action(lambda manager: manager.rotate_left())
        self.show_image(self.batch_manager.images_managers[-1].current_image)

    def rotate_right(self):
        """
        Поворот направо
        """
        if not self._has_image():
            return
        self.batch_manager.apply_action(lambda manager: manager.rotate_right())
        self.show_image(self.batch_manager.images_managers[-1].current_image)

    def flip_horizontal(self):
        """
        Отзеркаливание по горизонтали
        """
        if not self._has_image():
            return
        self.batch_manager.apply_action(
            lambda manager: manager.flip_horizontal()
        )
        self.show_image(self.batch_manager.images_managers[-1].current_image)

    def to_grayscale(self):
        """
        Ч/Б
        """
        if not self._has_image():
            return
        self.batch_manager.apply_action(lambda manager: manager.to_grayscale())
        self.show_image(self.batch_manager.images_managers[-1].current_image)

    def change_brightness(self, value: int):
        """
        Изменение яркости
        """
        if not self._has_image():
            return
        self.batch_manager.apply_action(
            lambda manager: manager.change_brightness(value)
        )
        self.show_image(self.batch_manager.images_managers[-1].current_image)

    def reset_image(self):
        """
        Возвращение оригинального изображения
        """
        if not self._has_image():
            return
        self.batch_manager.apply_action(lambda manager: manager.reset())
        self.show_image(self.batch_manager.images_managers[-1].current_image)

    def set_edit_buttons_enabled(self, enabled: bool):
        """
        Вкл/выкл кнопок
        """
        for btn in self.edit_buttons:
            btn.setEnabled(enabled)

    def resizeEvent(self, event: QResizeEvent):
        """
        Вызывается при изменении размера окна
        """
        super().resizeEvent(event)
        self.update_pixmap()
