import requests

def getmethod(name, url):
  request = requests.get(url)
  return {
    "content":request.content,
    "status":request.status_code,
    "text":request.text
  }

def postmethod(name, url, data=None, json=None):
  request = requests.post(url, data=None, json=None)
  return {
    "content":request.content,
    "status":request.status_code,
    "text":request.text
  }

def delmethod(name, url, data=None, json=None):
  request = requests.delete(url, data=None, json=None)
  return {
    "content":request.content,
    "status":request.status_code,
    "text":request.text
  }

libclass = {
  "request":{
    "get":getmethod,
    "post":postmethod
  }
}