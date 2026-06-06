import sys

# Qt 애플리케이션에 필요한 기본 모듈 import
try:
    from PySide6.QtWidgets import QApplication, QMainWindow
except ImportError:
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow
    except ImportError:
        print("PySide6 또는 PyQt6 라이브러리가 필요합니다.")
        sys.exit(1)

# --- 1. QApplication 인스턴스 생성 ---
# 모든 Qt GUI 애플리케이션은 단 하나의 QApplication 인스턴스를 필요로 함.
# 이 객체는 앱의 전반적인 제어와 이벤트 처리를 담당함.
# sys.argv: 커맨드 라인 인수를 Qt에 전달하는 역할을 함.
app = QApplication(sys.argv)

# --- 2. 메인 윈도우 생성 및 표시 ---
# QMainWindow: 메뉴, 툴바 등을 포함하는 표준적인 최상위 윈도우.
window = QMainWindow()
# show(): 윈도우 객체를 화면에 보이도록 함.
window.show()

# --- 3. 이벤트 루프 시작 ---
# app.exec(): 애플리케이션을 실행하고 이벤트 루프를 시작함.
# 이벤트 루프는 사용자 입력 등의 이벤트를 감지하고 처리하는 역할을 함.
# 윈도우가 닫히면 이벤트 루프가 종료되고, 종료 상태 코드를 반환함.
# sys.exit(): 스크립트가 Qt의 종료 코드로 안전하게 종료되도록 보장함.
sys.exit(app.exec())
