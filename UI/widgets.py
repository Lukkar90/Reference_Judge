# Python libs
try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk
import webbrowser


# tk_ToolTip_class101.py
# gives a Tkinter widget a tooltip as the mouse is above the widget
# tested with Python27 and Python34  by  vegaseat  09sep2014
# www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

# Modified to include a delay time by Victor Zaccardo, 25mar16

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class About():
    def __init__(self):
        about = tk.Toplevel()
        about.title("My second window")
        # top.iconbitmap("blabla")

        pad_value = 20
        padding = tk.Frame(about, padx=pad_value, pady=pad_value)
        padding.pack()

        justify = "w"
        y_space = (15, 0)
        width = (0, 150)
        label_font = 'Helvetica 10 bold'

        numb = "1.0.0"
        version_label = tk.Label(padding, text="Version", font=label_font)
        version_label.pack(anchor=justify, padx=width)
        version_numb = tk.Label(padding, text=f"{numb}")
        version_numb.pack(anchor=justify)

        _type = "MIT"
        license_label = tk.Label(padding, text=f"License", font=label_font)
        license_label.pack(pady=y_space, anchor=justify)
        license_type = tk.Label(padding, text=f"{_type}")
        license_type.pack(anchor=justify)
        license_link = tk.Label(padding, text="license link",
                                fg="blue", cursor="hand2")
        license_link.bind("<Button-1>", lambda e: callback(
            "https://github.com/Lukkar90/Reference_Judge/blob/master/LICENSE"))
        license_link.pack(anchor=justify)

        project_label = tk.Label(padding, text="Project site", font=label_font)
        project_label.pack(pady=y_space, anchor=justify)
        project_link = tk.Label(padding, text="GitHub link",
                                fg="blue", cursor="hand2")
        project_link.bind("<Button-1>", lambda e: callback(
            "https://github.com/Lukkar90/Reference_Judge"))
        project_link.pack(anchor=justify)

        contribute_label = tk.Label(
            padding, text="How to contribute", font=label_font)
        contribute_label.pack(pady=y_space, anchor=justify)
        contribute_link = tk.Label(
            padding, text="Contribute link", fg="blue", cursor="hand2")
        contribute_link.bind("<Button-1>", lambda e: callback(
            "https://github.com/Lukkar90/Reference_Judge/blob/master/CONTRIBUTING.md"))
        contribute_link.pack(anchor=justify)

        contact = "lukkarcontact@gmail.com"
        contact_label = tk.Label(padding, text="Contact", font=label_font)
        contact_label.pack(pady=y_space, anchor=justify)
        contact_link = tk.Label(padding, text=contact,
                                fg="blue", cursor="hand2")
        contact_link.bind("<Button-1>", lambda e: self.callback(
            contact))
        contact_link.pack(anchor=justify)

    def callback(self, url):
        webbrowser.open_new(url)
