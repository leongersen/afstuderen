count = []
scount = []
data = []

SECTOR_COUNT = 150
SECTOR_SIZE = 32
CHUNK_SIZE = 8


def end():
	print scount
	for w in count:
		print w




def keepCount ( a, b ):
	global count
	count[a][b] = count[a][b] + 1

for i in range(0, SECTOR_COUNT):
	data.append([0xFF] * SECTOR_SIZE)
	count.append([0] * SECTOR_SIZE)
	scount.append(0)

def eraseSector ( sector_address ):
	global data

	# track sector erases
	global scount
	scount[sector_address] = scount[sector_address] + 1

	data[sector_address] = [0xFF] * SECTOR_SIZE

def writeData ( sector_address, cursor_address, value ):
	global data

	index = 0;
	for c in value:
		keepCount(sector_address, cursor_address + index)
		data[sector_address][cursor_address + index] = c
		index = index + 1

def readFirstSectorByte ( sector_address ):
	global data
	return data[sector_address][0]

def readSector ( sector_address ):
	return "".join(data[sector_address])
