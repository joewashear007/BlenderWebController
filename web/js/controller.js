/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 * ----------------------------------------------------------------------------
 */
 
Hammer.plugins.fakeMultitouch();

function open (e) 	{ $("#DebugMsgList").append("<p>Connect!</p>"); $("#ToggleCxnStatus").removeClass("danger"); };
function close(e) 	{ $("#DebugMsgList").append("<p>Connection Closed!</p>"); $("#ToggleCxnStatus").addClass("danger"); };
function msg  (e) 	{ $("#DebugMsgList").append("<p>Received: "+ e.data + "</p>"); };
function error(e)  	{ $("#Status").text("Error");			};

$(document).ready(function(){
    //$("#CxnStatus p").remove();
    $("#CxnHTTPAddress").val(document.URL);
    $("#CxnWSAddress").val(address);
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
    })
    .on("tap",          function(event) { $("#SwipeEvent").text("tap");                                 })
    .on("dragleft",     function(event) { s.send(JSON.stringify({"Actuator":"RotateLeft", }));          })
    .on("dragright",    function(event) { s.send(JSON.stringify({"Actuator":"RotateRight", }));         })
    .on("dragdown",     function(event) { s.send(JSON.stringify({"Actuator":"RotateDown", }));          })
    .on("dragup",       function(event) { s.send(JSON.stringify({"Actuator":"RotateUp", }));            })
    .on("pinchin",      function(event) { s.send(JSON.stringify({"Actuator":"ZoomIn", }));              })
    .on("pinchout",     function(event) { s.send(JSON.stringify({"Actuator":"ZoomOut", }));             })
    .on("rotate",       function(event) { s.send(JSON.stringify({"Actuator":"ZRotateLeft", }));         })
    .on("release",      function(event) { s.send(JSON.stringify({"Stop":"All", }));                     });


});


