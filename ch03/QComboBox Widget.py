import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLabel,
        QVBoxLayout, QComboBox,
    )
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel,
            QVBoxLayout, QComboBox,
        )
        qt_modules = 'PyQt6'
    except ImportError:
        print("PySide6 또는 PyQt6가 설치되어 있지 않습니다.")
        sys.exit(1)

print(f"Using {qt_modules} binding.")


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ex: QComboBox")
        self.resize(400, 200)
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        lm = QVBoxLayout()
        lm.addWidget(QLabel('What is most important?'))

        self.items = ['faith', 'hope', 'love']

        self.cb = QComboBox()
        self.cb.addItems(self.items)

        # signal 연결
        self.cb.activated.connect(self.on_selected)
        self.cb.currentIndexChanged.connect(self.on_current_idx_changed)

        lm.addWidget(self.cb)

        self.dp_label = QLabel("")
        lm.addWidget(self.dp_label)

        self.setLayout(lm)

    def on_selected(self, idx: int):
        """activated signal 처리.
        사용자가 item을 클릭할 때마다 호출됨.
        동일 item을 다시 클릭해도 emit됨.
        """
        tmp = f"you selected: {self.items[idx]}"
        print(tmp)
        self.dp_label.setText(tmp)

    def on_current_idx_changed(self, idx: int):
        """currentIndexChanged signal 처리.
        선택된 index가 실제로 변경된 경우에만 호출됨.
        코드에서 setCurrentIndex() 호출 시에도 emit됨.
        """
        print(f"currentIndexChanged: {idx}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
