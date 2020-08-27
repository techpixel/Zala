from lark import Token, Tree
from lark.visitors import Transformer, Interpreter, Visitor
from baseparse import assigner, errors
from baseparse.errors import handletree

#Transform Tokens

def true(*item):
  return True

def false(*item):
  return False

def void(*item):  return None

def classnavigator(*items):
  print(items)

class TransformTokens(Transformer):
    NUMBER = int
    FLOAT = float
    WORD = assigner.Variable
    navigator = assigner.Navigator
    classnav = classnavigator
    VOID = void
    TRUE = true
    FALSE = false

    def ESCAPED_STRING(self, token):
        return str(token)[1:-1].replace('\\"', '"').replace("\\'", "'")

#Index Handler

class Indexer:
  def __init__(self, indexes):
    self.indexes = indexes
  
  def index(self, item):
    currentobj = item
    for index in self.indexes:
      try:
        currentobj = currentobj[index]
      except IndexError:
        raise errors.Context("IndexError", "List index out of range")
      except TypeError:
        raise errors.Context("TypeError", "Type not supported")
    return currentobj

  def key(self, item):
    currentobj = item
    for index in self.indexes:
      try:
        currentobj = currentobj[index]
      except KeyError:
        raise errors.Context("KeyError", "Invalid Key")
    return currentobj
#Interpreter


