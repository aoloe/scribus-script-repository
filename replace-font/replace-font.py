# replace fonts in the whole document
#
# © mit, ale rimoldi, 2023
import tkinter as tk
import re
from string import punctuation, whitespace

class EntryWithPlaceholder(tk.Entry):
    """
    inspired by (cc-by) Arthur Julião https://stackoverflow.com/a/68376685/5239250
    other sources:
    - https://blog.teclado.com/tkinter-placeholder-entry-field/
    TODO: does not work
    """

    def __init__(self, master=None, placeholder='', cnf={}, fg='black',
                 fg_placeholder='grey50', *args, **kw):
        super().__init__(master=None, cnf={}, bg='white', *args, **kw)
        self.has_text = False
        self.fg = fg
        self.fg_placeholder = fg_placeholder
        self.placeholder = placeholder
        self.bind('<FocusOut>', lambda event: self.display_placeholder())
        self.bind('<FocusIn>', lambda event: self.clear_placeholder())
        self.display_placeholder()

    def clear_placeholder(self):
        if not self.has_text:
            self.config(fg=self.fg)
            self.delete(0, tk.END)

    def display_placeholder(self):
        if super().get() == '':
            self.has_text = False
            self.config(fg=self.fg_placeholder)
            self.insert(0, self.placeholder)
        else:
            self.has_text = True

class FontSelector(tk.Frame):
    """
    Custom Tkinter widget for the font selector with live filter
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # self.root = tk.Toplevel(root)

        self.selection = None
        self.filter = ''

        self.filter_tk = tk.StringVar(self)
        self.filter_tk.trace("w", self.on_change)
        self.filter_ui = tk.Entry(self, textvariable=self.filter_tk)
        # self.filter_ui = EntryWithPlaceholder(self, textvariable=self.filter_tk, placeholder='Search')
        self.filter_ui.pack()

        frame = tk.Frame(self) # we need a frame, if we want scrollbar
        frame.pack()

        fonts = self.get_all_fonts()
        self.fonts_tk = tk.Variable(frame, value=fonts)
        self.fonts_ui = tk.Listbox(frame, listvariable=self.fonts_tk, height=12, exportselection=0)
        self.fonts_ui.bind('<ButtonRelease-1>', lambda e: self.set_selection())

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.config(command=self.fonts_ui.yview)
        scrollbar.pack(side="right", fill="y")

        self.fonts_ui.config(yscrollcommand=scrollbar.set)

        self.fonts_ui.pack()

    def get_all_fonts(self):
        try:
            return self.get_filtered_fonts('', scribus.getFontNames())
        except NameError:
            # for testing outside of scribus
            return self.get_filtered_fonts('', ['test', 'list', 'with', 'fake', 'font', 'names'])

    def get_filtered_fonts(self, filter, fonts):
        if filter == '':
            return fonts
        filter = filter.lower()
        return [font for font in fonts if filter in font.lower()]

    def on_change(self, *args):
        new_filter = self.filter_tk.get()
        if len(new_filter) > len(self.filter):
            self.fonts_tk.set(self.get_filtered_fonts(new_filter, self.fonts_tk.get()))
        else:
            self.fonts_tk.set(self.get_filtered_fonts(new_filter, self.get_all_fonts()))
        self.filter= new_filter

    def set_selection(self):
        selection = self.fonts_ui.curselection()
        if len(selection) > 0:
            self.selection = self.fonts_ui.get(selection[0])
        else:
            self.selection = None

    def focus():
        """ set the focus on this widgets' input fields """
        self.filter_ui.focus()

class Button:
    def __init__(self, label, action):
        self.label = label
        self.action = action

class ButtonsRow(tk.Frame):
    """
    Custom Tkinter widget with the list of buttons
    """
    def __init__(self, parent, buttons):
        tk.Frame.__init__(self, parent)
        for i, button in enumerate(buttons):
            button_tk = tk.Button(self, text=button.label, command=button.action)
            # button_tk.pack()
            button_tk.grid(column = i, row=0, sticky=tk.W, padx=5, pady=5)

