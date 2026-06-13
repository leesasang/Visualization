import sys
import time

# QThread: Qt의 thread abstraction.
# Signal: thread 간 안전하게 데이터를 전달하기 위한 Qt signal.
from PySide6.QtCore import QThread, Signal

# 예제 GUI를 구성하기 위한 widget들.
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    # 진행 상태(0~100)를 GUI로 전달하기 위한 signal.
    # emit(int) 형태로 사용됨.
    update_signal = Signal(int)

    def __init__(self, thread_id):
        super().__init__()

        # 단순 식별용 ID.
        self.thread_id = thread_id

    def run(self):
        """
        start()가 호출되면 Qt가 새 OS thread를 생성하고,
        그 thread 안에서 run()을 실행한다.

        QThread instance는 종료 후 다시 start()할 수 있다.
        따라서 이 예제에서는 같은 WorkerThread instance를 재사용하되,
        start()가 다시 호출될 때마다 run()이 다시 실행된다.
        """
        for i in range(101):
            # 실제 작업을 단순화하여 표현한 코드.
            # CPU를 계속 사용하는 계산이 아니라
            # 일정 시간 대기하는 상황을 가정한다.
            time.sleep(0.1)

            # 진행률을 GUI thread로 전달.
            # Qt의 queued connection을 통해
            # GUI thread에서 안전하게 처리된다.
            self.update_signal.emit(i)


class MonitorThread(QThread):
    # 모든 worker thread가 종료되었음을 알리는 signal.
    all_done = Signal()

    def __init__(self, threads):
        super().__init__()

        # 이번에 감시할 worker thread 목록.
        # WorkerThread 자체는 MW에서 계속 보관하고 재사용한다.
        # MonitorThread는 이 목록을 받아 wait()만 수행한다.
        self.threads = threads

    def run(self):
        """
        모든 worker thread가 종료될 때까지 기다린다.

        중요한 점:
        wait()를 호출하는 주체가 GUI thread가 아니라
        MonitorThread라는 것이다.

        따라서 wait()로 인해 block되는 것은
        MonitorThread이며 GUI event loop는 계속 동작한다.
        """
        for thread in self.threads:
            # 대상 worker thread가 종료될 때까지 대기.
            # 여기서 block되는 것은 이 run()을 실행 중인 MonitorThread임.
            thread.wait()

        # 모든 worker가 종료되었음을 GUI thread에 알림.
        self.all_done.emit()


