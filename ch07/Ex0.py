import sys
import time

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    # 진행 상태를 int 값으로 전달하기 위한 signal.
    update_signal = Signal(int)

    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id

    def run(self):
        # start() 호출 후 새 worker thread 안에서 실행됨.
        for i in range(101):
            time.sleep(0.1)
            self.update_signal.emit(i)


class MW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread wait() Blocking Example")

        self.init_ui()
        self.show()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.status_label = QLabel("Click 'Start All Threads' to run the threads", self)
        self.layout.addWidget(self.status_label)

        self.start_all_button = QPushButton("Start All Threads", self)
        self.start_all_button.clicked.connect(self.start_all_threads)
        self.layout.addWidget(self.start_all_button)

        self.progress_bars = []
        self.threads = []
        self.buttons = []

        for i in range(3):
            label = QLabel(f"Thread {i + 1} Example", self)

            progress_bar = QProgressBar(self)
            progress_bar.setRange(0, 100)

            button = QPushButton(f"Start Thread {i + 1}", self)
            button.clicked.connect(self.make_start_thread(i))

            self.layout.addWidget(label)
            self.layout.addWidget(progress_bar)
            self.layout.addWidget(button)

            worker = WorkerThread(i)
            worker.update_signal.connect(progress_bar.setValue)

            self.progress_bars.append(progress_bar)
            self.threads.append(worker)
            self.buttons.append(button)

    def make_start_thread(self, index):
        def start_thread():
            if not self.threads[index].isRunning():
                self.threads[index].start()

        return start_thread

    def start_all_threads(self):
        self.status_label.setText("Threads are running...")

        for thread in self.threads:
            if not thread.isRunning():
                thread.start()

        # 주의:
        # 이 method는 GUI thread에서 호출됨.
        # 따라서 내부에서 wait()를 호출하면 GUI thread가 block됨.
        self.wait_for_threads_to_finish()

    def wait_for_threads_to_finish(self):
        for thread in self.threads:
            # 대상 worker thread가 종료될 때까지 현재 thread를 block함.
            # 현재 thread가 GUI thread이므로 GUI event loop가 멈출 수 있음.
            thread.wait()

        self.status_label.setText("All threads completed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = MW()

    sys.exit(app.exec())
