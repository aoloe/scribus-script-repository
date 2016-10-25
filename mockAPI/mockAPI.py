class Scribus :
    UNIT_MILLIMETERS = 0
    ICON_WARNING = 0
    ICON_NONE = 0
    BUTTON_OK = 0
    BUTTON_YES = 0
    BUTTON_NO = 0

    def haveDoc(self) :
        return True
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

# scribus = Scribus()
