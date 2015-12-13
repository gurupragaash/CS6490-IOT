import subprocess
import os
import pickle

def load_data_from_file(fileName):
	inFile = open(fileName, "r")
	return pickle.load(inFile)

def write_data_to_file(data, fileName):
	outFile = open(fileName, "w")
	pickle.dump(data,outFile)

def pickle_send(msg, sock):
	data = pickle.dumps(msg)
	sock.send("%06x" % len(data))
	sock.send(data)
	#print("print legth of data is:", len(data), "data is:", data)
	return data

def get_ram():
	try:
		s = subprocess.check_output(["free","-m"])
		lines = s.split("\n")
		used_mem = float(lines[1].split()[2])
		total_mem = float(lines[1].split()[1])
		return (((used_mem/total_mem)))
	except:
		return 0

def get_temperature():
	try:
		dir_path="/opt/vc/bin/vcgencmd"
		s = subprocess.check_output([dir_path,"measure_temp"])
		return float(s.split("=")[1][:-3])
	except:
		return 0

def get_disk():
	try:
		s = subprocess.check_output(["df","/dev/root"])
		lines = s.split("\n")
		return lines[1].split("%")[0].split()[4]
	except:
		return 0

def get_load():
	try:
		s = subprocess.check_output(["cat","/proc/loadavg"])
		return float(s.split()[0])
	except:
		return 0
