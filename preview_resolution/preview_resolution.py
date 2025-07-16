# (c) MIT ale rimoldi
#
# Modify the preview resolution for all images in the document.
#
# For details see the README file.

try:
    import scribus
except ImportError as ex:
    print('This script must be run from inside Scribus')
    raise ex

def main():
    options = {
        'Low': scribus.IMAGE_PREVIEW_RESOLUTION_LOW,
        'Normal': scribus.IMAGE_PREVIEW_RESOLUTION_NORMAL,
        'Full': scribus.IMAGE_PREVIEW_RESOLUTION_FULL
    }

    resolution = scribus.itemDialog('Choose a preview resolution', 'Preview resolution', options.keys(), False)

    if resolution == '':
        return

    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        for item in scribus.getPageItems():
            if item[1] == 2:
                scribus.setImagePreviewResolution(options[resolution], item[0])

if __name__ == "__main__":
    main()

