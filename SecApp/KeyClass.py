import ConfigParser
from cypherHandle import *
import os
from Crypto.PublicKey import RSA
import base64
import string
import random
import hashlib


keyFileName='configs/seccuKey.ki'
encKeyFileName='configs/seccuKey.ki.crypt'




def GenRSA(ki,seed=None):
	key = RSA.generate(2048, os.urandom) #osrandom will be replaced by xy corrdinate sample
	
	# Create public key.																																			   
	ssh_rsa = ki + base64.b16encode('ssh-rsa')
	
	# Exponent.																																						
	exponent = '%x' % (key.e, )
	if len(exponent) % 2:
		exponent = '0' + exponent
	
	ssh_rsa += '%08x' % (len(exponent) / 2, )
	ssh_rsa += exponent
	
	modulus = '%x' % (key.n, )
	if len(modulus) % 2:
		modulus = '0' + modulus
	
	if modulus[0] in '89abcdef':
		modulus = '00' + modulus
	
	ssh_rsa += '%08x' % (len(modulus) / 2, )
	ssh_rsa += modulus
	
	#public_key = 'ssh-rsa %s' % (
	public_key = '%s' % (
		base64.b64encode(base64.b16decode(ssh_rsa.upper())), )
	return public_key

def genSHA(password): #this createas string for RSA generation
	hash_object = hashlib.sha256(password)
	hex_dig = hash_object.hexdigest()
	return str(hex_dig)


def genAESKey(password): #this encrypts database file
	ki=genSHA(password)
	RSA=GenRSA(ki) #adds random bits
	AESkey=RSA[0:32]#select 32 bits
	return AESkey

def genAESKeyStore(password): #this will encrypt key storage with AES
	keyStore=genSHA(password)
	store=keyStore[0:32]
	return store


#def randomGen(xlist,ylist):
	#points sampled every 30ms, points must be >(random (range 30))
#def keyfile(password,randomGen): # generates system key, used to store compresssed AES files and salsa20 database



def GenAll(password):
	guarded=genAESKeyStore(password)
	full=genAESKey(password)
	allofem="passd:   "+ password+"\nmakes:   "+guarded+"\nstore:   "+full
	return allofem



def writeKeyFile(password):
	key1=genAESKey(password)

	f = open(keyFileName, "w")
	f.write(key1)
	f.close()
	 

	key2=genAESKeyStore(password)
	encrypt_file(key2,keyFileName,encKeyFileName)
	#maybe write 0 to old file
	#delete ki file
	os.remove(keyFileName)
	#add function to encrypt with genAESKeyStore(password)
	return True


def readKeyFile(password):
	key2=genAESKeyStore(password)

	#make this function load directly to memory without IO
	decrypt_file(key2,encKeyFileName,keyFileName)

	f = open(keyFileName, "r")
	keybuffer=f.read() 
	f.close()
	currentKey=keybuffer
	del keybuffer
	os.remove(keyFileName)
	return currentKey