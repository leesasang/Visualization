import sys
import time

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    # worker thread에서 GUI thread로 문자열 message를 전달하기 위한 signal.
    update_signal = Signal(str)

    def run(self):
        # 이 method는 start() 호출 후 새 thread 안에서 실행됨.
        # 직접 run()을 호출하면 새 thread가 생성되지 않으므로 주의해야 함.
        for i in range(5):
            time.sleep(1)
            self.update_signal.emit(f"Working {i + 1}")  # 진행 상태를 GUI thread로 전달.

        # 작업 완료 message를 GUI thread로 전달.
        self.update_signal.emit("Task completed!")


class MW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread Example")

        self.init_ui()
        self.show()

    def init_ui(self):
        # GUI widget 생성.
        self.label = QLabel("Thread Example", self)
        self.button = QPushButton("Start Thread", self)

        # button click 시 worker thread 시작.
        self.button.clicked.connect(self.start_thread)

        # layout 설정.
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # QThread를 상속한 worker thread 객체 생성.
        self.worker = WorkerThread()

        # worker thread에서 발생한 signal을 GUI thread의 slot에 연결.
        # update_label()은 GUI thread에서 호출되므로 QLabel을 안전하게 update할 수 있음.
        self.worker.update_signal.connect(self.update_label)

    def start_thread(self):
        # 이미 thread가 실행 중이면 다시 시작하지 않음.
        # QThread를 중복 실행하는 것을 방지하기 위한 처리임.
        if not self.worker.isRunning():
            self.worker.start()

    def update_label(self, message):
        # GUI widget은 GUI thread에서 update해야 함.
        # worker thread는 직접 QLabel을 수정하지 않고 signal만 emit함.
        self.label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = MW()

    sys.exit(app.exec())
