import json

def jsonparse(jsonstr):
  return json.loads(jsonstr)

def jsonbuild(jsonstr):
  return json.dumps(jsonstr)

libclass = {
  "jsonlib":{
    "jsonparse":jsonparse,
    "jsonbuild":jsonbuild
  }
}