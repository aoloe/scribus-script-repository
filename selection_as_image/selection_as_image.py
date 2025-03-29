import scribus
try:
    from PIL import Image
    has_pil = True
except ImportError:
    has_pil = False
    import subprocess

# TODO: let he user choose the scale
SCALE = 1

def main():
    n = scribus.selectionCount()
    if n == 0:
        return

    old_unit = scribus.getUnit()
    scribus.setUnit(scribus.UNIT_POINTS)

    page_i = scribus.currentPage()
    w, h = scribus.getPageNSize(page_i)

    # the selection must be inside of the page size
    # (since only the inner part of the page will be exported)
    start = [w, h]
    end = [0, 0]
    

    for i in range(n):
        item = scribus.getSelectedObject(i)
        x, y = scribus.getPosition(item)
        w, h = scribus.getSize(item)
        # TODO: support rotated items
        # r = scribus.getRotation(item)
        start[0] = min(x, start[0])
        start[1] = min(y, start[1])
        end[0] = max(x + w, end[0])
        end[1] = max(y + h, end[1])

    scribus.setUnit(old_unit)

    png_filename = scribus.fileDialog("Exported image file name", ".png", "image.png", False, True, False)
    if png_filename == '':
        return

    i = scribus.ImageExport()
    i.type = 'PNG' # select one from i.allTypes list
    # TODO: set a scale
    i.scale = 100 * SCALE
    # TODO: make the file name variable
    i.saveAs(png_filename)

    if has_pil:
        png = Image.open(png_filename)
        png.crop((start[0] * SCALE, start[1] * SCALE, end[0] * SCALE, end[1] * SCALE)).save(png_filename)
    else:
        # use imagemagick's convert
        # TODO: this is untested
        x = start[0] * SCALE
        y = start[1] * SCALE
        w = (end[0] - start[0]) * SCALE
        h = (end[1] - start[1]) * SCALE
        subprocess.call(['convert', png_filename, '-crop', '{w}x{h}+{x}+{y}', png_filename])

if __name__ == '__main__':
    main()
