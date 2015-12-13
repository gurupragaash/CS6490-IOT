"""
Course Project 6490: Secure Authentication in IoT Devices
Team: Chandrasekhar Nagarajan, Damodar Sahasrabudhe, Gurupragaash Annasamy Mani, Praveen Thiraviya Rathinam
Description: Code to plot data 
Code reads outout of experiment stored in file and plots it using matplotlib
"""

import matplotlib.pyplot as plt
import pickle
NUM = 100

def load_data_from_file(fileName):
	inFile = open(fileName, "r")
	return pickle.load(inFile)

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 48}

plt.rc('font', **font)

#read data from files
rsa = load_data_from_file("timeDelayFromRSA")
zks = load_data_from_file("timeDelayFromZKS")
zks_xor = load_data_from_file("timeDelayFromZKS_XOR_RANDOM")
x = list(xrange(1, NUM+1)) 

plt.xlabel('No. of Iterations')
plt.ylabel('time (s)')

line1, = plt.plot(x,zks,linestyle="solid", marker='o', color="red", linewidth=2)	#ZKS
line2, = plt.plot(x,rsa, linestyle="solid", marker="o", color="blue", linewidth=2)	#RSA
line3, = plt.plot(x,zks_xor, linestyle="solid", marker='o', color="green", linewidth=2)	#O-ZKS

plt.legend([line1, line2, line3], ["ZKS","RSA", "O-ZKS"], loc = 7)
plt.title("Signing Time Comparison")
plt.show()	#show the graph.

