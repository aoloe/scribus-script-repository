""" From an A7 document, create a foldable fanzine on a A4 sheet.

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
import datetime

def show_error(message):
    scribus.messageBox('Scribus - Script Error', message, scribus.ICON_WARNING, scribus.BUTTON_OK)

def main():
    
    if not scribus.haveDoc():
        show_error("No document open.")
        return

    if scribus.pageCount() != 8:
        show_error("You need a document with eight pages.")
        return

    # TODO: ensure that the unit is mm

    for i in range(scribus.pageCount()):
        if scribus.getPageNSize(i + 1) != scribus.PAPER_A7_MM:
            show_error("All pages need to be A7.")
            return

    if scribus.pageCount() != 8:
        show_error("You need a document with eight pages.")
        return

    # Load the virtual environment in venv and then pypdf

    # ACTIVATE_FILENAME = inspect.getframeinfo(inspect.currentframe()).filename
    ACTIVATE_PATH = Path(__file__).resolve().parent
    venv_path = ACTIVATE_PATH / 'venv'
    if not venv_path.is_dir():
        show_error(f'You need to create a virtual environment called venv in the script folder:\n\n{venv_path}.\n\n See the README.md for more details.')
        return
    site_packages = next(venv_path.glob("lib/python*/site-packages"), None)

    if site_packages:
        site.addsitedir(site_packages)

    try:
        from pypdf import PdfReader, PdfWriter, PaperSize, Transformation
    except ImportError as ex:
        show_error(f'You need to create a virtual environment in\n\n{ACTIVATE_PATH}\n\nand pip install pypdf in there.\n\n See the README.md for more details.')
        return

    # Create a "linear" PDF from Scribus

    temp_folder = tempfile.mkdtemp(prefix='scribus-fanzine')
    temp_path = Path(temp_folder)
    temp_filename = temp_path / 'document.pdf'
    
    pdf = scribus.PDFfile()
    pdf.file = str(temp_filename)
    pdf.save()

    # Impose the PDF as an A4 fanzine

    reader = PdfReader(path / source['file'])
        
    temp_filename.unlink(missing_ok=True)
    temp_path.rmdir()



if __name__ == '__main__':
    main()
