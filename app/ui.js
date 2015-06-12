
	var IMEI = '355255042061441',
		menu = document.getElementById('menu'),
		nav = document.getElementById('nav'),
		webview = document.getElementById('viewport'),
		mapLoader = new Promise(function( resolve, reject ){
			webview.addEventListener('contentload', resolve);
		});

	menu.addEventListener('click', function(){
		nav.classList.toggle('visible');
	});

	var modeSelectionName = document.getElementById('modeSelectionName'),
		modeSelectionPannel = document.getElementById('modeSelectionPannel'),
		modeSelectionClose = document.getElementById('modeSelectionClose'),
		intervalSelection = document.getElementById('intervalSelection'),
		modeSelectioRadios = document.getElementsByName('modeSelection'),
		datePicker = document.getElementById('datePicker');
		datePickerSelect = document.getElementById('datePickerSelect');

	webview.addEventListener('consolemessage', function(e) {
	  console.log('Guest page logged a message: ', e.message);
	});

	function initDateSelection ( ) {

		var request = new XMLHttpRequest();
		request.open('GET', 'http://track.refreshless.com/' + IMEI + '/dates', true);

		request.onload = function() {
			var data = JSON.parse(request.responseText);
			data.forEach(function(d){
				var optionNode = document.createElement("option");
				optionNode.value = d;
				optionNode.innerHTML = d;

				datePickerSelect.appendChild(optionNode);
			});

			datePickerSelect.addEventListener('change', onDateSelectionChange);
			datePicker.classList.add('visible');
		};

		request.send();
	}

	function onDateSelectionChange ( ) {

		if ( datePickerSelect.value === '-' ) {
			return;
		}

		var request = new XMLHttpRequest();
		request.open('GET', 'http://track.refreshless.com/' + IMEI + '/sessions/' + datePickerSelect.value, true);

		request.onload = function() {
			mapLoader.then(function(){
				webview.contentWindow.postMessage(request.responseText, '*');
			});
		}

		request.send();
	}

	function postLog ( data ) {

		var request = new XMLHttpRequest();

		request.open('POST', 'http://track.refreshless.com/' + IMEI + '/track', true);
		request.setRequestHeader('Content-Type', 'application/json');

		request.onload = function() {
			console.log(request.responseText);
		};

		request.send(data);
	}

	function getSelectedMode ( ) {
		for ( var i = 0; i < modeSelectioRadios.length; i++ ) {
			if ( modeSelectioRadios[i].checked ){
				return modeSelectioRadios[i].value;
			}
		}
	}

	function setSelectedMode ( val ) {
		for ( var i = 0; i < modeSelectioRadios.length; i++ ) {
			modeSelectioRadios[i].checked = modeSelectioRadios[i].value === val;
		}
	}

	function parseConfig ( config ) {

		config = config.split(',');

		console.log(config);

		IMEI = config[0];
		setSelectedMode(config[1]);
		intervalSelection.value = config[2];
	}

	function toggleModeSelection ( ) {
		modeSelectionPannel.classList.toggle('visible');
	}

	function getConfigString ( ) {

		var config = 'CONFIG:,';

		config += getSelectedMode();
		config += ',';
		config += intervalSelection.value;
		config += ',';

		var request = new XMLHttpRequest();
		request.open('POST', 'http://track.refreshless.com/' + IMEI + '/config', true);
		request.send(config);

		return config;
	}


	initDateSelection();

	modeSelectionName.addEventListener('click', toggleModeSelection);
	modeSelectionClose.addEventListener('click', toggleModeSelection);
	modeSelectionClose.addEventListener('click', writeConfig);
