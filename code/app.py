from PySide6 import QtWidgets, QtGui, QtCore
from scrap import Scrap
from pathlib import Path
import sys
from pprint import pprint


scrap = Scrap()
class Root(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        # └── Create the main widget
        self.MAIN_WIDGET = QtWidgets.QWidget()
        self.MAIN_LAYOUT = QtWidgets.QHBoxLayout()


        # └── Create the 'scroll area' and the 'content area' and put them inside the main widget
        #     └── SCROLL AREA
        self.scroll_area = QtWidgets.QScrollArea()                                  # Create the scroll area
        self.scroll_area_widget = QtWidgets.QWidget()                               # Create and add a widget to that scroll area ( will contain our button )
        self.scroll_area_widget_layout = QtWidgets.QVBoxLayout()                    # Design a vertical layout box for our button

        titles = scrap._categories_title()                                          # titles for the buttons
        for i in range(len(titles)):                                                # Add the button to the layout box
            btn = QtWidgets.QPushButton(titles[i])
            self.scroll_area_widget_layout.addWidget(btn)
            btn.clicked.connect(lambda _, b=btn, i=i: self.scroll_button(b, i))

        self.scroll_area_widget.setLayout(self.scroll_area_widget_layout)           # Apply the layout to the scroll area 
        #           └── Scroll area properties
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setFixedWidth(175)

        #      └── CONTENT AREA
        self.content_scroll_area = QtWidgets.QScrollArea()
        self.stacked_layout_container = QtWidgets.QWidget()
        self.stacked_layout = QtWidgets.QStackedLayout()

        self.stacked_img_layout_container = QtWidgets.QWidget()
        self.stacked_img_layout = QtWidgets.QStackedLayout()

        IMG_DIR = Path(__file__).parent / "img_save_dir"
        img_book_title: dict = scrap.des_title()
        for i in range(len(scrap._categories_title())):
            self.content_area = QtWidgets.QWidget()                                     # Create the content area
            self.content_area_hlayout = QtWidgets.QHBoxLayout()                          # Design the vertical layout box for the contents
            self.content_area_vlayout = QtWidgets.QVBoxLayout()
            
            # putting the images
            title_text = scrap._categories_title()[i]
            title = img_book_title[title_text]
            IMG = IMG_DIR / title_text

            for img_path, img_title_index in zip(IMG.iterdir(), range(len(title))):
                # create containers
                book_info = QtWidgets.QWidget()
                book_info_layout = QtWidgets.QVBoxLayout()
                
                # create the image label
                img_label = QtWidgets.QLabel()
                img_label.setStyleSheet("border: 1px solid blue")
                pixmap = QtGui.QPixmap(img_path)
                img_label.setPixmap(pixmap)
                ## img_label.setScaledContents(True)

                # create the title label
                # img_title = QtWidgets.QLabel(img_book_title[img_title_index])

                # create the button link
                img_title_btn = QtWidgets.QPushButton(title[img_title_index])
                img_title_btn.clicked.connect(lambda _, b=img_title_btn, i=img_title_index: self.book_button(b, i))

                # book page
                book_info_page = QtWidgets.QWidget()
                book_info_page_layout = QtWidgets.QHBoxLayout()
                page_img_label = QtWidgets.QLabel()
                page_img_label.setStyleSheet("border: 1px solid blue")
                pixmap = QtGui.QPixmap(img_path)
                page_img_label.setPixmap(pixmap)
                page_img_text = QtWidgets.QLabel(f"ialhfsdkhakbkhd sfiuafhiquawhfn coweaofhu bqrhadfsbo cquafidkh askgf iewagfi qwyva kgaqyhfb iwhdbioaqfwg qi")
                book_info_page_layout.addWidget(page_img_label)
                book_info_page_layout.addWidget(page_img_text)
                book_info_page.setLayout(book_info_page_layout)
                self.stacked_img_layout.addWidget(book_info_page)
                self.stacked_img_layout_container.setLayout(self.stacked_img_layout)
                self.stacked_img_layout_container.setFixedSize(300, 200)

                
                book_info_layout.addWidget(img_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
                # book_info_layout.addWidget(img_title, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
                book_info_layout.addWidget(img_title_btn, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
                book_info.setLayout(book_info_layout)
                book_info.setFixedSize(300, 200)
                
                
                if self.content_area_hlayout.count() < 4:
                    self.content_area_hlayout.addWidget(book_info)
                    book_info_layout = QtWidgets.QVBoxLayout()

                else:
                    self.content_area_vlayout.addLayout(self.content_area_hlayout)
                    self.content_area_hlayout = QtWidgets.QHBoxLayout()
                    book_info_layout = QtWidgets.QVBoxLayout()
                    self.content_area_hlayout.addWidget(book_info)

                if self.content_area_hlayout.count() > 0:
                    self.content_area_vlayout.addLayout(self.content_area_hlayout)

            self.content_area.setLayout(self.content_area_vlayout)
            self.stacked_layout.addWidget(self.content_area)

        self.content_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.content_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.content_scroll_area.setWidgetResizable(True)
        self.stacked_layout_container.setLayout(self.stacked_layout)
        self.content_scroll_area.setWidget(self.stacked_layout_container)


        #      └── ADD THE SCROLL AREA AND CONTENT AREA TO THE MAIN LAYOUT
        self.MAIN_LAYOUT.addWidget(self.scroll_area)
        self.MAIN_LAYOUT.addWidget(self.content_scroll_area)
        self.MAIN_LAYOUT.addWidget(self.stacked_img_layout_container)

        # └── General window of the app configuration
        self.MAIN_WIDGET.setLayout(self.MAIN_LAYOUT)
        self.setCentralWidget(self.MAIN_WIDGET)


    def scroll_button(self, btn, index):
        # def __init__(self, btn):
        print(f"you clicked the '{ btn.text() }' button")
        self.stacked_layout.setCurrentIndex(index)

    def book_button(self, btn, index):
        print(f"you clicked on the '{ btn.text() }' button!!!")
        self.stacked_img_layout.setCurrentIndex(index)



if __name__ == "__main__":
    import sys
    from traceback import print_exc

    app = QtWidgets.QApplication(sys.argv)

    print("Before creating window")
    try:
        win = Root()
    except Exception:
        print("Exception during window creation:")
        print_exc()
        sys.exit(1)

    print("Before showing window")
    win.show()
    print("After showing window, before exec")
    app.exec()
    print("After app.exec()")
