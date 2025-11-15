import sys
import os
import PyPDF2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.pdf_path = None
        self.pdf_pages = []
        self.current_page = 0
        self.init_ui()

    def init_ui(self):
        # create menu bar and file menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        # create open action for file menu
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)

        # create next page action for toolbar
        next_page_action = QAction("Next Page", self)
        next_page_action.setShortcut("Right")
        next_page_action.triggered.connect(self.next_page)



        # create previous page action for toolbar
        prev_page_action = QAction("Previous Page", self)
        prev_page_action.setShortcut("Left")
        prev_page_action.triggered.connect(self.prev_page)
        self.addToolBar(Qt.TopToolBarArea).addAction(prev_page_action)
        # toolbar = self.addToolBar("Toolbar")
        # toolbar.addAction(next_page_action)

        # create image widget for displaying pages
        self.image_label = QLabel(self)
        self.setCentralWidget(self.image_label)

    def open_pdf(self):
        # open file dialog to select PDF file
        filename, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")

        # check if file was selected
        if filename:
            # set PDF path and load pages
            self.pdf_path = filename
            self.load_pdf_pages()

    def load_pdf_pages(self):
        # open PDF file and extract pages
        with open(self.pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for i in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(i)
                self.pdf_pages.append(page)

        # display first page
        self.display_page(0)

    def display_page(self, page_num):
        # render page as image and display in image widget
        page = self.pdf_pages[page_num]
        page_image = page.getPixmap().toImage()
        qimage = QImage(page_image)
        pixmap = QPixmap(qimage)
        self.image_label.setPixmap(pixmap)
        self.current_page = page_num

    def next_page(self):
        # display next page if available
        if self.current_page < len(self.pdf_pages) - 1:
            self.display_page(self.current_page + 1)

    def prev_page(self):
        # display previous page if available
        if self.current_page > 0:
            self.display_page(self.current_page - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pdf_viewer = PDFViewer()
    pdf_viewer.show()
    sys.exit(app.exec_())
