# import tkinter
# from tkinter import *
# from tkPDFViewer2 import tkPDFViewer as pdf
#
# filename = "../pdfs/03-Interactions.pdf"
#
# root = Tk()
# root.geometry("630x700+400+100")
# root.title("PDF Reader")
# root.configure(background='white')
#
#
# # root.resizable(False, False)
#
# # create a function to scroll the pdf
# def scroll(event):
#     # if event.delta:
#     #     pdf2.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
#     # else:
#     #     if event.num == 5:
#     #         move = 1
#     #     else:
#     #         move = -1
#     #     pdf2.canvas.yview_scroll(move, "units")
#     ...
#
#
# # Create a PDF Viewer
# pdf = pdf.ShowPdf()
# pdf2: tkinter.Frame = pdf.pdf_view(root, pdf_location=open(filename, "r"), width=77, height=100)
# pdf2.pack(expand=1, fill="both")
#
#
# # bind the enter key to the scroll function
# root.bind("<Enter>", scroll)
# # pdf2.pack(pady=(0, 0))
#
# root.mainloop()
# ------------------------------------------------------------------------------------------------------------------------
from tkinter import *
from tkPDFViewer2 import tkPDFViewer as pdf

filename = "../pdfs/Paper_Critique_Fast_Distributed_Complex_Join_Processing.pdf"

root = Tk()
root.geometry("630x700+400+100")
root.title("PDF Reader")
root.configure(background='white')
# root.resizable(False, False)

# Create a Canvas widget and add the PDF viewer as a child
canvas = Canvas(root, background="white")
canvas.pack(side=LEFT, fill=BOTH, expand=True)
pdf1 = pdf.ShowPdf()
pdf_viewer = pdf1.pdf_view(canvas, pdf_location=open(filename, "r"), width=77, height=100)

# Add a vertical scrollbar
scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.config(yscrollcommand=scrollbar.set)

# Create buttons to scroll up and down
btn_up = Button(root, text="↑", command=lambda: canvas.yview_scroll(-1, "units"))
btn_up.pack(side=LEFT)
btn_down = Button(root, text="↓", command=lambda: canvas.yview_scroll(1, "units"))
btn_down.pack(side=LEFT)

root.mainloop()
