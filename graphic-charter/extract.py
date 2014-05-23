
import scribus

from xml.etree import ElementTree as ET


from interface import color_def, font_def, graphic_chart_def

def extract_colors():
    """
    Extract and return all colors in the current document.
    """
    colors = []
    names = scribus.getColorNames()
    for name in names:
        cyan, magenta, yellow, black = scribus.getColor(name)
        is_spot = scribus.isSpotColor(name)
        colors.append(color_def("cmyk",
                                (cyan, magenta, yellow, black),
                                name))

    return colors


def extract_fonts():
    """
    Extract all fonts in the current document.
    """
    path = scribus.getDocName()
    root = ET.parse(path)

    fonts = set()
    for font_node in root.findall('.//*[@FONT]'):
        font_name = font_node.attrib['FONT']
        font_size = font_node.get('FONTSIZE', None)
        fonts.add((font_name, font_size))

    for font_node in root.findall('.//*[@CFONT]'):
        font_name = font_node.attrib['CFONT']
        font_size = font_node.get('CSIZE', None)
        fonts.add((font_name, font_size))

    return [font_def(name, style) for name, style in fonts]
    

def extract(chart):
    """
    Extract the graphic chart of the current document.
    """
    if not scribus.haveDoc():
        return  
    
    try:
        scribus.saveDoc()
        if not scribus.getDocName():
            raise IOError('Could not save document.')
    except:
        scribus.messageBox('Script failed',
                           'This script only works if you saved the document.')
        return

    colors = extract_colors()
    fonts = extract_fonts()
    for color in colors:
        chart.add_color(color)
    for font in fonts:
        chart.add_font(font)
    return chart


def main():
    chart = graphic_chart_def()
    extract(chart)

if __name__ == "__main__":
    main()

