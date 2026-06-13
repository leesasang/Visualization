import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

class MW (QMainWindow):
  def __init__(self):
    super().__init__()
    self.init_ui()
  def init_ui(self):
    """ application의 gui를 초기화하는 메서드"""
    self.fstr = os.path.dirname(
      os.path.abspath(__file__)
    )
    self.setMinimumSize(600,600)
    self.setWindowTitle("Menu bar Ex")
    self.setup_main_wnd()    # main window를 설정하는 메서드 (풀소스코드 참고)
    self.create_actions()    # menu bar에서 수행될 command들에 해당하는 action생성.
    self.create_menu()       # menu bar 생성. 앞서 생성된 action들을 활용.
    self.show()

  def create_actions (self):
    """어플리케이션의command를 만드는 method."""
    pass

  def create_menu(self):
    """어플리케이션의 menu bar를 만드는 method."""
    pass

if __name__ == "__main__":
  app = QApplication(sys.argv)
  wnd = MW()
  sys.exit(app.exec())
