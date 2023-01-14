class Scribus:
    def __init__(self):
        self.mock_instance = True
        self.items = {}
        self.selection = []

    UNIT_MILLIMETERS = 0
    ICON_WARNING = 0
    ICON_NONE = 0
    BUTTON_OK = 0
    BUTTON_YES = 0
    BUTTON_NO = 0

    def haveDoc(self) :
        return True
    def openDoc(self, name) :
        pass
    def closeDoc(self) :
        pass
    def messageBox(self, title, description,  icon, button1 = 0, button2 = 0, button3 = 0) :
        return button1
    def valueDialog(self, title, description, default = '') :
        return default
    def setRedraw(self, activate) :
        return True
    def getUnit(self) :
        return True
    def setUnit(self, unit) :
        return True
    def currentPage(self) :
        return 1
    def getPageNMargins(self, n) :
        return (14.1111111111, 14.1111111111, 14.1111111111, 14.1111111111)
    def getPageNSize(self, n) :
        return (210.0, 297.0)
    def setVGuides(self, guides) :
        return True
    def setHGuides(self, guides) :
        return True
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
