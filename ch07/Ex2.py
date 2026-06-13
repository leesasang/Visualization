import sys
import time

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class TaskSignals(QObject):
    # QRunnable은 QObject가 아니므로 Signal을 직접 선언하지 않음.
    # 대신 QObject를 상속한 별도 class에서 signal을 선언함.
    update_signal = Signal(str, int)


class Task(QRunnable):
    def __init__(self, num):
        super().__init__()

        # num은 label index로도 사용하므로 0부터 시작함.
        self.num = num

        # 작업 진행 상태를 main thread로 전달하기 위한 signal 객체.
        self.signals = TaskSignals()

    def run(self):
        # 이 method는 QThreadPool 내부의 worker thread에서 실행됨.
        # 따라서 이 안에서 QLabel 같은 GUI widget을 직접 수정하면 안 됨.
        for i in range(101):
            time.sleep(0.1)  # 작업을 모방하기 위한 시간 지연

            # GUI 갱신 요청은 signal을 통해 main thread로 전달함.
            # num은 0부터 시작하지만, 사용자에게 보여줄 때는 1부터 표시함.
            self.signals.update_signal.emit(
                f"Task {self.num + 1}: {i}% completed",
                self.num
            )

        # 작업 완료 메시지 전송.
        self.signals.update_signal.emit(
            f"Task {self.num + 1}: Task completed!",
            self.num
        )


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # QRunnable은 thread 자체가 아니라 task이므로,
        # 화면 표시도 Thread가 아니라 Task로 표현함.
        self.labels = [
            QLabel(f"Task {i + 1}: Waiting to start...", self)
            for i in range(3)
        ]

        for label in self.labels:
            self.layout.addWidget(label)

        self.start_button = QPushButton("Start All Tasks", self)
        self.start_button.clicked.connect(self.start_tasks)
        self.layout.addWidget(self.start_button)

        # Qt application 전체에서 공유되는 global thread pool 사용.
        self.pool = QThreadPool.globalInstance()

    @Slot()
    def start_tasks(self):
        # 버튼을 여러 번 눌러 동일한 작업들이 중복 등록되는 것을 막음.
        self.start_button.setEnabled(False)

        for i in range(3):
            # 각 작업마다 QRunnable 객체를 새로 생성함.
            # 기본 autoDelete=True이므로 작업 완료 후 QThreadPool이 객체를 정리함.
            task = Task(i)

            # 작업을 시작하기 전에 signal-slot connection을 먼저 수행해야 함.
            # start() 이후에 connect하면 작업이 먼저 signal을 emit할 수 있음.
            task.signals.update_signal.connect(self.update_label)

            # QRunnable 작업을 thread pool에 추가함.
            # 실제 run()은 QThreadPool 내부 worker thread에서 실행됨.
            self.pool.start(task)

    @Slot(str, int)
    def update_label(self, message, idx):
        # 이 slot은 main thread에서 실행되므로 GUI widget 수정 가능.
        self.labels[idx].setText(message)

        # 모든 task가 완료되면 버튼을 다시 활성화함.
        if all(label.text().endswith("Task completed!") for label in self.labels):
            self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
