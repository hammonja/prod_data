import json
import os
#import requests
from bom_functions import get_sage_boms
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

#from mail import send_message

path = 'c:/git/prod_data/BOMS'	

def get_git_boms():
	boms = {}	
	print ( 'Loading git boms :')
	for bom in os.listdir(path):		
		with open(path+'/'+str(bom)+'/'+str(bom)+'.json') as json_data:
			print ('.', end=' ')
			boms[bom] = json.load(json_data)
	print ( 'Loaded '+str(len(boms))+ ' git boms ' )			
	return boms

def get_unequal_boms():
	unequal_boms = []
	for bom in sage_boms:
		if bom in git_boms.keys():
			#if sage_boms[bom.encode('utf-8')] != git_boms[bom.encode('utf-8')]:				
			if sage_boms[bom] != git_boms[bom]:								
				unequal_boms.append(bom)
				#print (bom + '      FALSE')
			#else: 
				#print (bom + '     TRUE')
		#else: # new bom 
		#	print (bom + '      NEW')
			# unequal_boms.append(bom)
	return unequal_boms

def update_git_bom(bom):
	for fname in os.listdir(path+'/'+bom):
		r = http.request('GET','https://raw.githubusercontent.com/hammonja/prod_data/master/BOMS/'+bom+'/'+fname )
		with open(path+'/'+bom+'/'+fname, 'w') as out:					
			print ('updating : '+bom)			
			out.write(r.data.decode())		
	return
	
# get current boms from sage
sage_boms = get_sage_boms()


# get all boms from git
git_boms = get_git_boms()


# check if there is a mis-match
if sage_boms != git_boms:
	
	# update boms from git that are not equal
	for bom in get_unequal_boms():
		update_git_bom(bom)
			
	# get all boms from git again 
	git_boms = get_git_boms()

	# check again 
	if sage_boms != git_boms:
	
		# still unequal then send an email
		for bom in get_unequal_boms():
			print( 'The following BOM is out of sync with github : ' +bom )
			#send_message(text,bom)		
		
