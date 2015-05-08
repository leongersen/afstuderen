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

			serialConnectButton.innerHTML = 'Connect';
			serialConnectSelect.disabled = false;
			directSerialInput.disabled = true;

		} else {

			serialConnectButton.innerHTML = 'Disconnect';
			serialConnectSelect.disabled = true;
			directSerialInput.disabled = false;
			connectSerialPort(serialConnectSelect.value);
		}
	}

	function autoClearIsSet ( ) {
		return !!directSerialClearInput.checked;
	}


	function sendSerialMessage ( message ) {

		message += '\r\n';

		chrome.serial.send(connectedSerialPort, str2ab(message), onSerialSend);

		appendLog(message);

		if ( autoClearIsSet() ) {
			directSerialInput.value = "";
		}
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

		serialConnectSelect.appendChild(optionNode);
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

		sendSerialMessage(this.value);
	}

	chrome.serial.onReceive.addListener(onSerialReceive);

	var serialConnectSelect = document.getElementById('serialConnectSelect'),
		serialConnectButton = document.getElementById('serialConnectButton'),

		directSerialSendButton = document.getElementById('directSerialSendButton'),
		directSerialInput = document.getElementById('directSerialInput'),
		directSerialMonitor = document.getElementById('directSerialMonitor'),
		directSerialClearInput = document.getElementById('directSerialClearInput');
		directSerialClearButton = document.getElementById('directSerialClearButton');

	chrome.serial.getDevices(onGetDevices);

	serialConnectButton.addEventListener('click', connectedPortUI);

	directSerialSendButton.addEventListener('click', function(){
		sendSerialMessage(directSerialInput.value);
	});

	directSerialClearButton.addEventListener('click', function(){
		directSerialMonitor.innerHTML = "";
	});

	directSerialInput.addEventListener('keyup', onDirectEnter);

}());
