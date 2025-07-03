from PySide6 import QtWidgets, QtCore, QtGui
from scrap import Scrap
import sys
from pathlib import Path
import json
from pprint import  pprint

scrap = Scrap()
class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        



    def setup_ui(self):
        # CREATION OF THE DIFFERENT WINDOWS
        create = True
        if create:
            # I- Main window
            self.MAIN_WIDGET = QtWidgets.QWidget()
            self.MAIN_LAYOUT = QtWidgets.QHBoxLayout()

            self.MAIN_WIDGET.setLayout(self.MAIN_LAYOUT)
            ## II- Different sub-windows
            ### II.1- Categories area
            self.Categories_scroll_area = QtWidgets.QScrollArea()
            self.Categories_widget = QtWidgets.QWidget()
            self.Categories_widget_layout = QtWidgets.QVBoxLayout()

            self.Categories_widget.setLayout(self.Categories_widget_layout)
            self.Categories_scroll_area.setWidget(self.Categories_widget)

            self.Categories_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.Categories_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.Categories_scroll_area.setWidgetResizable(True)
            self.Categories_scroll_area.setFixedWidth(175)
            ### II.2- Categories content area
            self.Content_scroll_area = QtWidgets.QScrollArea()
            self.Content_stacked_widgets = QtWidgets.QWidget()
            self.Content_stacked_widgets_layout = QtWidgets.QStackedLayout()

            self.Content_stacked_widgets.setLayout(self.Content_stacked_widgets_layout)
            self.Content_scroll_area.setWidget(self.Content_stacked_widgets)

            self.Content_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.Content_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.Content_scroll_area.setWidgetResizable(True)
            ### II-3- Book info area
            self.Book_scroll_area = QtWidgets.QScrollArea()
            self.Book_stacked_widgets = QtWidgets.QWidget()
            self.Book_stacked_widgets_layout = QtWidgets.QStackedLayout()

            self.Book_stacked_widgets_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            self.Book_stacked_widgets.setLayout(self.Book_stacked_widgets_layout)
            self.Book_scroll_area.setWidget(self.Book_stacked_widgets)

            self.Book_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.Book_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.Book_scroll_area.setWidgetResizable(True)
        # CATEGORIES AREA
        category = True
        if category:
            ## III- Categories area formation
            categories_area = True
            if categories_area:
                categories = scrap._categories_title()
                for i in range(len(categories)):
                    btn = QtWidgets.QPushButton(categories[i])
                    self.Categories_widget_layout.addWidget(btn)
                    btn.clicked.connect(lambda _, b=btn, i=i: self.Categories_button(b, i))
            ## IV- Categories content area / Book info area
            cb = True
            if cb:
                IMG_DIR = Path(__file__).parent / "scrap" / "img_save_dir"
                PRICE_FILE = Path(__file__).parent / "scrap" / "price_save_dir" / "book_price.json"
                BOOK_TITLE_FILE = Path(__file__).parent / "scrap" / "title_save_dir" / "book_titles.json"
                with open(BOOK_TITLE_FILE, 'r') as file:
                    book_title = json.load(file)
                with open(PRICE_FILE, 'r') as file:
                    prices = json.load(file)

                for i in range(len(scrap._categories_title())):
                    content_widgets = QtWidgets.QWidget()
                    content_widgets_hlayout = QtWidgets.QHBoxLayout()
                    content_widgets_vlayout = QtWidgets.QVBoxLayout()


                    content_widgets.setLayout(content_widgets_vlayout)
                    self.Content_stacked_widgets_layout.addWidget(content_widgets)

                    titles_category = scrap._categories_title()[i]
                    title = book_title[titles_category]
                    title_prices_dict = prices[titles_category]
                    IMG = IMG_DIR / f"{ str(i).zfill(3) }_{ titles_category }"

                    for img_path, img_title_index, price in zip(IMG.iterdir(), range(len(title)), title_prices_dict):
                        book_info = QtWidgets.QWidget()
                        book_info_layout = QtWidgets.QVBoxLayout()

                        book_info.setLayout(book_info_layout)
                        book_info.setFixedSize(300, 300)

                        img_label = QtWidgets.QLabel()
                        img_label.setStyleSheet("border: 1px solid blue")
                        img_label.setScaledContents(False)
                        pixmap = QtGui.QPixmap(img_path)
                        img_label.setPixmap(pixmap)
                        book_info_layout.addWidget(img_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

                        book_title_btn = QtWidgets.QPushButton("More Info")
                        book_info_layout.addWidget(book_title_btn, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

                        book_info_des = QtWidgets.QLabel(f"{ title[img_title_index] }\n\n{ title_prices_dict[price] }")
                        book_info_des.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        book_info_des.setWordWrap(True)
                        book_info_des.setStyleSheet("font-size: 14px")
                        book_info_layout.addWidget(book_info_des, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

                        # book info area
                        book_info_page = QtWidgets.QWidget()
                        book_info_page_1_vlayout = QtWidgets.QVBoxLayout()
                        book_info_page_1_vlayout_hlayout = QtWidgets.QHBoxLayout()
                        book_info_page_1_vlayout_hlayout_vlayout = QtWidgets.QVBoxLayout()


                        book_info_page_1_vlayout.addLayout(book_info_page_1_vlayout_hlayout)
                        book_info_page.setLayout(book_info_page_1_vlayout)
                        
                        book_info_page_1_vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
                        self.Book_stacked_widgets_layout.addWidget(book_info_page)
                        book_info_page_index = self.Book_stacked_widgets_layout.count() - 1
                        book_title_btn.clicked.connect(lambda _, b=book_title_btn, i=book_info_page_index: self.Book_info_button(b, i))

                        book_img = QtWidgets.QLabel()
                        book_img.setStyleSheet("border: 1px solid blue")
                        pixmap = QtGui.QPixmap(img_path)
                        book_img.setPixmap(pixmap)
                        book_img.setScaledContents(True)
                        book_img.setFixedSize(200, 350)
                        book_info_page_1_vlayout_hlayout.addWidget(book_img)
                        book_info_page_1_vlayout_hlayout.addLayout(book_info_page_1_vlayout_hlayout_vlayout)

                        book_info_text = QtWidgets.QLabel(f"{ title[img_title_index] }\n\n{ title_prices_dict[price] }")
                        book_info_text.setStyleSheet("font-size: 20px")
                        book_info_page_1_vlayout_hlayout_vlayout.addWidget(book_info_text)


                        if content_widgets_hlayout.count() < 4:
                                content_widgets_hlayout.addWidget(book_info)
                        else:
                            content_widgets_vlayout.addLayout(content_widgets_hlayout)
                            content_widgets_hlayout = QtWidgets.QHBoxLayout()
                            content_widgets_hlayout.addWidget(book_info)
                    if content_widgets_hlayout.count() > 0:
                            content_widgets_vlayout.addLayout(content_widgets_hlayout)




        # ENDING
        self.MAIN_LAYOUT.addWidget(self.Categories_scroll_area)
        self.MAIN_LAYOUT.addWidget(self.Content_scroll_area)
        self.MAIN_LAYOUT.addWidget(self.Book_scroll_area)
        
        self.setCentralWidget(self.MAIN_WIDGET)


    # ACTION PART
    action = True
    if action:
        def Categories_button(self, btn, i):
            print(f"You clicked on the '{ btn.text() } button ( { i+1 }th button )!!!'")
            self.Content_stacked_widgets_layout.setCurrentIndex(i)

        def Book_info_button(self, btn, i):
            print(f"You clicked on the '{ btn.text() }' button ( { i+1 }th button )")
            self.Book_stacked_widgets_layout.setCurrentIndex(i)

if __name__ == "__main__":

    APP= QtWidgets.QApplication(sys.argv)

    # try:
    #     app = App()
    # except:
    #     print("Error during the creation of the app...")
    #     sys.exit(1)
    app = App()
    print("Before running the app...")
    app.show()
    print("After opening the app...")
    APP.exec()
    print("The app has been closed!!!")
