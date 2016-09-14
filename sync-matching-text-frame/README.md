# Synchronize the content of text frames

This frames allows you to propagate changes to a text frames to all other frames in the document that have a "similar" name.

Starting from 1.5.x please use pattern instead.

## Usage

- Create your document.
- Through the "X, Y, Z" tab in the properties palette, rename each text frame that has to keep in sync with a pattern.
  - As an example, if the frame contains the name of the current month you will name them "Month01", "Month02", ...
  - Only the part up to the first digit will be used to find the frames that have to be kept in sync (in this case "Month").
  - The prefixes "Copy of " and "Kopie von " are stripped.
- Change one of the frames name with this pattern.
- Select the modified frame and run the script.

If possible, you should run the script on a copy of the original document and save the result under a new name.
