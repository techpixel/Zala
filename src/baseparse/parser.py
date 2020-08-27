from lark import Lark, UnexpectedInput
from baseparse import transformer, errors

#
# File to hold lark's parse-related things
# Also includes full parser with transformer
#

parser = Lark.open('zala.lark', rel_to=__file__, parser='lalr', regex=True, propagate_positions=True) #lark parser

class Parser:
  def __init__(self, code, name=None):
    self.code = code

  def parse(self):
    global parser
    code = self.code

    # First, parse the code
    try:
      parsedCode = parser.parse(code)
    except UnexpectedInput as u: #handle lark errors as custom 
      exc_class = u.match_examples(parser.parse, errors.errors)
      if not exc_class:
        print(u)
      else:
        print(exc_class(u.get_context(code), u.line, u.column).return_exception())
        return
    else:
      parsedTokensCode = transformer.TransformTokens(visit_tokens=True).transform(parsedCode)
      try:
        result = transformer.BaseInterpreter().visit(parsedTokensCode)
      except errors.ContextError as e:
        print(e.builderror(code))
        return
      except errors.Context as e:
        print("UnexpectedOperation")
        print(e.name + ": " + e.error)
      else:
        return result