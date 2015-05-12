(function(){

	// Array buffer to string
	function ab2str ( buf ) {
		return String.fromCharCode.apply(null, new Uint8Array(buf));
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



	var connectedSerialPort = null, logBuffer = false;

	// UI:
	function connectedPortUI ( connect ) {

		if ( connectedSerialPort ) {

			chrome.serial.disconnect(connectedSerialPort, function(){});
			connectedSerialPort = null;

			serialConnectButton.innerHTML = 'Connect';
			serialConnectSelect.disabled = false;
			directSerialInput.disabled = true;

		} else if ( connect !== false ) {

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

		var data = ab2str(info.data);

		//console.log(logBuffer, info, data);

		if ( logBuffer !== false ) {

			logBuffer += data;

			if ( data.indexOf('</LOG>') != -1 ) {

				// Find valid JSON;
				var parse = logBuffer.substring(logBuffer.indexOf('['), logBuffer.lastIndexOf(']') + 1);
				// Remove line breaks, add comma separation to JSON, trim trailing comma;
				parse = parse.replace(/(\r\n|\n|\r)/gm, '').replace(/\]/g, '],').slice(0, -1);

				console.log(parse);
				logBuffer = false;
			}

		} else {
			appendLog(data);
		}
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

	//chrome.app.window.current().contentWindow.onblur = connectedPortUI.bind(null, false);


	var directStartLog = document.getElementById('directStartLog'),
		directQuit = document.getElementById('directQuit'),
		directRunScript = document.getElementById('directRunScript');

	directStartLog.addEventListener('click', function(){
		logBuffer = '';
		sendSerialMessage('LOG');
	});
	directQuit.addEventListener('click', sendSerialMessage.bind(null, 'QUIT'));
	directRunScript.addEventListener('click', sendSerialMessage.bind(null, 'AT#EXECSCR'));

}());
