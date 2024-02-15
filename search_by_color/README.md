# Serch Items by Color

Find the first shape or frame with a specific color name as fill or stroke.

If TKinter is installed, it will show the list of all colors with a filter, and let the user pick one of the colors.

In this case, the user can also choose to search in the current page only or in the whole document.

If Tkinter is not installed, the user will be prompted for the color name and the search will be performed in the full document.

Currently, the script is ready to support searching the color inside of groups, but Scribus does not support querying the color of items that are inside of a group yet (a patch has been submitted to make it work).

## Transitory behaviors

This scripts uses commands that, at the time of writing this script, are very new in scribus.

If `getGroupItems()` is not available, it won't search inside of Scribus (merged on 2024-01-07; might or not be in Scribus 1.6.1).

If `getUniqueItem()` does not find items inside of groups it won't be able to search inside of groups either (the patch has been submitted on 2024-02-15).
