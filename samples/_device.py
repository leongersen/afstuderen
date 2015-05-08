import SER
import MOD

SER.set_speed('115200')
SER.send('Starting\n')

import storage

SER.send('Import storage\n')

SER.send('Starting at: %s\n' % MOD.secCounter())
storage.initialize()
SER.send('Endint at: %s\n' % MOD.secCounter())

SER.send('Done initialize\n')

storage.write("a b c d e f g h i j k l m n o p q r s t u v w x y z")
SER.send('Done write 1')

storage.write("1 2 3 4 5 6 7 8 9 0")
SER.send('Done write 2')

SER.send(storage.read())
SER.send('End')
