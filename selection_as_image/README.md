# Export selection as image

Exports the selection as an image.

Uses pillow if installed (and seen by the Scripter from inside of Scribus), calls Imagemagick's convert, otherwise.

Not fully implemented:

- Rotated items are not taken into consideration.
- The scale is defined as a constant and not a parameter that can be set by the user.
