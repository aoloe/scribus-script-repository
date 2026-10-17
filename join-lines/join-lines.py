try:
    import scribus
except ImportError:
    print('This script must be run from inside Scribus')
    sys.exit()

def main():
    if not scribus.haveDoc():
        scribus.messageBox('Error', 'You need to have a document open')
        return

    if scribus.selectionCount() == 0 or scribus.getObjectType() != 'TextFrame':
        scribus.messageBox('Error', 'You need to select a text frame')
        return

    # get text of the whole story or the currently selected one
    selection_start, selection_length = scribus.getSelectedTextRange()
    selected_text = scribus.getAllText().strip('\r')

    scribus.deleteText()

    # remove the selection, if any
    scribus.selectText(0, 0)

    joined_text = ''
    trailing_pace = False
    for line in selected_text.split('\r'):
        line = line.rstrip()
        if len(line) == 0:
            joined_text += '\n'
            trailing_pace = False
            continue
        if line[-1] == '-':
            line = line[0:-1]
            trailing_pace = False
        else:
            if trailing_pace:
                joined_text += ' '
            trailing_pace = True

        joined_text += line


    scribus.insertText(joined_text, selection_start)

    scribus.selectText(selection_start, 0)
        
if __name__ == "__main__":
    main()
