import scribus

def get_unit_name(unit):
    if unit == scribus.UNIT_POINTS:
        return "pt"
    elif unit == scribus.UNIT_MILLIMETERS:
        return "mm"
    elif unit == scribus.UNIT_INCHES:
        return "in"
    elif unit == scribus.UNIT_PICAS:
        return "p"
    elif unit == scribus.UNIT_CENTIMETRES:
        return "cm"
    elif unit == scribus.UNIT_CICERO:
        return "c"
    return ""

def set_minimal_line_thickness(item, minimal_thickness):
    try:
        scribus.getLineColor(item)
    except:
        scribus.messageBox('', item)
        return
    if scribus.getLineColor(item) == 'None':
        return
    line_width = scribus.getLineWidth(item)
    if line_width < minimal_thickness:
        scribus.setLineWidth(minimal_thickness, item)

def main():
    if not scribus.haveDoc():
        return
    minimal_thickness = scribus.valueDialog('Line thickness', f'Minimal line thickness ({get_unit_name(scribus.getUnit())}):')
    try:
        minimal_thickness = float(minimal_thickness)
    except ValueError:
        return
    minimal_thickness = scribus.docUnitToPoints(minimal_thickness)
    current_page = scribus.currentPage()
    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        for item in scribus.getPageItems():
            if item[1] == 12:
                for group_item in scribus.getGroupItems(item[0]):
                    set_minimal_line_thickness(group_item[0], minimal_thickness)
            else:
                set_minimal_line_thickness(item[0], minimal_thickness)

    scribus.gotoPage(current_page)
if __name__ == '__main__':
    main()
