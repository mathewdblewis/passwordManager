from subprocess import check_output as call
import urllib.request

# url of passwords.py script on github
# url = "https://github.com/mathewdblewis/Y4S2Lectures/blob/master/CSC421/lec001.txt"

try:
	path = call('echo $PATH',shell=True).decode().split(':')[0] + '/passwords'
	file = str(urllib.request.urlopen(url).read())
	py = call('which python3',shell=True)
	'#!'+py+'\n'+'\n'.join(file.split('\n')[1:])
	open(path,'w').write()
	call('chmod 100 ' + path, shell=True)
except:
	print("The installation failed")
	exit(1)




