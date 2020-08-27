import requests
from baseparse import errors, transformer, assigner, parser

def import_online(name):
  pkgobj = requests.get(f"https://pakrat.teamzala.repl.co/scrp/{name}")
  if pkgobj.status_code == 404:
    raise errors.Context("PakratPackagerError", "The requested package was not found.")

  pkg = pkgobj.content.decode('utf-8').replace("<br>", "\n")
  pkg = parser.parser.parse(pkg)

  pkgParsedTokens = transformer.TransformTokens().transform(pkg)
  assigner.ClassBuilder.build(transformer.ClassInterpreter, name, pkgParsedTokens)


libclass = {
  "pakrat":{
    "import":import_online
  }
}