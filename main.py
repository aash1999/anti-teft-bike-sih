import RPi.GPIO as gpio
import random
import string
import hashlib
import pyrebase
import json
import datetime
import time
import haversine
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

config = {
  "apiKey": "AIzaSyCOvA5NheUV2pDPVRD_CDTrKW30vmrwtE0",
  "authDomain": "anti-teft-bike-sih-default-rtdb.firebaseapp.com",
  "databaseURL": "https://anti-teft-bike-sih-default-rtdb.firebaseio.com",
  "storageBucket": "anti-teft-bike-sih-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def write_rfid(message):
	try : 
		reader.write(message)
	except:
		print('Error')
	finally:
		gpio.cleanup()
def read_rfid():
	try:
		id, text = reader.read()
		return(id,text)
	except:
		print('Error')
	finally :
		gpio.cleanup()

def create_random_key(length = 48):
	letters = string.ascii_letters + string.digits + string.punctuation
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

def hash(message):
	result = hashlib.md5(message.encode())
	result = result.hexdigest()
	return result

def auth_rfid():
	print('Bike RFID Auth 3+')
	print('waiting for key')
	(uid,message) = read_rfid()
	data_from_file = {}
	print(uid , message)
	with open('auth.txt') as json_file:
		data_from_file = json.load(json_file)
	#print(data_from_file)
	#print(str(uid) == str(data_from_file['uid']) ,str(message) == str(data_from_file['message']) ,str(message) ,str(data_from_file['message'])   )
	if(str(uid) == str(data_from_file['uid']) and str(message) == str(data_from_file['message'])):
		
		print('S')
		new_message = hash(create_random_key())
		print('New Key' ,new_message )
		data_to_file = {'uid': uid , 'message':new_message+"                " }
		db.child('auth').update(data_to_file)
		try:
			write_rfid(new_message)
			with open('auth.txt','w') as outfile:
				json.dump(data_to_file,outfile)
			db.child('auth').update({'lock':True})
			return 1
		except:
			print('Error whie writing new key ')
	else:
		print('E')
		db.child('auth').update({'lock':False})
		return 0
def get_geo_distance(loc1,loc2):
	return haversine.haversine(loc1,loc2)
		
	
	
def main():
	auth_flag =0
	while(True):
		auth_flag = auth_rfid()
		if(auth_flag == 0):
			db.child('auth').update({'lock':False})
		else:
			break
		time.sleep(1)
	prev_location = (1,1)
	while(auth_flag == 1 and db.child('auth').child('lock').get().val() == True ):
		#Send Telegram Message
		last_location = (0,0)
		dist =0
		prev_dist = db.child('state').child('distance').child('Monday').get().val()
		if(prev_dist != None):
			dist =prev_dist
		dist = dist+ get_geo_distance(prev_location , last_location)
		prev_location = last_location
		db.child('state').child('distance').update({'Monday':dist})
		db.child('state').update({'lat':last_location[0],'long':last_location[1]})
		#print(True)
		time.sleep(1)
		
	
main()
#auth_rfid()
#(id,uid) = read_rfid()
#data_to_file= {'uid':id , 'message':uid}
#with open('auth.txt','w') as outfile:
#	json.dump(data_to_file,outfile)
#write_rfid('d6ab621aaf1e6fa5e359a2d418cd0f08')
#print(read_rfid())
