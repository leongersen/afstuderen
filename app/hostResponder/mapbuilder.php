<!DOCTYPE html>
<script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
<script src="map.js"></script>
<div id="map-canvas"></div>
<style>
	html, body, #map-canvas {
		height: 100%;
		margin: 0px;
		padding: 0px
	}
</style>
<script>

	var map, markers = [], mapOptions = {
		zoom: 16,
		center: new google.maps.LatLng(-34.397, 150.644)
	};

	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	window.addEventListener("message", function(){
		buildMap(JSON.parse(event.data));
	}, false);

</script>
