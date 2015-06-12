chrome.app.runtime.onLaunched.addListener(function() {

	chrome.app.window.create('window.html', {
		frame: "none",
		bounds: { width: 900, height: 650 }
	});
});
