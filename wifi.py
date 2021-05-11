import subprocess
import re
import os


if os.name == 'nt':
	print("\n\n\t==== WI-FI ====\n\n\n");		
	'''
	Ehhez a részhez ezt avettem alapul: https://github.com/davidbombal/red-python-scripts/blob/main/windows10-wifi.py
	'''		
	commandOutput = subprocess.run(["netsh","wlan","show","profiles"], capture_output = True).stdout.decode()
	#print(commandOutput)
	names = (re.findall("All User Profile     : (.*)\r", commandOutput))
	#print(names)
	wifilist = list()
	if len(names) != 0:
		for name in names:
			wifiProfile = dict()
			profileInfo = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
			if re.search("Security key           : Absent",profileInfo):
				continue
			else:
				wifiProfile["ssid"] = name
				wifiProfilePassword = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()	
				password = re.search("Key Content            : (.*)\r",wifiProfilePassword)
				if password == None:
					wifiProfile["password"] = None
				else:
					wifiProfile["password"] = password[1]
				wifilist.append(wifiProfile)
				
	print("\n\nA már ismert és mentett hálózatok:\n");				
	for x in range(len(wifilist)):
		print(wifilist[x])
	print("\n\n\tKész.");

else:
	print("NOT SUPPORTED");