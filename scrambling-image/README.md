# scrambling-image.py
This script replaces all images on all pages of the current Scribus document through cc-by images from flickr.

You would be wise to work on a copy of the original to avoid accidentally saving this scrambled version only to lose the original.

Partially inspired by Gregory Pittman's `scramble-text.py` script and by <http://megasnippets.com/en/source-codes/python/get_random_interesting_image_flickr>

## Licence

This program is free software under the MIT license.

Author: Ale Rimoldi <ale@graphicslab.org>

Please report bugs to http://github.com/aoloe/scribus-script-repository/

## Todo

- [ ] crop a part of the image that matches the size of the image in the document and then scale it, so that it haves the same size of the original image (imagemagick? pil?.
- [ ] show an alert explaining that the script replaces the current images.
- [ ] only run the script if the current document has been saved.
- [ ] the default action is to "Save as" after the dialog. But give an option not to do so.
- [ ] eventually, implement other sources for free images.
