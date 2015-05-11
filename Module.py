import MDM
import MOD
import SER

CRLF = "\r\n"
CONNECTED_HOST = ""

# Command handling

def _command (command, timeout = 5):

    # Clear input buffer before reading
    MDM.receive(1)

    MDM.send(command, 5)
    MDM.send(CRLF, 5)

    #SER.send("%s \n" % (command))

    return MOD.secCounter() + timeout

# Checks if any of the string in the 'targets' array are in the response,
# returns [array index of that string, response] or 0 on failure.
def _target (targets, timeout):
    res = ""

    while ( MOD.secCounter() < timeout ):

        res = res + MDM.receive(1)
        index = 0

        for target in targets:
            if ( res.rfind(target) != -1 ):
                return [index, res]
            index = index + 1

    return 0

def DIcommand (command, target, timeout = 5):
    timeout = _command(command, timeout)
    return _target([target], timeout)

def ATcommand (command, timeout = 5):
    timeout = _command(command, timeout)
    out = _target(["OK", "ERROR"], timeout)
    if ( out == 0 or out[0] == 1 ):
        return 0
    return out[1]


# One time settings and initialisation

def activeGPSAntenna ( ):
    return ATcommand('AT$GPSAT=1')

def enableErrorReporting ( ):
    return ATcommand('AT+CMEE=1')

def skipEscape ( ):
    return ATcommand('AT#SKIPESC=1')

def CPUclock ( clockSet ):
	return ATcommand("AT#CPUMODE=%s" % clockSet)

def unlockSIM ( PIN = "0000" ):

    state = ATcommand("AT+CPIN?")

    # It failed
    if ( state == 0 ):
        return 0;

    if ( state.rfind("SIM PIN") != -1 ):
        return ATcommand("AT+CPIN=%s" % PIN) != 0

    return 0

def attachNetwork ( checks = 10 ):

    # Request network attachment, then check if it works.

    ATcommand("AT+CGATT=1")

    while ( checks ):

        state = ATcommand("AT+CGATT?")

        if ( state == 0 ):
            checks = 0
            break

        if ( state.rfind("+CGATT: 1") != -1 ):
            break

        checks = checks - 1
        MOD.sleep(5)

    return checks != 0

def disableFlowControl ( ):
    return ATcommand("AT&K=0") # There is no read command, and it doesn't hurt to write it again.

def connectNetwork ( APN ):

    state = ATcommand("AT#SGACT?")

    # Leave if already active
    if ( state.rfind("#SGACT: 1,1") != -1 ):
        return 1 # was already attached

    ATcommand("AT#SGACT=1,0")
    ATcommand("AT+CGDCONT=1,\"IP\",%s,\"0.0.0.0\",0,0" % APN)

    return ATcommand("AT#SGACT=1,1") != 0


# Socket Handling

# Send escape sequence. Returns success. Might not be successful, as it may be send outside a request;
def sendEscapeSequence ( ):

    # Module doesn't care if it isn't in data mode
    # Must sleep AT LEAST  1 sec before and after escape sequence
    MOD.sleep(12)
    MDM.send("+++", 5)
    MOD.sleep(12)

    timeout = MOD.secCounter() + 5
    return _target(["OK"], timeout) != 0

# Dails into a socket; Returns success;
def socketDail ( host, port = 80 ):
    global CONNECTED_HOST
    CONNECTED_HOST = host
    return DIcommand("AT#SD=1,0,%s,\"%s\"" % (port, host), "CONNECT", 10) != 0

# Check the status of a socket; Returns 1 when socket 1 is suspended;
def socketIsSuspended ( ):
    return DIcommand("AT#SS=1", "#SS: 1,2", 5) != 0

# Resumes a suspended socket. Returns success;
def socketResume ( ):
    return DIcommand("AT#SO=1", "CONNECT", 5) != 0


# Networking

# Returns the content in a HTTP response, or integer 0 on timeout;
def receiveReponse ( ):

    timeout = MOD.secCounter() + 10

    str = ""
    length = ""
    newlinepos = 0

    while ( MOD.secCounter() < timeout ):

        newlinepos = str.find("\n\r")

        if ( (newlinepos != -1) and not length ):

            newlinepos = newlinepos + 2
            pos = str.find("Content-Length:") + 15

            while ( str[pos] != '\n' ):
                length = "%s%s" % (length, str[pos])
                pos = pos + 1

            length = int(length) + newlinepos

        else:
            MOD.sleep(5)
            str = str + MDM.receive(1)

        if ( length and len(str) >= length ):
            return str[newlinepos:(newlinepos+length)]

    return 0

# Make a POST request, sending the content to the connected host. Returns response;
def makeRequest ( path, content ):

    MDM.receive(1)

    message = ("POST %s HTTP/1.1\n"
        "Host: %s\n"
        "Content-Type: application/json\n"
        "Content-Length: %s\n"
        "\n"
        "%s") % (path, CONNECTED_HOST, len(content), content)

    MDM.send(message, 5)
    MDM.send(CRLF, 5)

    response = receiveReponse()

    return response
