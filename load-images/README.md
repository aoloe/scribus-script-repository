# Loading images

This directory contains a few scripts that automate the loading of images in your document.

## `load-images.py`

Load all images from a directory, one image per page.

It starts from the selected frame and creates an image of the frame size on each one of the following pages and loads the next image (alphabetically).

If the end of the document is reached, new pages are automatically created.

Warning: at the time of writing, if the document has been created in one language (french) and is being edited in a differnt one (english), there is a bug in scribus that makes it impossible for the script to create new pages.

In that case, You have to create enough pages before running the script (you can always remove the exceeding ones afterwards).

## `load-images-1.5-untested.py`

An untested version of `load-images.py` that copies the selected frame in the new pages instead of creating new frames.

## `load-images-existing-fames.py`

Load all images from a directory into the empty image frames in the current document.

You need to create enough (empty) image frames before running the script (see `edit > multiduplicate` for ways of duplicating your frames).
