#!/usr/bin/env python3
import cgi

html_head = """<!DOCTYPE html>
               <html lang="en"><head>
                    <title>WebSocket Client</title>
                    <style>
                        form, button, input {
                            display:inline;
                           }
                    </style>
                </head>"""
html_body = """<body><form id="form" style="display:inline">
                <input type="text" id="message"><button type="submit">Send</button></form>
                <form id="close"><button>Close</button></form>
                <hr>
                <div id="output"></div>"""
def html_script(address):
            print("""<script>
            var inputBox = document.getElementById("message");
            var output = document.getElementById("output");
            var form = document.getElementById("form");
            var close = document.getElementById("close");
            try {
                var s = new WebSocket(""")
            print(address)
            print("""");
                console.log("Created Websocket");
                s.onopen = function (e) {
                    console.log("Socket opened.");
                };
                s.onclose = function (e) {
                    var p = document.createElement("p");
                    p.innerHTML = e.data;
                    output.appendChild(p);
                    console.log("Socket closed.");
                };
                s.onmessage = function (e) {
                    console.log("Socket message:", e.data);
                    var p = document.createElement("p");
                    p.innerHTML = e.data;
                    output.appendChild(p);
                };
                s.onerror = function (e) {
                    console.log("Socket error:", e);
                };
            } catch (ex) {
                console.log("Socket exception:", ex);
            }

            close.addEventListener("submit", function (e) {
                console.log("Closed Started");
                e.preventDefault();
                s.close(1000, "Try to Close");
            }, false)

            form.addEventListener("submit", function (e) {
                console.log("Form Submitted");
                e.preventDefault();
                s.send(inputBox.value);
                inputBox.value = "";
            }, false)
 
            </script>
             
            </body>
            </html>""")
def main():
    print("Content-type: text/html\n\n")
    try:
        f = open("address.txt", "r")
        address = f.read()
        f.close()
    except Exception as e:
        address = "ws://localhost:9999"
    print(html_head)
    print(html_body)
    html_script(address)
    
try:
    main() 
except:
    cgi.print_exception()   

