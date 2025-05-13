import cv2
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QPalette
from PyQt5.QtWidgets import QFrame

class ImageWidget(QWidget):
    def __init__(self, parent=None, background_color="white"):
        super().__init__(parent)
        # label for displaying the image
        self.padding = 2
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)
        self.frame = QFrame(self)
        self.frame.setStyleSheet(f"background-color: {background_color}; border-radius: 5px;")
        self.layout.addWidget(self.frame)
        self.image_label = QLabel(self.frame)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setText("Image will be displayed here")
        self.image = None
        self.set_image(None)
        
    def set_image(self, image= None):
        W = self.frame.width()
        H = self.frame.height()
        if image is not None:
            self.image = image.copy()
            self.image_label.setFixedSize(W, H)
            # convert the image from BGR to RGB format
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # convert the image to QImage format
            q_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            # create a QPixmap from the QImage
            pixmap = QPixmap.fromImage(q_image)
            # scale the pixmap to fit within the label
            pixmap = pixmap.scaled(W, H, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # set the pixmap to the label
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("No image loaded")

    # On resize, update the image size
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_image(self.image)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = QWidget()
    # set the window size
    window.setGeometry(100, 100, 800, 600)
    window.setWindowTitle("Image Widget Example")
    layout = QVBoxLayout(window)
    image_widget = ImageWidget()
    layout.addWidget(image_widget)
    
    # Load an image using OpenCV
    image = cv2.imread("./test/1.jpg")
    
    # Set the image to the widget
    image_widget.set_image(image)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

