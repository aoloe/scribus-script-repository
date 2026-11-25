""" Crop the images in the selection and scape them to a target resolution (300 dpi)

© mit, ale rimoldi, 2026
"""

from pathlib import Path
import importlib.util
import site

import math

try:
    import scribus # pylint: disable=import-error
except ImportError:
    pass

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

def crop_image(item, Image, ImageOps):
    image_filename = scribus.getImageFile(item)
    if image_filename == "":
        show_error(f'{item} does has any image loaded.')
        return

    try:
        image = Image.open(image_filename)
    except:
        show_error(f'Failed to open {image_filename} for {item}')
        return

    # Respect the image's rotation in the EXIF fields, as does Scribus
    image = ImageOps.exif_transpose(image)

    document_unit = scribus.getUnit()
    scribus.setUnit(scribus.UNIT_INCHES)

    frame_width_in, frame_height_in = scribus.getSize(item)

    scribus.setUnit(scribus.UNIT_POINTS)

    frame_width, frame_height = scribus.getSize(item)

    image_x_offset = scribus.getProperty(item, 'imageXOffset')
    image_y_offset = scribus.getProperty(item, 'imageYOffset')
    image_x_scale = scribus.getProperty(item,'imageXScale')
    image_y_scale = scribus.getProperty(item,'imageYScale')
    image_width, image_height = image.size

    crop_box_left = 0 if image_x_offset == 0 else - image_x_offset
    crop_box_top = 0 if image_y_offset == 0 else - image_y_offset
    crop_box_right = crop_box_left + frame_width // image_x_scale
    crop_box_bottom = crop_box_top + frame_height // image_y_scale

    # do not crop if the image does not fill the frame
    if crop_box_left < 0 or crop_box_top < 0 or \
            crop_box_right > image_width + crop_box_left or crop_box_bottom > image_height + crop_box_top:
        show_error(f'The image does not fill the frame {item}.')
        scribus.setUnit(document_unit)
        return

    # show_error(f'{image_x_scale} x {image_y_scale}')
    image_x_dpi = (720 / image_x_scale) / 10
    image_y_dpi = (720 / image_y_scale) / 10

    if not math.isclose(image_x_dpi, image_y_dpi):
        show_error(f'The image\'s horizontal and vertical scaling are not the same.')
        scribus.setUnit(document_unit)
        return

    image_dpi = image_x_dpi


    # Only scale if the current DPI are 15% over the target
    scale_ratio = 1
    if image_dpi > IMAGE_TARGET_DPI * 115 / 100:
        scale_ratio = IMAGE_TARGET_DPI / image_dpi
        image = image.resize((int(image_width * scale_ratio), int(image_height * scale_ratio)), Image.LANCZOS)
        image_width *= scale_ratio
        image_height *= scale_ratio
        image_dpi = IMAGE_TARGET_DPI

    cropped = False
    # Crop it, if it overflows more than 5% in any direction
    if max(crop_box_left, crop_box_right) > frame_width * 0.05 or \
            max(crop_box_top, crop_box_bottom) > frame_height * 0.05:
        image = image.crop((
            crop_box_left * scale_ratio, \
            crop_box_top * scale_ratio, \
            crop_box_right * scale_ratio, \
            crop_box_bottom * scale_ratio))
        cropped = True

    # No change to save
    if scale_ratio == 1 and not cropped:
        scribus.setUnit(document_unit)
        return 

    # Save the action in the attributes and allow the user to restore the original state
    scribus.setObjectAttributes([
        {'Name': 'cropped source', 'Type': 'string',
            'Value': image_filename, 'Parameter': '', 'Relationship': '',
            'RelationshipTo': '', 'AutoAddTo': ''},
        {'Name': 'cropped', 'Type': 'string',
            'Value': f'{scale_ratio}, {crop_box_left}, {crop_box_right}', 'Parameter': '', 'Relationship': '',
            'RelationshipTo': '', 'AutoAddTo': ''}
        ], item)

    # Save the scaled and cropped file and load it in the frame
    target_path = Path(scribus.getDocName()).parent / IMAGES_FOLDER
    if not target_path.is_dir():
        target_path.mkdir()

    target_file = target_path / Path(image_filename).name
    image.save(target_file)
    scribus.loadImage(str(target_file), item)

    # Adjust the crop box
    if not cropped:
        if scale_ratio != 1:
            scribus.setProperty(item, 'imageXOffset', crop_box_left * scale_ratio)
            scribus.setProperty(item, 'imageYOffset', crop_box_top * scale_ratio)
    else:
        scribus.setScaleImageToFrame(True, True, item)

    scribus.setUnit(document_unit)

# TODO: use document wide attributes for the settings
IMAGES_FOLDER = 'images-edited'
IMAGE_TARGET_DPI = 300

def main():
    if not scribus.haveDoc():
        show_error("No document open.")
        return

    if scribus.getDocName() == '':
        show_error("You need to first save the document.")
        return

    if importlib.util.find_spec('pillow') is None:
        # Load pillow and check if PIL exists
        if not load_venv({'pillow': 'PIL'}):
            return
    try:
        from PIL import Image, ImageOps
    except ImportError:
        show_error('Could not import pillow')
        return

    # TODO: maybe add a progress dialog
    imagesCount = 0
    for i in range(scribus.selectionCount()):
        item = scribus.getSelectedObject(i)
        item_type = scribus.getObjectType(item)
        if item_type == 'ImageFrame':
            crop_image(item, Image, ImageOps)
            imagesCount += 1

    if imagesCount == 0: 
        show_error("No image selected.")

if __name__ == '__main__':
    main()
