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

    # get current selection
    selected_text = scribus.getFrameText()

    scribus.selectFrameText(0, 0)

    frame_text = scribus.getFrameText().strip('\r')
    
    if len(selected_text) == len(scribus.getFrameText()):
        scribus.messageBox('Error', 'There is no selection in the text frame')
        # no text selected
        return

    paragraphs_count = selected_text.count('\r') + 1

    frame_paragraphs = frame_text.strip('\r').split('\r')

    styles = []
    start = 0
    for paragraph in frame_paragraphs[0:paragraphs_count]:
        scribus.selectFrameText(start, len(paragraph))
        styles.append(scribus.getParagraphStyle())
        start += len(paragraph) + 1

    for i, paragraph in enumerate(frame_paragraphs[paragraphs_count:]):
        scribus.selectFrameText(start, len(paragraph))
        scribus.setParagraphStyle(styles[i % len(styles)])
        start += len(paragraph) + 1

    scribus.selectFrameText(0, 0)
        
if __name__ == "__main__":
    main()
