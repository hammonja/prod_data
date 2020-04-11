import sys
import json
from bom_functions import get_sage_bom
from bom_functions import write_bom_files


print('This program will retrieve a BON from Sage can create / update your local github files')
print('please enter BOM name')

bomName = input()
bom = get_sage_bom(bomName)
if len(bom) >0:
	write_bom_files(get_sage_bom(bomName))	
	print(json.dumps(bom, sort_keys=True, indent=4))
	print(bomName+ ' has been Sucessfully updated')
else:
	print (bomName +' not found ')

print('press any key to close')
input()
					
