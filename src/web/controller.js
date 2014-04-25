/*
# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/* -------------------------- Global Varibles ---------------------------- */ 
var s = null;
var somekeyDown = 0;
var isMaster = false;
var ipRegex = /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})/;
window.onbeforeunload = close;

/* -------------------------- Websocket Fucntions ---------------------------- 
 Functions used to handel the connection, opening, closing sendgin, and reciveing of the websocket
*/ 
function log(msg){
    $("#DebugMsgList").prepend('<li><p>'+ msg +'</p></li>').listview( "refresh" );
    console.log("MESSAGE: " + msg);
}
function open (e) 	{
    log("Connected!");
    $("#ToggleCxnBtn").text("Disconnect");
	$(".ErrMsg").fadeOut();
};
function close(e) 	{ 
	log("Connection Closed!"); 
    $("#ToggleCxnBtn").text("Connect");
	$(".ErrMsg").text("Not Connected").fadeIn();
};
function msg  (e) 	{ 
    var msg_data = JSON.parse(e.data);
    if (msg_data.hasOwnProperty("BUTTONS")){ addCustomButtons(msg_data.BUTTONS ); }
    if (msg_data.hasOwnProperty("SLAVE")){ toggleSlave(msg_data.SLAVE); }
    if (msg_data.hasOwnProperty("MASTER_STATUS")){
        isMaster = msg_data.MASTER_STATUS;
        styleMaster();
    }
	log(e.data);
};
function error(e)  	{ 
	log("Error: "+ e );
    $("#ToggleCxnBtn").text("Connect");    
	$(".ErrMsg").text("Error! - Check Msg").fadeIn();	
};
function send(key,msg,speed){
    var raw_data = {};
    raw_data[key] = msg;
    if(typeof(speed)!=='undefined')
    	raw_data["Speed"] = speed;
    var data = JSON.stringify(raw_data);
    if(s){
       s.send(data);
    }else{
        log("Event: "+ data);
    }
}
function toggleConnection() {
    /*Opens and closes a conenction using the address in #CxnWSAddress*/
	if(s){
		s.close(1000, "Try to Close");
		s = null;
	}else{
		try {
            address = $("#CxnWSAddress").val();
			if ( ipRegex.test(address)) {
				s = new WebSocket(address);
				s.onopen = open;
				s.onclose = close;
				s.onmessage = msg;
				s.onerror = error;
			}
		} catch (ex) {
			error("Could Not Connected");
		}
	}
}
function toggleLockCommand()    {    send("MASTER_REQUEST", !isMaster );  }
function toggleSlave(locked)    {   
    /*Toogle the control of all commands with locked status*/
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
function addCustomButtons(buttonJSON){
    var buttons = '<div data-role="controlgroup" data-type="horizontal" data-mini="true">';
    $.each(buttonJSON, function(index, obj) {
        if(obj.text == "" || obj.action == "")
            buttons += '</div><div data-role="controlgroup" data-type="horizontal" data-mini="true">';
        else
            buttons += '<a class="ui-btn ui-corner-all ui-shadow actionBtn" id="'+obj.action+'">'+obj.text+'</a>';
    });
    buttons += '</div>';
    $(".customButtons").html(buttons);
    log("Added Custom Buttons");
}
/* -------------------------- Document Ready Function ---------------------------- 
 Main function, Handels all events, swipe, and keybord control
 Makes the QR code
*/ 

$(document).ready(function(){
    $("#CxnHTTPAddress").val(document.URL);
    $("#CxnWSAddress").val(address);
    $("#CxnQR").qrcode(document.URL);
    $("#DebugMsgList").listview({create: function( event, ui ) {}} );
	toggleConnection();
	
    
    /* ---------------- UI Button Events --------------------------------- */

    $("#ToggleCxnBtn")   .click( toggleConnection );
    $(".MasterLock")     .click( toggleLockCommand ); 
    $("#DebugMsgListBtn").click( function() { $("#DebugMsgList").empty();   });
    
    $("a")     .bind("contextmenu", function(e) {         e.preventDefault();    });
    $("button").bind("contextmenu", function(e) {         e.preventDefault();    });
    /* ------------------ Control events ---------------------------------- */
    $("body").on("vmousedown ",  ".ctrlBtn",   function(e) { e.preventDefault(); send("Actuator", $(this).attr("id"), $("#btn_speed").val()/1000 );  });
    $("body").on("vmousedown ", ".actionBtn",  function(e) { e.preventDefault(); send("Actuator", $(this).attr("id"));  });
    $("body").on("mouseup",     "a,button",    function()  { send("Stop", "All");                });
    $(".ResetModel").mousedown(    function() { send("Reset", true);                });
    

    /* ---------------- Swipe Control --------------------- */
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
    
    /* -------------- KEyboard Events ----------------------- */
    $(document).keydown( function(event) {
        if ( event.which == 37 && !somekeyDown)
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZRotateLeft" ) : send("Actuator", "RotateLeft" ); }
        if ( event.which == 38 && !somekeyDown) 
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZoomOut" ) :send("Actuator", "RotateUp" ); }
        if ( event.which == 39 && !somekeyDown) 
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZRotateRight" ) :send("Actuator", "RotateRight" ); }
        if ( event.which == 40 && !somekeyDown) 
            { event.preventDefault(); somekeyDown = true; event.shiftKey ? send("Actuator", "ZoomIn" ) :send("Actuator", "RotateDown" ); }
        if ( event.which == 27 && !somekeyDown) 
            { somekeyDown = true; toggleConnection(); }   
    });
    $(document).keyup( function(event) { send("Stop", "All"); somekeyDown = false; });
});


