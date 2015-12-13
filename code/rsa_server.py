"""
Course Project 6490: Secure Authentication in IoT Devices
Team: Chandrasekhar Nagarajan, Damodar Sahasrabudhe, Gurupragaash Annasamy Mani, Praveen Thiraviya Rathinam
Description: Server for RSA
Code starts up multi threaded server. It accepts incoming connections, read temparature data and verifies RSA signature
"""

from socket import *
import thread
import pickle
import M2Crypto

#read data and verify key.
def connectIOT(Socket, dummy):
	msg_len = Socket.recv(6)
	print msg_len
	msg_len = int(msg_len, 16)
	msg = Socket.recv(msg_len)	#read from socket
	data = pickle.loads(msg)	#load dictionary from incoming data.
	print "message recieved: ", data
	RSA = M2Crypto.RSA.load_pub_key('public.pem')	#read public key from file.
	if RSA.verify_rsassa_pss(data['temp'] + data['time'], data['sign']) == 1:	#verify RSA signature
		print "data is authentic"
	else:
		print "intrusion alert"



serverPort = 12001
serverSocket = socket(AF_INET,SOCK_STREAM)
#reuse means forcefully bind on the ip and port
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(('',serverPort))
serverSocket.listen(5)	#set up server.
print "server up"
while 1:
	connectionSocket, addr = serverSocket.accept()
	thread.start_new_thread(connectIOT, (connectionSocket,1) )		#start new thread for incoming connection.



	

