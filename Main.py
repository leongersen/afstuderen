import GPS
import MOD
import SER
import GPIO

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

	position = GPS.getActualPosition()
	voltage = Gauge.getBatteryVoltage()
	soc = Gauge.getStateOfCharge()

	return '["%s,%s,%s"]' % (position, voltage, soc)

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

# Allow external readSector changes
def setReadsector ( line ):
	SER.send('Setting readSector to: ')
	SER.send(line)
	SER.send('\n')

	settings = line.split(',')
	Storage.readSector = int(settings[1])

# Throws all messages since boot on the serial port
def generateLog ( ):

	SER.send('\n\n<LOG>')

	while 1:
		message = Storage.read()

		if message == 0:
			break

		SER.send(message[0:1000])
		MOD.sleep(2)
		SER.send(message[1000:])

	# Next time we'll be writing in a new sector.
	Storage.incrementActiveSector()

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
			return 0

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
		generateLog()
		Module.CPUclock(0)
	elif received.find('CONFIG') == 0:
		updateSettings(received[7:])
	elif received.find('STATE') == 0:
		SER.send("\nsessionStart: %s\nactiveSector: %s\nreadSector: %s\n\n" % (Storage.sessionStart, Storage.activeSector, Storage.readSector))
	elif received.find('READ') == 0:
		setReadsector(received)

	return 0

# Calls initialization
def setup ( ):
	initSettings()

	# Don't start the network on a missing battery
	if Gauge.getStateOfCharge() > 5:
		initNetworkRelated()

	SER.send('Starting storage initialization at: %s\n' % MOD.secCounter())
	sector = Storage.initialize()
	SER.send('End at: %s. Sector: %s\n' % (MOD.secCounter(), sector))

	Module.CPUclock(0) # Clock back to default (@26Mhz)
	SER.send('CPU back down\n')

setup()


count = 0

while 1:

	SER.send('\n\n\nReady.\n')

	if acceptCommandInput():
		break

	startTime = MOD.secCounter()

	# Get message
	message = getComposedMessage()
	SER.send("Message: %s\n" % message)

	# TODO: Remove this
	SER.send('Message count: %s\n' % count)
	count = count + 1

	SER.send('Mode is: %s\n' % Config.Mode)

	if Config.Mode == 'Active':
		transmitMessage(message)
	elif Config.Mode == 'Passive':
		storeMessage(message)
	elif Config.Mode == 'Buffered':
		SER.send('Buffered mode, todo!\n')

	endTime = MOD.secCounter()
	timeSpend = endTime - startTime
	sleepTime = Config.Interval - timeSpend

	SER.send("Spend: %s, Interval: %s, Sleep: %s\n" % (timeSpend, Config.Interval, sleepTime))
	SER.send("GPIO: %s, RTS: %s\n" % (GPIO.getIOvalue(2), SER.getRTS()))

	# Sleep, but only if the emergency button isn't set.
	if sleepTime > 2 and GPIO.getIOvalue(2) == 0:
		SER.send('Going into powerSaving.\n')
		MOD.powerSaving(sleepTime)
		SER.send("Woke up! Reason (0=ext,1=time): %s\n" % MOD.powerSavingExitCause())
	elif sleepTime > 0:
		SER.send('Idle sleep.\n')
		MOD.sleep(10 * sleepTime)
	else:
		pass # If sleepTime < 0: continue right away.

SER.send('Stopping execution\n')
