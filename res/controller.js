/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <joewashear007@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Joseph Livecchi
 * ----------------------------------------------------------------------------
 */
 
Hammer.plugins.fakeMultitouch();

function open (e) 	{ $("#Status").text("Connected"); 		};
function close(e) 	{ $("#Status").text("Closed");			};
function msg  (e) 	{ $(".debug").append("<p>Received: "+ e.data + "</p>"); };
function error(e)  	{ $("#Status").text("Error");			};
$(document).ready(function(){
    try {
        if (address != "" ) {
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
    $("button").click( function () {
        if( $(this).attr("id") == "Status")	{	s.close(1000, "Try to Close");	}
        else 								{	s.send($(this).attr("id"));		}
    });
    $("#DebugTitle").click( function() {
        $(".debug").toggle();
    });
    $("#toggleControl").click( function() {
        $("#SwipeControl").fadeToggle();
        $("#ButtonControl").fadeToggle();
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
