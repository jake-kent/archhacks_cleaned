google.charts.load('current', { 'packages': ['map'] });
google.charts.setOnLoadCallback(drawMap);

var vis_data = [['Lat', 'Lng', 'School', 'Marker']]
var wash_U_index = 0;

$.getJSON("static/data/school_locs5.json", function(json) {
	for (var i = 0; i < json.length; i++){
		var marker = 'default';
		if (json[i].school == 'Washington University in St. Louis'){
			wash_U_index = i;
			// marker = 'washu'
		}
		vis_data.push([json[i].lat, json[i].lng, json[i].school+" ("+json[i].application_count+")", marker]);
	}
	if (vis_data.length > 400){
		console.log("Too many schools, over API limit");
	}
});

function drawMap() {
	var data = google.visualization.arrayToDataTable(vis_data);
	var options = {
		key: 'AIzaSyC8p1li5Zv09yIOJkFBu-_8ZikGnw8aTCY',
		showTip: true,
		zoomLevel: 4,
		enableScrollWheel: true,
		mapType: 'hybrid',
		icons: {
			// 'washu': {
			//     normal: 'icon.png',
			//     selected: 'icon.png'
			// }
		}
	 };
	var map = new google.visualization.Map(document.getElementById('map_div'));
	google.visualization.events.addOneTimeListener(map, 'ready', function(){ 
		map.setSelection([{row:wash_U_index, column:null}]);
	});
	map.draw(data, options);
};