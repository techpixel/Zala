from baseparse import errors
from baseparse.builtins import builtins  #are we lazy? yes we are!
import inspect, itertools, types, copy
from lark import Tree, Token, Lark
import lib #importing builtins. Instead of creating our own functions through our own language, lazily create python functions for import.
#dont use the assigner for now. there are probably better methods to handle this

assingee_types = ['varassign', 'funcassign', 'varcall', 'funccall']

variables = {}
functions = {}


class EmptyInterpreter:  #acts as a empty class, no trickery needed
    pass


def checkvalidkwarg(kwarg, func):
    params = inspect.signature(func).parameters
    if kwarg in params:
        if not params[kwarg].default == inspect.Signature().empty:
            return True
    return False


def cycle(args):
    argslist = []
    for arg in args:
        if not isinstance(args, inspect.Parameter):
            argslist.append(arg)
            continue
        elif arg.default == inspect.Signature().empty:
            argslist.append(arg)
    return argslist


def checkVarPositional(args):
    for arg in args:
        if not isinstance(args, inspect.Parameter):
            continue
        elif arg.kind == inspect.Parameter.VAR_POSITIONAL:
            return True
    return False

class Variable:
    def __init__(self, name):
        self.name = name.value if isinstance(name, Token) else name

    def __str__(self):
        return f'<Placeholder {self.name}>' if not self.name in variables else f'<Assigned Variable {self.name}={variables[self.name]}>'

    def build(self, value):
        variables[self.name] = value

    def delete(name):
        del variables[name]

    def binop_get(left, right):
        if not isinstance(left, int) and not isinstance(left, float):
            if left.name in variables:
                left = variables[left.name]
            elif isinstance(left, Navigator):
                left = left.navigate(EmptyInterpreter, [], lookfunc=False)
            else:
                raise errors.Context("ValueError", "Must use integer or variable")
        if not isinstance(right, int) and not isinstance(right, float):
            if right.name in variables:
                right = variables[right.name]
            elif isinstance(right, Navigator):
                right = right.navigate(EmptyInterpreter, [], lookfunc=False)
            else:
                raise errors.Context("ValueError", "Must use integer or variable")

        return left, right

    def basic_get(item):
        try:
            item.name
        except:
            return item
        else:
            if item.name in variables:
                return variables[item.name]
            elif isinstance(item, Navigator):
                return item.navigate(EmptyInterpreter, [], lookfunc=False)
            elif isinstance(item, Functions):
                return item
            elif isinstance(item, ClassInstance):
                return item
            elif item.name in baseclass:
                return ClassInstance(item.name, baseclass[item.name])
            else: 
                raise errors.Context("LookupError", "No such variable")

#
# Functions
#


class Functions:
    class Arguments:
        def __init__(self, name, value=None, type='definer'):
            self.name = name
            self.value = value
            if self.value is None:
                self.require = False
            else:
                self.require = True
            self.type = type

        def __str__(self):
            return f"<Arg {self.name}>" if self.value is None else f"<Kwarg {self.name}={self.value}>"

    def __init__(self, funcobj, args, tree, addfunc=True):
        self.name = funcobj
        self.args = args
        self.tree = tree
        
        if self.name in builtins:
            raise

        if addfunc:
            functions[self.name] = self

    def __str__(self):
        return f'<func "{self.name}">'

    def call(method, ob, args):
        name = ob.name if isinstance(ob, Variable) else ob
        if name in builtins:  #builtin functions
            func_args = []
            kwargs = {}
            signature = inspect.signature(builtins[name])
            params = signature.parameters
            for arg in args:
                if arg.value is not None:
                    if checkvalidkwarg(arg.name, builtins[name]):
                        kwargs.update({
                            arg.name: Variable.basic_get(arg.value)
                        })
                    else:
                        raise errors.Context(f"Invalid Kwarg {arg.name}")
                else:
                    func_args.append(Variable.basic_get(arg.name))

            if checkVarPositional(params):
                if len(cycle(params)) != len(func_args):
                    raise errors.Context(
                        "FunctionError",
                        "Missing or Extra Arguments for builtin " + name)
            return builtins[name](*func_args, **kwargs)

        elif name in functions:  #userfunctions
            return functions[name].runfunc(method, args)

        elif isinstance(ob, Functions):
            return ob.runfunc(method, args)

        elif isinstance(ob, Navigator):
            return ob.navigate(method, args, lookfunc=True)

        else:
            raise errors.Context("FunctionError", "Function not found or does not exist")

    def runfunc(self, method, args):
        Object = self
        name = self.name

        required = []
        userargs = []

        for arg in Object.args:
            if arg.value is None:
                required.append(arg)
        for arg in args:
            if arg.value is None:
                userargs.append(arg)

        if len(userargs) != len(required):
            raise errors.Context(
                "FunctionError",
                "Missing or Extra Arguments for function " + name)

        for name, obj in itertools.zip_longest(Object.args, args):
            argumentVariable = Variable(name.name)

            if obj is None:
                argumentVariable.build(Variable.basic_get(name.value))
                continue
            elif name.value is not None:
                argumentVariable.build(Variable.basic_get(obj.value))
            elif name.value is None:                
                argumentVariable.build(Variable.basic_get(obj.name))
            else:
                raise errors.Context('FunctionError',
                                     f'Invalid Kwarg {obj.name}')

        result = method().visit(Object.tree)

        for name in Object.args:
            Variable.delete(name.name)

        if result:
          return result[0]
        else:
          return

