import SER
import MOD

SER.set_speed('115200')
SER.send('Starting\n')

import Storage

SER.send('Imported storage\n')

SER.send('Starting at: %s\n' % MOD.secCounter())
sector = Storage.initialize()
SER.send('Endint at: %s. Sector: %s\n' % (MOD.secCounter(), sector))

SER.send('Done initialize\n')

# Can't do assignment in condition
while 1:
	data = Storage.read()
	if data == 0:
		break
	SER.send(data)
	SER.send('\n')

SER.send('End\n')
