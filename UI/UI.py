import tkinter as tk
from tkinter import filedialog #for Python 3
import sys

def on_entry_click(entry, placeholder):
    """function that gets called whenever entry is clicked"""
    if entry.get() == placeholder:
        entry.delete(0, "end")  # delete all the text in the source_entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')

def on_focusout(entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')

def btn_find_path(entry, askpath):

    path = askpath()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.config(fg='black')

# https://stackoverflow.com/a/17466924/12490791
class UI:
    def __init__(self, master):
        master.title(sys.argv[0])
        master.geometry("618x180")

        left_pad=20

        self.entry_text_placeholder = "Enter your path..."

        # Source
        self.source_label = tk.Label(text="Source:")
        self.source_label.grid(row=1, column=0, pady=(15, 5), stick=tk.W, padx=(left_pad, 0))

        self.source_entry = tk.Entry(master, borderwidth=1)
        self.source_entry.insert(0, self.entry_text_placeholder)
        self.source_entry.bind('<FocusIn>', self.on_entry_click_source)
        self.source_entry.bind('<FocusOut>', self.on_focusout_source)
        self.source_entry.config(fg='grey')
        self.source_entry.grid(row=2, column=0, ipadx=200, columnspan=2, pady=(0, 5), stick="we", padx=(left_pad, 0))

        # Images to buttons
        self.img_open_folder=tk.PhotoImage(file="images/open_folder.gif")
        self.img_open_file=tk.PhotoImage(file="images/open_file.gif")

        # Source buttons for path
        self.source_btn_folder = tk.Button(master, command=self.source_btn_folder_open)
        self.source_btn_folder.config(image=self.img_open_folder)
        self.source_btn_folder.grid(row=2, column=2, padx=5)

        self.source_btn_file = tk.Button(master, command=self.source_btn_file_open)
        self.source_btn_file.config(image=self.img_open_file)
        self.source_btn_file.grid(row=2, column=3)


        # Target
        self.target_label = tk.Label(text="Target:")
        self.target_label.grid(row=3, column=0, pady=(0, 5), stick=tk.W, padx=(left_pad, 0))

        self.target_entry = tk.Entry(master, borderwidth=1)
        self.target_entry.insert(0, self.entry_text_placeholder)
        self.target_entry.bind('<FocusIn>', self.on_entry_click_target)
        self.target_entry.bind('<FocusOut>', self.on_focusout_target)
        self.target_entry.config(fg='grey')
        self.target_entry.grid(row=4, column=0, columnspan=2, pady=(0, 5), stick="we", padx=(left_pad, 0))

        # Target buttons for path
        self.target_btn_folder = tk.Button(master, command=self.target_btn_folder_open)
        self.target_btn_folder.config(image=self.img_open_folder)
        self.target_btn_folder.grid(row=4, column=2)

        self.target_btn_file = tk.Button(master, command=self.target_btn_file_open)
        self.target_btn_file.config(image=self.img_open_file)
        self.target_btn_file.grid(row=4, column=3)


        # Button
        self.btn_match = tk.Button(text="Match images")
        self.btn_match.grid(row=5, column=0, pady=(20, 0), ipadx=220, stick=tk.W, padx=(left_pad, 0))

    def on_entry_click_source(self, event):
        """function that gets called whenever entry is clicked"""
        on_entry_click(self.source_entry, self.entry_text_placeholder)

    def on_focusout_source(self, event):
        on_focusout(self.source_entry, self.entry_text_placeholder)

    def on_entry_click_target(self, event):
        """function that gets called whenever entry is clicked"""
        on_entry_click(self.target_entry, self.entry_text_placeholder)

    def on_focusout_target(self, event):
        on_focusout(self.target_entry, self.entry_text_placeholder)

    def source_btn_folder_open(self):

        btn_find_path(self.source_entry, filedialog.askdirectory)

    def source_btn_file_open(self):

        btn_find_path(self.source_entry, filedialog.askopenfilename)

    def target_btn_folder_open(self):

        btn_find_path(self.target_entry, filedialog.askdirectory)

    def target_btn_file_open(self):

        btn_find_path(self.target_entry, filedialog.askopenfilename)



    def button_click(self):
        pass
        # If button is clicked, run this method and open window 2


def main():  # run mianloop
    root = tk.Tk()
    app = UI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
