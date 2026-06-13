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

        self.setWindowTitle("QFileDialog.getOpenFileNames Example")

        # button을 누르면 복수 file 선택 dialog가 표시됨.
        button = QPushButton("Open Files", self)
        button.clicked.connect(self.open_files)

        self.setCentralWidget(button)
        self.show()

    def open_files(self):
        # 복수 file을 선택하는 dialog.
        # 첫 번째 반환값은 file path 문자열들의 list임.
        file_names, selected_filter = QFileDialog.getOpenFileNames(
            self,
            "Open files",
            "",
            "Images (*.png *.jpg *.jpeg);;Text files (*.txt);;All files (*.*)",
        )

        # 사용자가 하나 이상의 file을 선택한 경우 list가 비어 있지 않음.
        if file_names:
            QMessageBox.information(
                self,
                "Selected Files",
                "\n".join(file_names) + f"\n\nFilter: {selected_filter}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
