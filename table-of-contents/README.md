# Table of contents

Generate the table of contents in the current frame by looking at the styles used in the document.

## The paragraph styles

By default, the script looks for the styles "h1", "h2", and "h3".

```py
headings = ['h1', 'h2', 'h3']
```

Also, by default, the script applies the styles "toc1", "toc2", and "toc3".

```py
toc_styles = ['toc1', 'toc2', 'toc3']
```

If you want to track style of different names (or add more styles), simply modify the `headings` variable.

## Sections and page numbering

In Scribus you can define sections and

- define the starting page number
- format the page number with different schemas (roman, letters, ...)

Since it's not possible yet to read the section setting from the scripter API, the script define a `sections` global variable where you can add the sections you have defined:

```py
sections = [
    {
        'end': 0, # last page index in this section (0 = to the end)
        'format': '1', # one of '1', 'i', 'I', 'a', 'A' # TODO: scribus has more possible formats
        'start_number': 1,
    },
]
```

## Initialize the table of contents

- Create the styles for the heading and the table of contents.
- Create your content, using "h1", "h2", and "h3" styles for the headings.
- Create a text frame where you want the table of contents to appear.

## Filling the table of contents

- Select the table of contents text frame
- Run the `table-of-contents.py` script.

## Setting the heading and toc styles from the attributes

By adding the attributes `heading_styles` or `toc_styles` you can define custom styles to be used.  
Not only you can customize the name of the styles, but you can create multiple table of contents, by tracking different toc styles.

- In _File > Document Setup > Document Item Attributes_ create the attributes `heading_styles_ and / or `toc_styles`, using the type string.
- Select the frame where you want the table of contents and use the context menu to add the `heading_styles_ and / or `toc_styles` attribute, setting the value to a comma separated list with the name of the styles.

## Future development

- Read the sections from Scribus
