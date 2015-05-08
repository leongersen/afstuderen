import SPI
import SER

SER.set_speed('115200')
SER.send('Starting\n')

# SPI.new(SCLK_pin, MOSI_pin, MISO_pin, <SS0>, <SS1>,…<SS7>)
SPIobj = SPI.new(7, 5, 3, 9)

# SPI.init (CPOL, CPHA, <SSPOL>, <SS>)
SPIobj.init(0, 0, 0, 0)

a = '\x9F'
b = '\x00'
c = '\x00'

data = SPIobj.readwrite(a, 10)

SER.send('Data: %s\n' % data)
SER.send('End\n')
