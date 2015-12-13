"""
Course Project 6490: Secure Authentication in IoT Devices
Team: Chandrasekhar Nagarajan, Damodar Sahasrabudhe, Gurupragaash Annasamy Mani, Praveen Thiraviya Rathinam
Description: Client for ZKS
Code connects to server and computes hash and ZKS signature and sends them to server along with temparature data
"""

from socket import *
import random
import pickle
import time
import sys, getopt
import md5
import datetime
from utils import *

#Global Definitions here
HASH_LENGTH = 128
RANDOM_RANGE = 10000
HIGH_TEMP=100
LOW_TEMP=-30
NUM_TIMES=100
RANDOM_NUMBER_SIZE = 1024 
OZKS = False

#compute has of message to be used later. Using MD5
def compute_hash(data, timeStamp, randomPairs):
	hash1 = md5.new()
	hash1.update(str(data))
	hash1.update(str(timeStamp))
	hash1.update(str(randomPairs))
	return '{0:b}'.format(int(hash1.hexdigest(),16))

#2048 bit public key 
p = 2146879574488551682242734434573304031276897588342845099152970652603669123515638503230207986834751246351679936778425636899845970801684145235336341055954114580156045401145044361935126417393740848074552457663599613130619832474086935666600797454157453293173275538065297462659405039958717196879535837802838406529
q = 48497688212136310126338604340285061531190478982745255456071882112606990687649660184188146783248313848995842638707855524761910298478675991462720146742310251541125132800813203774835159052121314191758457350574043578340656710467835132979704782830552616575364716218006010445133644304598255418663771442279373191863

n = p*q 
s = 79225359123569881258003859580914407004147441225651981519916418522918322243228819250422778902808765579629440790779114873974508492077708412355991081842518737922535912356988125800385958091440700414744122565198151991641852291832224322881925042277890280876557962944079077911487397450849207770841235599108184251873
v = long(s*s) % n
 
#print "n = ",n
#print "v = ",v	

#calculate signature for message
def sign_data(temp, r_array):
	ts = datetime.datetime.now()
	if (r_array == None):			#generate random numbers equal to length of hash used for ZKS.
		r_array = list()
		for i in range(0, HASH_LENGTH):
			r_array.append(random.getrandbits(RANDOM_NUMBER_SIZE))
	else:	#generate one random number and XOR it with random number array to generate psudo random - used for OZKS.
		random_number = random.getrandbits(RANDOM_NUMBER_SIZE)	
		r_array = [x ^ random_number for x in r_array];		#XOR

	r2_mod_n = list()
	sr = list()
	r = list()
	data = dict()		#preparing dictionary to be sent across.
	data['ts']=ts	#adding timestamp to avoid replay attack
	data['temp'] = temp
	data['name'] = sys.argv[3] 

	#This computes r2_mod_n from r_array
	r2_mod_n = [(i ** 2) % n for i in r_array]		

    rethash=compute_hash(temp, ts, r2_mod_n)	#compute hash.

	for i in range(0, len(rethash)):
		bit = rethash[i]
		if bit == '1':		#if hash bit is 1, append sr mod n.
			sr.append(long(s * r_array[i]) % n)
		else:		#if hash bit is 1, append r mod n.
			r.append(r_array[i] % n)

	#prepare final dictionary to be sent across to server.
	data['r2_mod_n'] = r2_mod_n
	data['sr'] = sr
	data['r'] = r
	end = datetime.datetime.now()
	timeTaken = end - ts 	#time required to sign data.
	return (data, str(timeTaken)[5:], r_array)

sName = str(sys.argv[1])
sPort = int(sys.argv[2])

r_array = None
       
start = datetime.datetime.now()
timeTakenList = list()
for x in range (0,NUM_TIMES):		#repeat experiment 100 times.
	Sock = socket(AF_INET, SOCK_STREAM)
	try:
	   Sock.connect((sName,sPort))
	except:
	   print("connection failed")
	   sys.exit()
        if(OZKS == False):	#call OZKS
            (data, timeTaken, r_array) = sign_data(random.sample(xrange(LOW_TEMP,HIGH_TEMP),1), None)
        else:		#call ZKS.
            (data, timeTaken, r_array) = sign_data(random.sample(xrange(LOW_TEMP,HIGH_TEMP),1), r_array)
	timeTakenList.append(timeTaken)
        pickle_send(data, Sock)
	#time.sleep(1)
	Sock.close()

#print("After signing Get ram is %s Get disk is %s Get load is %s Get temp is %s" %(get_ram(), get_disk(), get_load(), get_temperature())) 
end = datetime.datetime.now()
timeTaken = end-start
print("End signing at %s. Time taken %s " %(end, timeTaken))

#save output to files to be ploted later.
if(OZKS == False):
    write_data_to_file(timeTakenList, "timeDelayFromZKS")
else
    write_data_to_file(timeTakenList, "timeDelayFromZKS_XOR_RANDOM")



