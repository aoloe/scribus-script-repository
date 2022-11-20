# Table of contents

**Work in progress**

This script needs `selectFrameText()` which has been introduced in Scribus 1.5.6 on the 16 july 2020.

You're welcome to suggest a (minimal?) UI and further featurees for this script.

## Notes

## Adding the table of contents to the pdf

### pdftk

```sh
pdftk your-file.pdf update_info "$bookmarks_file" output "$tmp_dir/$f"
```



<https://www.youtube.com/watch?v=5dv_02v0zzc>

```sh
pdftk your-file.pdf dump_data > metadata.txt
```

In the resulting `metadata.txt, in between

```
NumberOfPages: 8
PageMediaBegin
```

add one entry for Toc item:

```
BookmarkBegin
BookmarkTitle:
BookmarkLevel:
BookmarkPageNumber:
```

The result will be something like:

```
NumberOfPages: 8
BookmarkBegin
BookmarkTitle: First title
BookmarkLevel: 1
BookmarkPageNumber: 2
BookmarkBegin
BookmarkTitle: Second title
BookmarkLevel: 1
BookmarkPageNumber: 2
PageMediaBegin
```

Put the modified metadata into a copy of the pdf.

```sh
pdftk your-file.pdf update_info_utf8 metadata.txt output your-file-with-toc.pdf
```


### `selectFrameText()`

`selectText()` works on the whole frame chain. we need `selectFrameText()` to detect styles inside of specific text frames.

<https://bugs.scribus.net/view.php?id=16159>

```py
# get the first 4 chars of a frame
scribus.deselectAll()
scribus.selectObject('Text1')
scribus.selectFrameText(0, 4)
print(scribus.getFrameText() == 'This')
# get all chars starting from 5 in a chained frame
scribus.selectFrameText(5, -1)
print(scribus.getFrameText() == 'is some text with no style in the first frame.')

# select in an empty frame
scribus.deselectAll()
scribus.selectObject('Text4')
scribus.selectFrameText(0, 0)
print(scribus.getFrameText() == '')

# select in a chained empty frame
scribus.deselectAll()
scribus.selectObject('Text6')
scribus.selectFrameText(0, 0)
print(scribus.getFrameText() == '')

# get all chars starting from 5 in an unchained frame
scribus.deselectAll()
scribus.selectObject('Text3')
scribus.selectFrameText(5, -1)
print(scribus.getFrameText() == 'is some text.')
scribus.selectFrameText(0, 0)
# remove the selection
print(len(scribus.getFrameText()) == 18)
scribus.selectFrameText(5, 13)

# push the count to its limit
print(scribus.getFrameText() == 'is some text.')
# set count 1 over the limit
try:
    scribus.selectFrameText(5, 14)
    print('don\'t print this', scribus.getFrameText())
except IndexError:
    print(True)
# select the first 5 chars in the second frame in a chain
scribus.deselectAll()
scribus.selectObject('Text2')
scribus.selectFrameText(0, 5)
print(scribus.getFrameText() == 'which')
# select all chars after the first 6 in the second frame in a chain
scribus.selectFrameText(6, -1)
print(scribus.getFrameText() == 'has the style abc and is in the chained frame.')
# select with. a way too big count
try:
    scribus.selectFrameText(1000, 5)
    print('don\'t print this', scribus.getFrameText())
except IndexError:
    print(True)
```
