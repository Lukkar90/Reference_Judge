# python libs
from tkinter import*
from tkinter import filedialog
import sys


def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if entry.get() == 'Enter your user name...':
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')


def on_focusout(event):
    if entry.get() == '':
        entry.insert(0, 'Enter your username...')
        entry.config(fg='grey')


def myClick():
    pass


def run_UI():

    # window
    root = Tk()
    root.title(sys.argv[0])
    root.geometry("400x400")

    text_description = """
    Source path is for images references,
    Target path is for renders from app.
    """

    # Description
    description = Label(text=text_description)
    description.grid(row=0, column=0, pady=5, padx=20, stick=W)

    # Source
    source_label = Label(text="Source:")
    source_label.grid(row=1, column=0, pady=(0, 5))

    source_entry = Entry(root, borderwidth=1)
    source_entry.insert(0, 'Enter your user name...')
    source_entry.bind('<FocusIn>', on_entry_click)
    source_entry.bind('<FocusOut>', on_focusout)
    source_entry.config(fg='grey')
    source_entry.grid(row=2, column=0, pady=(0, 5))

    myButton = Button(root, text="Enter your name", command=myClick)

    my_btn = Button(root, text="open file", command=open)
    my_btn.grid(row=3, column=0)

    root.mainloop()


run_UI()