def cancel(root):
    root.quit()
    root.withdraw()

def replace(root, search_font, replace_font):
    # TODO store the current page and (if) current selection and restore them at the end of the replace.
    # TODO: do the replacement!
    if search_font.selection is None or replace_font.selection is None:
        # TODO: can we highlight a the concerned list?
        return

    # print(search_font.selection)
    # print(replace_font.selection)


    try:
        scribus.setRedraw(False)
    except:
        # if we're not in scribus, we cannot return (for debug purposes)
        return

    currentPage = scribus.currentPage()
    currentItem = scribus.getSelectedObject()

    for item in get_document_text_frames():
        scribus.deselectAll()
        scribus.selectObject(item)
        for run in get_runs_by_font(search_font.selection):
            print(run)
            scribus.selectFrameText(run[0], run[1] - run[0])
            scribus.setFont(replace_font.selection)

    scribus.docChanged(True)

    scribus.gotoPage(currentPage)
    if currentItem != '':
        scribus.selectObject(currentItem)
    scribus.setRedraw(True)

    cancel(root)

def get_document_text_frames():
    """
    if we're in scribus, return each text frame. otherwise return an empty list
    """
    try:
        for page in [p + 1 for p in range(scribus.pageCount())]:
            scribus.gotoPage(page)
            page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
                if item[1] == 4]
            for item, _ in page_text_frames:
                yield item
    except Exception:
        return []

def get_runs_by_font(search_font):
    """
    return runs (start, end) with the searched font (word by word) in the currently selected textframe
    TODO: probably, this function is too long and not testable...
    """
    frame_text = scribus.getFrameText()
    frame_length = len(frame_text)
    a = None
    b = None
    for m in re.finditer(r'\b\S+', frame_text):
        if a is not None and b < m.start() - 1:
            yield (a, b)
            a = None
        if a == None:
            a = m.start()
        b = m.end()
        scribus.selectFrameText(a, b - a)
        # get the font at the start of the selection
        selection_font = scribus.getFont()
        font_matches = selection_font == search_font
        if not font_matches:
            a = None
        # the punctuation at the end of the word can be in a different font
        punctuation_length = 0
        while frame_text[b - 1 - punctuation_length] in punctuation:
            punctuation_length += 1
        if punctuation_length > 0:
            scribus.selectFrameText(b - punctuation_length, punctuation_length)
            selection_font = scribus.getFont()
            if font_matches:
                if selection_font != search_font:
                    b -= punctuation_length
            else:
                if selection_font == search_font:
                    a = b - punctuation_length
        # add the spaces after the word, up to the last one with the searched font
        space_length = 0
        while b + space_length + 1 < frame_length and frame_text[b + space_length + 1] in whitespace:
            space_length += 1
        if space_length > 0:
            # TODO: check that the extension of the selection is correct
            scribus.selectFrameText(b, punctuation_length)
            selection_font = scribus.getFont()
            if selection_font == search_font:
                if a is None:
                    a = b
                b += punctuation_length

        # print(f'>>> {a} : {b}')
    if a is not None:
        yield (a, b)

def main():
    # if we're inside scribus, do nothing if there is no document open
    try:
        if not scribus.haveDoc():
            return
    except:
        pass

    root = tk.Tk()
    # dialog = Dialog(root)
    root.attributes('-type', 'dialog')

    root.bind('<Escape>', lambda *args: cancel(root))

    search_font = FontSelector(root)
    search_font.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

    replace_font = FontSelector(root)
    replace_font.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

    t_username_label = ButtonsRow(root, [Button('Replace', lambda: replace(root, search_font, replace_font)), Button('Cancel', lambda: cancel(root))])
    t_username_label.grid(column=0, row=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
