# images-missing-relink.py

This script checks if the document contains image frames with a broken link.
If any is found, it will ask if you want to look for the correct image and then
prompt for the new location of the first image.
It will then check all other image frames with a broken link and look for an image
of the same name in the new location. It the image is there, the link will be
replaced.
## Licence

This program is free software under the MIT license.

Author: Ale Rimoldi <ale@graphicslab.org>

Please report bugs to http://github.com/aoloe/scribus-script-repository/

## Todo

- implement it in "Extras > Manage images"
