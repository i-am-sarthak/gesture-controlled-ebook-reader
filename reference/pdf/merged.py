from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
import math
import fitz
from tkinter import PhotoImage


class PDFReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = fitz.open(self.filepath)
        self.first_page = self.pdf.load_page(0)
        self.width, self.height = self.first_page.rect.width, self.first_page.rect.height
        zoomdict = {800: 0.8, 700: 0.6, 600: 1.0, 500: 1.0}
        width = int(math.floor(self.width / 100.0) * 100)
        # zooming the page
        # self.zoom = zoomdict[width]
        self.zoom = 0.78

    # this will get the metadata from the document like
    # author, name of document, number of pages
    def get_metadata(self):
        # getting metadata from the open PDF document
        metadata = self.pdf.metadata
        # getting number of pages from the open PDF document
        numPages = self.pdf.page_count
        # returning the metadata and the numPages
        return metadata, numPages

    # the function for getting the page
    def get_page(self, page_num):
        # loading the page
        page = self.pdf.load_page(page_num)
        # checking if zoom is True
        if self.zoom:
            # creating a Matrix whose zoom factor is self.zoom
            mat = fitz.Matrix(self.zoom, self.zoom)
            # gets the image of the page
            pix = page.get_pixmap(matrix=mat)
        # returns the image of the page
        else:
            pix = page.get_pixmap()
        # a variable that holds a transparent image
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        # converting the image to bytes
        imgdata = px1.tobytes("ppm")
        # returning the image data
        return PhotoImage(data=imgdata)

    # function to get text from the current page
    def get_text(self, page_num):
        # loading the page
        page = self.pdf.load_page(page_num)
        # getting text from the loaded page
        text = page.getText('text')
        # returning text
        return text


# creating a class called PDFViewer
class PDFViewer:
    # initializing the __init__ / special method
    def __init__(self, master):
        # path for the pdf doc
        self.path = None
        # state of the pdf doc, open or closed
        self.fileisopen = None
        # author of the pdf doc
        self.author = None
        # name for the pdf doc
        self.name = None
        # the current page for the pdf
        self.current_page = 0
        # total number of pages for the pdf doc
        self.numPages = None
        # creating the window
        self.master = master
        # gives title to the main window
        self.master.title('PDF Viewer')
        # gives dimensions to main window
        # TODO:
        self.master.geometry('580x520+440+180')
        # this disables the minimize/maximize button on the main window
        self.master.resizable(width=0, height=0)
        # loads the icon and adds it to the main window
        # self.master.iconbitmap(self.master, 'pdf_file_icon.ico')
        # creating the menu
        self.menu = Menu(self.master)
        # adding it to the main window
        self.master.config(menu=self.menu)
        # creating a sub menu
        self.filemenu = Menu(self.menu, tearoff=0)
        # giving the sub menu a label
        self.menu.add_cascade(label="File", menu=self.filemenu)
        # adding a two buttons to the sub menus
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)
        # creating the top frame
        self.top_frame = ttk.Frame(self.master, width=580, height=460)
        # placing the frame using inside main window using grid()
        self.top_frame.grid(row=0, column=0)
        # the frame will not propagate
        self.top_frame.grid_propagate(False)
        # creating the bottom frame
        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        # placing the frame using inside main window using grid()
        self.bottom_frame.grid(row=1, column=0)
        # the frame will not propagate
        self.bottom_frame.grid_propagate(False)
        # creating a vertical scrollbar
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        # adding the scrollbar
        self.scrolly.grid(row=0, column=1, sticky=(N, S))
        # creating a horizontal scrollbar
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        # adding the scrollbar
        self.scrollx.grid(row=1, column=0, sticky=(W, E))
        # creating the canvas for display the PDF pages
        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        # inserting both vertical and horizontal scrollbars to the canvas
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        # adding the canvas
        self.output.grid(row=0, column=0)
        # configuring the horizontal scrollbar to the canvas
        self.scrolly.configure(command=self.output.yview)
        # configuring the vertical scrollbar to the canvas
        self.scrollx.configure(command=self.output.xview)
        # loading the button icons
        # self.uparrow_icon = PhotoImage(file='uparrow.png')
        # self.downarrow_icon = PhotoImage(file='downarrow.png')
        # resizing the icons to fit on buttons
        # self.uparrow = self.uparrow_icon.subsample(3, 3)
        # self.downarrow = self.downarrow_icon.subsample(3, 3)
        # creating an up button with an icon
        # self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow, command=self.previous_page)
        # text button
        self.upbutton = ttk.Button(self.bottom_frame, text='Previous Page', command=self.previous_page)
        # adding the button
        self.upbutton.grid(row=0, column=1, padx=(int(270 / 1.3), 5), pady=8)
        # creating a down button with an icon
        # self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        # text button
        self.downbutton = ttk.Button(self.bottom_frame, text='Next Page', command=self.next_page)
        # adding the button
        self.downbutton.grid(row=0, column=3, pady=8)
        # label for displaying page numbers
        self.page_label = ttk.Label(self.bottom_frame, text='')
        # adding the label
        self.page_label.grid(row=0, column=4, padx=100)

    # function for opening pdf files
    def open_file(self):
        # open the file dialog
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        # checking if the file exists
        if filepath:
            # declaring the path
            self.path = filepath
            # extracting the pdf file from the path
            filename = os.path.basename(self.path)
            # passing the path to PDFMiner
            self.miner = PDFReader(self.path)
            # getting data and numPages
            data, numPages = self.miner.get_metadata()
            # setting the current page to 0
            self.current_page = 0
            # checking if numPages exists
            if numPages:
                # getting the title
                self.name = data.get('title', filename[:-4])
                # getting the author
                self.author = data.get('author', None)
                self.numPages = numPages
                # setting fileopen to True
                self.fileisopen = True
                # calling the display_page() function
                self.display_page()
                # replacing the window title with the PDF document name
                self.master.title(self.name)

    # the function to display the page
    def display_page(self):
        # checking if numPages is less than current_page and if current_page is less than
        # or equal to 0
        if 0 <= self.current_page < self.numPages:
            # getting the page using get_page() function from miner
            self.img_file = self.miner.get_page(self.current_page)
            # inserting the page image inside the Canvas
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            # the variable to be stringified
            self.stringified_current_page = self.current_page + 1
            # updating the page label with number of pages
            self.page_label['text'] = str(self.stringified_current_page) + ' of ' + str(self.numPages)
            # creating a region for inserting the page inside the Canvas
            region = self.output.bbox(ALL)
            # making the region to be scrollable
            self.output.configure(scrollregion=region)

            # function for displaying next page

    def next_page(self):
        # checking if file is open
        if self.fileisopen:
            # checking if current_page is less than or equal to numPages-1
            if self.current_page <= self.numPages - 1:
                # updating the page with value 1
                self.current_page += 1
                # displaying the new page
                self.display_page()

    # function for displaying the previous page
    def previous_page(self):
        # checking if fileisopen
        if self.fileisopen:
            # checking if current_page is greater than 0
            if self.current_page > 0:
                # decrementing the current_page by 1
                self.current_page -= 1
                # displaying the previous page
                self.display_page()


# creating the root winding using Tk() class
root = Tk()
# instantiating/creating object app for class PDFViewer
app = PDFViewer(root)
# calling the mainloop to run the app infinitely until user closes it
root.mainloop()
