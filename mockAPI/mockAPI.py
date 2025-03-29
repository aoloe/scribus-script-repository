class Scribus:
    def __init__(self):
        self.mock_instance = True
        self.items = {}
        self.selection = []
        
        self.docName = ''
        self.page = 1
        self.page_counter = 1
        self.column_guides = {'number': 0, 'gap': 0, 'reference': 0, 'guides': []}
        self.row_guides = {'number': 0, 'gap': 0, 'reference': 0, 'guides': []}

    UNIT_MILLIMETERS = 0
    ICON_WARNING = 0
    ICON_NONE = 0
    BUTTON_OK = 0
    BUTTON_YES = 0
    BUTTON_NO = 0

    def haveDoc(self) :
        return self.docName != ''
    def getDocName(self) :
        return self.docName
    def openDoc(self, name) :
        pass
    def closeDoc(self) :
        pass
    def messageBox(self, title, description,  icon=ICON_NONE, button1=0, button2=0, button3=0) :
        print(f'{title}:\n{description}')
        return button1
    def valueDialog(self, title, description, default='') :
        return default
    def setRedraw(self, activate) :
        return True
    def getUnit(self) :
        return True
    def setUnit(self, unit) :
        return True
    def newPage(self):
        self.page_counter += 1
    def pageCount(self):
        return self.page_counter
    def currentPage(self) :
        return self.page
    def gotoPage(self, page):
        self.page = page
    def getPageNMargins(self, n) :
        return (14.1111111111, 14.1111111111, 14.1111111111, 14.1111111111)
    def getPageNSize(self, n) :
        return (210.0, 297.0)
    def setVGuides(self, guides) :
        return True
    def setHGuides(self, guides) :
        return True
    def getColumnGuides(self):
        return self.column_guides
    def getRowGuides(self):
        return self.row_guides
    def setColumnGuides(self, number, gap=None, refer_to=0):
        self.column_guides = {
            'number': number,
            'gap': gap if gap != None else self.column_guides['gap'],
            'refer_to': refer_to if refer_to != None else self.column_guides['refer_to'],
        }
    def setRowGuides(self, number, gap=0.0, refer_to=0):
        self.row_guides = {
            'number': number,
            'gap': gap if gap != None else self.row_guides['gap'],
            'refer_to': refer_to if refer_to != None else self.row_guides['refer_to'],
        }
    def setBaseLine(self, line_height_mm, margin_top) :
        return True
    def selectText(self, start, end, frame) :
        pass
    def getCharStyles(self) :
        return []
    def setCharacterStyle(self, name) :
        pass
    def createCharStyle(self, style_name, **keywords):
        pass

    def createText(self, x, y, w, h, name=None):
        if name is None:
            name = f'Text{len(self.items) + 1}'
        item = MockPageItem('Text', x, y, w, h, name)
        self.items[name] = item
    def createLine(self, x1, y1, x2, y2, name=None):
        if name is None:
            name = f'Line{len(self.items) + 1}'
        item = MockPageItem('Line', x1, y2, x2 - x1, y2 - y1, name)
        self.items[name] = item

    def getPosition(self, name):
        return self.items[name].x, self.items[name].y
    def getSize(self, name):
        return self.items[name].w, self.items[name].h

    def selectionCount(self):
        return len(self.selection)
    def getSelectedObject(self, i):
        return self.selection[i]

    def PDFfile(self):
        return PDFfile()

    def mock_inject_items(self, items):
        self.selection = items
    def mock_inject_selection(self, items):
        self.selection = items

class MockPageItem:
    def __init__(self, itemType, x, y, w, h, name=None):
        self.itemType = itemType
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name

class PDFfile:
    file = ''
    def save(self):
        pass
