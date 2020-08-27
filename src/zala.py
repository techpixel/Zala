import baseparse
import argparse, os
import repl

#argparse

argparser = argparse.ArgumentParser(description='Run the Zala Program')

argparser.add_argument("-f", "--file", action="store", help="run the file")
argparser.add_argument("-r", "--repl", action="store_true", help="enter REPL mode")

args = argparser.parse_args()
      
if args.file: #read file
  try:
    with open(args.file, 'r') as f:
      code = f.read()
  except OSError as e:
    argparser.exit(status=1, message="cant open file '%s': %s\n" % (args.file, e))
elif args.repl: #init repl mode
  try:
    os.system('clear')
    print('Zala 0.1 release')
    while True:
      repl.repl()
  except (KeyboardInterrupt, EOFError):
      os.system('clear')
      argparser.exit(status=0, message="Left REPL mode.\n")
else:
  argparser.exit(status=1, message="no options set\n")

def main(name, code):
  fileParse = baseparse.parser.Parser(code, name=name)
  fileParse.parse()


if __name__ == '__main__':
  main(args.file.split('.')[0], code)