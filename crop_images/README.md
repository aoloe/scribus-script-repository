# Crop images

Crop the jpg image to its bounding box, and scales it to a target DPI.

The image file gets copied into a (newly created) `images-edited` folder and the frame is linked to it.

You can apply the script to multiple image frames at a time.

A few Warnings:

- The script only works correctly for images that are used only once in the document or if all usages have the same crop and frame size.
- Images with the same name in the target

This script main usage is with a collection of images:

- You add the images directly into the Scribus document.
- You then fit them in the frame and move them around in the bounding box.
- Once the whole document is ready to be exported to PDF, you crop the images and get a much lighter PDF.
- The path to the original image is stored in the item's 'original source' attribute.
- The values `scale_ration, crop_box_left, crop_box_right` are stored as a comma separated string in the 'cropped' attribute.  
  (In the future, this should help creating an "uncrop_images" script)

## Installing Pillow

The script uses the Pillow (PIL) library. You need to install it in a virtual environment inside of the folder where this script is placed.

On Linux or Mac you can do:

```
cd fanzine/
python3 -m venv venv
source venv/bin/activate
pip install pillow
```

On Windows, you have to replace the `source` command by:

```
source venv/Scripts/activate
```

with Git Bash or with the Microsoft own shells:

```
venv\Scripts\activate
```

You only need to do it once, before starting the script for the first time in Scribus.


## TODO

Some ideas for future developments

- Should we also process images that are inside of groups?

  ```py
          elif item_type == 'Group':
              if hasattr(scribus, 'getGroupItems'):
                  for item in scribus.getGroupItems(item,
                          recursive=True, type=scribus.ITEMTYPE_IMAGEFRAME):
                      crop_image(item['name'])
              else:
                  scribus.messageBox('Warning', f'The group {item} will be skipped.', scribus.ICON_WARNING)
  ```
- This script could be used as a basis for doing the resizing and crop in C++ when a PDF is exported:
  - collect all images that have an overflow
  - check if they are used multiple times
  - check if it is worth to export one single image with the new union of all areas
  - check if, after being cropped, the image is smaller in Kb.
- Use a project file to define (or document wide attributes, if they will be implemented):
  - the target folder,
  - the name of the venv folder,
  - the target DPI.
