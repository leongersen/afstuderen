(function(){

	// Array buffer to string
	function ab2str ( buf ) {
		var bufView = new Uint8Array(buf);
		var encodedString = String.fromCharCode.apply(null, bufView);
		return decodeURIComponent(escape(encodedString));
	}

	// String to array buffer
	function str2ab ( str ) {
		var encodedString = unescape(encodeURIComponent(str));
		var bytes = new Uint8Array(encodedString.length);
		for (var i = 0; i < encodedString.length; ++i) {
			bytes[i] = encodedString.charCodeAt(i);
		}
		return bytes.buffer;
	}



	var connectedSerialPort = null;

	// UI:
	function connectedPortUI ( ) {
		if ( connectedSerialPort ) {
			chrome.serial.disconnect(connectedSerialPort, function(){});
			connectedSerialPort = null;
			serialButton.innerHTML = 'Connect';
			serialSelect.disabled = false;
			directSerialInterface.disabled = true;
		} else {
			serialButton.innerHTML = 'Disconnect';
			serialSelect.disabled = true;
			directSerialInterface.disabled = false;
			connectSerialPort(serialSelect.value);
		}
	}


	function sendSerialMessage ( message ) {
		chrome.serial.send(connectedSerialPort, str2ab(message), onSerialSend);
		appendLog(message);
	}

	function appendLog ( message ) {
		directSerialMonitor.innerHTML += message;
		directSerialMonitor.scrollTop = directSerialMonitor.scrollHeight;
	}





	// UI: create options for all available serial ports
	function createPortOption ( port ) {
		var optionNode = document.createElement("option");
		optionNode.value = port.path;
		optionNode.innerHTML = port.path;

		serialSelect.appendChild(optionNode);
	}

	// Connect to a serial port
	function connectSerialPort ( path ) {
		chrome.serial.connect(path, {
			bitrate: 115200,
			dataBits: "eight",
			parityBit: "no",
			stopBits: "one",
			ctsFlowControl: false
		}, onSerialConnect);
	}



	function onGetDevices ( ports ) {
		ports.forEach(createPortOption);
	}

	function onSerialReceive ( info ) {
		console.log(info);
		console.log(ab2str(info.data));
		appendLog(ab2str(info.data));
	}

	function onSerialSend ( sendInfo ){
		console.log(sendInfo);
	}

	function onSerialConnect ( connectionInfo ) {
		connectedSerialPort = connectionInfo.connectionId;
	}

	function onSerialDisconnect ( ) {


	}

	function onDirectEnter ( event ) {

		if ( event.keyCode !== 13 ) {
			return;
		}

		sendSerialMessage(this.value + '\r\n');
		this.value = "";
	}

	chrome.serial.onReceive.addListener(onSerialReceive);

	var serialSelect = document.getElementById('serialSelect'),
		serialButton = document.getElementById('serialButton'),
		directSerialInterface = document.getElementById('directSerialInterface'),
		directSerialMonitor = document.getElementById('directSerialMonitor');

	chrome.serial.getDevices(onGetDevices);

	serialButton.addEventListener('click', connectedPortUI);
	directSerialInterface.addEventListener('keyup', onDirectEnter);

}());
