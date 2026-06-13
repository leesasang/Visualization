import sys

from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window의 title 설정.
        self.setWindowTitle("QMessageBox StandardButton Example")

        # 여러 button을 배치하기 위한 central widget 생성.
        central_widget = QWidget(self)

        # button들을 격자 형태로 배치하기 위한 layout 생성.
        layout = QGridLayout(central_widget)

        # 테스트할 QMessageBox.StandardButton 목록.
        button_items = [
            ("Ok", QMessageBox.StandardButton.Ok),
            ("Cancel", QMessageBox.StandardButton.Cancel),
            ("Open", QMessageBox.StandardButton.Open),
            ("Close", QMessageBox.StandardButton.Close),
            ("Save", QMessageBox.StandardButton.Save),
            ("SaveAll", QMessageBox.StandardButton.SaveAll),
            ("Discard", QMessageBox.StandardButton.Discard),
            ("Apply", QMessageBox.StandardButton.Apply),
            ("Reset", QMessageBox.StandardButton.Reset),
            ("RestoreDefaults", QMessageBox.StandardButton.RestoreDefaults),
            ("Help", QMessageBox.StandardButton.Help),
            ("Yes", QMessageBox.StandardButton.Yes),
            ("YesToAll", QMessageBox.StandardButton.YesToAll),
            ("No", QMessageBox.StandardButton.No),
            ("NoToAll", QMessageBox.StandardButton.NoToAll),
            ("Abort", QMessageBox.StandardButton.Abort),
            ("Ignore", QMessageBox.StandardButton.Ignore),
            ("Retry", QMessageBox.StandardButton.Retry),
        ]

        # 각 StandardButton을 확인하기 위한 QPushButton 생성.
        for idx, (button_name, standard_button) in enumerate(button_items):
            button = QPushButton(button_name, self)

            # 각 QPushButton에 대응되는 QMessageBox.StandardButton을 저장.
            button.standard_button = standard_button

            # button이 click되면 button_clicked method가 호출되도록 연결.
            button.clicked.connect(self.button_clicked)

            # button을 layout에 추가.
            row = idx // 3
            col = idx % 3
            layout.addWidget(button, row, col)

        # central widget 설정.
        self.setCentralWidget(central_widget)

        # Main window 크기 설정.
        self.resize(520, 320)

        # Main window를 화면에 표시.
        self.show()

    def button_clicked(self, checked):
        # Dialog 관련 기능 테스트를 위한 method.
        # checked는 QPushButton이 checkable일 때 현재 선택 상태를 나타냄.
        # 일반 QPushButton에서는 보통 False가 전달됨.
        print("click", checked)

        # signal을 발생시킨 QPushButton 객체를 얻음.
        button = self.sender()

        # QPushButton에 표시된 text 확인.
        button_name = button.text()

        # QPushButton에 저장해 둔 QMessageBox.StandardButton 확인.
        standard_button = button.standard_button

        # QMessageBox.information() static method 사용.
        # 4번째 인자인 buttons만 선택된 button에 따라 다르게 전달함.
        ans = QMessageBox.information(
            self,
            f"QMessageBox.StandardButton.{button_name}",
            f"This dialog uses StandardButton.{button_name}.",
            standard_button,
        )

        print("Selected QMessageBox button:", ans)
        print("Selected QMessageBox button name:", ans.name)


if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # Main window 객체 생성.
    wnd = MW()

    # Qt event loop 시작.
    app.exec()
