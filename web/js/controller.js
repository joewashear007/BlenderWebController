/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 * ----------------------------------------------------------------------------
 */

/* -------------------------- Global Varibles ---------------------------- */ 
Hammer.plugins.fakeMultitouch();
var s = null;
var somekeyDown = 0;
var isMaster = false;

window.onbeforeunload = close;

/* -------------------------- Websocket Fucntions ---------------------------- 
 Functions used to handel the connection, opening, closing sendgin, and reciveing of the websocket
*/ 
function log(msg, title="Message" ){
    $("#DebugMsgList").listview({create: function( event, ui ) {}} );
    $("#DebugMsgList").prepend('<li><h3>'+title+'</h3><p>'+ msg +'</p></li>').listview( "refresh" );
}
function open (e) 	{ 
	log("Connected!"); 
	$("#ToggleCxnStatus").removeClass("danger"); 
	$(".ErrMsg").fadeOut();
};
function close(e) 	{ 
	log("Connection Closed!"); 
	$("#ToggleCxnStatus").addClass("danger"); 
	$(".ErrMsg").text("Not Connected").fadeIn();
};
function msg  (e) 	{ 
    msg_data = JSON.parse(e.data);
    if (msg_data.hasOwnProperty("SLAVE")){ toggleSlave(msg_data["SLAVE"]); }
    if (msg_data.hasOwnProperty("MASTER_STATUS")){
        isMaster = msg_data["MASTER_STATUS"];
        styleMaster();
    }
	log(e.data);
};
function error(e)  	{ 
	log("Error: "+ e ); 
	$("#ToggleCxnStatus").addClass("danger"); 
	$(".ErrMsg").text("Error! - Check Msg").fadeIn();	
};
function send(key,msg){
    var raw_data = {};
    raw_data[key] = msg;
    var data = JSON.stringify(raw_data);
    if(s){
       s.send(data);
    }else{
        log("Event: "+ data);
    }
}
function toggleConnection() {
    //Opens and closes a conenction using the address in #CxnWSAddress
	if(s){
		s.close(1000, "Try to Close");
		$("#ToggleCxnBtn").text("Connect");
		s = null;
	}else{
		try {
            address = $("#CxnWSAddress").val();
			if (address != "" ||  address != "$address") {
				s = new WebSocket(address);
				s.onopen = open;
				s.onclose = close;
				s.onmessage = msg;
				s.onerror = error;
				$("#ToggleCxnBtn").text("Disconnect");
			}
		} catch (ex) {
			error("Could Not Connected");
		}
	}
}
function toggleLockCommand()    {    send("MASTER_REQUEST", !isMaster );  }
function toggleSlave(locked)    {   
    //Toogle the control of all commands with locked status
    if(locked){
        $(".ctrlBtn").attr("disabled", true)
        $(".ErrMsg").text("Locked").fadeIn();	
    }else{
        $(".ctrlBtn").attr("disabled", false);
        $(".ErrMsg").text("Locked").fadeOut();
    }
}
function styleMaster(){ 
    if(isMaster){
        log("You are now Master"); 
        $(".MasterLock").addClass("danger");
    }else{
        $(".MasterLock").removeClass("danger");
    }
    
}

/* -------------------------- Document Ready Function ---------------------------- 
 Main function, Handels all events, swipe, and keybord control
 Makes the QR code
*/ 

$(document).ready(function(){
    $("#CxnHTTPAddress").val(document.URL);
    $("#CxnWSAddress").val(address);
	toggleConnection();
	
    var qrcode = new QRCode(document.getElementById("CxnQR"), document.URL);
    
    // ---------------- UI Button Events ---------------------------------
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
    $("#ToggleCxnBtn")   .click( toggleConnection );
    $("#MasterLock")     .click( toggleLockCommand ); 
    $("#PopWrapCloseBtn").click( function() { $("#PopWrap").fadeOut();      });
    $("#DebugMsgListBtn").click( function() { $("#DebugMsgList").empty();   });
    $("#ToggleControl")  .click( function() {
        $("#SwipeControl").fadeToggle();
        $("#ButtonControl").fadeToggle();
        $(this).text();
    });
    $("a").bind('taphold', function(event) {
        event.preventDefault();
    });
    //------------------ Control events ----------------------------------
    
    //Arrow Button click event
    $(".ctrlBtn").mousedown(    function() { send("Actuator", $(this).attr("id"));  })
                 .mouseup  (    function() { send("Stop", "All");                   });
    // Reset Button
    $(".ResetModel").mousedown(    function() { send("Reset", true);                })
                    .mouseup  (    function() { send("Stop", "All");                });

    // Swipe Control
    var element = document.getElementById('SwipeControl');
    var hammertime = Hammer(element, {
            prevent_default: true,
            no_mouseevents: true
    })
    .on("tap",          function(event) { send("Stop"    , "All"            );  })
    .on("dragleft",     function(event) { send("Actuator", "RotateLeft"     );  })
    .on("dragright",    function(event) { send("Actuator", "RotateRight"    );  })
    .on("dragdown",     function(event) { send("Actuator", "RotateDown"     );  })
    .on("dragup",       function(event) { send("Actuator", "RotateUp"       );  })
    .on("pinchin",      function(event) { send("Actuator", "ZoomIn"         );  })
    .on("pinchout",     function(event) { send("Actuator", "ZoomOut"        );  })
    .on("rotate",       function(event) { send("Actuator", "ZRotateLeft"    );  })
    .on("release",      function(event) { send("Stop"    , "All"            );  });
    
    //Keyboard Events
    $(document).keydown( function(event) {
        //Left Arrow
        if ( event.which == 37 && !somekeyDown)
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZRotateLeft" ) : send("Actuator", "RotateLeft" ); }
        // Up Arrow 
        if ( event.which == 38 && !somekeyDown) 
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZoomOut" ) :send("Actuator", "RotateUp" ); }
        //Right Arrow
        if ( event.which == 39 && !somekeyDown) 
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZRotateRight" ) :send("Actuator", "RotateRight" ); }
        //Down Arrow    
        if ( event.which == 40 && !somekeyDown) 
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZoomIn" ) :send("Actuator", "RotateDown" ); }
        // Esccape Keyboard
        if ( event.which == 27 && !somekeyDown) 
            { somekeyDown = true; toggleConnection(); }   
    });
    $(document).keyup( function(event) { send("Stop", "All"); somekeyDown = false; });
});


