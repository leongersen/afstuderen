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

# Builds message from peripherals
def getComposedMessage ( ):
	return '["%s"]' % GPS.getActualPosition() # TODO add gauge, and current sense

# Write settings to config
def updateSettings ( line ):
	SER.send('Updating settings to: ')
	SER.send(line)
	SER.send('\n')

	# Ignore any message that is *way* too long
	if (len(line) > 50):
		return 0

	settings = line.split(',')

	# settings[0] is 'reserved'
	Config.Mode = settings[1]
	Config.Interval = int(settings[2])

def chunkSectorMessage ( message ):
	dataLen = len(message)

	# To prevent overflowing the serial buffer,
	# Chunk the result if it is overly long.
	if ( dataLen > 2000 ):
		SER.send(message[0:2000])
		MOD.sleep(3)
		SER.send(message[2000:])
	else:
		SER.send(message)

# Throws all messages since boot on the serial port
def logOut ( ):

	SER.send('\n\n<LOG>')

	while 1:
		message = Storage.read()
		if message == 0:
			message = Storage.readActive()
			chunkSectorMessage(message)
			break

		chunkSectorMessage(message)

		#SER.send('\n')
		#MOD.sleep(5)

	SER.send('</LOG>\n\n')

# Stores a message
def storeMessage ( message ):
	Storage.write(message)

# Handles socket state and transmits a message using GPRS
def transmitMessage ( message ):

	# If the socket is not open, we'll dial.
	if Module.socketIsSuspended() == 0:

		SER.send('Dail socket, state is: %s\n' % Module.ATcommand('AT#SS=1'))

		if Module.socketDail( Config.API ) == 0:
			SER.send('Failed to open a socket\n')

	elif Module.socketResume() == 0:
		SER.send('Failed socket resume\n')

	response = Module.makeRequest("/", message)

	if ( response == 0 ):
		SER.send('Request failed\n')
	else:
		updateSettings(response)

	if ( Module.sendEscapeSequence() == 0 ):
		SER.send('Failed to escape, not in command mode\n')

	return 0

# Configure general device settings
def initSettings ( ):
	# Set error reporting to numeric;
	Module.enableErrorReporting()
	SER.send('Done enableErrorReporting\n')

	# Don't send the (+++) escape sequence when suspending a socket;
	Module.skipEscape()
	SER.send('Done skipEscape\n')

	# Flow control is not connected;
	Module.disableFlowControl()
	SER.send('Done disableFlowControl\n')

	# Test module only;
	Module.activeGPSAntenna()
	SER.send('Done activeGPSAntenna\n')

# Attach to the GPRS network
def initNetworkRelated ( ):

	# Unlock SIM card by entering PIN;
	Module.unlockSIM()
	SER.send('Done unlockSIM\n')

	if ( Module.attachNetwork() == 0 ):
		SER.send('Failed attachNetwork\n')
	SER.send('Done attachNetwork\n')

	if ( Module.connectNetwork( Config.APN ) == 0 ):
		SER.send('Failed connectNetwork\n')
	SER.send('Done connectNetwork\n')

# Read the serial port, see if the user wants something
def acceptCommandInput ( ):

	received = SER.read()

	SER.send("Read: %s\n" % received)

	if received.find('QUIT') == 0:
		return 1
	elif received.find('LOG') == 0:
		Module.CPUclock(3)
		logOut()
		Module.CPUclock(0)
	elif received.find('CONFIG') == 0:
		updateSettings(received[7:])
	elif received.find('STATE') == 0:
		SER.send("\nsessionStart: %s\nactiveSector: %s\nreadSector: %s\n\n" % (Storage.sessionStart, Storage.activeSector, Storage.readSector))

	return 0

# Calls initialization
def setup ( ):
	initSettings()
	initNetworkRelated()

	SER.send('Starting storage initialization at: %s\n' % MOD.secCounter())
	sector = Storage.initialize()
	SER.send('End at: %s. Sector: %s\n' % (MOD.secCounter(), sector))

	Module.CPUclock(0) # Clock back to default (@26Mhz)
	SER.send('CPU back down\n')

setup()


count = 0

while 1:

	if acceptCommandInput():
		break

	startTime = MOD.secCounter()

	# Get message
	message = getComposedMessage()
	SER.send("Message: %s\n" % message)
	SER.send('Message count: %s\n' % count)
	count = count + 1

	SER.send('Mode is: %s\n' % Config.Mode)

	if Config.Mode == 'Active':
		transmitMessage(message)
	elif Config.Mode == 'Passive':
		storeMessage(message)
	elif Config.Mode == 'Buffered':
		SER.send('Buffered mode, todo!\n')

	SER.send('Ready, sleep check.\n')

	endTime = MOD.secCounter()
	timeSpend = endTime - startTime
	sleepTime = Config.Interval - timeSpend

	SER.send("Spend: %s\nInterval: %s\nSleep: %s\n" % (timeSpend, Config.Interval, sleepTime))

	if sleepTime > 4:
		MOD.powerSaving(sleepTime)
		SER.send("Woke up! Reason: %s\n" % MOD.powerSavingExitCause())
	elif sleepTime > 0:
		MOD.sleep(10 * sleepTime)
	else:
		pass # If sleepTime < 0 we'll continue right away.

SER.send('Stopping execution\n')
