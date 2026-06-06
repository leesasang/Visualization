import sys
import time

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Worker(QThread):
    """
    별도의 thread에서 작업을 수행하고
    완료 시 Signal을 emit하는 worker.
    """

    work_done = Signal(str)

    def run(self):
        import threading

        tid = threading.current_thread().name
        print(f"[Worker] run() executing in: {tid}")

        # 시간이 걸리는 작업을 simulation.
        time.sleep(1)

        self.work_done.emit(f"Work completed in: {tid}")


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QueuedConnection Ex")
        self.resize(420, 180)

        self.label = QLabel(
            "Button을 누르면 worker thread에서 작업 후\n"
            "main thread의 Slot이 비동기로 호출됨."
        )
        self.button = QPushButton("Start Worker")
        self.button.clicked.connect(self.start_worker)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def start_worker(self):
        self.button.setEnabled(False)
        self.label.setText("Worker thread 실행 중...")

        self.worker = Worker()

        # QueuedConnection: Slot이 receiver(main)의
        # Event Loop에서 비동기적으로 실행됨.
        self.worker.work_done.connect(
            self.on_work_done,
            Qt.ConnectionType.QueuedConnection,
        )

        self.worker.start()

    def on_work_done(self, message):
        """
        QueuedConnection으로 연결된 Slot.

        Worker thread에서 emit된 Signal이
        main thread의 posted event queue에 등록된 뒤,
        main thread의 Event Loop가 처리할 때 호출됨.
        """

        import threading

        tid = threading.current_thread().name
        print(f"[QueuedConnection] on_work_done() called in: {tid}")
        print(f"[QueuedConnection] message: {message}")

        self.label.setText(
            f"Result: {message}\n"
            f"Slot executed in: {tid}"
        )
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
