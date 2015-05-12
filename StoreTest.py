import SER
import MOD

SER.set_speed('115200')
SER.send('Starting\n')

import Storage

SER.send('Imported storage\n')

SER.send('Starting at: %s\n' % MOD.secCounter())
sector = Storage.initialize()
SER.send('Endint at: %s. Sector: %s\n' % (MOD.secCounter(), sector))

SER.send('Done initialize\n\n\n')

Storage.readSector = 102

# Can't do assignment in condition
while 1:
	data = Storage.read()

	if data == 0:
		break

	dataLen = len(data)

	# To prevent overflowing the serial buffer,
	# Chunk the result if it is overly long.
	if ( dataLen > 1000 ):
		SER.send(data[0:1000])
		MOD.sleep(1)
		SER.send(data[1000:])
	else:
		SER.send(data)

SER.send('\n\nEnd\n')
