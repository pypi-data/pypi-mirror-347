from tkinter import Tk, Frame

class BuchoFrame(Frame):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.init_view()

    def init_view(self):
        self.text_view = Tk.Text(self)
        self.text_view.insert(Tk.END, self.text)
        self.text_view.configure(state=Tk.DISABLED)
        self.text_view.pack(fill=Tk.BOTH, expand=True)

    def run(self):
        self.pack(fill=Tk.BOTH, expand=True)
        self.mainloop()
