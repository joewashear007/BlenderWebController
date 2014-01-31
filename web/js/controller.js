/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 * ----------------------------------------------------------------------------
 */
 
//Hammer.plugins.fakeMultitouch();

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
});


function getEl(id) {
    return document.getElementById(id);
}


var log_elements = {};
var prevent_scroll_drag = true;

function getLogElement(type, name) {
    var el = log_elements[type + name];
    if(!el) {
        return log_elements[type + name] = getEl("log-"+ type +"-"+ name);
    }
    return el;
}

// log properties
var properties = ['gesture','center','deltaTime','angle','direction',
    'distance','deltaX','deltaY','velocityX','velocityY', 'pointerType',
    'scale','rotation','touches','target'];

function logEvent(ev) {
    if(!ev.gesture) {
        return;
    }

    // add to the large event log at the bottom of the page
    var log = [this.id, ev.type];
    //event_log.innerHTML = log.join(" - ") +"\n" + event_log.innerHTML;

    // highlight gesture
    var event_el = getLogElement('gesture', ev.type);
    event_el.className = "active";


    for(var i= 0,len=properties.length; i<len; i++) {
        var prop = properties[i];
        var value = ev.gesture[prop];
        switch(prop) {
            case 'center':
                value = value.pageX +"x"+ value.pageY;
                break;
            case 'gesture':
                value = ev.type;
                break;
            case 'target':
                value = ev.gesture.target.tagName;
                break;
            case 'touches':
                value = ev.gesture.touches.length;
                break;
        }
        getLogElement('prop', prop).innerHTML = value;
    }
}


// get all the events
var all_events = [];
$("#events-list li").each(function() {
    var li = $(this);
    var type = li.text();
    li.attr("id", "log-gesture-"+type);
    all_events.push(type);
});


// start!
var hammertime = Hammer(getEl('SwipeBox'), {
        prevent_default: true,
        no_mouseevents: true
    })
    .on(all_events.join(" "), logEvent);
