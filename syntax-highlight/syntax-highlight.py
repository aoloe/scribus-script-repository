import sys
from pygments import highlight
from pygments.util import ClassNotFound as pygments_classNotFound

try: 
    import scribus
except ImportError: 
    # if you want to use the mock instead of Scribus, copy in here the mockAPI from
    # the script repository
    import mockAPI
    scribus = mockAPI.Scribus()

from pygments.formatter import Formatter
from pygments.token import Token
# from pygments.token import Token, Text, STANDARD_TYPES


class ScribusFormatter(Formatter):
    # TODO: we could give the user a way to change this... or not?
    base_char_style = 'Code'
    def __init__(self, code_length, **options):
        Formatter.__init__(self, **options)
        # css classes are "defined" in https://github.com/dagwieers/pygments/blob/d4425131d42a69651d27260e45bdfd68f29f06ad/pygments/token.py#L124
        # TODO: we can use this to create a list of styles, intialize them to the values in style and create them in scribus on first actual usage
        self.code_length = code_length
        print(self.code_length)
        self.character_styles = {
            Token.Text: self.base_char_style,
            Token.Keyword: self.base_char_style+'_keyword',
            Token.Punctuation: self.base_char_style+'_punctuation',
            Token.Literal.String.Double: self.base_char_style+'_literal',
            Token.Literal.String.Single: self.base_char_style+'_literal',

            Token.Name: self.base_char_style,
            Token.Operator: self.base_char_style+'_operator',
            Token.Operator.Word: self.base_char_style+'_keyword',
            Token.Name.Builtin: self.base_char_style+'_stdlib',
            Token.Literal.Number.Integer: self.base_char_style+'_literal',
        }
        self.existing_styles = scribus.getCharStyles()
        if self.base_char_style not in self.existing_styles:
            scribus.createCharStyle(self.base_char_style)
        # for token, style in self.style:
        #    pass

    def format(self, tokensource, outfile):
        current_frame = scribus.getSelectedObject()
        # TODO: also support formatting a selection as soon as the API has getTextSelection -> (start, length)
        # resete the character styles
        scribus.setCharacterStyle(self.base_char_style)

        pos = 0
        last_val = ''
        last_type = None
        for token_type, token_value in tokensource:
            print(token_type)
            print(token_value)
            token_length = len(token_value)
            # scribus does not have a \n after the last character,
            # the code has it
            if pos + token_length > self.code_length:
                token_length -= 1
            # print(pos)
            # print(token_length)
            scribus.selectText(pos, token_length, current_frame)
            pos += token_length
            style_name = self.get_char_style(token_type)
            scribus.setCharacterStyle(style_name, current_frame)

    def get_char_style(self, token_type):
        style_name = self.character_styles.get(token_type, self.base_char_style)
        print(self.existing_styles)
        if style_name not in self.existing_styles:
            color = self.style.style_for_token(token_type).get('color')
            self.existing_styles.append(style_name)
            arguments = {}
            if color:
                scribus.defineColorRGB(style_name,
                    *[int(color[i:i+2], 16) for i in range(0, 6, 2)]);
                arguments['fillcolor'] = style_name
            # TODO: add other style elements (underline, italic, bold)
            # (bold and italic won't be easy)
            # TODO: add the parent_style to the API
            scribus.createCharStyle(style_name, **arguments)

        return style_name

# TODO: read the text from the frame

print('=====')

code = scribus.getAllText()

# TODO: read the item's attributes
attribute = ''
for a in scribus.getObjectAttributes():
    if a['Name'] == 'syntax-highlight':
        attribute = a['Value']

print('>>>> '+attribute)

if attribute != '':
    try:
        from pygments.lexers import get_lexer_by_name
        lexer = get_lexer_by_name(attribute)
    except pygments_classNotFound:
        pass
else:
    from pygments.lexers import guess_lexer
    try:
        lexer = guess_lexer(code)
    except pygments_classNotFound:
        pass

if not lexer:
    sys.exit()

# TODO: do nothing is the lexer is 'text' (guess_lexer did not find anything better)
# print(lexer)

# code = scribus.getAllText().decode('utf-8')
highlight(code, lexer, ScribusFormatter(len(code)))
