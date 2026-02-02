from pathlib import Path

from PIL import Image
from PIL.ImageEnhance import Brightness
from PIL.ImageOps import mirror

from constants import MODIFIED_DIRECTORY


# Класс для управления картинками
class ImageManager:
    """Пример использования класса ImageManager

    image_manager = ImageManager()\n
    image_manager.load("example.jpg")\n
    image_manager.rotate_left()\n
    image_manager.flip_horizontal()\n
    image_manager.change_brightness(150)\n
    image_manager.save()
    """

    def __init__(self) -> None:
        self._current_image = None
        self._current_path = None
        self._original_image = None

    @property
    def current_image(self):
        """Свойство для проверки, что изображение загружено"""
        if self._current_image is None or self._current_path is None:
            raise ValueError("Изображение еще не было загружено")
        return self._current_image

    @current_image.setter
    def current_image(self, image: Image.Image):
        self._current_image = image

    # Загружает картинку и путь до нее
    def load(self, path: str | Path) -> Image.Image:
        self._current_path = Path(path)
        image = Image.open(path)
        self._original_image = image.copy()
        self.current_image = image
        return self.current_image

    # Сохраняет картинку в папку для измененных изображений
    def save(self):
        modified_dir = self._current_path.parent / MODIFIED_DIRECTORY
        modified_dir.mkdir(exist_ok=True)
        new_path = (
            modified_dir
            / f"{self._current_path.stem}_modified{self._current_path.suffix}"
        )
        self.current_image.save(new_path)

    # Возвращает оригинал изображения
    def reset(self):
        if self._original_image is None:
            raise ValueError("Нет оригинального изображения")
        self.current_image = self._original_image.copy()

    # Поворот влево
    def rotate_left(self) -> None:
        self.current_image = self.current_image.rotate(90)

    # Поворот вправо
    def rotate_right(self) -> None:
        self.current_image = self.current_image.rotate(-90)

    # Отзеркаливание
    def flip_horizontal(self) -> None:
        self.current_image = mirror(self.current_image)

    # Черно-белый фильтр
    def to_grayscale(self) -> None:
        self.current_image = self.current_image.convert("L")

    # Меняет яркость
    def change_brightness(self, delta: int = 100):
        """
        Меняет яркость картинки. По дефолту 100 - оригинальная картинка,
        0 - полностью черная
        """
        delta_float = float(delta / 100)
        self.current_image = Brightness(self.current_image).enhance(delta_float)
