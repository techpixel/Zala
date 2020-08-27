from baseparse import parser
import os

# Create a mini REPL interpreter


def repl():
    code = input('\033[33m \033[0m')
    replParser = parser.Parser(code)
    parsedCode = replParser.parse()
    if not parsedCode is None: 
      for result in parsedCode:
          print(result)
