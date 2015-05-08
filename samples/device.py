import SER
import MOD

SER.set_speed('115200')
SER.send('Starting\n')

import interface

#ra = interface.readFirstSectorByte(0x00)

interface.readSector(0x00)

SER.send('End\n')
