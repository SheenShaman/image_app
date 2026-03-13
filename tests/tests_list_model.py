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
        model = ImageListModel()
        assert model.is_image("photo.jpg") is True
        assert model.is_image("image.png") is True
        assert model.is_image("animation.gif") is True
        assert model.is_image("picture.bmp") is True

    def test_get_files(self):
        current_dir = os.path.dirname(__file__)
        try:
            model = ImageListModel(current_dir)
        except TypeError:
            model = ImageListModel()
            model.dir_path = current_dir

        files = model.get_files()

        assert type(files) == list
        assert files is not None
        if files:
            for file in files[:3]:
                assert isinstance(file, str)



