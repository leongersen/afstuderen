import SPI
import GPIO
import MOD
#import SER

#SER.set_speed('115200')

# SPI.new(SCLK_pin, MOSI_pin, MISO_pin, <SS0>, <SS1>,�<SS7>)
SPIobj = SPI.new(8, 10, 5, 7)

# SPI.init (CPOL, CPHA, <SSPOL>, <SS>)
SPIobj.init(0, 0, 0, 0)

SECTOR_COUNT = 0x7FF
SECTOR_SIZE = 0xFFF
CHUNK_SIZE = 128

# Address from INT to 3 bytes
def mbytewrap ( b1, b2 ):
	merge = (b1 << 12) | b2
	return chr((merge & 0xFF0000) >> 16) + chr((merge & 0x00FF00) >> 8) + chr(merge & 0x0000FF)

def writeEnable ( ):
	SPIobj.readwrite('\x06')

def eraseSector ( sector_address ):
	addr = mbytewrap(sector_address, 0x00)
	msg = '\x20%s' % addr

	writeEnable()
	writ = SPIobj.readwrite(msg)
	MOD.sleep(3) # Stay within safeties for sector erase (abs.max 450ms)
	return writ

def writeData ( sector_address, cursor_address, value ):
	addr = mbytewrap(sector_address, cursor_address)
	msg = '\x02%s%s' % (addr, value)

	writeEnable()
	return SPIobj.readwrite(msg)

def readFirstSectorByte ( sector_address ):
	#SER.send('A: %s\n' % sector_address)
	addr = mbytewrap(sector_address, 0x00)
	msg = '\x03' + addr
	read = SPIobj.readwrite(msg, 7)
	#SER.send('B: %s\n' % SPIobj.readwrite('\x0500'))
	#SER.send('C: %s\n' % read)
	return ord(read[5])

def readSector ( sector_address ):
	x = ''
	n = 0x000

	while ( n <= 0xF80 ):
		read = SPIobj.readwrite('\x03' + mbytewrap(sector_address, n), 132)
		read = read[4:]

		# Stop reading if the remainder of the sector is empty
		if ord(read[0]) == 0xFF:
			break

		x = x + read
		n = n + 0x080;

	return x
