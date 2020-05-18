from subprocess import check_output as call
import urllib.request

# url of passwords.py script on github
url = 'https://raw.githubusercontent.com/mathewdblewis/passwordManager/master/passwords.py'

try:
	path = call('echo $PATH',shell=True).decode().split(':')[0] + '/passwords'
	file = urllib.request.urlopen(url).read().decode()
	file = '\n'.join(file.split('\n')[1:])
	py = call('which python3',shell=True).decode()
	file = '#!'+py+'\n'+file
	open(path,'w').write(file)
	call('chmod 700 ' + path, shell=True)
except Exception as e:
	print("The installation failed")
	exit(1)

