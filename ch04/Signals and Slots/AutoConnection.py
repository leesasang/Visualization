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


class Worker(QThread):
    """
    별도의 thread에서 Signal을 emit하는 worker.
    """

    notify = Signal(str)

    def run(self):
        import threading

        tid = threading.current_thread().name

        time.sleep(0.5)
        self.notify.emit(f"from worker thread ({tid})")


class MW(QWidget):
    """
    AutoConnection 동작을 확인하는 main window.

    같은 Signal-Slot 연결이라도 emit하는 thread에 따라
    DirectConnection 또는 QueuedConnection으로 자동 결정됨.
    """

    manual_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AutoConnection Ex")
        self.resize(460, 260)

        self.label = QLabel(
            "AutoConnection은 emit하는 thread에 따라\n"
            "Direct 또는 Queued로 자동 결정됨."
        )

        self.btn_same = QPushButton(
            "Emit from Main Thread (→ Direct)"
        )
        self.btn_worker = QPushButton(
            "Emit from Worker Thread (→ Queued)"
        )

        self.btn_same.clicked.connect(self.emit_from_main)
        self.btn_worker.clicked.connect(self.start_worker)

        # AutoConnection (기본값): connect()에
        # connection type을 지정하지 않으면 AutoConnection임.
        self.manual_signal.connect(self.on_notify)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_same)
        layout.addWidget(self.btn_worker)
        self.setLayout(layout)

    def emit_from_main(self):
        """
        Main thread에서 Signal을 emit함.

        Sender와 receiver가 같은 thread이므로
        AutoConnection은 DirectConnection으로 동작함.
        """

        import threading

        tid = threading.current_thread().name
        print(f"\n[Main] emit_from_main() in: {tid}")
        print("[Main] before emit")
        self.manual_signal.emit(f"from main thread ({tid})")
        print("[Main] after emit")

    def start_worker(self):
        """
        Worker thread에서 Signal을 emit하게 함.

        Sender와 receiver가 다른 thread이므로
        AutoConnection은 QueuedConnection으로 동작함.
        """

        self.btn_worker.setEnabled(False)

        self.worker = Worker()

        # 동일한 Slot에 연결하되, connection type은 기본값(Auto).
        self.worker.notify.connect(self.on_notify)
        self.worker.finished.connect(
            lambda: self.btn_worker.setEnabled(True)
        )

        self.worker.start()

    def on_notify(self, message):
        """
        AutoConnection으로 연결된 Slot.

        같은 thread에서 emit되면 즉시 호출되고,
        다른 thread에서 emit되면 Event Loop를 통해 호출됨.
        """

        import threading

        tid = threading.current_thread().name
        print(f"[Slot] on_notify() called in: {tid}")
        print(f"[Slot] message: {message}")

        self.label.setText(
            f"Signal: {message}\n"
            f"Slot executed in: {tid}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
