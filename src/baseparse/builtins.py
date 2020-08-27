# Types Conversion

def intf(value, base=None):
  if base:
    return int(value, base=base)
  return int(value)
  
def strf(value):
  return str(value)

def floatf(value):
  return float(value)

# Basic I/O

def printf(*args, end='\n'):
  return print(*args, end=end)

def inputf(prompt):
  return input(prompt)

def password(prompt):
  import getpass
  return getpass.getpass(prompt)

def clear():
  import os
  os.system('clear')

# Subshell

def subshell(value):
  import os
  os.system(value)

def rangef(start, stop):
  return range(start, stop)

builtins = {
  'int':intf,
  'str':strf,
  'float':floatf,
  'print':printf,
  'input':inputf,
  'password':password,
  'clear':clear,
  'subshell':subshell,
  'range':rangef
}