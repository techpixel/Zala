from functools import wraps
from lark import Tree

# Work with lark's current error handling method while creating our own method to create custom error handling.

# Syntax Errors

class ZalaSyntaxError(SyntaxError):
  def __str__(self):
    context, line, column = self.args
    return '%s at line %s, column %s.\n\n%s' % (self.label, line, column, context)

  # Return a string version of our custom error to print during REPL/File Read mode

  def return_exception(self):
    context, line, column = self.args
    return '%s at line %s, column %s.\n\n%s' % (self.label, line, column, context)

class MissingString(ZalaSyntaxError):
    label = 'Missing String Character' 
class MissingSemicolon(ZalaSyntaxError):
    label = 'Missing Semicolon' 
class UnexpectedSemicolon(ZalaSyntaxError):
    label = 'Unexpected Semicolon' 
class MissingOpeningBracket(ZalaSyntaxError):
    label = 'Missing Opening Bracket' 
class MissingClosedBracket(ZalaSyntaxError):
    label = 'Missing Closed Bracket' 
class MissingClosedBracketScan2(ZalaSyntaxError):
    label = 'Missing Closed Bracket' 
class MissingSemicolonScan2(ZalaSyntaxError):
    label = 'Missing Semicolon' 
class UnexpectedOpeningBracket(ZalaSyntaxError):
		label = "Unexpected Opening Bracket"
class UnexpectedClosingBracket(ZalaSyntaxError):
		label = "Unexpected Closing Bracket"

errors = { #match errors on current example errors.
        MissingString : [
          '"a;',
          'a";'
        ],
        UnexpectedSemicolon : [
          ';',
          '1 + 1;;'
        ],
        MissingSemicolon : [
          '( 1 + 1 )',
          '( 1 + 1 ) * 2',
          '( 1 + 1 ) + 2'
        ],
        MissingClosedBracketScan2 : [
          '( 1 + 1',
        ],
        MissingSemicolonScan2 : [
          '1 + 1',
        ],
        MissingClosedBracket : [
          '( 1 + 1 ;',
        ],
        MissingOpeningBracket : [
          '1 + 1 )'
        ],
				UnexpectedOpeningBracket : [
					'(',
					'(( 1 + 1)',
				],
				UnexpectedClosingBracket : [
					')',
					'( 1 + 1))',
				]
      }

# Transformer & Interpreter Errors

plaintext = None

class Context(Exception):
  def __init__(self, name, error, *args):
    self.name = name
    self.error = error
    self.args = args

class ContextError(Exception):
  def __init__(self, errorcontext, name, error, *args):
    self.name = name
    self.error = error
    self.message = name + ": " + error
    self.args = args

    context = errorcontext.meta

    self.start = context.start_pos
    self.end = context.end_pos
    self.line = context.line
    self.col = context.column

    self.traceback = None #placeholder for future traceback implementation

  def builderror(self, plaintext):
    errorline = self.line
    line = plaintext.split('\n')[errorline - 1]

    start = self.start
    end = self.end

    arrows = " "*(len(line) - len(line[start:])) + "^"*(len(line[start:end])) + " "*(len(line[:end]))

    return f'{self.message}, in line {errorline}, column {self.col}\n\n{line}\n{arrows}\n'


def handletree(func):
    @wraps(func)
    def inner(cls, tree):
        values = []
        for child in tree.children:
          try:
            value = cls.visit(child) if isinstance(child, Tree) else child
          except Context as c:
            raise ContextError(child, c.name, c.error)
          values.append(value)
        return func(cls, values)
    return inner