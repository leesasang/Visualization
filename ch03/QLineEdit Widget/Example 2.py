import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget,
        QLabel, QLineEdit, QPushButton,
    )
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget,
            QLabel, QLineEdit, QPushButton,
        )
        qt_modules = 'PyQt6'
    except ImportError:
        print("PySide6 또는 PyQt6가 설치되어 있지 않습니다.")
        sys.exit(1)


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(340, 120)   # 창 크기 고정
        self.setWindowTitle("QLineEdit Example")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        QLabel("Please enter your name below.", self).move(50, 10)

        name_label = QLabel("Name:", self)
        name_label.move(10, 50)

        # QLineEdit 생성 및 설정
        self.name_edit = QLineEdit(self)
        self.name_edit.resize(210, 24)
        self.name_edit.move(80, 47)
        self.name_edit.setStyleSheet(
            "background-color: yellow; color: rgb(50, 150, 250);"
        )
        self.name_edit.setMaxLength(30)
        self.name_edit.setPlaceholderText("Enter your name")

        # Signal 연결
        self.name_edit.returnPressed.connect(self.on_return_pressed)
        self.name_edit.selectionChanged.connect(self.on_selection_changed)
        self.name_edit.textChanged.connect(self.on_text_changed)
        self.name_edit.textEdited.connect(self.on_text_edited)

        clear_button = QPushButton("Clear", self)
        clear_button.move(100, 85)
        clear_button.clicked.connect(self.clear_text)

        ok_button = QPushButton("OK", self)
        ok_button.move(200, 85)
        ok_button.clicked.connect(self.accept_text)

    def clear_text(self):
        """입력 필드를 초기화함."""
        self.name_edit.clear()

    def accept_text(self):
        """입력된 text를 console에 출력하고 창을 닫음."""
        print(f"입력된 이름: {self.name_edit.text()}")
        self.close()

    def on_return_pressed(self):
        print("[returnPressed] Enter 키가 눌렸습니다.")

    def on_selection_changed(self):
        print("[selectionChanged] 선택 범위가 변경됐습니다.")

    def on_text_changed(self, text: str):
        print(f"[textChanged] '{text}'")

    def on_text_edited(self, text: str):
        print(f"[textEdited] '{text}'")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MW()
    sys.exit(app.exec())
