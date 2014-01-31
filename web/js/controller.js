/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 * ----------------------------------------------------------------------------
 */
 
Hammer.plugins.fakeMultitouch();

function open (e) 	{ $("#DebugMsgList").append("<p>Connect!</p>"); $("#ToggleCxnStatus").removeClass("buttonErr"); };
function close(e) 	{ $("#DebugMsgList").append("<p>Connection Closed!</p>"); $("#ToggleCxnStatus").addClass("buttonErr"); };
function msg  (e) 	{ $("#DebugMsgList").append("<p>Received: "+ e.data + "</p>"); };
function error(e)  	{ $("#Status").text("Error");			};

$(document).ready(function(){
    $("#CxnStatus p").remove();
    $("#CxnStatus button").before("<p>Host:" + document.URL + "</p>");
    $("#CxnStatus button").before("<p>Websocket:" + address + "</p>");
    var qrcode = new QRCode(document.getElementById("CxnQR"), document.URL);
    try {
        if (address != "" ||  address != "$address") {
            var s = new WebSocket(address);
            s.onopen = open;
            s.onclose = close;
            s.onmessage = msg;
            s.onerror = error;
        }
    } catch (ex) {
        console.log("Socket exception:", ex);
        $("#Status").text("Error");
    }
    $(".ctrlBtn").mousedown( function () {
        var data = {"Actuator":$(this).attr("id"), };
        s.send(JSON.stringify(data));
    }).mouseup(function(){
		var data = {"Stop":"All", };
        s.send(JSON.stringify(data));
	});
    $("#ToggleCxnStatus").click( function() { 
        $("#PopWrapHead > h3").text("Cxn Status");
        $("#DebugInfo").hide();
        $("#CxnStatus").show();
        $("#PopWrap").fadeIn();
    });
	$("#ToggleDebugInfo").click( function() { 
        $("#PopWrapHead > h3").text("Messages");
        $("#DebugInfo").show();
        $("#CxnStatus").hide();
        $("#PopWrap").fadeIn();
    });
    $("#ResetModel").mouseup(function() { s.send(JSON.stringify({"Reset":true}));});
    $("#PopWrapCloseBtn").click(function(){ $("#PopWrap").fadeOut(); });
    $("#DebugMsgListBtn").click(function(){ $("#DebugMsgList").empty(); });
    $("#CxnStatusDiscxnBtn").click(function(){ s.close(1000, "Try to Close"); });
    $("#ToggleControl").click( function() {
        $("#SwipeControl").fadeToggle();
        $("#ButtonControl").fadeToggle();
        $(this).text();
    });

    // // start!
    var element = document.getElementById('SwipeControl');
    var hammertime = Hammer(element, {
            prevent_default: true,
            no_mouseevents: true
    }).on("tap", function(event) {
            $("#SwipeEvent").text("tap");
        }).on("swipeleft", function(event) {
            $("#SwipeEvent").text("swipeleft");
        }).on("swiperight", function(event) {
            $("#SwipeEvent").text("swiperight");
        }).on("swipedown", function(event) {
            $("#SwipeEvent").text("swipedown");
        }).on("swipeup", function(event) {
            $("#SwipeEvent").text("swipeup");
        }).on("pinchin", function(event) {
            $("#SwipeEvent").text("pinchin");
        }).on("pinchout", function(event) {
            $("#SwipeEvent").text("pinchout");
        }).on("rotate", function(event) {
            $("#SwipeEvent").text("rotate");
        });


});


