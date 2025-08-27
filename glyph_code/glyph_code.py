""" Show the unicode code for the selected character(s)

(c) MIT ale rimoldi"""

try:
    import scribus
except ImportError as ex:
    print('\nThis script must be run from inside Scribus\n')
    raise ex

def main():
    if not scribus.haveDoc():
        scribus.messageBox('Scribus - Script Error', "No document open", scribus.ICON_WARNING, scribus.BUTTON_OK)
        return

    if scribus.selectionCount() != 1 or scribus.getObjectType() != 'TextFrame':
        scribus.messageBox('Scribus - Script Error', "You need a text selection", scribus.ICON_WARNING, scribus.BUTTON_OK)
        return
    
    text = scribus.getFrameText()

    scribus.messageBox('Glyph', f'{text}:\n{' '.join([hex(ord(c)) for c in text])}', scribus.ICON_WARNING, scribus.BUTTON_OK)


if __name__ == "__main__":
    main()
