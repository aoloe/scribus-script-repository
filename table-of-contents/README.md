# Table of contents

Generate the table of contents in the current frame by looking at the styles used in the document.

## The paragraph styles

By default, the script looks for the styles "h1", "h2", and "h3".

```py
headings = ['h1', 'h2', 'h3']
```

If you want to track style of different names (or add more styles), simply modify the `headings` variable.

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

## Future development

In the future we might want to create a new non printable layer with one copy of each frame for each occurrences of a heading: in this way we could detect multiple headings per text frame.