class MW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread Monitor Example")

        self.init_ui()
        self.show()

    def init_ui(self):
        # 전체 widget을 수직으로 배치하는 layout.
        self.layout = QVBoxLayout(self)

        # 현재 상태를 표시하는 label.
        self.status_label = QLabel(
            "Click 'Start All Threads' to run the threads",
            self,
        )
        self.layout.addWidget(self.status_label)

        # 모든 worker를 한 번에 실행하는 버튼.
        self.start_all_button = QPushButton("Start All Threads", self)
        self.start_all_button.clicked.connect(self.start_all_threads)
        self.layout.addWidget(self.start_all_button)

        # Example 0과 동일하게 progress bar, worker thread,
        # 개별 실행 button을 list로 관리한다.
        self.progress_bars = []
        self.threads = []
        self.buttons = []

        # 현재 실행 중인 monitor thread.
        # monitor가 없거나 종료된 상태이면 None으로 둔다.
        self.monitor_thread = None

        for i in range(3):
            label = QLabel(f"Thread {i + 1} Example", self)

            progress_bar = QProgressBar(self)
            progress_bar.setRange(0, 100)

            button = QPushButton(f"Start Thread {i + 1}", self)
            button.clicked.connect(self.make_start_thread(i))

            self.layout.addWidget(label)
            self.layout.addWidget(progress_bar)
            self.layout.addWidget(button)

            # WorkerThread는 여기서 한 번 생성하고 계속 재사용한다.
            # 종료 후에도 self.threads에서 제거하지 않는다.
            worker = WorkerThread(i)

            # worker가 emit한 진행률 값을 해당 progress bar에 반영.
            worker.update_signal.connect(progress_bar.setValue)

            # worker가 종료되면 해당 개별 실행 button을 다시 활성화.
            # WorkerThread는 재사용하므로 reference를 None으로 바꾸지 않는다.
            worker.finished.connect(
                lambda idx=i: self.on_worker_finished(idx)
            )

            self.progress_bars.append(progress_bar)
            self.threads.append(worker)
            self.buttons.append(button)

    def make_start_thread(self, index):
        """
        index별 실행 함수를 생성한다.

        lambda를 직접 사용하는 대신 별도 함수를 만들어
        현재 index 값을 안전하게 캡처한다.
        """

        def start_thread():
            self.start_worker_thread(index)

        return start_thread

    def start_worker_thread(self, index):
        """
        특정 worker 하나만 실행한다.
        """
        worker = self.threads[index]

        # 이미 실행 중이면 중복 실행하지 않는다.
        # 실행 중인 QThread에 다시 start()를 호출하면 안 된다.
        if worker.isRunning():
            return

        # 이전 실행 결과가 progress bar에 남아 있을 수 있으므로 초기화.
        # WorkerThread도 emit(0)을 보내지만, button을 누른 즉시 UI 상태를
        # 명확히 보여주기 위해 GUI thread에서 먼저 0으로 설정한다.
        self.progress_bars[index].setValue(0)

        # 실행 중에는 같은 worker를 다시 시작하지 못하도록 button 비활성화.
        self.buttons[index].setEnabled(False)

        # 기존 WorkerThread instance를 재사용하여 다시 시작.
        # 종료된 QThread는 다시 start()할 수 있다.
        worker.start()

    def on_worker_finished(self, index):
        """
        worker 종료 시 호출된다.
        """
        # WorkerThread는 재사용하므로 self.threads[index]를 제거하지 않는다.
        # 다음 실행에서는 같은 WorkerThread instance에 다시 start()를 호출한다.
        self.buttons[index].setEnabled(True)

    def start_all_threads(self):
        """
        모든 worker를 실행하고,
        MonitorThread를 통해 종료를 감시한다.
        """

        # 이미 monitor가 실행 중이면 전체 실행을 중복 시작하지 않는다.
        # MonitorThread는 worker thread들의 종료를 감시하는 역할이므로,
        # 여러 개가 동시에 실행될 필요가 없다.
        if self.monitor_thread is not None and self.monitor_thread.isRunning():
            return

        self.status_label.setText("Threads are running...")

        # 전체 실행 중에는 전체 실행 button을 비활성화한다.
        # MonitorThread가 종료되면 on_monitor_finished()에서 다시 활성화한다.
        self.start_all_button.setEnabled(False)

        # 이번 MonitorThread가 wait()로 감시할 worker 목록.
        workers_to_monitor = []

        for index, worker in enumerate(self.threads):
            # 이미 실행 중인 worker는 새로 시작하지 않는다.
            # 다만 현재 실행 중인 worker도 전체 완료 판단에 포함되어야 하므로
            # monitor의 감시 대상에는 추가한다.
            if worker.isRunning():
                workers_to_monitor.append(worker)
                continue

            # 실행 중이 아닌 worker는 기존 WorkerThread instance를 재사용하여 시작한다.
            self.progress_bars[index].setValue(0)
            self.buttons[index].setEnabled(False)

            workers_to_monitor.append(worker)
            worker.start()

        # 모든 worker 종료를 감시할 monitor 생성.
        # WorkerThread는 재사용하지만 MonitorThread는 이번 감시 작업을 위한
        # 일회성 thread로 새로 생성한다.
        self.monitor_thread = MonitorThread(workers_to_monitor)

        # 모든 worker 종료 시 상태 label 갱신.
        self.monitor_thread.all_done.connect(
            self.update_status_label
        )

        # monitor 종료 시 후처리.
        self.monitor_thread.finished.connect(
            self.on_monitor_finished
        )

        # monitor 시작.
        # 내부 run()에서 각 worker에 대해 wait()를 호출하지만,
        # GUI thread가 아닌 MonitorThread가 block되므로 GUI는 계속 응답 가능.
        self.monitor_thread.start()

    def update_status_label(self):
        """
        모든 worker가 종료되었을 때 호출된다.
        """
        self.status_label.setText("All threads completed!")

    def on_monitor_finished(self):
        """
        MonitorThread 종료 후 정리 작업.
        """

        # 전체 실행 button 다시 활성화.
        self.start_all_button.setEnabled(True)

        # MonitorThread는 이번 감시 작업이 끝났으므로 reference 제거.
        # WorkerThread들은 self.threads에 그대로 남겨 재사용한다.
        self.monitor_thread = None

    def closeEvent(self, event):
        """
        창 닫기 요청 처리.

        실행 중인 thread가 있는 상태에서 QWidget이 파괴되면
        다음과 같은 문제가 발생할 수 있다.

        QThread: Destroyed while thread is still running

        이를 방지하기 위해 실행 중인 thread가 있으면
        창 닫기를 거부한다.
        """

        # 현재 실행 중인 worker 목록 수집.
        running_workers = [
            thread
            for thread in self.threads
            if thread.isRunning()
        ]

        # MonitorThread가 존재하고 현재 실행 중인지 확인.
        # MonitorThread 역시 QThread이므로 실행 중인 상태에서 객체가
        # 파괴되면 문제가 발생할 수 있다.
        monitor_running = (
            self.monitor_thread is not None
            and self.monitor_thread.isRunning()
        )

        # worker thread 또는 monitor thread 중 하나라도 실행 중이면
        # window close를 허용하지 않는다.
        if running_workers or monitor_running:
            self.status_label.setText(
                "Threads are still running. Wait until they finish."
            )

            # close 요청을 취소함.
            event.ignore()
            return

        # 실행 중인 thread가 하나도 없는 경우에만
        # 부모 클래스의 closeEvent()를 호출하여 정상적으로 window를 닫음.
        super().closeEvent(event)


if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # 메인 윈도우 생성.
    wnd = MW()

    # Qt event loop 시작.
    sys.exit(app.exec())
