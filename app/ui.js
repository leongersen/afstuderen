
	var menu = document.getElementById('menu'),
		nav = document.getElementById('nav');

	menu.addEventListener('click', function(){
		nav.classList.toggle('visible');
	});

	var modeSelectionName = document.getElementById('modeSelectionName'),
		modeSelectionPannel = document.getElementById('modeSelectionPannel'),
		modeSelectionClose = document.getElementById('modeSelectionClose');

	function toggleModeSelection ( ) {
		modeSelectionPannel.classList.toggle('visible');
	}

	modeSelectionName.addEventListener('click', toggleModeSelection);
	modeSelectionClose.addEventListener('click', toggleModeSelection);
