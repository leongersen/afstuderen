
	function buildMap ( coords ) {

		var bounds = new google.maps.LatLngBounds(), mainPoly = [], colors = ['blue', 'brown', 'green', 'orange', 'pink'], atColor = 0;

		coords.forEach(function( coord, index ){

			var position = new google.maps.LatLng(coord[0], coord[1]);

			mainPoly.push(position);
			bounds.extend(position);
			markers.push(new google.maps.Marker({
				position: position,
				map: map,
				title: '' + coord[2],
				icon: 'markers/' + colors[atColor] + '_MarkerA.png',
				zIndex: atColor + 2
			}));

			if ( coord[2] > 5 ) {
				atColor++;
			}
		});

		map.setCenter(new google.maps.LatLng(coords[0][0], coords[0][1]));
		map.fitBounds(bounds);

		var flightPath = new google.maps.Polyline({
			path: mainPoly,
			strokeColor: "#FF0000",
			strokeOpacity: 1.0,
			strokeWeight: 2
		});

		flightPath.setMap(map);
	}
