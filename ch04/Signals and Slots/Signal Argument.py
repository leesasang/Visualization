import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Signal Argument Ex")
        self.resize(380, 280)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("What is most important?"))

        # QButtonGroup: 복수의 button을 그룹으로 관리함.
        self.bg = QButtonGroup(self)

        self.cb01 = QCheckBox("1. faith")
        self.cb02 = QCheckBox("2. hope")
        self.cb03 = QCheckBox("3. love")

        for cb in (self.cb01, self.cb02, self.cb03):
            layout.addWidget(cb)
            self.bg.addButton(cb)

        # 기본값: exclusive mode (하나만 선택 가능).
        self.bg.setExclusive(True)

        # buttonClicked Signal은 클릭된 button의 reference를
        # argument로 Slot에 전달함.
        self.bg.buttonClicked.connect(self.on_button_clicked)

        self.dp_label = QLabel("")
        layout.addWidget(self.dp_label)

        # 별도의 checkbox로 exclusive mode를 전환함.
        self.mode_cb = QCheckBox("Check for multiple selection")

        # stateChanged Signal은 check 상태를 나타내는
        # int 값을 argument로 Slot에 전달함.
        self.mode_cb.stateChanged.connect(self.on_mode_changed)
        layout.addWidget(self.mode_cb)

        self.setLayout(layout)

    def on_button_clicked(self, button):
        """
        QButtonGroup.buttonClicked Signal의 Slot.

        이 Signal은 클릭된 button의 reference를
        argument로 전달함.

        Parameters
        ----------
        button : QAbstractButton
            클릭된 button의 reference.
            buttonClicked Signal이 전달하는 argument임.
        """

        text = button.text()
        print(f"[buttonClicked] selected: {text}")
        self.dp_label.setText(f"Selected: {text}")

    def on_mode_changed(self, state):
        """
        QCheckBox.stateChanged Signal의 Slot.

        이 Signal은 check 상태를 나타내는 int 값을
        argument로 전달함.
        Qt.CheckState.Checked(2) 또는
        Qt.CheckState.Unchecked(0) 등의 값이 전달됨.

        Parameters
        ----------
        state : int
            check 상태를 나타내는 값.
            stateChanged Signal이 전달하는 argument임.
        """

        if state == Qt.CheckState.Checked.value:
            self.bg.setExclusive(False)
            print("[stateChanged] multiple selection enabled")
        else:
            self.bg.setExclusive(True)
            print("[stateChanged] exclusive selection enabled")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
