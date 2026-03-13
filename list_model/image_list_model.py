import os

from constants import IMAGE_FORMATS


class ImageListModel:
    """
    Класс фильтрует изображение по выбранному пути
    """

    def __init__(self):
        self.dir_path: str | None = None
        self.files: list[str] = []

    def scan_directory(self, dir_path: str) -> None:
        """
        Проверяет, существует ли путь
        и является ли он папкой
        """
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"Путь не существует: {dir_path}")
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(f"Путь не является папкой: {dir_path}")
        self.dir_path = dir_path
        self.get_files()

    def is_image(self, filename):
        """Проверяет, является ли файл изображением"""
        _, ext = os.path.splitext(filename)
        return ext.lower() in IMAGE_FORMATS

    def get_files(self) -> list[str]:
        """Возвращает список файлов изображений в папке"""
        image_files = []
        for item in os.listdir(self.dir_path):
            item_path = os.path.join(self.dir_path, item)
            if os.path.isfile(item_path) and self.is_image(item):
                image_files.append(item)
        self.files = sorted(image_files)
        return self.files.copy()
