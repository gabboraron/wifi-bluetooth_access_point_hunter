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
	


	'''
	Ehhez a részhez ezt vettem alapul: https://www.geeksforgeeks.org/how-to-find-available-wifi-networks-using-python/
	másik megoldás: https://stackoverflow.com/a/3191659/6274697
	'''
	print("\n\nJelenleg elérhető hálózatok:\n");			
	commandOutput = subprocess.run(["netsh", "wlan", "show", "network", "mode=Bssid"], capture_output = True).stdout.decode()
	currentAvailableNetworksNames    = (re.findall("SSID \d : (.*)\r", commandOutput))
	#currentAvailableNetworksBSSID = (re.findall("         Signal             : (\d+)%\r", commandOutput))
	#currentAvailableNetworksStrength = (re.findall("         Signal             : (\d+)%\r", commandOutput))
	#print(currentAvailableNetworksNames);			
	for x in range(len(currentAvailableNetworksNames)):
		print(currentAvailableNetworksNames[x])

	print("\n\nEgyezések:\n");			
	for x in range(len(wifilist)):
		if wifilist[x]["ssid"] in currentAvailableNetworksNames:
			print(wifilist[x])

	print("\n\n\tKész.");
else:
	print("NOT SUPPORTED");