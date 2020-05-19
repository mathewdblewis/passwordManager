#!/usr/local/bin/python3


# make sure we are using the right version

from sys import version
if version[0]!='3':
	print("python 2 is deprecated, please use python 3")
	exit()


# imports

import json; from getpass import getpass; import sys
from os import system, remove, urandom
from os.path import expanduser,realpath
from random import randint as rand
from subprocess import run; import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
try: import pyperclip
except: pass


fileName = expanduser('~')+'/.passwordmanager.enc'
saltLen = 16


# utilities

def helpstr(state):
	if state == 'viewEntry': 
		print("p = copy password to clipboard")
		print("u = copy username to clipboard")
		print("v = print password")
		print("w = copy website to clipboard")
		print("o = open website")
		print("e = edit entry")
		print("d = delete entry")
		print("press enter to return to search")

	if state == 'main':
		print("a = add entry")
		print("c = change master password")
		print("x = to quit this program")
		print("press enter to search")


def Print(s):
	system('clear')
	print('*'*len(s)+'****\n'+'* '+s+' *\n'+'*'*len(s)+'****\n')


def copy(data):
	try:
		run("pbcopy", universal_newlines=True, input=data)
		return
	except: pass
	try:
		pyperclip.copy(data)
		return
	except: pass
	print("The copy to clipboard feature is unavailable")
	print("you can print your password to console with")


def randstr(l,s):
	nums = "1234567890"
	lets = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
	syms = "~!@#$%^&*()_+-={}|[]<>?,./"
	used = ""
	if 'n' in s: used += nums
	if 'l' in s: used += lets
	if 's' in s: used += syms
	if used == "": raise Exception('not enough character types chosen')
	return "".join([used[rand(0,len(used)-1)] for _ in range(l)])


def save(data,final=False):
	if final: start = 'c'		# file starts with c because the file is "closed"
	else:     start = 'o'		# file starts with o because the file is "open"
	salt    = urandom(saltLen)
	kdf     = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
	cipher  = Fernet(base64.urlsafe_b64encode(kdf.derive(data['password'].encode('utf-8'))))
	towrite = start.encode('utf-8')+salt+cipher.encrypt(json.dumps(data).encode('utf-8'))
	open(fileName,'wb').write(towrite)



# states

def load(empty):
	file,plainText,data = "","",{}
	try:
		file = open(fileName,'rb').read()
		if file[0] == 'o'.encode('utf-8'):
			Print("WARNING")
			print("Your password manager either apears to already be open")
			print("or you are recovering your previous session after improperly quiting")
			x = input("Press 'c' to continue or anything else to quit: ")
			if 'c' != x: return ('exitState',)
			file = file[1:]
		salt,file = file[1:saltLen+1],file[saltLen+1:]
	except: return ('setup',)	# create new password manager
	Print("PASSWORD MANAGER")
	
	while True:
		print("\nEnter your master password here. You can also press enter to exit")
		password = getpass("or d to delete the password file and create a new password manager: ")
		if password == '': return ('exitState',)
		elif password == 'd':
			print("Are you sure you want to delete the password file? This cannot be undone.")
			if getpass("Enter y if yes: ")=='y':
				remove(fileName)
				return ('setup',)
		kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
		cipher = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8'))))
		try:
			plainText = cipher.decrypt(file)
			break
		except: print('\nWrong password')

	try: data = json.loads(plainText)
	except:
		print('ERROR: the file has been corrupted')
		return ('exitState',)
	save(data)
	return ('search',data)


def setup(empty):
	Print('WELCOME TO PASSWORD MANAGER!')
	while True:
		password = getpass('To start, first enter your master password or press enter to quit: ')
		if password == "": return ('exitState',)
		if len(password)<10:
			print("your password must be at least 10 characters long.")
			continue
		if password == getpass('Reenter your master password: '): break
		print("Your passwords don't match, try again")
	data = {'password':password,'entries':{}}
	save(data)
	print('You will now be taken to the main page, from there enter h for help')
	input('Enter anything to continue: ')
	return ('main',data)


def search(params):
	data,B = params[0],False
	Print('SEARCH')
	print('Press enter twice consecutively to return to main menu')
	print('or enter the name of an entry to search for it')
	while True:
		x = input(': ')
		if x=='':
			if B: return ('main',data)
			print('\n'.join(sorted([s for s in data['entries']])))
			B = True
		else:
			B = False
			if x[-1]==' ' and x.strip() in data['entries']: return ('viewEntry',data,x.strip())
			else:
				S = sorted([s for s in data['entries'] if s[:len(x)]==x])
				if   len(S)==0 and len(x)!=0: print('No entries starting with "' + x + '" found')
				elif len(S)==0 and len(x)==0:
					print('Your password manager is empty!')
					print('Go to the main menue and enter "a" to add an entry.')
				elif len(S)==1: return ('viewEntry',data,S[0])
				else: print('\n'.join(S))


def main(params):
	data = params[0]
	Print('PASSWORD MANAGER')
	print('(Enter "h" for help)')
	while True:
		x = input(': ')
		if   x=='a': return ('addEntry',data)
		elif x=='':  return ('search',data)
		elif x=='c': return ('changeMasterPassword',data)
		elif x=='x':
			save(data,final=True)
			return ('exitState',)
		elif x=='h': helpstr('main')
		else:        print('Unknown option "' + x + '"')


def changeMasterPassword(params):
	Print("CHANGE MASTER PASSWORD")
	data = params[0]
	while True:
		print("\nPress Enter to return to the main page")
		password = getpass('Enter new password: ')
		if password == "": return ('exitState',)
		if len(password)<10:
			print("your password must be at least 10 characters long.")
			continue
		if password == '': return ('main',data)
		elif password!=getpass('Re-enter new password: '): print("passwords don't match, try again")
		else:
			data['password'] = password
			break
	save(data)
	input("The new password has been saved, press enter to continue: ")
	return ('main',data)


