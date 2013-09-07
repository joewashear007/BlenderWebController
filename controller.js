$(document).ready(function(){
	try {
		if (address == ""){
			address = "ws://192.168.1.100:9999/";
		}
		var s = new WebSocket(address);
		//$(".debug").append("<p>Created Web socket</p>");
		s.onopen = function (e) {
			//$(".debug").append("<p>Socket Opened</p>");
			$("#Status").text("Connected");
		};
		s.onclose = function (e) {
			//$(".debug").append("<p>Socket Closed: " + e.data+" </p>");
			$("#Status").text("Closed");
		};
		s.onmessage = function (e) {
			$(".debug").append("<p>Received: "+ e.data + "</p>");
		};
		s.onerror = function (e) {
			//$(".debug").append("<p>Web socket Error!: " + e + "</p>");
			$("#Status").text("Error");
		};
	} catch (ex) {
		console.log("Socket exception:", ex);
		$("#Status").text("Error");
	}
	$("button").click( function () {
		if( $(this).attr("id") == "Status"){
			s.close(1000, "Try to Close");
		} else {
			//$(".debug").append("<p>Click: " + $(this).attr("id") + "</p>" )
			s.send($(this).attr("id"));
		}
	});
	$("#DebugTitle").click( function() {
		$(".debug").toggle();
	});
});
