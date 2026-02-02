from typing import Callable

from managers.image_manager import ImageManager


class BatchManager:
    def __init__(self):
        self.images_managers: list[ImageManager] = []

    def load_images(self, paths):
        for path in paths:
            image_manager = ImageManager()
            image_manager.load(path)
            self.images_managers.append(image_manager)

    def save_all(self):
        for image_manager in self.images_managers:
            image_manager.save()

    def reset_all(self):
        for image_manager in self.images_managers:
            image_manager.reset()

    def apply_action(self, action: Callable[[ImageManager], None]):
        for image_manager in self.images_managers:
            action(image_manager)
