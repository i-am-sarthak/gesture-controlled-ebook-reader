import os
import time
from threading import Thread
from tkinter import Canvas, END, Event, Frame, PhotoImage, Scrollbar, Text, Tk
from tkinter import ttk

import fitz

pdf_file: str = "./test_pdf.pdf"
recognised_gestures_file = "recognised_gestures.txt"

pdf_canvas: Canvas
image_object_list: list[PhotoImage]


def pdf_view(master: Frame, pdf_location: str, height: int, width: int) -> Canvas:
    canvas: Canvas = Canvas(master, width=width, height=height)

    scrollbar: Scrollbar = Scrollbar(master, command=canvas.yview)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame: Frame = Frame(canvas, width=width, height=height, bg="white")

    canvas.create_window((0, 0), window=frame, anchor="nw")

    # noinspection PyUnusedLocal
    def on_configure(event: Event) -> None:
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_configure)

    text: Text = Text(frame, yscrollcommand=scrollbar.set, width=width, height=height)
    text.grid(row=0, column=0)

    scrollbar.config(command=text.yview)

    def add_image() -> None:
        # noinspection PyUnresolvedReferences
        pdf: fitz.Document = fitz.open(pdf_location)

        for page in pdf:
            # noinspection PyUnresolvedReferences
            pixmap: fitz.Pixmap = page.get_pixmap(dpi=72)
            pixmap: fitz.Pixmap = fitz.Pixmap(pixmap, 0) if pixmap.alpha else pixmap
            tk_image: PhotoImage = PhotoImage(data=pixmap.tobytes("ppm"))
            image_object_list.append(tk_image)

        for image in image_object_list:
            text.image_create(END, image=image)
            text.insert(END, "\n\n")
        text.configure(state="disabled")

    master.after(250, lambda: Thread(target=add_image).start())

    return canvas


def scroll(event: Event) -> None:
    pdf_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def scroll_down() -> None:
    pdf_canvas.event_generate("<MouseWheel>", delta=-120)


def scroll_up() -> None:
    pdf_canvas.event_generate("<MouseWheel>", delta=120)


def previous_page() -> None:
    pdf_canvas.yview_scroll(-10, "units")


def next_page() -> None:
    pdf_canvas.yview_scroll(10, "units")


def main() -> None:
    global pdf_canvas, image_object_list

    root: Tk = Tk()
    root.geometry('725x610+380+120')
    root.title("Hand Gesture Controlled eBook Reader")
    root.resizable(False, False)

    top_frame: ttk.Frame = ttk.Frame(root, width=725, height=550)
    top_frame.grid(row=0, column=0)
    top_frame.grid_propagate(False)
    bottom_frame: ttk.Frame = ttk.Frame(root, width=725, height=50)
    bottom_frame.grid(row=1, column=0, pady=5)
    bottom_frame.grid_propagate(False)

    ttk.Button(bottom_frame, text='Scroll Up', command=scroll_up). \
        grid(row=0, column=2, padx=(270, 5))
    ttk.Button(bottom_frame, text='Scroll Down', command=scroll_down) \
        .grid(row=0, column=3)
    ttk.Button(bottom_frame, text='Previous Page', command=previous_page). \
        grid(row=1, column=2, padx=(270, 5))
    ttk.Button(bottom_frame, text='Next Page', command=next_page) \
        .grid(row=1, column=3)

    image_object_list = []
    pdf_canvas = pdf_view(top_frame, pdf_location=pdf_file, height=550, width=725)
    pdf_canvas.grid(row=0, column=0)

    pdf_canvas.bind_all("<MouseWheel>", scroll)
    pdf_canvas.bind_all("<Up>", lambda event: scroll_up())
    pdf_canvas.bind_all("<Down>", lambda event: scroll_down())
    pdf_canvas.bind_all("<Left>", lambda event: previous_page())
    pdf_canvas.bind_all("<Right>", lambda event: next_page())

    root.mainloop()


if __name__ == '__main__':
    Thread(target=main).start()

    with open(recognised_gestures_file, "w") as f:
        f.write("")
    last_modified_time = os.path.getmtime(recognised_gestures_file)
    file_content: list[str] = []
    while True:
        current_modified_time = os.path.getmtime(recognised_gestures_file)
        if current_modified_time != last_modified_time:
            with open(recognised_gestures_file, "r") as f:
                file_content = f.readlines()
            if len(file_content) != 0:
                if file_content[-1] == "scroll_up\n":
                    scroll_up()
                elif file_content[-1] == "scroll_down\n":
                    scroll_down()
                elif file_content[-1] == "previous_page\n":
                    previous_page()
                elif file_content[-1] == "next_page\n":
                    next_page()
            last_modified_time = current_modified_time
        time.sleep(0.01)
