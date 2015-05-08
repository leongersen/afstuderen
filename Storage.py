import Interface as Interface

# Sector currently being written
activeSector = 0

# Page currently being written
activeCursor = 0

# First sector written in since initialization
sessionStart = 0


def end ():
	Interface.end()




def write ( value ):

	global activeSector
	global activeCursor

	# Start going through the value from the start
	positionInValue = 0

	# Stop when all characters have been written
	while positionInValue < len(value):

		# If the cursor was reset, clear the next sector before proceeding
		if activeCursor == 0:
			clearNextSector()

		# Number of bytes we can still fill
		remainingInPage = Interface.CHUNK_SIZE - (activeCursor % Interface.CHUNK_SIZE)

		# Get the part of the value that fits in the current page
		chunk = value[positionInValue:(positionInValue + remainingInPage)]
		chunkLength = len(chunk)

		Interface.writeData(activeSector, activeCursor, chunk)

		# Move pointers
		activeCursor = activeCursor + chunkLength
		positionInValue = positionInValue + chunkLength

		# Wrap both the page cursor and the sector pointer, if needed
		if activeCursor > Interface.SECTOR_SIZE - 1:
			activeCursor = 0
			activeSector = activeSector + 1
			if activeSector > Interface.SECTOR_COUNT - 1:
				activeSector = 0

# Clears the next sector, so there is always an empty one
def clearNextSector ( ):
	global activeSector

	next = activeSector + 1
	if next > Interface.SECTOR_COUNT - 1:
		next = 0

	Interface.eraseSector( next )

# Read all sectors since initialization
def read ( ):

	global sessionStart
	global activeSector

	set = []
	at = sessionStart

	# Can't really move this into while due to wrapping
	if at != activeSector:
		set.append( Interface.readSector(at) )

	while at != activeSector:

		at = at + 1
		if at >= Interface.SECTOR_COUNT:
			at = 0

		set.append( Interface.readSector(at) )

	# Ignore session start, we've read it
	sessionStart = activeSector

	return set

# Find the first empty sector
def initialize ( ):

	global activeSector
	global activeCursor
	global sessionStart

	sector = 0x00

	while 1:

		# Read at sector start
		fetch = Interface.readFirstSectorByte(sector)

		if fetch == 0xFF:
			break;

		sector = sector + 1

		# Wrap back to the first sector on overflow
		if sector > Interface.SECTOR_COUNT - 1:
			sector = 0x00
			break;

	activeSector = sector
	activeCursor = 0x00
	sessionStart = activeSector
