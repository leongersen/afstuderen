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

Storage.write("a b c d e f g h i j k l m n o p q r s t u v w x y z")
SER.send('Done write 1\n')

Storage.write("1 2 3 4 5 6 7 8 9 0")
SER.send('Done write 2\n')

SER.send("".join(Storage.read()))
SER.send('End')
