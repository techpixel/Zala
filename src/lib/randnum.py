import random

charlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

def randint(a, b):
  return random.randrange(a, b)

def randchar():
  global charlist
  return random.choice(charlist)

libclass = {
  "random":{
    "randint":randint,
    "randchar":randchar
  }
}