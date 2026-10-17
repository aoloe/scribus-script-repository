# Join lines

Sometimes, when you copy text from an external source, after each _printed_ line theres is a new line.

This scripts joins the lines inside of a paragraph:

- In the current selection or current frame.
- A paragraph is marked by a double new line.
- All the formatting will be reset.
- Dashes at the end are removed (except if there are two of them, then they are replaced by one single dash.
- At the time of writing, the result cannot be (correctly) undone.
