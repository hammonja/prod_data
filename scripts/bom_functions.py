import pyodbc
import json
import os

def __query_db(query):

	cnxn = pyodbc.connect('DSN=L50M_sagel50_44432;;UID=JamesSQL;PWD=vxBFp6=NL6cm')
	cursor = cnxn.cursor()

	boms = {}

	cursor.execute(query)
	rows = cursor.fetchall()
	for row in rows:
		part = { "stockcode" : row.stockcode, "description" : row.description, "quantity" : str(row.quantity), "location" : row.location}
		try: 
			if row.bomreference not in boms.keys():		
				boms[row.bomreference] = []

			boms[row.bomreference].append (part)					
		except:
			print (' Unable to process ' + str(row))
	return boms

def get_sage_boms():

	query = ' '.join((  
	    "SELECT bomreference ,bomcomponents.stockcode ,bomcomponents.description ,quantity ,location ",
	    "FROM bomheaders , bomcomponents ",
	    "WHERE ",
	    "bomheaders.id = bomcomponents.headerid ", 
	    "order "
	    "by bomreference"
	))
	return __query_db(query)

def get_sage_bom(bom_name):

	query = ' '.join((  
	    "SELECT bomreference ,bomcomponents.stockcode ,bomcomponents.description ,quantity ,location ",
	    "FROM bomheaders , bomcomponents ",
	    "WHERE ",
	    "bomheaders.id = bomcomponents.headerid and ",
	    "bomreference = '"+bom_name+"' ", 
	    "order "
	    "by bomreference"
	))
	return __query_db(query)


	
def write_bom_files(boms): 
	for bom in boms:
		path = "c:/git/prod_data/BOMS/"+str(bom)+"/"
		if not os.path.exists(path):			
			os.makedirs(path)		

		#create json file 
		with open(path+bom+".json", 'wb') as outfile:	
			outfile.write(json.dumps(boms[bom], sort_keys=True, indent=4, separators=(',', ': ')))

		#create readme.md file 		
		with open(path+"readme.md", 'wb') as outfile:	
			outfile.write("|stockcode|description|quantity|location|\n")
			outfile.write("|---------|-----------|--------|--------|\n")
			for item in boms[str(bom)]:				
				outfile.write("|"+item['stockcode'].encode("UTF-8")+\
						"|"+item['description'].encode("UTF-8")+\
						"|"+item['quantity'].encode("UTF-8")+\
						"|"+item['location'].encode("UTF-8")+"|\n")

		#create sage import file 
		#ORM400_BRD_477,02013,100R MRS25,,1,1,R27,Each,,,, 
		seq = 0
		with open(path+bom+".bom", 'wb') as outfile:	
			for item in boms[str(bom)]:							
				outfile.write(bom.encode("UTF-8")+","+item['stockcode'].encode("UTF-8")+\
						","+item['description'].encode("UTF-8")+\
						",,"+str(seq).encode("UTF-8")+\
						","+item['quantity'].encode("UTF-8")+\
						","+item['location'].encode("UTF-8")+",,,,\n")
				seq = seq + 1

	return