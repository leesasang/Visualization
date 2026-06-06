# 1. 필요한 library 및 module을 import 하기
import sys

# PySide6/PyQt6 사용을 확인하기 위한 flag
PYSIDE = False
PYQT = False

# PySide6를 우선적으로 import 하도록 시도
try:
    import PySide6.QtCore
    from PySide6.QtWidgets import (QApplication, QWidget, QLabel)
    PYSIDE = True
except ImportError: # ImportError만 처리하여 예외 처리 명확성 증가
    pass # 실패 시, 특별한 처리 없이 넘어감

# PySide6 import에 실패했을 경우, PyQt6를 import 하도록 시도
if not PYSIDE:
    try:
        import PyQt6.QtCore
        from PyQt6.QtWidgets import (QApplication, QWidget, QLabel)
        PYQT = True
    except ImportError: # ImportError만 처리하여 예외 처리 명확성 증가
        pass # 실패 시, 특별한 처리 없이 넘어감

# 2. 만들고자 하는 GUI 프로그램의 class를 구현
# QWidget을 상속받아 새로운 class MW를 정의
class MW(QWidget):
    def __init__(self):
        """ 생성자(Constructor) """
        # 부모 class인 QWidget의 생성자를 호출하여 초기화
        super().__init__()
        # UI 초기화를 담당하는 method 호출
        self.initialize_ui()

    def initialize_ui(self):
        """Application의 UI 설정을 담당"""
        # Window의 위치와 크기를 설정. 
        # setGeometry(x position, y position, width, height)
        self.setGeometry(200, 100, 400, 200)

        # Window의 title bar에 보일 text를 설정
        self.setWindowTitle("Main Window in PyQt or PySide. 한글.")

        # Window에 포함될 widget들을 설정하는 method 호출
        self.setup_main_wnd()

        # 설정된 Window를 화면에 표시 
        # (부모가 없는 widget은 show() 호출 필요)
        self.show()

    def setup_main_wnd(self):
        """메인 Window에 포함될 widget들을 생성 및 설정"""
        # QLabel widget을 생성. 
        # 생성자의 인자로 'self'를 넘겨주어, 이 widget의 parent를 MW instance로 지정.
        hello_label = QLabel(self)

        # Label에 표시될 text를 'Hello, World and Qt!'로 설정
        hello_label.setText('Hello, World and Qt!')

        # Label의 위치를 
        # parent widget의 좌상단으로부터 x=150, y=90 위치로 이동 
        # (절대 위치 지정 방식)
        hello_label.move(150,90)

# 3. Main script로 동작하는 루틴 구현
if __name__ == '__main__':
    # PySide 사용 시 PySide6 버전 정보 출력
    if PYSIDE:
        print(PySide6.__version__)
        print(PySide6.QtCore.__version__)
    # PyQt 사용 시 PyQt6(Qt) 버전 정보 출력
    elif PYQT:
        print(PyQt6.QtCore.qVersion())
    # PySide6나 PyQt6 모두 사용 불가능할 경우 메시지 출력 후 종료
    else: 
        print("Neither PySide6 nor PyQt6 is available. Please install one.")
        sys.exit(1)

    # 모든 PyQt/PySide GUI application은 
    # 하나의 QApplication instance를 필요로 함
    # sys.argv를 통해 command line arguments를 application에 전달
    app = QApplication(sys.argv)

    # Main window(MW)의 instance를 생성
    window = MW()

    # application의 event loop를 시작
    # app.exec()가 반환하는 종료 코드를 
    # sys.exit()에 전달하여 script를 안전하게 종료
    sys.exit(app.exec())
