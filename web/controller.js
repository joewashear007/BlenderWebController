/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 * ----------------------------------------------------------------------------
 */

/* -------------------------- Global Varibles ---------------------------- */ 
var s = null;
var somekeyDown = 0;
var isMaster = false;

window.onbeforeunload = close;

/* -------------------------- Websocket Fucntions ---------------------------- 
 Functions used to handel the connection, opening, closing sendgin, and reciveing of the websocket
*/ 
function log(msg, title ){
    if(typeof(title)==='undefined') title="Message" ;
    $("#DebugMsgList").prepend('<li><h3>'+title+'</h3><p>'+ msg +'</p></li>').listview( "refresh" );
}
function open (e) 	{ 
	log("Connected!"); 
	$(".ErrMsg").fadeOut();
};
function close(e) 	{ 
	log("Connection Closed!"); 
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
	$(".ErrMsg").text("Error! - Check Msg").fadeIn();	
};
function send(key,msg,speed){
    if(typeof(speed)==='undefined') speed = 0.001;
    var raw_data = {};
    raw_data[key] = msg;
    raw_data["Speed"] = speed;
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
        $(".ctrlBtn").addClass('ui-disabled');
        $(".ErrMsg").text("Locked").fadeIn();	
    }else{
        $(".ctrlBtn").removeClass('ui-disabled');
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
    $("#DebugMsgList").listview({create: function( event, ui ) {}} );
	toggleConnection();
	$("#CxnQR").qrcode(document.URL);
    
    // ---------------- UI Button Events ---------------------------------

    $("#ToggleCxnBtn")   .click( toggleConnection );
    $(".MasterLock")     .click( toggleLockCommand ); 
    $("#DebugMsgListBtn").click( function() { $("#DebugMsgList").empty();   });
    $("a").bind("contextmenu", function(e) {         e.preventDefault();    });
    $("button").bind("contextmenu", function(e) {         e.preventDefault();    });
    //------------------ Control events ----------------------------------
    
    //Arrow Button click event
    //$(".ctrlBtn").on("mousedown vmousedown tap",  function(e) {  e.preventDefault(); send("Actuator", $(this).attr("id"), $("#btn_speed").val()/1000 );  })
    //             .on("mouseup mouseleave vmouseup vmouseout",  function() { send("Stop", "All");                   });
    $(".ctrlBtn").on("vmousedown ",  function(e) {  e.preventDefault(); send("Actuator", $(this).attr("id"), $("#btn_speed").val()/1000 );  })
                 .on("vmouseup ",  function() { send("Stop", "All");                   });
    // Reset Button
    $(".ResetModel").mousedown(    function() { send("Reset", true);                })
                    .mouseup  (    function() { send("Stop", "All");                });

    // Swipe Control
    var element = document.getElementById('SwipeControl');
    var hammertime = Hammer(element, {
            prevent_default: true,
            no_mouseevents: true,
            transform_always_block: true
    })
    .on("tap",          function(event) { send("Stop"    , "All" ); })
    .on("release",      function(event) { send("Stop"    , "All" ); })
    .on("dragleft",     function(event) { send("Actuator", "RotateLeft" , ($("#swipe_speed").val()/1000)    );  event.gesture.stopDetect();})
    .on("dragright",    function(event) { send("Actuator", "RotateRight", ($("#swipe_speed").val()/1000)    );  event.gesture.stopDetect();})
    .on("dragdown",     function(event) { send("Actuator", "RotateDown" , ($("#swipe_speed").val()/1000)    );  event.gesture.stopDetect();})
    .on("dragup",       function(event) { send("Actuator", "RotateUp"   , ($("#swipe_speed").val()/1000)    );  event.gesture.stopDetect();})
    .on("pinchin",      function(event) { send("Actuator", "ZoomIn"     , ($("#swipe_speed").val()/1000)    );  event.gesture.stopDetect();})
    .on("pinchout",     function(event) { send("Actuator", "ZoomOut"    , ($("#swipe_speed").val()/1000)    );  event.gesture.stopDetect();})
    .on("rotate",       function(event) { if(event.gesture.rotation < 0 ){
                                                send("Actuator", "ZRotateLeft", ($("#swipe_speed").val()/1000)    ); 
                                          }else{ 
                                                send("Actuator", "ZRotateRight", ($("#swipe_speed").val()/1000)   ); }
                                          event.gesture.stopDetect();
                                        });
    
    
    
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


