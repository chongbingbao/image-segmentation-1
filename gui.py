from PySide.QtCore import *
from PySide.QtGui import *

import sys


class Main(QWidget):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        layout  = QVBoxLayout(self)

        picture = PictureLabel("cat-bw.jpg", self)
        picture.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.addWidget(picture)
        layout.addWidget(QLabel("Click for foreground. Shift + Click for background."))

class PictureLabel(QLabel):
    BACKGROUND_POINTS_COLOR = QColor(180, 50, 50, 100)
    FOREGROUND_POINTS_COLOR = QColor(50, 180, 50, 100)
    SCALE = 5

    def __init__(self, image_path, parent=None):
        super(PictureLabel, self).__init__(parent)
        self.image = QPixmap(image_path)
        # Scaling
        self.image = self.image.scaled(self.image.size() * self.SCALE)
        self.setPixmap(self.image)

        self.background_points = set()
        self.foreground_points = set()


    def mousePressEvent(self, event):
        self.new_point(event)

    def mouseMoveEvent(self, event):
        self.new_point(event)

    def new_point(self, event):
        # Getting the point's coordinates
        point = (event.x() / self.SCALE, event.y() / self.SCALE)

        # Ignoring the point if it was already in either of the sets
        for points_set in [self.background_points, self.foreground_points]:
            if point in points_set:
                #points_set.remove(point)
                return

        # Adding the point to the appropriate set
        background = event.modifiers() == Qt.ShiftModifier
        chosen_set = self.background_points if background else self.foreground_points
        chosen_set.add(point)

        self.repaint()

    def paintEvent(self, event):
        super(PictureLabel, self).paintEvent(event)
        painter = QPainter(self)

        painter.drawPixmap(0, 0, self.image)

        # Drawing background points
        painter.setPen(PictureLabel.BACKGROUND_POINTS_COLOR)
        painter.setBrush(PictureLabel.BACKGROUND_POINTS_COLOR)
        for point in self.background_points:
            painter.drawRect(point[0] * self.SCALE, point[1] * self.SCALE, self.SCALE, self.SCALE)

        # Drawing foreground points
        painter.setPen(PictureLabel.FOREGROUND_POINTS_COLOR)
        painter.setBrush(PictureLabel.FOREGROUND_POINTS_COLOR)
        for point in self.foreground_points:
            painter.drawRect(point[0] * self.SCALE, point[1] * self.SCALE, self.SCALE, self.SCALE)


a = QApplication([])
m = Main()
m.show()
sys.exit(a.exec_())