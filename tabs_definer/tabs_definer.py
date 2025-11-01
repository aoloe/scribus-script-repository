""" Define tabs in styles, based on the content of non-printable text frames

For details see the README file.

(c) MIT your name"""

try:
    import scribus
except ImportError as ex:
    print('\nThis script must be run from inside Scribus\n')
    raise ex

def show_error(message):
    scribus.messageBox('Scribus - Script Error', message, scribus.ICON_WARNING, scribus.BUTTON_OK)

def main():
    tabs_aligment = {'l': 0, 'r': 1, '.': 2, ',': 3, 'c': 4}
    if not scribus.haveDoc():
        show_error("No document open")
        return

    if scribus.selectionCount() != 1 or scribus.getObjectType() != 'TextFrame':
        show_error("You need a text selection")
        return

    current_unit=scribus.getUnit() #get unit and change it to mm
    scribus.setUnit(scribus.UNIT_MILLIMETERS)


    text_definition = scribus.getAllText()
    for style_text_definition in text_definition.split('\n'):
        style_definition = style_text_definition.split(',')
        style_name = style_definition[0]
        style_tabs = []
        for tabs_definition in style_definition[1:]:
            tabs = tabs_definition.split(':')
            
            position = int(tabs[0]) if tabs[0].isdigit() else float(tabs[0])
            # the tabs position is always in pt
            position = position * 2.835
            align = 0 if len(tabs) == 1 else tabs_aligment[tabs[1]]
            style_tabs.append((position, align))

        scribus.createParagraphStyle(name=style_name, tabs=style_tabs)

    scribus.setUnit(current_unit)

if __name__ == "__main__":
    main()

