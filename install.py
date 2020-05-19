from subprocess import check_output as call
import urllib.request
from os import system

# url of passwords.py script on github
url = 'https://raw.githubusercontent.com/mathewdblewis/passwordManager/master/passwords.py'


# get dependencies
try: system("pip3 install cryptography")
except:
	print("could not install dependency 'cryptography'")
	exit(1)


# get file
file = ""
try: file = urllib.request.urlopen(url).read().decode()
except:
	print("the source code could not be found")
	exit(1)
file = '#!'+call('which python3',shell=True).decode()+'\n'+'\n'.join(file.split('\n')[1:])


# get path
default = call('echo $PATH',shell=True).decode().split(':')[0] + '/passwords'
path = ""
while True:
	print('\n\nGive the full path of where you would like to put this program.')
	print('You must provide an absolute path, the path "' + default + '" is recommended.')
	path = input('Press enter now to use the default or type out your prefered path here: ')
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
print("\npasswords has been installed!")
print("To run it, enter 'passwords' below")
