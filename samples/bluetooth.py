import SER
import MOD

SER.set_speed('38400')
MOD.sleep(100)
SER.send('AT+UART=115200,1,0\r\n')
MOD.sleep(10)
SER.send('AT+UART?\r\n')
out = SER.read()


SER.set_speed('115200')
MOD.sleep(100)
SER.send(out)
SER.send('\nEND')
