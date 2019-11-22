# Syntax highlighter

Highlight the code in a frame.

## Install

Before running the script, you need to install the Python 2 version of [Pygments](http://pygments.org/).

You can install it with your package manager (in my case it did not pull in any dependency) or with Pip.

Using virtual environment will probably not work (well), since you will need to run Scribus after having activated it.

## Usage

Select the text frame with the code to be highlighted and run the script.

If Pygments cannot guess the language, create an item attribute (context menu > Attributes...) with named `syntax-highlight` with the language name as its value (see the [Pygment's languages list](http://pygments.org/docs/lexers/)).

## Notes

### The basic tokens to get started

Here is how a simple code is parsed into tokens:


```py
print("Hello World")
```

- Token.Keyword: print
- Token.Punctuation: () :
- Token.Literal.String.Double: " stringcontent
- Token.Text: space

```py
for i in range(3):
    print('Hello World')
```

- Token.Operator.Word: in
- Token.Name.Builtin: for
- Token.Literal.Number.Integer: 3

### Patches

There is a not yet merge patch that is useful: it creates a new style with a sane font size.

```
diff --git a/scribus/plugins/scriptplugin/cmdstyle.cpp b/scribus/plugins/scriptplugin/cmdstyle.cpp
index 723435ee7..47561fcfa 100644
--- a/scribus/plugins/scriptplugin/cmdstyle.cpp
+++ b/scribus/plugins/scriptplugin/cmdstyle.cpp
@@ -116,8 +116,11 @@ PyObject *scribus_createcharstyle(PyObject* /* self */, PyObject* args, PyObject
 		const_cast<char*>("tracking"),
 		const_cast<char*>("language"),
 		nullptr};
+
+	const auto defaultStyle = ScCore->primaryMainWindow()->doc->charStyles().getDefault();
+
 	char *Name = const_cast<char*>(""), *Font = const_cast<char*>(""), *Features = const_cast<char*>("inherit"), *FillColor = const_cast<char*>("Black"), *FontFeatures = const_cast<char*>(""), *StrokeColor = const_cast<char*>("Black"), *Language = const_cast<char*>("");
-	double FontSize = 200, FillShade = 1, StrokeShade = 1, ScaleH = 1, ScaleV = 1, BaselineOffset = 0, ShadowXOffset = 0, ShadowYOffset = 0, OutlineWidth = 0, UnderlineOffset = 0, UnderlineWidth = 0, StrikethruOffset = 0, StrikethruWidth = 0, Tracking = 0;
+	double FontSize = defaultStyle->fontSize() / 10, FillShade = 1, StrokeShade = 1, ScaleH = 1, ScaleV = 1, BaselineOffset = 0, ShadowXOffset = 0, ShadowYOffset = 0, OutlineWidth = 0, UnderlineOffset = 0, UnderlineWidth = 0, StrikethruOffset = 0, StrikethruWidth = 0, Tracking = 0;
 	if (!PyArg_ParseTupleAndKeywords(args, keywords, "es|esdesesdesddddddddddddes", keywordargs,
 																									"utf-8", &Name, "utf-8", &Font, &FontSize, "utf-8", &Features,
 																									"utf-8", &FillColor, &FillShade, "utf-8", &StrokeColor, &StrokeShade, &BaselineOffset, &ShadowXOffset,
```

## Todo

- [x] Actually read the content of the frame
- [x] Optionally read the language from the item attributes
- [x] Make sure that the characte styles are reset before setting the new ones.
- [ ] Make sure that a text frame is selected.
- [ ] Allow highlighting a text selection.
  - Probably needs a new scripter API command.
- [x] Make sure that the character style `Code` is defined
- [x] Create the colors used by the highlither
  - Their names should be prefixed with `Code_`
- [ ] Create the character styles used for the specific code snippet
  - [ ] Create the styles with the default formatting defined by Pygments
	- [x] color
	- [ ] underline
	- [ ] bold
	- [ ] italic
  - [ ] Base the new styles on the `Code` style (needs a patch for `createCharStyle()`).
	- needs a patch for the `createCharStyle()` API command.
- [ ] Complete the matching between token types and styles
  - We don't want one style for each possible token type. Which types do we need?
- [ ] if no attribute is set, the scripter should ask for a language and set it... the auto detection does not work.
- [ ] any way to create this as a c++ plugin?
  - https://doc.qt.io/qt-5/qtwidgets-richtext-syntaxhighlighter-example.html
	- but, then, i will probably have to recreate the lexers
