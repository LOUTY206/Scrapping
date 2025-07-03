from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QFrame
)
from PySide6.QtCore import Signal, Qt
import sys

class ClickableWidget(QFrame):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("QFrame { background-color: #eef; border: 1px solid #99c; }")
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Create a clickable widget
        click_widget = ClickableWidget()
        inner_layout = QVBoxLayout(click_widget)

        label1 = QLabel("This is inside a 'button'")
        label2 = QLabel("Click anywhere here!")
        inner_layout.addWidget(label1)
        inner_layout.addWidget(label2)

        click_widget.clicked.connect(self.on_widget_clicked)

        layout.addWidget(click_widget)

    def on_widget_clicked(self):
        print("The layout-button was clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
