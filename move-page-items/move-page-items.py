# horizontally move all the items in a list of pages by a give amount
#
# © mit, ale rimoldi, 2023

try:
    import scribus
except ImportError:
    print('This script must be run from inside Scribus')
    sys.exit()

pagesString = scribus.valueDialog("", "Page numbers (separated by commas)")
horizontalMovement = int(scribus.valueDialog("", "Horizontal movement (in the current unit)"))

for page in [int(p.strip()) for p in pagesString.split(',')]:
    try:
        scribus.gotoPage(page)
        scribus.deselectAll()
        for item in scribus.getPageItems():
            scribus.moveObject(horizontalMovement, 0, item[0])
    except Exception as e:
        pass