#
# Classes and Navigators
#

baseclass = {}


class ClassBuilder:
    def build(method, name, tree):
        global baseclass
        generated_dict = method(baseclass).visit(tree) if isinstance(
            tree, Tree) else tree   

        classname = name if isinstance(name, str) else name.name

        if isinstance(generated_dict, list):
          newdict = {classname:{}}
          for item in generated_dict:
            newdict[name].update(item)
          generated_dict = newdict
        else:
          generated_dict = {classname:generated_dict}
        
        baseclass.update(generated_dict)
        #return baseclass

    def import_module(name, method, tokentransformer=None):
        if hasattr(lib, name):
          builtinlib = getattr(lib, name)
          baseclass.update(builtinlib.libclass)
        else:
          try:
            f = open(name + ".zl")
          except:
            raise errors.Context("ImportError", "No module found")
          else:
            parser = Lark.open('zala.lark', rel_to=__file__, parser='lalr', regex=True, propagate_positions=True)
            parsedImport = parser.parse(f.read())

            parsedTokenImport = tokentransformer().transform(parsedImport)

            ClassBuilder.build(method, name, method(baseclass).visit(parsedTokenImport))

#View as Class for PyExtensions and PakratImports
class ClassInstance:
  def __init__(self, name, dictitem):
    self.name = name
    self.dict = copy.deepcopy(dictitem)

  def __str__(self):
    return f"<class \"{self.name}\">"

  def __repr__(self):
    return str(self.dict)

class Navigator:
    def __init__(self, path):
        self.basepath = path if len(path) == 1 else path[0]
        self.parsedpath = [pathname.name for pathname in path]
        self.funcdata = path[-1]  #closest name to last
        self.name = self.funcdata.name

    def __str__(self):
        return f"<Navigator Function {self.name}>"

    def navigate(self, method, args, lookfunc=True):
        global baseclass
        selector = baseclass

        if not self.parsedpath[0] in selector:
          if self.parsedpath[0] in variables:
            varobj = variables[self.parsedpath[0]]
            selector = varobj.dict
            vararg = Functions.Arguments(varobj)
            args.insert(0, vararg)

            del self.parsedpath[0]        
          if isinstance(self.parsedpath[0], ClassInstance):
            varobj = self.parsedpath[0]
            selector = varobj.dict
            vararg = Functions.Arguments(varobj)
            args.insert(0, vararg)

            del self.parsedpath[0]
            
        for path in self.parsedpath:
            if path in selector:
                selectedpath = selector[path]

                if isinstance(selectedpath, types.FunctionType):
                  return pyfunc(args, selectedpath)

                if isinstance(selectedpath, list) and len(selectedpath) == 1:
                  selectedpath = selectedpath[0]

                if isinstance(selectedpath, dict):
                      selector = selectedpath
                        
                elif isinstance(selectedpath, Functions) and lookfunc:
                    return selectedpath.runfunc(method, args)
                elif not lookfunc:
                    return selectedpath
            else:
              raise errors.Context("NavigationError", f"No such item {path}")

        if isinstance(selectedpath, dict):
          return ClassInstance(path, selectedpath)

        raise errors.Context("NavigationError", "Object not found")

#        if not self.parsedpath[0] in selector:
#          if self.parsedpath[0] in variables:
#            selector = variables[self.parsedpath[0]].dict
#            args.insert(0, Functions.Arguments(variables[self.parsedpath[0]]))
#            del self.parsedpath[0]
#          else:
#            raise errors.Context("NavigatonError", "Class does not exist")

    #modify attribute

    def modify(navigator, value):
        self = navigator
        global baseclass
        selector = baseclass
        modifycopy = False

        if not self.parsedpath[0] in selector:
          if self.parsedpath[0] in variables:
            selector = variables[self.parsedpath[0]].dict
            modifycopy = True

        for path in self.parsedpath[:1]:
            if path in selector:
                selectedpath = selector[path]

                if isinstance(selectedpath, dict):
                  selector = selectedpath
                else:
                  raise errors.Context("NavigatonError", "Navigator Stopped Unexpectedly while attempty to modify attribute")  
        
        if modifycopy:
          selector[self.parsedpath[-1]] = value
          variables[self.parsedpath[0]].dict = selector
        else:
          selector[self.parsedpath[-1]] = value


def pyfunc(args, func):
    func_args = []
    kwargs = {}
    signature = inspect.signature(func)
    params = signature.parameters
    for arg in args:
        if arg.value is not None:
            if checkvalidkwarg(arg.name, func):
                kwargs.update({
                            arg.name: Variable.basic_get(arg.value)
                        })
            else:
                raise errors.Context(f"Invalid Kwarg {arg.name}")
        else:
            func_args.append(Variable.basic_get(arg.name))

    if checkVarPositional(params):
        if len(cycle(params)) != len(func_args):
            raise errors.Context(
                        "FunctionError", f"Missing or Extra Arguments for builtin {func.__name__}")
    return func(*func_args, **kwargs)