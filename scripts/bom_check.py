import json
import os
from bom_functions import get_sage_boms
import requests
import certifi
import urllib3
from datetime import datetime

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
now = datetime.now()
print (now.strftime("%d/%m/%Y %H:%M:%S")+' :-------------START-----------')
path = 'c:/git/prod_data/BOMS'	

def get_git_boms():
	boms = {}		
	for bom in os.listdir(path):		
		with open(path+'/'+str(bom)+'/'+str(bom)+'.json', encoding='utf8' ) as json_data:			
			boms[bom] = json.load(json_data)	
	return boms

def get_unequal_boms():
	unequal_boms = []
	for bom in sage_boms:
		if bom in git_boms.keys():
			if sage_boms[bom] != git_boms[bom]:								
				unequal_boms.append(bom)
	return unequal_boms

def update_git_bom(bom):
	for fname in os.listdir(path+'/'+bom):
		r = http.request('GET','https://raw.githubusercontent.com/hammonja/prod_data/master/BOMS/'+bom+'/'+fname )
		with open(path+'/'+bom+'/'+fname, 'w') as out:							
			out.write(r.data.decode())		
	return
	
# get current boms from sage'
sage_boms = get_sage_boms()


# get all boms from local machine'
git_boms = get_git_boms()

# compare boms'
mis_match_boms = get_unequal_boms()

# check if there is a mis-match'
if len(mis_match_boms) >0 :
	
	# update boms from git that are not equal'
	for bom in mis_match_boms:
		update_git_bom(bom)
			
	# get all boms from git
	git_boms = get_git_boms()

	# compare boms	
	mis_match_boms = get_unequal_boms()
	if len(mis_match_boms) >0 :	
		# still unequal then send an email
		email = {"from": "accounts@bentham.co.uk","to": "jameshammond@bentham.co.uk","subject": "BOM CHECKER", "replyTo ": "jameshammond@bentham.co.uk"}
		html = ' '
		for bom in mis_match_boms:			
			html = html + 'The following BOM is out of sync with github : ' +bom + '<br>'			
			print( 'The following BOM is out of sync with github : ' +bom)		
		email['html'] =  html
		print(requests.post('http://10.0.0.75:3000/email', json = email).text)			
else:	
	print( 'Sage and Git agree')		