class BaseInterpreter(Interpreter):
    # Begin Interpreter

    def __init__(self, specialmethod=None):
      self.specialmethod = BaseInterpreter if not specialmethod else specialmethod

    # Bin Ops

    @handletree
    def add(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        return left + right

    @handletree
    def sub(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        return left - right

    @handletree
    def mul(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        return left * right

    @handletree
    def div(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        if right == 0:
            raise errors.Context('ZeroDivision', 'Cannot Divide by Zero')
        return left / right

    @handletree
    def neg(self, args):
        value = assigner.Variable.binop_get(args[0], 0)
        return -value[0]

    # RelExpr
    # Notes: In technicality BinOp should also support relexpr (excluding eq), so please ignore binop

    @handletree
    def gt(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        return left > right

    @handletree
    def ge(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        return left >= right

    @handletree
    def lt(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        return left < right

    @handletree
    def le(self, args):
        left, right = assigner.Variable.binop_get(args[0], args[1])
        return left <= right

    @handletree
    def eq(self, args):
        left = assigner.Variable.basic_get(args[0])
        right = assigner.Variable.basic_get(args[1])
        return left == right

    @handletree
    def neq(self, args):
        left = assigner.Variable.basic_get(args[0])
        right = assigner.Variable.basic_get(args[1])
        return left != right

    # LogiExpr

    def logi_and(self, args):
        left = assigner.Variable.basic_get(args[0])
        right = assigner.Variable.basic_get(args[1])
        return left and right

    def logi_or(self, args):
        left = assigner.Variable.basic_get(args[0])
        right = assigner.Variable.basic_get(args[1])
        return left or right

    def logi_not(self, args):
        item = assigner.Variable.basic_get(args[0])
        return not item

    # If Statement

    def iffunc(self, tree):
      args = tree.children
      relexpr = BaseInterpreter().visit(args[0])
      relexpr = assigner.Variable.basic_get(relexpr)

      if relexpr:
        return self.specialmethod().visit(args[1])
      elif args[-1].data == 'elsefunc':
        return self.specialmethod().visit(args[-1])
    
    @handletree
    def elsefunc(self, args):
      return args

    # Variables

    @handletree
    def var_assign(self, args):
        if isinstance(args[0], assigner.Navigator):
          assigner.Navigator.modify(args[0], assigner.Variable.basic_get(args[1]))
        else:
          assigner.Variable.build(args[0],
                                assigner.Variable.basic_get(args[1]))
    
    # Functions

    def def_block(self, tree): #we need the tree as is, no eval
      return tree

    @handletree
    def params(self, args):
      return args
    
    defparams = params

    @handletree
    def defkwarg(self, args):
      return assigner.Functions.Arguments(args[0].name, 
                                          value=assigner.Variable.basic_get(args[1]))

    def defarg(self, tree):
      return assigner.Functions.Arguments(tree.children[0].name)

    @handletree
    def kwarg(self, args):
      return assigner.Functions.Arguments(args[0].name, 
                                          value=assigner.Variable.basic_get(args[1]),
                                          type='caller')

    @handletree
    def arg(self, args):
      return assigner.Functions.Arguments(assigner.Variable.basic_get(args[0]),
                                          type='caller')

    @handletree
    def func_def(self, args):
      assigner.Functions(args[0].name, args[1], args[2])

    @handletree
    def func(self, args):
      if args[0].name in assigner.baseclass:
        return assigner.ClassInstance(args[0].name, assigner.baseclass[args[0].name])
      return assigner.Functions.call(DefInterpreter, args[0], args[1])

    @handletree
    def class_def(self, args):
      assigner.ClassBuilder.build(ClassInterpreter, args[0], args[1])
    
    def class_block(self, tree):
      return tree

    # Value

    @handletree
    def value(self, args):
      item = assigner.Variable.basic_get(args[0])
      if isinstance(args[-1], Indexer):
        if isinstance(item, list):
          indexer = args.pop(-1)
          indexedlist = indexer.index(item)
          return assigner.Variable.basic_get(indexedlist)
        if isinstance(item, dict):
          indexer = args.pop(-1)
          dictvalue = indexer.key(item)  
          return assigner.Variable.basic_get(dictvalue)
        if isinstance(item, str):
          indexer = args.pop(-1)
          indexes = indexer.indexes
          
          if len(indexes) > 1:
            raise errors.Context("IndexError","String Supports Single Index Only")

          strvalue = item[indexes[0]]
          return strvalue
        else:
          raise errors.Context("TypeError", "Type does not support index.")
      return item

    relvalue = value

    @handletree
    def listrule(self, args):
      return args

    @handletree
    def indexers(self, args):
      if len(args) == 0:
        return
      else:
        return Indexer(assigner.Variable.basic_get(args))

    @handletree
    def dictionary(self, args):
      keys = args[::2]
      values = args[1::2]
      if len(keys) != len(values):
        raise errors.Context("ValueError", "Dict does not match up with key")
      
      userdict = dict(zip(keys, values))
      return userdict

    # Loops

    def basicloop(self, tree):
      args = tree.children
      loopAmount = args[0]
      loopTree = args[1]

      for x in range(loopAmount):
        try:
          LoopInterpreter(specialmethod=LoopInterpreter).visit(loopTree)
        except StopLoop:
          break

    def iteratorloop(self, tree):
      args = tree.children
      iterator = BaseInterpreter().visit(args[0]) if isinstance(args[0], Tree) else assigner.Variable.basic_get(args[0])
      variables = args[1]
      loopTree = args[2]

      try:
        iter(iterator)
      except TypeError:
        raise errors.ContextError(tree, "TypeError", "Cannot use this object type as iterator")
      else:
        for item in iterator:
          variables.build(item)
          try:
            LoopInterpreter(specialmethod=LoopInterpreter).visit(loopTree)
          except StopLoop:
            break

    def relexprloop(self, tree):
      args = tree.children
      loopTree = args[1]

      while True:
        relexpr = BaseInterpreter().visit(args[0]) if isinstance(args[0], Tree) else assigner.Variable.basic_get(args[0])
        if relexpr:
          try:
            LoopInterpreter(specialmethod=LoopInterpreter).visit(loopTree)
          except StopLoop:
            break
        else:
          break

    # Misc

    @handletree
    def start(self, args):
      for arg in args:
        if not arg == None:
          yield arg

    # Imports

    def importfunc(self, tree):
      assigner.ClassBuilder.import_module(tree.children[0].name, ClassInterpreter, tokentransformer=TransformTokens)

returns = 0

class DefInterpreter(BaseInterpreter):

  def def_block(self, tree):
    for child in tree.children:
      try:
        value = DefInterpreter().visit_children(child)
      except errors.Context as e:
        raise errors.ContextError(child, e.name, e.error)

      global returns
      if returns == 1:
        returns = 0
        return value[0][0]
    
    return
  
  def def_block_items(self, tree):
    return tree

  @handletree
  def returner(self, args):
    global returns
    returns += 1
    return args

  def iffuncdef(self, tree):
    args = tree.children
    relexpr = BaseInterpreter().visit(args[0])
    relexpr = assigner.Variable.basic_get(relexpr)

    if relexpr:
      return DefInterpreter().visit(args[1])
    elif args[-1].data == 'elsefuncdef':
      return DefInterpreter().visit(args[-1])
    
  @handletree
  def elsefuncdef(self, args):
    return args

class ClassInterpreter(BaseInterpreter):
    def __init__(self, baseclass):
      self.baseclass = baseclass

    @handletree
    def func_def(self, args):
      return {args[0].name:assigner.Functions(args[0].name, args[1], args[2], addfunc=False)}

    @handletree
    def class_def(self, args):
      name = args[0].name

      userclass = {name:{}}

      for arg in args:
        if isinstance(arg, list):
          for item in arg:
            userclass[name].update({item.name:item})
        if isinstance(arg, dict):
          userclass[name].update(arg)

      return userclass
    
    @handletree
    def var_assign(self, args):
      return {args[0].name:args[1]}

    @handletree
    def class_block(self, args):
      updatecurrent = {}

      for arg in args:
        updatecurrent.update(arg)

      return updatecurrent
    
    @handletree
    def class_block_items(self, args):
      return args[0][0]

    @handletree
    def start(self, args):
      return args

class StopLoop(Exception):
  pass

class LoopInterpreter(BaseInterpreter):
  @handletree
  def loop_block_items(self, args):
    return args
  
  @handletree
  def loop_block_item(self, args):
    return args

  def breaker(self, tree):
    raise StopLoop

  def iffuncloop(self, tree):
    args = tree.children
    relexpr = BaseInterpreter().visit(args[0])
    relexpr = assigner.Variable.basic_get(relexpr)

    if relexpr:
      return LoopInterpreter().visit(args[1])
    elif args[-1].data == 'elsefuncloop':
      return LoopInterpreter().visit(args[-1])
      
  @handletree
  def elsefuncloop(self, args):
    return args
