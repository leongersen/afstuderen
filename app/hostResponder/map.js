
	var map, markers = [], flightPath, mapOptions = {
		zoom: 7,
		streetViewControl: false,
		center: new google.maps.LatLng(52.255553, 5.535402)
	};

	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	window.addEventListener("message", function(){
		buildMap(JSON.parse(event.data));
	}, false);

	function clearMap ( ) {
		for (var i = 0; i < markers.length; i++) {
			markers[i].setMap(null);
		}
		markers = [];

		if ( flightPath ) {
			flightPath.setMap(null);
		}
	}

	function buildMap ( coords ) {

		clearMap();

		var bounds = new google.maps.LatLngBounds(),
			mainPoly = [], colors = ['blue', 'brown', 'darkgreen','green', 'orange', 'paleblue', 'pink', 'purple', 'red', 'yellow'],
			atColor = 0;

		coords.forEach(function( coord, index ){

			var position = new google.maps.LatLng(coord[0], coord[1]);

			mainPoly.push(position);
			bounds.extend(position);
			markers.push(new google.maps.Marker({
				position: position,
				map: map,
				title: 'Count: ' + coord[2] +
						' speed: ' + coord[3] +
						' SOC: ' + coord[4] +
						' VCELL: ' + coord[5],
				icon: '/markers/' + colors[atColor % 10] + '_MarkerA.png',
				zIndex: atColor + 2
			}));

			if ( coord[2] > 10 ) {
				atColor++;
			}
		});

		map.setCenter(new google.maps.LatLng(coords[0][0], coords[0][1]));
		map.fitBounds(bounds);

		flightPath = new google.maps.Polyline({
			path: mainPoly,
			strokeColor: "#FF0000",
			strokeOpacity: 1.0,
			strokeWeight: 2
		});

		flightPath.setMap(map);
	}
