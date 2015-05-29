import IIC

IICbus = IIC.new(6, 9, 0x36)
IICbus.init()

def getBatteryVoltage ( ):
	R_VCELL = IICbus.readwrite('\x02', 2)
	VCELL_LSB = ord(R_VCELL[1]) >> 4
	VCELL_MSB = ord(R_VCELL[0]) << 4
	return VCELL_MSB + VCELL_LSB

def getStateOfCharge ( ):
	R_SOC = IICbus.readwrite('\x04', 2)
	# Ignore the decimals for now
	return ord(R_SOC[0])
