
	window.addEventListener("message", function(){
		buildGraph(JSON.parse(event.data));
	}, false);


	//google.setOnLoadCallback(drawChart);

	function drawChart( speed, sat, vcell, soc ) {

		var options = {
			legend: { position: 'top' }
		};

		var chart = new google.visualization.LineChart(document.getElementById('speed'));
		chart.draw(speed, options);

		var chart = new google.visualization.LineChart(document.getElementById('sat'));
		chart.draw(sat, options);

		var chart = new google.visualization.LineChart(document.getElementById('vcell'));
		chart.draw(vcell, options);

		var chart = new google.visualization.LineChart(document.getElementById('soc'));
		chart.draw(soc, options);
	}

	function buildGraph ( coords ) {

		var speedTable = new google.visualization.DataTable(),
			satTable = new google.visualization.DataTable(),
			vcellTable = new google.visualization.DataTable(),
			socTable = new google.visualization.DataTable(),
			speedSet = [],
			satSet = [],
			vcellSet = [],
			socSet = [];

		speedTable.addColumn('date', 'Time');
		speedTable.addColumn('number', 'Speed (km/h)');

		satTable.addColumn('date', 'Time');
		satTable.addColumn('number', 'Number of satellites');

		vcellTable.addColumn('date', 'Time');
		vcellTable.addColumn('number', 'Battery voltage (V)');

		socTable.addColumn('date', 'Time');
		socTable.addColumn('number', 'State of Charge (%)');

		coords.forEach(function( coord, index ){
			speedSet.push([new Date(coord[6]), Number(coord[3])]);
			satSet.push([new Date(coord[6]), Number(coord[7])]);
			vcellSet.push([new Date(coord[6]), Number(coord[5])]);
			socSet.push([new Date(coord[6]), Number(coord[4])]);
		});

		speedTable.addRows(speedSet);
		satTable.addRows(satSet);
		vcellTable.addRows(vcellSet);
		socTable.addRows(socSet);

		var formatter = new google.visualization.NumberFormat({pattern:'#.##'});
		formatter.format(vcellTable, 1);

		drawChart(speedTable, satTable, vcellTable, socTable);
	}
