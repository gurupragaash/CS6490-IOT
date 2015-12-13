"""
Course Project 6490: Secure Authentication in IoT Devices
Team: Chandrasekhar Nagarajan, Damodar Sahasrabudhe, Gurupragaash Annasamy Mani, Praveen Thiraviya Rathinam
Description: Server for ZKS
Code starts up multi threaded server. It accepts incoming connections, read temparature data, compute hash and verifies ZKS signature
"""

import socket, select, sys
import thread
import pickle
import md5

#Global variables declaration here 
#public keys
publicKeys = dict()
publicKeys['iot2'] = {'n':10967535067, 'v': 4273848869}

#2048 bit public key 
publicKeys['iot1'] = {'n':104118696232549650274888535117607400919617862641797541627069701316305899186327133126619818776808842308861381047295587957740310341320957212874317915867115925913397690676771840274449481918801309129895128333633357900393827354376432195835562022311988045813564555616577285137243083706927712264934964794726268677369390657835217240686312909076754053623750497999088933964620284149421019589232939139758087750265617576094295995127732935356224449619857941809575691840976868081295745089314235142904194963961004289440419655392784214248216309472128901307337192992928677518107212750680808453497837692713095429613367331211508873527, 'v': 29535754305638407281658244427796349648917129583834478740810690995163363883166773054060178606948791013477575660943662465473907953850190080721556385889288565661138707212371745084476545657916808434761647317044558334199214287785285337312881889971743675568990222360305290187746503218323414148861369174761863419372353804068770772540286633942386769501436147281380362038304733706643379437557298115622994032883442120699298125855340147034883967045303797681411217000712923773590239602097865491322053801718886543881737966409454738699770040141347966844713150212579182198736780231823919416473193908497269508401846334630171596509}

host = ""
port = 5000

#compute has of message to be used later. Using MD5
def compute_hash(data, timeStamp, randomPairs):
    hashValue = md5.new()
    hashValue.update(str(data))
    hashValue.update(str(timeStamp))
    hashValue.update(str(randomPairs))
    return '{0:b}'.format(int(hashValue.hexdigest(), 16))

#using pickle data structure to ease data transmission over sockets
def read_unpickle(sock):
    length = (sock.recv(6))		#read length of data in socket
    if not length:
            print("No data. close connection and abort !!")
            return None
    length = int(length, 16)
    data = ""
    while True:			#read data from socket. Using length to read those many bytes from socket to avoid partial reading.
        data = data + sock.recv(length - len(data))
        if not data:
                print("No data. close connection and abort !!")
                return None
        if len(data) == length:
            break;
    msg = pickle.loads(data)		#convert data from pickle to dictionary
    return msg

#verify signature in incoming message
def verify_signature(clientData):
    valid = 1
	#reading keys and incoming message from dictionary - n,s, r, sr mod n, r2 mod n and r mod n values
    n = publicKeys[clientData['name']]['n']
    v = publicKeys[clientData['name']]['v']
    r2_mod_n = clientData['r2_mod_n']
    sr = clientData['sr']
    r = clientData['r']
    temp = clientData['temp']
    ts = clientData['ts']
    hashValue = compute_hash(temp, ts, r2_mod_n)	#compute hash

    sr_count = 0
    r_count = 0
    print ("Length of hashvalue is %d and Hash is %s" %(len(hashValue), type(hashValue)))
    for i in range(0, len(hashValue)):
        bit = hashValue[i]
	vr2_mod_n = (long(v) * long(r2_mod_n[i])) % n	#calculate vr2_mod_n
	
	if bit == '1':	#if hash bit is 1 then test vr2_mod_n = square of (sr mod n)
	    a=long(sr[sr_count]) * long(sr[sr_count])
	    if a % n == long(vr2_mod_n):	
                #print "sr matched for r2_mod_n: ", r2_mod_n[i], " sr_mod_n: ", sr[sr_count]
                sr_count = sr_count + 1
	    else:	#throwing error if not matched
                #print "sr not matched for r2_mod_n: ", r2_mod_n[i], " sr_mod_n: ", sr[sr_count]
                sr_count = sr_count + 1
                valid = 0
			
	else:	#if hash bit is 0 then test r2_mod_n = square of (r mod n)
            #print "inside r: r2 calc: ", r[r_count], "r2 recieved: " ,r2_mod_n[i]
            if (long(r[r_count])*long(r[r_count])) % n == long(r2_mod_n[i]):	
                #print "r matched for r2_mod_n: ", r2_mod_n[i], " r_mod_n: ", r[r_count]
                r_count = r_count + 1
            else:
                #print "r not matched for r2_mod_n: ", r2_mod_n[i], " r_mod_n: ", r[r_count]
                r_count = r_count + 1
                valid = 0
    print("Verification succcess(%s)" %((valid == 1)))
    return (valid == 1)


def process_connection(clientHdl, name):
    print ("----------------------------%s start--------------------------------------" %(name))
    while True:
        clientData = read_unpickle(clientHdl)	#read data from socket
        if (clientData == None):
            print ("----------------------------%s closed --------------------------------------"%(name))
            return
        verify_signature(clientData)

def main():
    try:
		#create server socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #reuse means forcefully bind on the ip and port
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(10)		#listen on port
        print ("Hub is running.....")
    except:
        print ("Error: unable to open socket %s", sys.exc_info()[0])
	
    i = 1
    while True:
            clientHdl, addr = sock.accept()
            try:
                thread.start_new_thread( process_connection, (clientHdl, "Connection"+str(i), ))		#start new thread, for new incoming connection
            except:
                print ("Error: unable to start thread for a new connection %s with error %s", (i, sys.exc_info()[0]))
            i += 1
    sock.close()

if __name__ == "__main__": 
    main()
