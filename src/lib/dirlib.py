import os

def getdir():
  return os.getcwd()

def env():
  return dict(os.environ.items())

def getenv(name, default=None):
  return os.getenv(name)

def read(name):
  try:
    with open(name, 'r') as f:
      return f.read()
  except FileNotFoundError:
      return None

def write(name, text):
  with open(name, 'w') as f:
    f.write(text)

def append(name, text):
  with open(name, 'a') as f:
    f.write(text)

libclass = {
  "dirlib":{
    "getdir":getdir,
    'getenv':getenv,
    'read':read,
    'write':write,
    'append':append
  }
}