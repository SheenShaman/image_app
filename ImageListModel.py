"""
методы:
- scan_directory(dir_path: str)
в папке по переданному пути фильтровать файлы с расширениями (.jpg, .jpeg, .png, .bmp, .gif)
- get_files()
возвращает список имен файлов
"""
import os
from pathlib import Path


class ImageListModel:
    """
    Класс фильтрует изображение по выбранному пути
    """
    image_format = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.path()

    def path(self):
        """Проверяет, существует ли путь
        и является ли он папкой"""
        if not os.path.exists(self.dir_path):
            raise FileNotFoundError(f"Путь не существует: {self.dir_path}")
        if not os.path.isdir(self.dir_path):
            raise NotADirectoryError(f"Путь не является папкой: {self.dir_path}")

    def is_image(self, filename):
        """Проверяет, является ли файл изображением"""
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.image_format

    def get_image(self):
        """Возвращает список файлов изображений в папке"""
        image_files = []
        for item in os.listdir(self.dir_path):
            item_path = os.path.join(self.dir_path, item)
            if os.path.isfile(item_path):
                if self.is_image(item):
                    image_files.append(item)
        return sorted(image_files)





