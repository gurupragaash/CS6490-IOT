"""
Course Project 6490: Secure Authentication in IoT Devices
Team: Chandrasekhar Nagarajan, Damodar Sahasrabudhe, Gurupragaash Annasamy Mani, Praveen Thiraviya Rathinam
Description: Generate keys for RSA using M2Crypto
"""

import M2Crypto

Bob = M2Crypto.RSA.gen_key (2048, 7)	#generate 2048 bit public key.
Bob.save_key ('private.pem', None)	#save private key to file
Bob.save_pub_key ('public.pem')		#save public key to file

