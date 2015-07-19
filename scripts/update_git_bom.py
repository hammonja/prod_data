import sys
from bom_functions import get_sage_bom
from bom_functions import write_bom_files

#update selected bom 
if len(sys.argv) > 1 :
	write_bom_files(get_sage_bom(sys.argv[1]))
else:
	print " this program must be run with a single argument = <bom name>"



					
