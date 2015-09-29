import os
import platform
#Finds specified firefox profile, in our case 'default', and if it cannot find a profile named default, it creates a new one named default.
def env(profile):
	uos = platform.system()
	mes = 'OS Detected: %s' % uos
	machine = platform.machine()
	if uos == 'Windows':
		fd = os.getenv('APPDATA') + '\Mozilla\Firefox\Profiles'
		if machine == 'AMD64':
			ff = r'"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"'
		else:
			ff = r'"C:\Program Files\Mozilla Firefox\firefox.exe"'
	elif uos == 'Linux':
		fd = os.getenv('HOME') + '/.mozilla/firefox'
		ff = 'firefox'
	else:
		print(mes)
		print('OS Not Compatible.')
		exit()
	status = 0
	for file in os.listdir(fd):
		if file.endswith(".%s" % profile):
			mdir = file
			status = 1
	if not status:
		print('Profile not detected... Creating profile')
		os.system("%s -CreateProfile %s" % ff % profile)
		for file in os.listdir(fd):
			if file.endswith(".%s" % profile):
				mdir = file
				status = 1
		if status != 1:
			print('Profile Creation Failed.')
			exit()
		fdir = (fd + '/' + mdir)
	elif status == 1:
		print('Profile detected, continuing.')
		fdir = (fd + '/' + mdir)
	return fdir
