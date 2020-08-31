# Python libs
from tkinter import filedialog #for Python 3
from tkinter import messagebox
import tkinter as tk
import sys

# external libs
from cv2 import destroyAllWindows

# internal libs
from UI.widgets import CreateToolTip
from Reference_Judge.check_argv_correctness.helpers.errors import ERRORS_MESSAGES
from Reference_Judge.config import IMAGES_SIZES, ARGV
from Reference_Judge.Reference_Judge import Reference_Judge

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
class MainGUIApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        master.title(sys.argv[0])
        window_width = 618
        window_height = 570
        master.geometry(f"{window_width}x{window_height}")

        self.entry_text_placeholder = "Enter your path..."
        self.entry_text_width_placeholder = IMAGES_SIZES["default width"]


        # Create frames
        frame_matching = tk.LabelFrame(master, padx=10, pady=15)
        frame_matching.grid(row=0, column=0, padx=10, pady=(25, 15))

        frame_output = tk.LabelFrame(master, padx=10, pady=15)
        frame_output.grid(row=1, column=0, padx=10, pady=(15, 0))

        frame_optional = tk.LabelFrame(master, padx=10, pady=15)
        frame_optional.grid(row=2, column=0, padx=10, pady=(15, 0), stick="we")

        # Source
        self.source_label = tk.Label(frame_matching, text="Original refs:")
        self.source_label.grid(row=0, column=0, pady=(0, 5), stick="w")

        self.source_entry = tk.Entry(frame_matching, borderwidth=1)
        self.source_entry.insert(0, self.entry_text_placeholder)
        self.source_entry.bind('<FocusIn>', self.on_entry_click_source)
        self.source_entry.bind('<FocusOut>', self.on_focusout_source)
        self.source_entry.config(fg='grey')
        self.source_entry.grid(row=1, column=0, ipadx=200, pady=(0, 5), stick="we")

        # Images to buttons
        self.img_open_folder=tk.PhotoImage(file="UI/images/open_folder.gif")
        self.img_open_file=tk.PhotoImage(file="UI/images/open_file.gif")

        # Source buttons for path
        self.source_btn_folder = tk.Button(frame_matching, command=self.source_btn_folder_open)
        self.source_btn_folder.config(image=self.img_open_folder)
        self.source_btn_folder.grid(row=1, column=2, padx=5)

        self.source_btn_file = tk.Button(frame_matching, command=self.source_btn_file_open)
        self.source_btn_file.config(image=self.img_open_file)
        self.source_btn_file.grid(row=1, column=3)


        # Target
        self.target_label = tk.Label(frame_matching, text="App refs:")
        self.target_label.grid(row=2, column=0, pady=(0, 5), stick="w")

        self.target_entry = tk.Entry(frame_matching, borderwidth=1)
        self.target_entry.insert(0, self.entry_text_placeholder)
        self.target_entry.bind('<FocusIn>', self.on_entry_click_target)
        self.target_entry.bind('<FocusOut>', self.on_focusout_target)
        self.target_entry.config(fg='grey')
        self.target_entry.grid(row=3, column=0, ipadx=200, pady=(0, 5), stick="we")

        # Target buttons for path
        self.target_btn_folder = tk.Button(frame_matching, command=self.target_btn_folder_open)
        self.target_btn_folder.config(image=self.img_open_folder)
        self.target_btn_folder.grid(row=3, column=2)

        self.target_btn_file = tk.Button(frame_matching, command=self.target_btn_file_open)
        self.target_btn_file.config(image=self.img_open_file)
        self.target_btn_file.grid(row=3, column=3)
        
        # Save
        self.mode = tk.StringVar()
        self.mode.set(ARGV["save"][0])

        self.save_radio = tk.Radiobutton(frame_output, text="Save", variable=self.mode, value=ARGV["save"][0], command=self.disable_output_entry)
        self.save_radio.grid(row=0, column=0, stick="w")

        # Output
        self.output_label = tk.Label(frame_output, text="Output files:")
        self.output_label.grid(row=1, column=0, pady=(0, 5), stick="w")

        self.output_entry = tk.Entry(frame_output, borderwidth=1)
        self.output_entry.insert(0, self.entry_text_placeholder)
        self.output_entry.bind('<FocusIn>', self.on_entry_click_output)
        self.output_entry.bind('<FocusOut>', self.on_focusout_output)
        self.output_entry.config(fg='grey')
        self.output_entry.grid(row=2, ipadx=200, stick="we")

        # Output buttons for path
        self.output_btn_folder = tk.Button(frame_output, command=self.output_btn_folder_open)
        self.output_btn_folder.config(image=self.img_open_folder)
        self.output_btn_folder.grid(row=2, padx=5, column=2)

        self.output_btn_file = tk.Button(frame_output, command=self.output_btn_file_open)
        self.output_btn_file.config(image=self.img_open_file)
        self.output_btn_file.grid(row=2, column=3)

        # Show
        self.show_radio = tk.Radiobutton(frame_output, text="Show", variable=self.mode, value=ARGV["show"][0], command=self.disable_output_entry)
        self.show_radio.grid(row=3, column=0, pady=(13, 0), stick="w")

        # Width
        self.width_label = tk.Label(frame_optional, text="Width:")
        self.width_label.grid(row=0, column=0, pady=(0, 5), stick="w")

        self.width_text = tk.StringVar() # the text in  your entry
        self.width_entry = tk.Entry(frame_optional, borderwidth=1, textvariable = self.width_text)
        self.width_entry.insert(0, self.entry_text_width_placeholder)
        self.width_entry.grid(row=1, column=0, pady=(0, 20), stick="w")

        # By ratio
        self.by_ratio = tk.StringVar()

        self.by_ratio_checkbox = tk.Checkbutton(
            frame_optional,
            text="Search by the same ratio",
            variable=self.by_ratio,
            onvalue=ARGV["search by ratio"][0],
            offvalue="default"
        )
        self.by_ratio_checkbox.deselect()
        self.by_ratio_checkbox.grid(row=2, column=0, stick="w")

        # Match images
        self.match_btn = tk.Button(master, text="Match images", bg="#f5f5f5", command=self.match_images)
        self.match_btn.config(height=3)
        self.match_btn.grid(row=3, column=0, pady=(20, 0), stick="we", padx=(10, 10))


        # Add tooltips to widgets
        entry_tooltip_match = "Path of single file, dir or URL..."
        entry_tooltip_output = "Path of single file or dir..."
        save_tooltip = "Save matched images in chosen directory"
        show_tooltip = "Show matched images"
        width_tooltip = "Width of each separate image"
        by_ratio_tooltip = ('Match images refs: "Original -> App", with diffrent sizes but the same ratio.\n'
        "Not recommended due to distortions.")
        btn_folder_tooltip = "Choose folder..."
        btn_file_tooltip = "Choose file..."
        match_btn_tooltip = "Run the script!"

        CreateToolTip(self.source_entry, entry_tooltip_match)
        CreateToolTip(self.target_entry, entry_tooltip_match)
        CreateToolTip(self.output_entry, entry_tooltip_output)
        CreateToolTip(self.width_entry, width_tooltip)

        CreateToolTip(self.source_label, entry_tooltip_match)
        CreateToolTip(self.target_label, entry_tooltip_match)
        CreateToolTip(self.output_label, entry_tooltip_output)
        CreateToolTip(self.width_label, width_tooltip)

        CreateToolTip(self.save_radio, save_tooltip)
        CreateToolTip(self.show_radio, show_tooltip)

        CreateToolTip(self.by_ratio_checkbox, by_ratio_tooltip)

        CreateToolTip(self.source_btn_file, btn_file_tooltip)
        CreateToolTip(self.source_btn_folder, btn_folder_tooltip)

        CreateToolTip(self.target_btn_file, btn_file_tooltip)
        CreateToolTip(self.target_btn_folder, btn_folder_tooltip)

        CreateToolTip(self.output_btn_file, btn_file_tooltip)
        CreateToolTip(self.output_btn_folder, btn_folder_tooltip)

        CreateToolTip(self.match_btn, match_btn_tooltip)



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

    def on_entry_click_output(self, event):
        """function that gets called whenever entry is clicked"""
        on_entry_click(self.output_entry, self.entry_text_placeholder)

    def on_focusout_output(self, event):
        on_focusout(self.output_entry, self.entry_text_placeholder)

    def source_btn_folder_open(self):

        btn_find_path(self.source_entry, filedialog.askdirectory)

    def source_btn_file_open(self):

        btn_find_path(self.source_entry, filedialog.askopenfilename)

    def target_btn_folder_open(self):

        btn_find_path(self.target_entry, filedialog.askdirectory)

    def target_btn_file_open(self):

        btn_find_path(self.target_entry, filedialog.askopenfilename)

    def output_btn_folder_open(self):

        btn_find_path(self.output_entry, filedialog.askdirectory)

    def output_btn_file_open(self):

        btn_find_path(self.output_entry, filedialog.askopenfilename)
        
    def disable_output_entry(self):

        if self.mode.get() == ARGV["save"][0]:

            self.output_label.configure(state="normal")
            self.output_entry.configure(state="normal")
            self.output_btn_folder.configure(state="normal")
            self.output_btn_file.configure(state="normal")

        elif self.mode.get() == ARGV["show"][0]:

            self.output_label.configure(state="disabled")
            self.output_entry.configure(state="disabled")
            self.output_btn_folder.configure(state="disabled")
            self.output_btn_file.configure(state="disabled")
        else:
            raise ValueError(f"Not existing ARG:\n{self.mode.get()}")

    def match_images(self):

        _argv=list()

        program_name = sys.argv[0]
        _argv.append(program_name)
        

        source = self.source_entry.get()
        if self.path_exists(source):
            _argv.append(source)


        target = self.target_entry.get()
        if self.path_exists(target):
            _argv.append(target)


        mode = self.mode.get()
        if self.mode_exists(mode):
            _argv.append(mode)


        output = self.output_entry.get()
        if self.path_exists(output) and mode == ARGV["save"][0]:
            _argv.append(output)


        width = self.width_entry.get()
        if self.width_exists(width):
            _argv.append(width)


        by_ratio = self.by_ratio.get()
        if by_ratio != "default":
            _argv.append(by_ratio)


        window_name = "Wrong input"
        if self.pop_up_invalid_entry_path(window_name, source, target, mode, output, width):
            return

        try:
            Reference_Judge(_argv)
        except SystemExit as error:
            messagebox.showwarning(window_name, error)

        if mode == ARGV["show"][0]:
            destroyAllWindows() # to avoid bug with not closing last window

        if mode == ARGV["save"][0]:
            messagebox.showinfo("Done!", f"You saved images in: {output}")

    def path_exists(self, path):
        return path != self.entry_text_placeholder and isinstance(path, str)

    def mode_exists(self, mode):

        modes = [
            ARGV["save"][0],
            ARGV["show"][0]
        ]

        return mode in modes

    def width_exists(self, width):
        return width != str(IMAGES_SIZES["default width"])

    def pop_up_invalid_entry_path(self, window_name, source, target, output, mode, width):

        if not source or source == self.entry_text_placeholder:
            return messagebox.showwarning(window_name, "No original references")

        if not target or target == self.entry_text_placeholder:
            return messagebox.showwarning(window_name, "No app references")

        if mode == ARGV["save"][0] and (not output or output == self.entry_text_placeholder):
            return messagebox.showwarning(window_name, "No output path")

        if not width.isnumeric():
            return messagebox.showwarning(window_name, "Width should be numeric")

        return None


def main():  # run mainloop
    root = tk.Tk()
    app = MainGUIApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
