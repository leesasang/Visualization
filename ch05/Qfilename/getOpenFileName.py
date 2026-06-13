import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
)


class MW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFileDialog.getOpenFileName Example")

        # button을 central widget으로 설정함.
        # button을 누르면 단일 file 선택 dialog가 표시됨.
        button = QPushButton("Open File", self)
        button.clicked.connect(self.open_file)

        self.setCentralWidget(button)
        self.show()

    def open_file(self):
        # 단일 file을 선택하는 dialog.
        # 반환값은 file path 문자열과 선택된 filter 문자열임.
        file_name, selected_filter = QFileDialog.getOpenFileName(
            self,                              # parent widget
            "Open file",                       # dialog title
            "",                                # start directory
            "Text files (*.txt *.html *.py);;All files (*.*)",
        )

        # 사용자가 Cancel을 누르면 file_name은 빈 문자열임.
        if file_name:
            QMessageBox.information(
                self,
                "Selected File",
                f"File: {file_name}\nFilter: {selected_filter}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