def addEntry(params):
	data = params[0]
	Print('ADD ENTRY')
	print("Provide the following: service name, username, website, notes, password")
	print("'notes' may be multilined, to stop writting to 'notes' press enter on an empty line")
	while True:
		service = input("\nEntry name: ").strip()
		if service in data['entries']: print('this entry already exists')
		elif service == '': print("the entry can't have an empty string for its name")
		else: break
	username = input("username: ")
	website = input("website: ")
	if website[:7] not in ['https:/','http://','']: website = 'https://' + website
	
	print("enter your notes below:")
	notes = ""
	while True:
		nextline = input()
		notes += nextline+'\n'
		if nextline == '': break
	notes = notes[:-1]
	
	print("\nTo generate a password, enter the desired length (at least 10, at most 99)")
	print("followed by some subset of the characters 'n','l','s'")
	print("Including n will generate a password with numbers")
	print("and similarly for 'l' and letters and 's' for symbols")
	print("For example, '30 ns' will result in a password")
	print("of length 30 with only numbers and symbols")
	print("If a number is not provided or not enough symbols are used")
	print("this setting will default to '30 nls'")

	x = input("To use a custom password, simply press enter: ")
	if x == '':
		while True:
			password = getpass("password: ")
			if password == '': print("you must provide a password")
			elif password == getpass("reenter password: "): break
			else: print("passwords don't match, try again")
	else:
		l = 30
		try: l = int(x[:2])
		except: pass
		try: password = randstr(l,x)
		except: password = randstr(l,'snl')
	
	data['entries'][service] = {'username':username,'website':website,'notes':notes,'password':password}
	save(data)
	input('Your entry has been saved, press enter to continue: ')
	return ('viewEntry',data,service)


def viewEntry(params):
	data,serviceName = params
	entry = data['entries'][serviceName]
	Print(serviceName)
	print('(Enter "h" for help)\n')
	if entry['username']!='': print('Username:\t'     , entry['username'])
	if entry['website']!='':  print('Website:\t'      , entry['website'])
	if entry['notes']!='':
		print('Notes:')
		print(entry['notes'])
	while True:
		x = input(': ')
		if   x=='p': copy(entry['password'])
		elif x=='v': print(entry['password'])
		elif x=='u': copy(entry['username'])
		elif x=='w': copy(entry['website'])
		elif x=='o':
			if entry['website']!='': system('open ' + entry['website'])
			else: print("no website for this entry, option unavailable")
		elif x=='e': return ('editEntry',data,serviceName)
		elif x=='':  return ('search',data)
		elif x=='h': helpstr('viewEntry')
		elif x=='d': return ('deleteEntry',data,serviceName)
		else:        print('Unknown option "' + x + '"')


def deleteEntry(params):
	data,serviceName = params
	print("Are you sure you want to delete this entry?")
	i = input('If yes press "y", press anything else to exit: ')
	if i=='y':
		del data['entries'][serviceName]
		save(data)
		return ('search',data)
	return ('viewEntry',data,serviceName)


def editEntry(params):
	data,serviceName = params
	Print('EDIT ENTRY')
	print("When prompted to modify a field either enter the new value")
	print("or press enter to leave it unchanged")
	print("'notes' may be multilined, to stop writting to 'notes' press enter on an empty line")
	while True:
		service = input("\nEntry name: ").strip()
		if service in data['entries']: print('this entry already exists')
		else: break
	username = input("username: ")
	website = input("website: ")
	if website[:7] not in ['https:/','http://','']: website = 'https://' + website
	
	print("enter your notes below:")
	notes = ""
	while True:
		nextline = input()
		notes += nextline+'\n'
		if nextline == '': break
	notes = notes[:-1]

	x = input("To use a custom password or keep your old password, press enter: ")
	if x == '':
		while True:
			password = getpass("password: ")
			if password == '': break
			elif password == getpass("reenter password: "): break
			else: print("passwords don't match, try again")
	else:
		l = 30
		try: l = int(x[:2])
		except: pass
		try: password = randstr(l,x)
		except: password = randstr(l,'snl')
	
	if service != '':
		data['entries'][service] = data['entries'][serviceName]
		del data['entries'][serviceName]
		serviceName = service
	service = serviceName
	temp = {'username':username,'website':website,'notes':notes,'password':password}
	for x in temp:
		if temp[x] == '': temp[x] = data['entries'][service][x]
	data['entries'][service] = temp
	save(data)
	input('Your entry has been saved, press enter to continue: ')
	return ('viewEntry',data,service)



if __name__ == '__main__':
	devmode = len(sys.argv) == 2 and sys.argv[1] == '-devmode'
	state = ('load',)
	try:
		while True:
			if    state[0] == 'exitState':              exit()
			elif  state[0] == 'load':                   state = load(state[1:])
			elif  state[0] == 'search':                 state = search(state[1:])
			elif  state[0] == 'setup':                  state = setup(state[1:])
			elif  state[0] == 'viewEntry':              state = viewEntry(state[1:])
			elif  state[0] == 'addEntry':               state = addEntry(state[1:])
			elif  state[0] == 'editEntry':              state = editEntry(state[1:])
			elif  state[0] == 'deleteEntry':            state = deleteEntry(state[1:])
			elif  state[0] == 'main':                   state = main(state[1:])
			elif  state[0] == 'changeMasterPassword':   state = changeMasterPassword(state[1:])
			else: raise Exception('unknown state: "' +  state[0] + '"')
	except Exception as e:
		if devmode: raise e
		else: print("SOFTWARE ERROR\nPlease notify the developer")
		exit(1)







