from flask import Flask, render_template, url_for, abort
from baseparse import errors, transformer

currentapp = None
connections = {}
classitems = {}
weberrors = {}

def app(module="flaskapp"):
  global currentapp
  currentapp = Flask(module)

def connect(func, route):
  global connections
  connections[func.name] = route

def errorhandler(func, status):
  global connections
  connections[status] = func 

def setup(userclass):
  global connections

  if not hasattr(userclass, "dict"):
    raise errors.Context("FlaskSetupError", "Must use class")
  if len(connections) == 0:
    raise errors.Context("FlaskSetupError", "No connections setup")
  if app is None:
    raise errors.Context("FlaskSetupError", "Please setup app first")

  global classitems
  classitems = userclass.dict

  if classitems.keys() != connections.keys():
    raise errors.Context("FlaskSetupError", "Class Defentions dont match route connections")
  for key in classitems:
    route = connections[key]
    exec(f"""
@currentapp.route("{route}")
def {key}():
  global classitems
  return classitems["{key}"].runfunc(transformer.DefInterpreter, [])  
    """)
  
  global weberrors
  for status in weberrors:
    exec(f"""
@currentapp.errorhandler("{status}")
def {weberrors[status].name}(e):
  global weberrors
  return weberrors["{status}"].runfunc(transformer.DefInterpreter, [e])  
    """)

def start(host="0.0.0.0", port=8080):
  currentapp.run(host=host, port=port)
  
libclass = {
  "flasklib":{
    "app":app,
    "connect":connect,
    "setup":setup,
    "start":start,
    "abort":abort,
    "render_template":render_template,
    "url_for":url_for
  }
}