from pathlib import Path

from PIL import Image
from PIL.ImageEnhance import Brightness
from PIL.ImageOps import mirror


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
        self.current_image = Image.open(path)
        print(self._current_path)
        return self.current_image

    # Сохраняет картинку
    def save(self):
        new_path = (
            self._current_path.parent
            / f"{self._current_path.stem}_modified{self._current_path.suffix}"
        )
        self.current_image.save(new_path)

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
