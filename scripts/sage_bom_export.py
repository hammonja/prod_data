import json
from bom_functions import get_sage_boms
from bom_functions import write_bom_files

# installation script , this will write all the boms
# to disc
write_bom_files(get_sage_boms())
					
