""" From an A7 document with up to 8 pages, create a foldable fanzine on a A4 sheet.

For details see the README file.

(c) 2026 MIT ale rimoldi"""

try:
    import scribus
except ImportError as ex:
    print('\nThis script must be run from inside Scribus\n')
    raise ex

from pathlib import Path

import site
# import inspect
import tempfile
import importlib.util
import datetime
import math

def show_error(message):
    scribus.messageBox('Scribus - Script Error', message, scribus.ICON_WARNING, scribus.BUTTON_OK)

def load_venv(packages):
    """load_venv(packages) -> bool

       Load the virtual environment in venv with the packages

       packages -- A dict, the key being the name of the package and the value
                   a folder in site-packages to test if the package is indeed
                   installed.
                   It can be a list if the package name is identical to
                   the folder name.
    """
    ACTIVATE_PATH = Path(__file__).resolve().parent
    venv_path = ACTIVATE_PATH / 'venv'
    if not venv_path.is_dir():
        show_error(f'You need to create a virtual environment called venv in the script folder:\n\n{venv_path}.\n\nSee the README.md for more details.')
        return False

    # Find site-packages on Windows or Linux/Mac
    site_packages = None

    for pattern in ('Lib/site-packages', 'lib/python*/site-packages'):
        matches = list(venv_path.glob(pattern))
        if matches:
            site_packages = matches[0]
            break

    if site_packages is None:
        show_error("Could not find the site-packages in the virtual environment.")
        return False

    site.addsitedir(site_packages)

    if type(packages) is list:
        packages = dict(zip(packages, packages))
    for package, folder in packages.items():
        if not (site_packages / folder).is_dir():
            show_error(f'You need to pip install {package} in your virtual environment\n\n{ACTIVATE_PATH}.\n\n See the README.md for more details.')
            return False

    return True

def export_pdf(filename):
    pdf = scribus.PDFfile()
    pdf.file = str(filename)
    pdf.save()

def impose_pdf(temp_filename, output_filename):
    """ Impose the PDF as an A4 fanzine """

    try:
        from pypdf import PdfReader, PdfWriter, PageObject, Transformation
    except ImportError as ex:
        show_error("Could not import pypdf. Is it installed in your virtual environment?")
        return


    reader = PdfReader(temp_filename)
    writer = PdfWriter()
    sheet = PageObject.create_blank_page(
        width=scribus.PAPER_A4[1],
        height=scribus.PAPER_A4[0]
    )

    # Page arrangement
    layout = [
        (7, True), (6, True), (5, True), (4, True),
        (8, False), (1, False), (2, False), (3, False),
    ]

    # Place the A7 pages on the A4 sheet
    for i, (page_num, rotate_180) in enumerate(layout):
        if page_num > len(reader.pages):
            continue

        page = reader.pages[page_num - 1]

        col = i % 4
        row = i // 4

        x = col * scribus.PAPER_A7[0]
        y = scribus.PAPER_A7[1] if row == 0 else 0

        if rotate_180:
            transform = (
                Transformation()
                .rotate(180)
                .translate(
                    tx=x + scribus.PAPER_A7[0],
                    ty=y + scribus.PAPER_A7[1]
                )
            )
        else:
            transform = Transformation().translate(
                tx=x,
                ty=y
            )

        sheet.merge_transformed_page(page, transform)

    writer.add_page(sheet)

    with open(output_filename, "wb") as f:
        writer.write(f)

def is_close_tuples(a, b):
    for i in range(min(len(a), len(b))):
        if not math.isclose(a[i], b[i]):
            return False
    return True

def main():
    
    if not scribus.haveDoc():
        show_error("No document open.")
        return

    unit_current=scribus.getUnit() #get unit and change it to mm
    scribus.setUnit(scribus.UNIT_MILLIMETERS)

    for i in range(min(8, scribus.pageCount())):
        if not is_close_tuples(scribus.getPageNSize(i + 1), scribus.PAPER_A7_MM):
            show_error(f'All pages need to be A7.')
            return

    if importlib.util.find_spec('pypdf') is None:
        if not load_venv(['pypdf']):
            return

    suggested_filepath = scribus.getDocName()
    if suggested_filepath == '':
        suggested_filepath = Path.home() / 'fanzine.pdf'
        doc_parent_path = Path.home()
    else:
        suggested_filepath = Path(suggested_filepath).with_suffix('.pdf')
        doc_parent_path = suggested_filepath.parent

    # Get the target filename
    # if scribus.SCRIBUS_VERSION_INFO < (1,7,5):
    #     # In older versions, it was called issave and the implementation did not
    #     # match the documentation. Do we need to change something?
    #     is_open = False
    is_open = False
    output_filename = scribus.fileDialog('Save the imposed fanzine', 'PDF files (*.pdf)', str(suggested_filepath), True, is_open)
    if output_filename == '':
        return

    output_path = Path(output_filename)
    if not output_path.is_absolute():
        # TODO: check that this is what the user saw
        output_filename = doc_parent_path / output_filename
   
    # Create the unimposed PDF from Scribus
    temp_folder = tempfile.mkdtemp(prefix='scribus-fanzine')
    temp_path = Path(temp_folder)
    temp_filename = temp_path / 'document.pdf'

    export_pdf(temp_filename)

    # Impose the pdf
    if output_filename is not None:
        impose_pdf(temp_filename, output_filename)
    
    temp_filename.unlink(missing_ok=True)
    temp_path.rmdir()
    scribus.setUnit(unit_current)

if __name__ == '__main__':
    main()
