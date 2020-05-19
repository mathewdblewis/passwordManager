from subprocess import check_output as call
import urllib.request
from os import system


def Print(s,clear=True):
	if clear: system('clear')
	else: print("")
	print('*'*len(s)+'****\n'+'* '+s+' *\n'+'*'*len(s)+'****\n')

# url of passwords.py script on github
url = 'https://raw.githubusercontent.com/mathewdblewis/passwordManager/master/passwords.py'


# get dependencies
Print("INSTALLING DEPENDENCIES",clear=False)
try: system("pip3 install cryptography")
except:
	print("could not install dependency 'cryptography'")
	exit(1)
try: system("pip3 install pyperclip")
except: pass


# get file
file = ""
try: file = urllib.request.urlopen(url).read().decode()
except:
	print("the source code could not be found")
	exit(1)
file = '#!'+call('which python3',shell=True).decode()+'\n'+'\n'.join(file.split('\n')[1:])


# get path
Print("INSTALLING PASSWORD MANAGER",clear=False)
default,paths = "",call('echo $PATH',shell=True).decode().split(':')
for path in paths:
	try: open(path+'/passwords','w')
	except: continue
	default = path+'/passwords'
	break

path = ""
while True:
	print('Give the full path of where you would like to put this program.')
	print('You must provide an absolute path',end='')
	if default!='': print('the path "' + default + '" is recommended.')
	else: print(".")
	if default!='': print('Press enter now to use the default or ')
	path = input('type out your prefered path here: ')
	if path == '': path = default
	if path[0] != '/':
		print("ERROR: you must provide an absolute path")
		continue
	try: open(path,'w')
	except:
		print("ERROR: this file cannot be written to, give a different path")
		continue
	break


# install program
open(path,'w').write(file)
call('chmod 700 ' + path, shell=True)


# prompt the user
Print("ALL DONE!",clear=False)
print("passwords has been installed!")
print("To run the CLI, enter '" + path.split('/')[-1] + "' below")

