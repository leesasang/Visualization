class CustomDlg(QDialog):
    def __init__(self, parent=None):
        """ 생성자(Constructor) """
        super().__init__(parent)

        self.setWindowTitle('Hello, QDialog')

        # QDialogButtonBox를 사용하여 표준 버튼 (OK, Cancel)을 생성
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        # button_box의 accepted 시그널을 QDialog의 내장 슬롯인 accept에 연결
        self.button_box.accepted.connect(self.accept)
        # button_box의 rejected 시그널을 QDialog의 내장 슬롯인 reject에 연결
        self.button_box.rejected.connect(self.reject)

        # 대화상자 내부 레이아웃 설정
        self.layout = QVBoxLayout()
        message = QLabel('Is something ok?')
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
