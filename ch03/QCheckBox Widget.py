import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLabel,
        QVBoxLayout, QCheckBox, QButtonGroup,
    )
    from PySide6.QtCore import Qt
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel,
            QVBoxLayout, QCheckBox, QButtonGroup,
        )
        from PyQt6.QtCore import Qt
        qt_modules = 'PyQt6'
    except ImportError:
        print("PySide6 또는 PyQt6가 설치되어 있지 않습니다.")
        sys.exit(1)

print(f"Using {qt_modules} binding.")


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ex: QCheckBox with Exclusive Toggle")
        self.resize(400, 250)
        self.init_ui()
        self.show()

    def init_ui(self):
        lm = QVBoxLayout()
        self.setLayout(lm)

        lm.addWidget(QLabel('What is most important?'))

        # QCheckBox 3개 생성 및 layout에 추가
        checkbox_texts = ['1. faith', '2. hope', '3. love']
        self.checkboxes = [QCheckBox(text) for text in checkbox_texts]
        for cb in self.checkboxes:
            lm.addWidget(cb)

        # 선택 결과 표시용 label
        self.dp_label = QLabel("")
        lm.addWidget(self.dp_label)

        # QButtonGroup으로 그룹화 → exclusive 모드로 시작
        self.bg = QButtonGroup(self)
        for cb in self.checkboxes:
            self.bg.addButton(cb)
        self.bg.setExclusive(True)
        self.bg.buttonClicked.connect(self.on_checkbox_clicked)

        # exclusive 모드 전환용 check box
        # exclusive=True → 복수 선택 불가이므로, 초기 체크 상태는 False
        self.cb_toggle_exclusive = QCheckBox("Check it for multiple selection.")
        self.cb_toggle_exclusive.setChecked(not self.bg.exclusive())
        self.cb_toggle_exclusive.toggled.connect(self.on_toggle_exclusive)
        lm.addWidget(self.cb_toggle_exclusive)

    def on_checkbox_clicked(self, button):
        """그룹 내 check box 클릭 시 호출됨.
        클릭된 button instance가 인자로 전달됨.
        """
        self.dp_label.setText(button.text())

    def on_toggle_exclusive(self, state: bool):
        """exclusive 모드 on/off 전환 처리.
        전환 전에 모든 check box를 unchecked 상태로 초기화함.
        """
        print(f"multiple selection mode: {state}")
        self.reset_checkboxes(False)
        self.bg.setExclusive(not state)

    def reset_checkboxes(self, state: bool):
        """모든 check box를 주어진 상태(state)로 설정함.

        exclusive 모드에서는 Qt가 "항상 하나는 checked 상태를 유지"하도록 강제함.
        따라서 현재 checked된 버튼에 setChecked(False)를 호출해도 Qt가 이를 무시함.
        결과적으로 exclusive 모드가 활성화된 상태에서는 모든 버튼을 unchecked로 만들 수 없음.
        이를 우회하기 위해 setExclusive(False)로 잠시 해제 후 초기화하고 원래 상태로 복원함.

        세 방식 모두 for문을 사용함. 차이는 어떤 컨테이너를 순회하느냐에 있음.

        approach 01 — self.checkboxes 순회, toggle() 이용:
            현재 checked 상태를 확인 후 반전시키는 방식.
            for cb in self.checkboxes:
                if cb.isChecked(): cb.toggle()

        approach 02 — self.checkboxes 순회, setChecked() 이용:
            목표 상태를 직접 지정하는 방식.
            for cb in self.checkboxes:
                cb.setChecked(state)

        approach 03 — bg.buttons() 순회 (현재 사용):
            QButtonGroup에서 직접 버튼 목록을 가져오므로
            self.checkboxes 같은 별도 attribute를 유지하지 않아도 됨.
        """
        old_exclusive = self.bg.exclusive()
        self.bg.setExclusive(False)

        for cb in self.bg.buttons():   # approach 03
            cb.setChecked(state)

        self.bg.setExclusive(old_exclusive)
        print("--------------")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
