# replace fonts in the whole document
#
# © mit, ale rimoldi, 2023
import sys
import tkinter as tk

class FontSelector:
    def __init__(self, title='Scribus - Select font'):
        self.font_selected = None
        self.filter = ''

        self.root = tk.Tk()
        self.root.attributes('-type', 'dialog')
        # self.root.geometry('120x120-80+40')
        self.root.title(title)
        self.root.bind('<Escape>', self.cancel)
        self.root.bind('<Return>', self.send)

        tk.Label(self.root, text=title, anchor='w').pack()

        self.input_filter_tk = tk.StringVar()
        self.input_filter_tk.trace("w", self.on_change)
        input_filter = tk.Entry(self.root, textvariable=self.input_filter_tk)
        input_filter.pack()
        input_filter.focus()

        frame = tk.Frame(self.root) # we need a frame, if we want scrollbar
        frame.pack()

        fonts = self.get_all_fonts()
        print(fonts)
        self.fonts_tk = tk.Variable(value=fonts)
        self.fonts_ui = tk.Listbox(frame, listvariable=self.fonts_tk, height=12)

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.config(command=self.fonts_ui.yview)
        scrollbar.pack(side="right", fill="y")

        self.fonts_ui.config(yscrollcommand=scrollbar.set)

        self.fonts_ui.pack()

        mySubmitButton = tk.Button(self.root, text='Submit', command=self.send)
        mySubmitButton.pack()
        self.root.mainloop()

    def get_all_fonts(self):
        try:
            return self.get_filtered_fonts('', scribus.getFontNames())
        except NameError:
            # for testing outside of scribus
            return self.get_filtered_fonts('', ['test', 'list', 'with', 'fake', 'font', 'names'])
        
    def get_filtered_fonts(self, filter, fonts):
        # print(f'if {filter} in {fonts}')
        if filter == '':
            print('emtpy')
            return fonts
        filter = filter.lower()
        return [font for font in fonts if filter in font.lower()]

    def on_change(self, *args):
        new_filter = self.input_filter_tk.get()
        if len(new_filter) > len(self.filter):
            self.fonts_tk.set(self.get_filtered_fonts(new_filter, self.fonts_tk.get()))
        else:
            self.fonts_tk.set(self.get_filtered_fonts(new_filter, self.get_all_fonts()))
        self.filter= new_filter

    def cancel(self, *args):
        self.font_selected = None
        self.root.quit()
        self.root.withdraw()

    def send(self, *args):
        selection = self.fonts_ui.curselection()
        if len(selection) > 0:
            print(selection, selection[0])
            self.font_selected = self.fonts_ui.get(selection[0])
        else:
            self.font_selected = None
        self.root.quit()
        self.root.withdraw()

def main():
    try:
        fontSelector = FontSelector('Search font')
        if fontSelector.font_selected is None:
            return
        print("font_selected " + fontSelector.font_selected)
        fontSelectors = FontSelector('Replace font')
        if fontSelectors.font_selected is None:
            return
        # TODO: do the replacement in each text frames or story
    finally:
        try:
            if scribus.haveDoc():
                scribus.redrawAll()
        except:
            pass

if __name__ == '__main__':
    try:
        import scribus
    except ImportError:
        print('This script must be run from inside Scribus')
        # sys.exit()

    main()
