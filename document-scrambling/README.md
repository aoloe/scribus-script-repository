# Scrambling a document

This script scrambles the content of a scribus document:

- text is scrambled by shuffling the letters of the document without losing the words rythm and the formatting.
- images are blurred at a very high level.

If there is a selection, only the selected frames are scrambled.

Don't forget to only run the script on a copy of your document! Otherwise, you risk to lose your work.

# Requirements

- For blurring the images, you need ImageMagick installed
- Scribus 1.5 with the patches uploaded in the tickets: 12253, 12583.

# How does it work

- Get the fields to be processed:
  - If there is a selection, only the selected fields are processed and the list of selected fields is recorded.
  - Only the text and image fields are retained.
- The eventual current selection is cancelled.
- Go through all the text frames and collect all the characters that are not on the list to be ignored.
- Shuffle the collected characters
- For each text frame:
  - Loop through all the characters,
  - put the next shuffled character before it,
  - by retaining the case,
  - and delete the current caracter.
- For each image frame:
  - Use ImageMagick's `identify` to get the image size.
  - Make a copy of the linked image with a very strong blur (with sigma defined as size divided by 50).
  - Load the blurred image into the image frame.
- Restore the initial selection.


# Todo:

- correctly handle emtpy image frames and inline images (if needed)
