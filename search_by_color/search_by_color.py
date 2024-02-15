"""Find the first shape or frames with a specific color name as fill or stroke.

For more details see the README.md

(c) MIT 2024, ale rimoldi <ale@graphicslab.org>
"""
has_tk = True
try:
    import tkinter as tk
except ImportError:
    has_tk = False

has_scribus = True
try:
    import scribus
except ImportError:
    has_scribus = False

class LiveFilterListSelector(tk.Frame):
    """
    Custom Tkinter widget for a list selector with live filter
    """
    def __init__(self, parent, all_items):
        tk.Frame.__init__(self, parent)

        self.all_items = all_items

        self.selection = None
        self.filter = ''

        self.filter_tk = tk.StringVar(self)
        self.filter_tk.trace("w", self.on_change)
        self.filter_ui = tk.Entry(self, textvariable=self.filter_tk)
        # self.filter_ui = EntryWithPlaceholder(self, textvariable=self.filter_tk, placeholder='Search')
        self.filter_ui.pack()

        frame = tk.Frame(self) # we need a frame, if we want scrollbar
        frame.pack()

        self.items_tk = tk.Variable(frame, value=self.all_items)
        self.items_ui = tk.Listbox(frame, listvariable=self.items_tk, height=12, exportselection=0)
        self.items_ui.bind('<ButtonRelease-1>', lambda e: self.set_selection())

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.config(command=self.items_ui.yview)
        scrollbar.pack(side="right", fill="y")

        self.items_ui.config(yscrollcommand=scrollbar.set)

        self.items_ui.pack()

    def get_filtered_items(self, filter):
        if filter == '':
            return self.all_items
        filter = filter.lower()
        return [item for item in self.all_items if filter in item.lower()]

    def on_change(self, *args):
        self.items_tk.set(self.get_filtered_items(self.filter_tk.get()))

    def set_selection(self):
        selection = self.items_ui.curselection()
        if len(selection) > 0:
            self.selection = self.items_ui.get(selection[0])
        else:
            self.selection = None

    def focus(self):
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
            button_tk.grid(column = i, row=0, sticky=tk.W, padx=5, pady=5)

def get_all_colors():
    try:
        return scribus.getColorNames()
    except NameError:
        # for testing outside of scribus
        return ['Red', 'Yellow', 'Blue', 'Pink', 'Black', 'White']

def search_color(color, scope):
    if color is None:
        return
    current_page = scribus.currentPage()
    if scope == 'all':
        first_page = 1
        last_page = scribus.pageCount()
    else:
        first_page = current_page
        last_page = first_page

    for page in range(first_page, last_page + 1):
        scribus.gotoPage(page)
        for item in scribus.getPageItems():
            items = [item[0]]
            if item[1] == 12: # it's a group
                items = [inner[0] for inner in scribus.getGroupItems(item[0], recursive=True)]
            # print('>>>', items)

            for item_name in items:
                try:
                    # only starting from february 2024, scribus can query colors inside of groups
                    if scribus.getFillColor(item_name) == color or scribus.getLineColor(item_name) == color:
                        scribus.deselectAll()
                        scribus.selectObject(item_name)
                        return
                except:
                    pass

    scribus.gotoPage(current_page)

def get_color_and_scope_from_dialog():
    root = tk.Tk()
    # dialog = Dialog(root)
    root.title('Search by Color')
    root.attributes('-type', 'dialog')

    def cancel():
        nonlocal root
        root.quit()
        root.withdraw()

    color = None
    scope = None
    def ok():
        nonlocal color, scope
        color = search_color.selection
        scope = scope_tk.get()
        cancel()

    root.bind('<Escape>', lambda *args: cancel())

    search_color = LiveFilterListSelector(root, get_all_colors())
    search_color.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

    scope_tk = tk.StringVar(root, 'all')
    scope_all = tk.Radiobutton(root, text="All document", variable=scope_tk, value='all')
    scope_all.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    scope_page = tk.Radiobutton(root, text="This page", variable=scope_tk, value='page')
    scope_page.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

    buttons_row = ButtonsRow(root, [Button('Search', ok), Button('Cancel', cancel)])
    buttons_row.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

    root.mainloop()

    return color, scope

def get_color_and_scope_from_input_field():
    try:
        color = scribus.valueDialog('Search by Color', 'Color name')
    except NameError:
        color = ''
    return color, 'all'

def main():
    # if we're inside scribus, do nothing if there is no document open
    try:
        if not scribus.haveDoc():
            return
    except NameError:
        # return
        pass

    if has_tk:
        color, scope = get_color_and_scope_from_dialog()
    else:
        color, scope = get_color_and_scope_from_input_field()
    if has_scribus:
        search_color(color, scope)
    else:
        print(color, scope)


if __name__ == '__main__':
    main()

