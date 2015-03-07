
var center = new google.maps.LatLng(30, -40);

function initialize() {
    var googleMapOptions = {
	zoom: 2,
	center: center
    };

    map = new google.maps.Map(document.getElementById("map-canvas"), googleMapOptions);
    $.each(addresses, function(idx, address) {
	addMarker(map, address);
    });
}

google.maps.event.addDomListener(window, 'load', initialize);

function addMarker(map, address) {
    var contentString = '<div id="content"><h4 id="firstHeading" class="firstHeading"><a href="/user/' + address.username + '/" target="_blank"><img alt="' + address.username + '" src="' + address.avatar + '" width="50" height="50" style="corner-radius: 10px"><br>' + address.username + '</a></h4><div id="bodyContent"><p>' + address.location + '</p></div></div>';
    var infowindow = new google.maps.InfoWindow({
	content: contentString
    });
    var marker = new google.maps.Marker({
	position: address.latlong,
	map: map,
	title: 'Uluru (Ayers Rock)'
    });
    google.maps.event.addListener(marker, 'click', function() {
	infowindow.open(map,marker);
    });
}
