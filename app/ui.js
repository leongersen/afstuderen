
	var menu = document.getElementById('menu'),
		nav = document.getElementById('nav');

	menu.addEventListener('click', function(){
		nav.classList.toggle('visible');
	});

	var modeSelectionName = document.getElementById('modeSelectionName'),
		modeSelectionPannel = document.getElementById('modeSelectionPannel'),
		modeSelectionClose = document.getElementById('modeSelectionClose'),
		intervalSelection = document.getElementById('intervalSelection'),
		modeSelectioRadios = document.getElementsByName('modeSelection');

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

	function toggleModeSelection ( ) {
		modeSelectionPannel.classList.toggle('visible');
	}

	function getConfigString ( ) {

		var config = 'CONFIG:,';

		config += getSelectedMode();
		config += ',';
		config += intervalSelection.value;
		config += ',';

		return config;
	}

	modeSelectionName.addEventListener('click', toggleModeSelection);
	modeSelectionClose.addEventListener('click', toggleModeSelection);

//CONFIG. readout, config.split(','); setSelectedMode(config[1]), intervalSelection.value = config[2]
//
////google.maps.event.addDomListener(window, 'load', );
//
//window.onload = function ( ) {
//	buildMap(JSON.parse(dummyCoords));
//};

	var webview = document.getElementById('viewport');

	webview.addEventListener('contentload', loaded);

	function loaded() {
		webview.contentWindow.postMessage(dummyCoords, '*')
	}
