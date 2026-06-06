import os
import sys

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QKeyEvent, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MW(QMainWindow):
    """
    QMainWindow는 QObject를 상속하므로
    Custom Signal을 class variable로 선언할 수 있음.
    """

    # Custom Signal 선언.
    # int argument 1개를 전달함.
    # 반드시 class variable로 선언해야 함.
    change_pixmap = Signal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.fstr = os.path.dirname(os.path.abspath(__file__))
        self.setGeometry(100, 100, 200, 300)
        self.setWindowTitle("Custom Signal Ex")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        self.idx = 0

        # Custom Signal에 Slot을 연결함.
        self.change_pixmap.connect(self.change_pixmap_handler)

        layout = QVBoxLayout()

        info_label = QLabel(
            "<p>Press <i>+</i> or <i>-</i> to change image</p>"
        )
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        self.img_label = QLabel()

        img_path = os.path.join(self.fstr, "img", "0.png")
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"이미지 로딩 실패: {img_path}")
        self.img_label.setPixmap(
            pixmap.scaled(
                QSize(180, 250),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.img_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event: QKeyEvent):
        """
        key press Event Handler.

        + 또는 - key 입력 시
        이미지 변경을 위한 Custom Signal을 emit함.

        이 method에서 이미지를 직접 변경하지 않고,
        Custom Signal을 emit하여
        연결된 Slot에서 처리하게 함.
        """

        if event.key() == Qt.Key.Key_Plus:
            self.change_pixmap.emit(1)
        elif event.key() == Qt.Key.Key_Minus:
            self.change_pixmap.emit(-1)

        # 기본 key event 처리를 위해 반드시 호출해야 함.
        # 이를 생략하면 하위 widget의 key 입력 기능,
        # menu 단축키, focus 이동 등의
        # Qt 기본 event 전달 흐름이 중단됨.
        super().keyPressEvent(event)

    def change_pixmap_handler(self, offset: int):
        """
        Custom Signal(change_pixmap)에 연결된 Slot.

        Parameters
        ----------
        offset : int
            이미지 index의 변화량.
            change_pixmap Signal이 emit할 때
            전달하는 argument임.
        """

        self.idx = (self.idx + offset) % 10

        img_path = os.path.join(
            self.fstr, "img", f"{self.idx}.png"
        )
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"이미지 로딩 실패: {img_path}")
        self.img_label.setPixmap(
            pixmap.scaled(
                QSize(180, 250),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
