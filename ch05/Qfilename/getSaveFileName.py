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

        self.setWindowTitle("QFileDialog.getSaveFileName Example")

        # button을 누르면 저장할 file path를 선택하는 dialog가 표시됨.
        button = QPushButton("Save File", self)
        button.clicked.connect(self.save_file)

        self.setCentralWidget(button)
        self.show()

    def save_file(self):
        # 저장할 file path를 선택하는 dialog.
        # 이 method는 실제 저장을 수행하지 않고, 저장할 path만 반환함.
        file_name, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save file",
            "",
            "Text files (*.txt);;Python files (*.py);;All files (*.*)",
        )

        # 사용자가 Cancel을 누르면 file_name은 빈 문자열임.
        if file_name:
            # 실제 file 저장은 반환된 path를 이용하여 직접 수행해야 함.
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("Hello QFileDialog\n")
                f.write(f"Selected filter: {selected_filter}\n")

            QMessageBox.information(
                self,
                "Saved",
                f"File saved to:\n{file_name}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
