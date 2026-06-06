import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("DirectConnection Ex")
        self.resize(380, 180)

        self.label = QLabel("Button을 클릭하면 Slot이 즉시 실행됨.")
        self.button = QPushButton("Click Me")

        # DirectConnection: Slot이 즉시 호출됨.
        self.button.clicked.connect(
            self.on_clicked,
            Qt.ConnectionType.DirectConnection,
        )

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def on_clicked(self):
        """
        DirectConnection으로 연결된 Slot.

        Signal이 emit되면 이 method가
        emit한 thread에서 즉시 호출됨.
        Event System을 거치지 않는 직접 함수 호출임.
        """

        import threading

        tid = threading.current_thread().name
        print(f"[DirectConnection] on_clicked() called in: {tid}")
        self.label.setText(
            f"Slot executed directly in: {tid}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
