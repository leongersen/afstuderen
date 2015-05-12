import GPS
import MOD
import SER

# Set serial BAUD rate
SER.set_speed('115200')

SER.send('Start custom imports\n')

import Module
SER.send('Imported Module\n')

Module.CPUclock(3) # Clock to 104Mhz
SER.send('Ramped up CPU\n')

import Config
SER.send('Imported Config\n')

import Gauge
SER.send('Imported Gauge\n')

import Storage
SER.send('Imported Storage\n')

SER.send('Done importing\n')

def getComposedMessage ( ):
	return '["%s"]' % GPS.getActualPosition()

def updateSettings ( response ):

	SER.send(response)

	# Push to Fix mode, interval. Use setting from control panel;
	#GPS.powerSavingMode(2, Config.IntervalGPS)

# Throws all messages since boot on the serial port
def logOut ( ):
	
	SER.send('\n\n<LOG>')

	while 1:
		message = Storage.read()
		if message == 0:
			break

		dataLen = len(message)

		# To prevent overflowing the serial buffer,
		# Chunk the result if it is overly long.
		if ( dataLen > 1000 ):
			SER.send(message[0:1000])
			MOD.sleep(1)
			SER.send(message[1000:])
		else:
			SER.send(message)

	SER.send('</LOG>\n\n')

# Stores a message
def storeMessage ( message ):
	Storage.write(message)

# Handles socket state and transmits a message using GPRS
def transmitMessage ( message ):

	# If the socket is not open, we'll dial.
	if Module.socketIsSuspended() == 0:

		SER.send('Dail socket')

		if Module.socketDail( Config.API ) == 0:
			pass # Failed to open a socket.

	elif Module.socketResume() == 0:
		SER.send('Failed socket resume\n')

	response = Module.makeRequest("/", message)

	if ( response == 0 ):
		pass # The request failed.
	else:
		updateSettings(response)

	if ( Module.sendEscapeSequence() == 0 ):
		pass # Failed to escape, not in command mode.





# Set error reporting to numeric;
Module.enableErrorReporting()
SER.send('Done enableErrorReporting\n')

# Don't send the (+++) escape sequence when suspending a socket;
Module.skipEscape()
SER.send('Done skipEscape\n')

# Unlock SIM card by entering PIN;
Module.unlockSIM()
SER.send('Done unlockSIM\n')

# Flow control is not connected;
Module.disableFlowControl()
SER.send('Done disableFlowControl\n')

# Test module only;
Module.activeGPSAntenna()
SER.send('Done activeGPSAntenna\n')

if ( Module.attachNetwork() == 0 ):
	SER.send('Failed attachNetwork\n')
SER.send('Done attachNetwork\n')

if ( Module.connectNetwork( Config.APN ) == 0 ):
	SER.send('Failed connectNetwork\n')
SER.send('Done connectNetwork\n')

SER.send('Starting initialization at: %s\n' % MOD.secCounter())

sector = Storage.initialize()
SER.send('End at: %s. Sector: %s\n' % (MOD.secCounter(), sector))

Module.CPUclock(0) # Clock back to default (@26Mhz)
SER.send('CPU back down\n')

count = 0

while 1:

	received = SER.read()

	SER.send("Read: %s\n" % received)

	if received.find('QUIT') == 0:
		break
	elif received.find('LOG') == 0:
		Module.CPUclock(3)
		logOut()
		Module.CPUclock(0)

	message = getComposedMessage()
	SER.send("Message: %s\n" % message)

	SER.send('Message count: %s\n' % count)
	storeMessage(message)
	count = count + 1

	#transmitMessage(message)

	MOD.sleep(5);

SER.send('Stopping execution\n')
