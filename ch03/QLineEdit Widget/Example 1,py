import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLabel,
        QVBoxLayout, QLineEdit,
    )
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel,
            QVBoxLayout, QLineEdit,
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
        self.setWindowTitle("QLineEdit Signal Example")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        lm = QVBoxLayout()

        lm.addWidget(QLabel('What is most important?'))

        self.le = QLineEdit()
        self.le.setMaxLength(10)                         # 최대 10자 제한
        self.le.setPlaceholderText("Type something...")  # placeholder text

        # 각 Signal을 Slot(메서드)에 연결
        self.le.returnPressed.connect(self.on_return_pressed)
        self.le.textChanged.connect(self.on_changed)
        self.le.textEdited.connect(self.on_edited)
        self.le.editingFinished.connect(self.on_editing_finished)

        lm.addWidget(self.le)

        # 결과 표시용 Label 4개 생성
        self.dp_label0 = QLabel("textChanged: (대기 중)")
        self.dp_label1 = QLabel("textEdited: (대기 중)")
        self.dp_label2 = QLabel("editingFinished: (대기 중)")
        self.dp_label3 = QLabel("textChanged (직접 연결): (대기 중)")

        for lbl in (self.dp_label0, self.dp_label1,
                    self.dp_label2, self.dp_label3):
            lm.addWidget(lbl)

        # textChanged Signal을 QLabel.setText에 직접 연결하는 방법
        self.le.textChanged.connect(self.dp_label3.setText)

        self.setLayout(lm)

    def on_return_pressed(self):
        """Enter/Return 키 입력 시 호출됨."""
        selected = self.le.selectedText()
        print(f"[returnPressed] selected text: '{selected}'")

    def on_changed(self, text: str):
        """textChanged Signal 처리.
        코드에 의한 setText() 호출 시에도 emit됨.
        """
        self.dp_label0.setText(f"textChanged: '{text}'")

    def on_edited(self, text: str):
        """textEdited Signal 처리.
        사용자가 직접 키보드로 입력할 때만 emit됨.
        """
        self.dp_label1.setText(f"textEdited: '{text}'")

    def on_editing_finished(self):
        """editingFinished Signal 처리.
        이 Signal은 인자를 전달하지 않으므로 text()로 직접 가져옴.
        """
        current_text = self.le.text()
        self.dp_label2.setText(f"editingFinished: '{current_text}'")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
