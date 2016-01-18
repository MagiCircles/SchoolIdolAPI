
function initialize() {
    var googleMapOptions = {
	zoom: zoom,
	center: center
    };

    var map = new google.maps.Map(document.getElementById("map-canvas"), googleMapOptions);
    var oms = new OverlappingMarkerSpiderfier(map);
    var infowindow = new google.maps.InfoWindow();
    oms.addListener('click', function(marker, event) {
	infowindow.close();
	infowindow.setContent(marker.contentString);
	infowindow.open(map, marker);
    });
    oms.addListener('spiderfy', function(markers) {
	infowindow.close();
    });
    $.each(addresses, function(idx, address) {
	addMarker(map, address, oms);
    });
}

google.maps.event.addDomListener(window, 'load', initialize);

function addMarker(map, address, oms) {
    var contentString = '<div id="content"><h4 id="firstHeading" class="firstHeading"><a href="/user/' + address.username + '/" target="_blank"><img alt="' + address.username + '" src="' + address.avatar + '" width="50" height="50" style="corner-radius: 10px"><br>' + address.username + '</a></h4><div id="bodyContent"><p>' + address.location + '</p></div></div>';
    var marker = new google.maps.Marker({
	position: address.latlong,
	map: map,
	title: address.username,
	icon: new google.maps.MarkerImage(address.icon, null, null, null, new google.maps.Size(45, 45)),
    });
    marker.contentString = contentString;
    oms.addMarker(marker);
}

$(document).ready(function() {
    var ctx = $("#agechart").get(0).getContext("2d");
    var chart = new Chart(ctx).Line(data);
});
