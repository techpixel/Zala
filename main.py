#
#
# LNVHSJHAUYABVISJVAVAL
# PARHKSJDKHAJKSSABBDA     
# DHASJSHDUXBSIAHIUCV   
#           AJDHJDHD    
#          ASJDDSKA     
#         VHJKYWTS      
#        SNCGSVBA       
#       SDBAEARZ        
#      ASDAHKHV         
#     TSDHKJHD          
#    RHYXHANF           
#   SSHGCUASJFSAHISSA   
#  AKUSBAIELAJSIDJEAV   
# BAUSHUWTABVKSHUACKE   
#
#
# Thank you for having the time to look at our project. We have
# worked so hard on this and we hope you enjoy using it as much
# as we do.
#
# For the Best Experience, Make your terminal window full screen
#
# Help With Shell:
#
# Press Ctrl + Shift + S to open the shell
#
# Run tests with "python src/zala.py -f tests/example.zl"
# Open the built-in interpreter/REPL mode with:
# "python src/zala.py -r"
#
# There are multiple repls associated with Zala.
#

import os, getch, time

start = time.time()

os.system('python src/zala.py -f example.zl')

print("--- %s seconds ---" % (time.time() - start))

while 1: pass

os.system('python src/zala.py -r')