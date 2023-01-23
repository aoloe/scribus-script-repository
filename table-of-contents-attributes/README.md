# Table of contents

Generate the attributes for the table of contents by looking at the styles used in the document.

At the time of writing, Scribus can only create single level table of contents.  
[Multilevel Table of Content support](https://bugs.scribus.net/view.php?id=16887) contains a patch for producing multilevel table of contents: you probably need to really

## The paragraph styles

By default, the script looks for the styles "h1", "h2", and "h3".

```py
heading_styles = ['h1', 'h2', 'h3']
```

Also, by default, the script applies the styles "toc1", "toc2", and "toc3".

```py
toc_styles = ['toc1', 'toc2', 'toc3']
```

If you want to track style of different names (or add more styles), simply modify the _styles_ variables.


## Initialize the table of contents

- Create a text frame with the name "Table of Contents" (using the properties palette).
- Create the paragraph styles "h1", "h2", "h3" (or the styles with the names you are using in `headings`.
- In the "Document Item Attributes" section of the "Document Setup", create an attribute with the following values

  - "Name": "Table of Contents"
  - "Type": String

- In the "Table of Contents" section of "Document Setup", add a table of contents with the following values
  - Item Attribute: choose the "Table of Contents" attribute you have created above.
  - Destination Frame: choose the frame called "Table of Contents"
  - Paragraph Style: choose the TOC style you want to see applied in the table of contents.

## Updating the table of contents

- Create your content, using "h1", "h2", and "h3" styles for the headings. (Take care to put only one heading in each frame.)
- Run the `table-of-contents.py` script.
- Run _Extras > Generate Table of Contents_
