import os
import pytest
from list_model import ImageListModel


class TestModel:

    def test_scan_directory(self):
        test_path = "test_example"
        if not os.path.exists(test_path):
            pytest.skip(f"Тестовая папка не существует: {test_path}")
        result = ImageListModel.scan_directory(dir_path=test_path)
        assert isinstance(result, list)


    def test_is_image(self):
        assert ImageListModel.is_image("photo.jpg") == True
        assert ImageListModel.is_image("image.png") == True
        assert ImageListModel.is_image("animation.gif") == True
        assert ImageListModel.is_image("picture.bmp") == True

    def test_get_files(self):
        current_dir = os.path.dirname(__file__)
        result = ImageListModel.get_files(current_dir)
        assert isinstance(result, list)


object_1 = TestModel()


