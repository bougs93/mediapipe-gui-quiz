'''
TUTORIAL - Circular Progress Bar
  - Qt Widgets (CUSTOM WIDGETS / Python / PySide6) PART 1

      https://www.youtube.com/watch?v=E7lhFwcDpMI

      https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QWidget.setFixedSize
'''

import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
import PySide6.QtGui
from PySide6.QtWidgets import *

class CircularProgress(QWidget):
    def __init__(self):
        # QWidget.__init__(self)
        super().__init__()

        # custom proerties
        self.value = 50
        self.width = 200    # 200
        self.height = 200   # 200
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = 0x498bd1
        self.max_value = 100
        self.font_family = 'Segoe UI'
        self.font_size = 12
        self.text ='SAMPLE'         # WG 추가
        self.suffix = '%'
        self.text_color = 0x498bd1

        # set default size without layout
        self.resize(self.width, self.height)  # <- WG 위젯 포함시 보이지 않는 증상

        # WG Add
        # self.setFixedSize(self.width, self.height)  # <- WG 위젯 포함시 보이지 않는 증상 해결방법
        # or main.py | self.progress.setMinimumSize(self.progress.width, self.progress.height)
        self.add_shadow(True)

    def add_shadow(self, enable):
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 80))
            self.setGraphicsEffect(self.shadow)

    def set_value(self, value):
        self.value = value
        self.repaint()  # Render progess bar after change value


    # Paint event ( Desiger your circular progress here)
    #   https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainter.html#PySide6.QtGui.PySide6.QtGui.QPainter.setFont
    #   https://doc.qt.io/qtforpython-6/PySide6/QtGui/QFont.html#PySide6.QtGui.PySide6.QtGui.QFont
    def paintEvent(self, event):
        width = self.width - self.progress_width    # 가변 가로 = 가로 - 진행률 두께
        height = self.height - self.progress_width  # 가변 높이 = 높이 - 진행률 두께
        margin = int( self.progress_width / 2 )           # 여백
        value = int(self.value * 360 / self.max_value)
        # Painter
        paint = QPainter(self)
        # paint.begin(self)  # <- WG
        paint.setRenderHint(QPainter.Antialiasing)  # remove pixelated edges
        paint.setFont(QFont(self.font_family, self.font_size, weight=QFont.Bold))
        # Create rectangele (사각형)
        rect = QRect(0, 0, self.width, self.height) # 위젯과 동일한 너비,높이 사각형을 만들고
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)    # 펜을 사용하여 테두리 제거

        # PEN
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)
        # Set Round Cap
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)    # 펜끝부분이 둥근형태 스타일
        
        # Create ARC / Circular progress
        paint.setPen(pen)
        #   Ark 360' is equal to 360*16 in the Qt, or 5760/16.    https://codetorial.net/pyqt5/paint/drawing_arc.html
        # paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)  # (x, y, w, h, a, alen) 
        paint.drawArc(int(margin), int(margin), int(width), int(height), -90 * 16, -int(value) * 16)  # (x, y, w, h, a, alen) 

        # Create Text
        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)
        # print(rect)
        rect1 = QRect(0, 0, rect.width(), rect.height()-50)                     # WG 수정
        paint.drawText(rect1, Qt.AlignCenter, f"{self.text}" )
        rect2 = QRect(0, 20, rect.width(), rect.height())
        # 100% 표시 숨기기
        # paint.drawText(rect2, Qt.AlignCenter, f"{self.value}{self.suffix}" )    # WG 수정
        # paint.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}" )

        # End
        # paint.end() # QPaint는 항상 end()로 닫아야 함.  # <- WG


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularProgress()
    window.show()
    sys.exit(app.exec())




        