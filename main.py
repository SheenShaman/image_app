import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import Qt


def main():
    """
    Проверка работоспособности
    """
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PyQt5 тест")
    window.resize(400, 200)

    layout = QVBoxLayout(window)

    label = QLabel("✅ PyQt5 работает")
    label.setAlignment(Qt.AlignCenter)

    button = QPushButton("Закрыть")
    button.clicked.connect(app.quit)

    layout.addWidget(label)
    layout.addWidget(button)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
