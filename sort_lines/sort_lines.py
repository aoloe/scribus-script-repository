"""Sort the lines in the selected frame or in the current selection

For more details see the README.md

(c) MIT 2024, ale rimoldi <ale@graphicslab.org>
"""

has_scribus = True
try:
    import scribus
except ImportError:
    pass

# scribus.getSelectionTextFrame() does not exist yet.
# we approximate it with a function that compares the result of getFrameText with 
# the result of the same function when no selection is around.
# finally, it restores the selection.
def getSelectionTextFrame():
    selected_text = scribus.getFrameText()
    scribus.selectFrameText(0, 0)
    frame_text = scribus.getFrameText()
    if len(selected_text) == len(frame_text):
        return None, None
    selection_start = frame_text.find(selected_text)
    selection_length = len(selected_text)
    scribus.selectFrameText(selection_start, selection_length)
    return selection_start, selection_length

def main():
    # if we're inside scribus, do nothing if there is no document open
    try:
        if not scribus.haveDoc():
          scribus.messageBox('Error', 'You need to have a document open')
        if scribus.selectionCount() != 1 or scribus.getObjectType() != 'TextFrame':
          scribus.messageBox('Error', 'You need one active text frame')
    except NameError:
        print('This script must be run from inside Scribus')
        return

    selected_text = scribus.getFrameText()
    try:
        # TODO: returns None if there is no selection?
        selection_start, selection_length = scribus.getSelectionTextFrame()
    except NameError:
        selection_start, selection_length = scribus.getSelectionTextFrame()

if __name__ == '__main__':
    main()

