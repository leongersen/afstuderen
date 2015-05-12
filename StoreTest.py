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

SER.send('Sector: %s\n' % sector)
SER.send('ReadSector: %s\n' % Storage.readSector)
SER.send('activeSector: %s\n' % Storage.activeSector)

Storage.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam facilisis elit vitae ex mollis consequat. Nunc eu sapien ipsum. Morbi urna sapien, dapibus eu lectus eget, malesuada pretium arcu. Praesent vehicula mi eu mauris consectetur, sit amet sodales nisi rhoncus. Donec eu sollicitudin mi. Sed et lacus congue sem iaculis tincidunt. Donec nec lorem ac velit commodo ullamcorper. Suspendisse nulla felis, sodales at sodales vitae, scelerisque a urna. Suspendisse mollis eros non risus semper porttitor. Quisque quis nunc ornare purus massa nunc. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam facilisis elit vitae ex mollis consequat. ")

Storage.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ac ligula vitae nibh placerat ullamcorper ut id ipsum. Nunc vehicula ligula quis ex lacinia, et viverra arcu posuere. Fusce pretium sapien odio, in blandit sapien efficitur eget. Aliquam sagittis imperdiet nunc vel convallis. Duis fermentum nisl et vestibulum suscipit. Nullam eget orci eleifend, euismod massa non, molestie turpis. Vivamus tortor elit, tempor vel urna at, semper laoreet nibh. Phasellus tristique efficitur metus vitae suscipit. Praesent eget nisi at massa cras amet. Nunc vehicula ligula quis ex lacinia, et viverra arcu posuere. ")

SER.send('ReadSector: %s\n' % Storage.readSector)
SER.send('activeSector: %s\n' % Storage.activeSector)
SER.send('--------------------\n')

# Can't do assignment in condition
while 1:
	data = Storage.read()
	if data == 0:
		break
	SER.send(data)
	SER.send('\n\n\n')

SER.send('\n\nEnd\n')
