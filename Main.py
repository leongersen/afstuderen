import GPS
import MOD
import SER

# Set serial BAUD rate
SER.set_speed('115200')

SER.send('Start custom imports\n')

import Module
SER.send('Imported Module\n')

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

def sendData ( data ):

	# If the socket is not open, we'll dial.
	if Module.socketIsSuspended() == 0:

		SER.send('Dail socket')

		if Module.socketDail( Config.API ) == 0:
			pass # Failed to open a socket.

	elif Module.socketResume() == 0:
		SER.send('Failed socket resume\n')

	response = Module.makeRequest("/", data)

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

while 1:

	received = SER.read()

	SER.send("Read: %s\n" % received)

	if received.find('QUIT') == 0:
		break
	elif received.find('LOG') == 0:
		break

	message = getComposedMessage()
	SER.send("Message: %s\n" % message)
	
	#sendData(message)



	MOD.sleep(10);

SER.send('END')
