#! /usr/bin/env python3

# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



import tempfile
import http.server
import threading
import os
import socket
import socketserver
import base64
import hashlib
import struct
import shutil
import webbrowser
import json
from io import StringIO
from string import Template

def writeWebsite(file, new_address):
	site_part1 = """<!DOCTYPE html> <html lang=en> <head> <meta charset=utf-8> <meta name=viewport content="width=device-width, user-scalable=no, initial-scale=1, height=device-height" /> <title>BlenderWebController</title> <link rel=stylesheet href=http://cdnjs.cloudflare.com/ajax/libs/jquery-mobile/1.4.1/jquery.mobile.min.css /> <style>html{font-size:100%}body,input,select,textarea,button,.ui-btn{font-size:1em;line-height:1.3;font-family:sans-serif}legend,.ui-input-text input,.ui-input-search input{color:inherit;text-shadow:inherit}.ui-mobile label,div.ui-controlgroup-label{font-weight:normal;font-size:16px}.ui-field-contain{border-bottom-color:#828282;border-bottom-color:rgba(0,0,0,.15);border-bottom-width:1px;border-bottom-style:solid}.table-stroke thead th,.table-stripe thead th,.table-stripe tbody tr:last-child{border-bottom:1px solid #d6d6d6;border-bottom:1px solid rgba(0,0,0,.1)}.table-stroke tbody th,.table-stroke tbody td{border-bottom:1px solid #e6e6e6;border-bottom:1px solid rgba(0,0,0,.05)}.table-stripe.table-stroke tbody tr:last-child th,.table-stripe.table-stroke tbody tr:last-child td{border-bottom:0}.table-stripe tbody tr:nth-child(odd) td,.table-stripe tbody tr:nth-child(odd) th{background-color:#eee;background-color:rgba(0,0,0,.04)}.ui-btn,label.ui-btn{font-weight:bold;border-width:1px;border-style:solid}.ui-btn:link{text-decoration:none!important}.ui-btn-active{cursor:pointer}.ui-corner-all{-webkit-border-radius:.6em;border-radius:.6em}.ui-btn-corner-all,.ui-btn.ui-corner-all,.ui-slider-track.ui-corner-all,.ui-flipswitch.ui-corner-all,.ui-li-count{-webkit-border-radius:.3125em;border-radius:.3125em}.ui-btn-icon-notext.ui-btn-corner-all,.ui-btn-icon-notext.ui-corner-all{-webkit-border-radius:1em;border-radius:1em}.ui-btn-corner-all,.ui-corner-all{-webkit-background-clip:padding;background-clip:padding-box}.ui-popup.ui-corner-all>.ui-popup-arrow-guide{left:.6em;right:.6em;top:.6em;bottom:.6em}.ui-shadow{-webkit-box-shadow:0 1px 2px rgba(255,255,255,0.5);-moz-box-shadow:0 1px 2px rgba(255,255,255,0.5);box-shadow:0 1px 2px rgba(255,255,255,0.5)}.ui-shadow-inset{-webkit-box-shadow:inset 0 1px 2px rgba(255,255,255,0.5);-moz-box-shadow:inset 0 1px 2px rgba(255,255,255,0.5);box-shadow:inset 0 1px 2px rgba(255,255,255,0.5)}.ui-overlay-shadow{-webkit-box-shadow:0 0 12px rgba(0,0,0,.6);-moz-box-shadow:0 0 12px rgba(0,0,0,.6);box-shadow:0 0 12px rgba(0,0,0,.6)}.ui-btn-icon-left:after,.ui-btn-icon-right:after,.ui-btn-icon-top:after,.ui-btn-icon-bottom:after,.ui-btn-icon-notext:after{background-color:#000;background-color:rgba(0,0,0,0.7);background-position:center center;background-repeat:no-repeat;-webkit-border-radius:1em;border-radius:1em}.ui-alt-icon.ui-btn:after,.ui-alt-icon .ui-btn:after,html .ui-alt-icon.ui-checkbox-off:after,html .ui-alt-icon.ui-radio-off:after,html .ui-alt-icon .ui-checkbox-off:after,html .ui-alt-icon .ui-radio-off:after{background-color:#000;background-color:rgba(0,0,0,.15)}.ui-nodisc-icon.ui-btn:after,.ui-nodisc-icon .ui-btn:after{background-color:transparent}.ui-shadow-icon.ui-btn:after,.ui-shadow-icon .ui-btn:after{-webkit-box-shadow:0 1px 0 rgba(255,255,255,.4);-moz-box-shadow:0 1px 0 rgba(255,255,255,.4);box-shadow:0 1px 0 rgba(255,255,255,.4)}.ui-btn.ui-checkbox-off:after,.ui-btn.ui-checkbox-on:after,.ui-btn.ui-radio-off:after,.ui-btn.ui-radio-on:after{display:block;width:18px;height:18px;margin:-9px 2px 0 2px}.ui-checkbox-off:after,.ui-btn.ui-radio-off:after{filter:Alpha(Opacity=30);opacity:.3}.ui-btn.ui-checkbox-off:after,.ui-btn.ui-checkbox-on:after{-webkit-border-radius:.1875em;border-radius:.1875em}.ui-radio .ui-btn.ui-radio-on:after{background-image:none;background-color:#fff;width:8px;height:8px;border-width:5px;border-style:solid}.ui-alt-icon.ui-btn.ui-radio-on:after,.ui-alt-icon .ui-btn.ui-radio-on:after{background-color:#000}.ui-icon-loading{background:url("images/ajax-loader.gif");background-size:2.875em 2.875em}.ui-bar-a,.ui-page-theme-a .ui-bar-inherit,html .ui-bar-a .ui-bar-inherit,html .ui-body-a .ui-bar-inherit,html body .ui-group-theme-a .ui-bar-inherit{background:#cdbfac;border-color:#f95806;color:#f60;text-shadow:0 0 5px #f5ede3;font-weight:bold}.ui-bar-a{border-width:1px;border-style:solid}.ui-overlay-a,.ui-page-theme-a,.ui-page-theme-a .ui-panel-wrapper{background:#f5ede3;border-color:#f60;color:#333;text-shadow:0 0 0 #000}.ui-body-a,.ui-page-theme-a .ui-body-inherit,html .ui-bar-a .ui-body-inherit,html .ui-body-a .ui-body-inherit,html body .ui-group-theme-a .ui-body-inherit,html .ui-panel-page-container-a{background:#fff;border-color:#154890;color:#333;text-shadow:0 2px 0 #f3f3f3}.ui-body-a{border-width:1px;border-style:solid}.ui-page-theme-a a,html .ui-bar-a a,html .ui-body-a a,html body .ui-group-theme-a a{color:#69f;font-weight:bold}.ui-page-theme-a a:visited,html .ui-bar-a a:visited,html .ui-body-a a:visited,html body .ui-group-theme-a a:visited{color:#38c}.ui-page-theme-a a:hover,html .ui-bar-a a:hover,html .ui-body-a a:hover,html body .ui-group-theme-a a:hover{color:#059}.ui-page-theme-a a:active,html .ui-bar-a a:active,html .ui-body-a a:active,html body .ui-group-theme-a a:active{color:#059}.ui-page-theme-a .ui-btn,html .ui-bar-a .ui-btn,html .ui-body-a .ui-btn,html body .ui-group-theme-a .ui-btn,html head+body .ui-btn.ui-btn-a,.ui-page-theme-a .ui-btn:visited,html .ui-bar-a .ui-btn:visited,html .ui-body-a .ui-btn:visited,html body .ui-group-theme-a .ui-btn:visited,html head+body .ui-btn.ui-btn-a:visited{background:#e1d4c0;border-color:#154890;color:#333;text-shadow:0 2px 0 #f3f3f3}.ui-page-theme-a .ui-btn:hover,html .ui-bar-a .ui-btn:hover,html .ui-body-a .ui-btn:hover,html body .ui-group-theme-a .ui-btn:hover,html head+body .ui-btn.ui-btn-a:hover{background:#cdbfac;border-color:#154890;color:#333;text-shadow:0 2px 0 #f3f3f3}.ui-page-theme-a .ui-btn:active,html .ui-bar-a .ui-btn:active,html .ui-body-a .ui-btn:active,html body .ui-group-theme-a .ui-btn:active,html head+body .ui-btn.ui-btn-a:active{background:#69f;border-color:#154890;color:#333;text-shadow:0 2px 0 #f3f3f3}.ui-page-theme-a .ui-btn.ui-btn-active,html .ui-bar-a .ui-btn.ui-btn-active,html .ui-body-a .ui-btn.ui-btn-active,html body .ui-group-theme-a .ui-btn.ui-btn-active,html head+body .ui-btn.ui-btn-a.ui-btn-active,.ui-page-theme-a .ui-checkbox-on:after,html .ui-bar-a .ui-checkbox-on:after,html .ui-body-a .ui-checkbox-on:after,html body .ui-group-theme-a .ui-checkbox-on:after,.ui-btn.ui-checkbox-on.ui-btn-a:after,.ui-page-theme-a .ui-flipswitch-active,html .ui-bar-a .ui-flipswitch-active,html .ui-body-a .ui-flipswitch-active,html body .ui-group-theme-a .ui-flipswitch-active,html body .ui-flipswitch.ui-bar-a.ui-flipswitch-active,.ui-page-theme-a .ui-slider-track .ui-btn-active,html .ui-bar-a .ui-slider-track .ui-btn-active,html .ui-body-a .ui-slider-track .ui-btn-active,html body .ui-group-theme-a .ui-slider-track .ui-btn-active,html body div.ui-slider-track.ui-body-a .ui-btn-active{background-color:#69f;border-color:#154890;color:#fff;text-shadow:1px 1px 1px #333}.ui-page-theme-a .ui-radio-on:after,html .ui-bar-a .ui-radio-on:after,html .ui-body-a .ui-radio-on:after,html body .ui-group-theme-a .ui-radio-on:after,.ui-btn.ui-radio-on.ui-btn-a:after{border-color:#69f}.ui-page-theme-a .ui-btn:focus,html .ui-bar-a .ui-btn:focus,html .ui-body-a .ui-btn:focus,html body .ui-group-theme-a .ui-btn:focus,html head+body .ui-btn.ui-btn-a:focus,.ui-page-theme-a .ui-focus,html .ui-bar-a .ui-focus,html .ui-body-a .ui-focus,html body .ui-group-theme-a .ui-focus,html head+body .ui-btn-a.ui-focus,html head+body .ui-body-a.ui-focus{-webkit-box-shadow:0 0 12px #69f;-moz-box-shadow:0 0 12px #69f;box-shadow:0 0 12px #69f}.ui-bar-b,.ui-page-theme-b .ui-bar-inherit,html .ui-bar-b .ui-bar-inherit,html .ui-body-b .ui-bar-inherit,html body .ui-group-theme-b .ui-bar-inherit{background:#e47297;border-color:#aa0114;color:#aa0114;text-shadow:0 0 5px #ffe9e8;font-weight:bold}.ui-bar-b{border-width:1px;border-style:solid}.ui-overlay-b,.ui-page-theme-b,.ui-page-theme-b .ui-panel-wrapper{background:#292929;border-color:#bbb;color:#292929;text-shadow:0 1px 0 #f3f3f3}.ui-body-b,.ui-page-theme-b .ui-body-inherit,html .ui-bar-b .ui-body-inherit,html .ui-body-b .ui-body-inherit,html body .ui-group-theme-b .ui-body-inherit,html .ui-panel-page-container-b{background:#292929;border-color:#fff;color:#333;text-shadow:0 1px 0 #f3f3f3}.ui-body-b{border-width:1px;border-style:solid}.ui-page-theme-b a,html .ui-bar-b a,html .ui-body-b a,html body .ui-group-theme-b a{color:#38c;font-weight:bold}.ui-page-theme-b a:visited,html .ui-bar-b a:visited,html .ui-body-b a:visited,html body .ui-group-theme-b a:visited{color:#38c}.ui-page-theme-b a:hover,html .ui-bar-b a:hover,html .ui-body-b a:hover,html body .ui-group-theme-b a:hover{color:#059}.ui-page-theme-b a:active,html .ui-bar-b a:active,html .ui-body-b a:active,html body .ui-group-theme-b a:active{color:#059}.ui-page-theme-b .ui-btn,html .ui-bar-b .ui-btn,html .ui-body-b .ui-btn,html body .ui-group-theme-b .ui-btn,html head+body .ui-btn.ui-btn-b,.ui-page-theme-b .ui-btn:visited,html .ui-bar-b .ui-btn:visited,html .ui-body-b .ui-btn:visited,html body .ui-group-theme-b .ui-btn:visited,html head+body .ui-btn.ui-btn-b:visited{background:#f6f6f6;border-color:#ddd;color:#333;text-shadow:0 1px 0 #f3f3f3}.ui-page-theme-b .ui-btn:hover,html .ui-bar-b .ui-btn:hover,html .ui-body-b .ui-btn:hover,html body .ui-group-theme-b .ui-btn:hover,html head+body .ui-btn.ui-btn-b:hover{background:#ededed;border-color:#ddd;color:#333;text-shadow:0 1px 0 #f3f3f3}.ui-page-theme-b .ui-btn:active,html .ui-bar-b .ui-btn:active,html .ui-body-b .ui-btn:active,html body .ui-group-theme-b .ui-btn:active,html head+body .ui-btn.ui-btn-b:active{background:#e8e8e8;border-color:#ddd;color:#333;text-shadow:0 1px 0 #f3f3f3}.ui-page-theme-b .ui-btn.ui-btn-active,html .ui-bar-b .ui-btn.ui-btn-active,html .ui-body-b .ui-btn.ui-btn-active,html body .ui-group-theme-b .ui-btn.ui-btn-active,html head+body .ui-btn.ui-btn-b.ui-btn-active,.ui-page-theme-b .ui-checkbox-on:after,html .ui-bar-b .ui-checkbox-on:after,html .ui-body-b .ui-checkbox-on:after,html body .ui-group-theme-b .ui-checkbox-on:after,.ui-btn.ui-checkbox-on.ui-btn-b:after,.ui-page-theme-b .ui-flipswitch-active,html .ui-bar-b .ui-flipswitch-active,html .ui-body-b .ui-flipswitch-active,html body .ui-group-theme-b .ui-flipswitch-active,html body .ui-flipswitch.ui-bar-b.ui-flipswitch-active,.ui-page-theme-b .ui-slider-track .ui-btn-active,html .ui-bar-b .ui-slider-track .ui-btn-active,html .ui-body-b .ui-slider-track .ui-btn-active,html body .ui-group-theme-b .ui-slider-track .ui-btn-active,html body div.ui-slider-track.ui-body-b .ui-btn-active{background-color:#38c;border-color:#1c4a70;color:#fff;text-shadow:0 1px 0 #059}.ui-page-theme-b .ui-radio-on:after,html .ui-bar-b .ui-radio-on:after,html .ui-body-b .ui-radio-on:after,html body .ui-group-theme-b .ui-radio-on:after,.ui-btn.ui-radio-on.ui-btn-b:after{border-color:#38c}.ui-page-theme-b .ui-btn:focus,html .ui-bar-b .ui-btn:focus,html .ui-body-b .ui-btn:focus,html body .ui-group-theme-b .ui-btn:focus,html head+body .ui-btn.ui-btn-b:focus,.ui-page-theme-b .ui-focus,html .ui-bar-b .ui-focus,html .ui-body-b .ui-focus,html body .ui-group-theme-b .ui-focus,html head+body .ui-btn-b.ui-focus,html head+body .ui-body-b.ui-focus{-webkit-box-shadow:0 0 12px #38c;-moz-box-shadow:0 0 12px #38c;box-shadow:0 0 12px #38c}.ui-disabled,.ui-state-disabled,button[disabled],.ui-select .ui-btn.ui-state-disabled{filter:Alpha(Opacity=30);opacity:.3;cursor:default!important;pointer-events:none}.ui-btn:focus,.ui-btn.ui-focus{outline:0}.ui-noboxshadow .ui-shadow,.ui-noboxshadow .ui-shadow-inset,.ui-noboxshadow .ui-overlay-shadow,.ui-noboxshadow .ui-shadow-icon.ui-btn:after,.ui-noboxshadow .ui-shadow-icon .ui-btn:after,.ui-noboxshadow .ui-focus,.ui-noboxshadow .ui-btn:focus,.ui-noboxshadow input:focus,.ui-noboxshadow .ui-panel{-webkit-box-shadow:none!important;-moz-box-shadow:none!important;box-shadow:none!important}.ui-noboxshadow .ui-btn:focus,.ui-noboxshadow .ui-focus{outline-width:1px;outline-style:auto}</style> <style>body{-webkit-touch-callout:none!important;height:100%}a{-webkit-user-select:none!important}.ctrlBtn{padding-top:.7em}#SwipeControl{height:100%}#popup-strength input{display:none}#popup-strength .ui-slider-track{margin-left:15px}#Page-Swipe .fullHeight{position:absolute;top:40px;right:0;bottom:70px;left:0}.iconButton{-webkit-border-radius:.3125em!important;border-radius:.3125em!important}.ui-footer{position:fixed;bottom:0;left:0;right:0}</style> <script src=http://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.js></script> <script src=http://cdnjs.cloudflare.com/ajax/libs/jquery-mobile/1.4.1/jquery.mobile.min.js></script> <script src=http://cdnjs.cloudflare.com/ajax/libs/hammer.js/1.0.6/hammer.min.js></script> <script src=http://cdnjs.cloudflare.com/ajax/libs/jquery.qrcode/1.0/jquery.qrcode.min.js></script> </head> <body> <div data-role=panel id=mypanel> <ul id=nav-list data-role=listview data-inset=true data-divider-theme=a data-theme=a> <li data-role=list-divider>Contoller Mode</li> <li><a href=#Page-Buttons>Buttons</a></li> <li><a href=#Page-Swipe>Swipe</a></li> <li data-role=list-divider>Settings</li> <li><a href=#Page-Cxn>Connection</a></li> <li><a href=#Page-Info>Info</a></li> </ul> </div> <div data-role=page id=Page-Buttons> <div data-role=header> <a href=#mypanel class="ui-btn ui-icon-bars ui-corner-all ui-btn-icon-notext iconButton"> &nbsp; </a> <h1>Button Control</h1> <div class=ui-btn-right> <a class="ui-btn ui-icon-recycle ui-corner-all ui-btn-icon-notext iconButton ResetModel"> &nbsp; </a> <a class="ui-btn ui-icon-lock ui-corner-all ui-btn-icon-notext iconButton MasterLock"> &nbsp; </a> </div> </div> <div role=main class=ui-content> <h2 class="ui-bar ui-bar-b ui-corner-all ErrMsg">Not Connected</h2> <div class="ui-grid-a ui-responsive"> <div class=ui-block-a> <div class=ui-grid-solo> <div class=ui-block-a><a href=# id=RotateUp class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-arrow-u ctrlBtn">&nbsp; </a></div> </div> <div class=ui-grid-a> <div class=ui-block-a><a href=# id=RotateLeft class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-arrow-l ctrlBtn">&nbsp; </a></div> <div class=ui-block-b><a href=# id=RotateRight class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-arrow-r ctrlBtn">&nbsp; </a></div> </div> <div class=ui-grid-solo> <div class=ui-block-a><a href=# id=RotateDown class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-arrow-d ctrlBtn">&nbsp; </a></div> </div> </div> <div class=ui-block-b> <div class=ui-grid-a> <div class=ui-block-a><a href=# id=ZoomIn class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-plus ctrlBtn">&nbsp; </a></div> <div class=ui-block-b><a href=# id=ZoomOut class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-minus ctrlBtn">&nbsp; </a></div> </div> <div class=ui-grid-a> <div class=ui-block-a><a href=# id=ZRotateLeft class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-back ctrlBtn">&nbsp; </a></div> <div class=ui-block-b><a href=# id=ZRotateRight class="ui-btn ui-shadow ui-corner-all ui-btn-icon-top ui-icon-forward ctrlBtn">&nbsp; </a></div> </div> </div> </div> </div> <div data-role=footer data-id=main-footer id=button-footer> <div data-role=controlgroup data-type=horizontal data-mini=true> <a class="ui-btn ui-corner-all ui-shadow"><<</a> <a class="ui-btn ui-corner-all ui-shadow"><</a> <a class="ui-btn ui-corner-all ui-shadow">Play</a> <a class="ui-btn ui-corner-all ui-shadow">></a> <a class="ui-btn ui-corner-all ui-shadow">>></a> </div> <a href=#button-popup-strength data-rel=popup data-position-to=#button-footer class="ui-btn ui-btn-right ui-corner-all ui-shadow ui-icon-gear ui-btn-icon-notext iconButton">Sensitivity</a> </div> <div data-role=popup id=button-popup-strength class="ui-corner-all ui-content"> <a href=# data-rel=back class="ui-btn ui-corner-all ui-shadow ui-btn-a ui-icon-delete ui-btn-icon-notext ui-btn-right">Close</a> <h3>Adjust Movement Sensitivity</h3> <form> <label for=strength class=ui-hidden-accessible>Sensitivity</label> <input name=strength id=btn_speed min=1 max=100 value=50 type=range data-highlight=true data-popup-enabled=true> </form> </div> </div> <div data-role=page id=Page-Swipe> <div data-role=header> <a href=#mypanel class="ui-btn ui-icon-bars ui-corner-all ui-btn-icon-notext iconButton"> &nbsp; </a> <h1>Swipe Control</h1> <div class=ui-btn-right> <a class="ui-btn ui-icon-recycle ui-corner-all ui-btn-icon-notext iconButton ResetModel"> &nbsp; </a> <a class="ui-btn ui-icon-lock ui-corner-all ui-btn-icon-notext iconButton MasterLock"> &nbsp; </a> </div> </div> <div role=main class="ui-content fullHeight"> <h2 class="ui-bar ui-bar-b ui-corner-all ErrMsg">Not Connected</h2> <div id=SwipeControl class="ui-body ui-body-a ui-corner-all"> <p id=SwipeEvent>Swipe Controls <p> <ul> <li><b>TAP:</b> Stop </li> <li><b>SWIPE:</b> Rotate</li> <li><b>PINCH:</b> Zoom </li> <li><b>ROTATE:</b> Rotate Z Axis </li> </ul> </div> </div> <div data-role=footer data-id=main-footer id=slide-footer> <div data-role=controlgroup data-type=horizontal data-mini=true> <a class="ui-btn ui-corner-all ui-shadow"><<</a> <a class="ui-btn ui-corner-all ui-shadow"><</a> <a class="ui-btn ui-corner-all ui-shadow">Play</a> <a class="ui-btn ui-corner-all ui-shadow">></a> <a class="ui-btn ui-corner-all ui-shadow">>></a> </div> <a href=#swipe-popup-strength data-rel=popup data-position-to=#slide-footer class="ui-btn ui-btn-right ui-corner-all ui-shadow ui-icon-gear ui-btn-icon-notext iconButton">Sensitivity</a> </div> <div data-role=popup id=swipe-popup-strength class="ui-corner-all ui-content"> <a href=# data-rel=back class="ui-btn ui-corner-all ui-shadow ui-btn-a ui-icon-delete ui-btn-icon-notext ui-btn-right">Close</a> <h3>Adjust Movement Sensitivity</h3> <form> <label for=strength class=ui-hidden-accessible>Sensitivity</label> <input name=strength id=swipe_speed min=1 max=100 value=5 type=range data-highlight=true data-popup-enabled=true> </form> </div> </div> <div data-role=page id=Page-Cxn> <div data-role=header> <a href=#mypanel class="ui-btn ui-icon-bars ui-corner-all ui-btn-icon-notext iconButton"> &nbsp; </a> <h1>Connection Settings</h1> <a href=#popupLogin data-rel=popup data-position-to=window class="ui-btn ui-corner-all ui-shadow ui-icon-camera ui-btn-icon-notext iconButton">&nbsp; </a> </div> <div role=main class=ui-content> <h2 class="ui-bar ui-bar-b ui-corner-all ErrMsg">Not Connected</h2> <h3 class="ui-bar ui-bar-a ui-corner-all">Http & Websocket Address</h3> <div data-role=controlgroup> <input name=httpAddr type=url id=CxnHTTPAddress data-wrapper-class="controlgroup-textinput ui-btn" /> <input name=wsAddr type=url id=CxnWSAddress data-wrapper-class="controlgroup-textinput ui-btn" data-clear-btn="true"/> <button id=ToggleCxnBtn>Connect</button> </div> </div> <div data-role=popup id=popupLogin data-theme=a class=ui-corner-all> <form> <div style="padding:10px 20px"> <a href=# data-rel=back class="ui-btn ui-corner-all ui-shadow ui-btn-a ui-icon-delete ui-btn-icon-notext ui-btn-right">Close</a> <h3>Scan to connect</h3> <span id=CxnQR></span> </div> </form> </div> </div> <div data-role=page id=Page-Info> <div data-role=header> <a href=#mypanel class="ui-btn ui-icon-bars ui-corner-all ui-btn-icon-notext iconButton"> &nbsp; </a> <h1>Swipe Control</h1> <button id=DebugMsgListBtn class="ui-btn ui-icon-check ui-corner-all ui-btn-icon-notext iconButton"> &nbsp; </button> </div> <div role=main class=ui-content> <h2 class="ui-bar ui-bar-b ui-corner-all ErrMsg">Not Connected</h2> <h3 class="ui-bar ui-bar-a ui-corner-all">Received Messages</h3> <ul data-role=listview data-inset=True id=DebugMsgList></ul> </div> </div> </body> """
	site_part2 = Template("""<script>var address="$address";""").safe_substitute(address=new_address)
	site_part3 = """var s=null;var somekeyDown=0;var isMaster=false;window.onbeforeunload=close;function log(b,a){if(typeof(a)==="undefined"){a="Message"}$("#DebugMsgList").prepend("<li><h3>"+a+"</h3><p>"+b+"</p></li>").listview("refresh")}function open(a){log("Connected!");$(".ErrMsg").fadeOut()}function close(a){log("Connection Closed!");$(".ErrMsg").text("Not Connected").fadeIn()}function msg(a){msg_data=JSON.parse(a.data);if(msg_data.hasOwnProperty("SLAVE")){toggleSlave(msg_data.SLAVE)}if(msg_data.hasOwnProperty("MASTER_STATUS")){isMaster=msg_data.MASTER_STATUS;styleMaster()}log(a.data)}function error(a){log("Error: "+a);$(".ErrMsg").text("Error! - Check Msg").fadeIn()}function send(a,d,c){if(typeof(c)==="undefined"){c=0.001}var e={};e[a]=d;e.Speed=c;var b=JSON.stringify(e);if(s){s.send(b)}else{log("Event: "+b)}}function toggleConnection(){if(s){s.close(1000,"Try to Close");$("#ToggleCxnBtn").text("Connect");s=null}else{try{address=$("#CxnWSAddress").val();if(address!=""||address!="$address"){s=new WebSocket(address);s.onopen=open;s.onclose=close;s.onmessage=msg;s.onerror=error;$("#ToggleCxnBtn").text("Disconnect")}}catch(a){error("Could Not Connected")}}}function toggleLockCommand(){send("MASTER_REQUEST",!isMaster)}function toggleSlave(a){if(a){$(".ctrlBtn").addClass("ui-disabled");$(".ErrMsg").text("Locked").fadeIn()}else{$(".ctrlBtn").removeClass("ui-disabled");$(".ErrMsg").text("Locked").fadeOut()}}function styleMaster(){if(isMaster){log("You are now Master");$(".MasterLock").addClass("danger")}else{$(".MasterLock").removeClass("danger")}}$(document).ready(function(){$("#CxnHTTPAddress").val(document.URL);$("#CxnWSAddress").val(address);$("#DebugMsgList").listview({create:function(c,d){}});toggleConnection();$("#CxnQR").qrcode(document.URL);$("#ToggleCxnBtn").click(toggleConnection);$(".MasterLock").click(toggleLockCommand);$("#DebugMsgListBtn").click(function(){$("#DebugMsgList").empty()});$("a").bind("contextmenu",function(c){c.preventDefault()});$("button").bind("contextmenu",function(c){c.preventDefault()});$(".ctrlBtn").on("vmousedown ",function(c){c.preventDefault();send("Actuator",$(this).attr("id"),$("#btn_speed").val()/1000)}).on("vmouseup ",function(){send("Stop","All")});$(".ResetModel").mousedown(function(){send("Reset",true)}).mouseup(function(){send("Stop","All")});var a=document.getElementById("SwipeControl");var b=Hammer(a,{prevent_default:true,no_mouseevents:true,transform_always_block:true}).on("tap",function(c){send("Stop","All")}).on("release",function(c){send("Stop","All")}).on("dragleft",function(c){send("Actuator","RotateLeft",($("#swipe_speed").val()/1000));c.gesture.stopDetect()}).on("dragright",function(c){send("Actuator","RotateRight",($("#swipe_speed").val()/1000));c.gesture.stopDetect()}).on("dragdown",function(c){send("Actuator","RotateDown",($("#swipe_speed").val()/1000));c.gesture.stopDetect()}).on("dragup",function(c){send("Actuator","RotateUp",($("#swipe_speed").val()/1000));c.gesture.stopDetect()}).on("pinchin",function(c){send("Actuator","ZoomIn",($("#swipe_speed").val()/1000));c.gesture.stopDetect()}).on("pinchout",function(c){send("Actuator","ZoomOut",($("#swipe_speed").val()/1000));c.gesture.stopDetect()}).on("rotate",function(c){if(c.gesture.rotation<0){send("Actuator","ZRotateLeft",($("#swipe_speed").val()/1000))}else{send("Actuator","ZRotateRight",($("#swipe_speed").val()/1000))}c.gesture.stopDetect()});$(document).keydown(function(c){if(c.which==37&&!somekeyDown){c.preventDefault();somekeyDown=true;c.shiftKey?send("Actuator","ZRotateLeft"):send("Actuator","RotateLeft")}if(c.which==38&&!somekeyDown){c.preventDefault();somekeyDown=true;c.shiftKey?send("Actuator","ZoomOut"):send("Actuator","RotateUp")}if(c.which==39&&!somekeyDown){c.preventDefault();somekeyDown=true;c.shiftKey?send("Actuator","ZRotateRight"):send("Actuator","RotateRight")}if(c.which==40&&!somekeyDown){c.preventDefault();somekeyDown=true;c.shiftKey?send("Actuator","ZoomIn"):send("Actuator","RotateDown")}if(c.which==27&&!somekeyDown){somekeyDown=true;toggleConnection()}});$(document).keyup(function(c){send("Stop","All");somekeyDown=false})});$(function(){$("#mypanel").panel().enhanceWithin()});</script> </html>"""
	html = open(file ,"w")
	html.write(site_part1)
	html.write(site_part2)
	html.write(site_part3)
	html.close()


class QuiteCGIHandler(http.server.CGIHTTPRequestHandler):
    def log_message(self, format, *args):
        pass #Hides all messages for Request Handler

# Inherit this class to handle the websocket connection
class WebSocketHandler(socketserver.BaseRequestHandler):

#-------------- Over ride these  ----------------------------------------
    def on_message(self, msg):
        #msg is a array, decoded from JSON
        #Override this function to handle the input from webcontroller
        print(msg)
        #self.send_message("Got :" + ast.literal_eval(msg))
        
    def handle_message(self, msg):    
        #only the user with the lock can control
        if self._hasLock():
            msg_data = json.loads(msg)
            if "MASTER_REQUEST" in msg_data:
                if msg_data["MASTER_REQUEST"]:
                    WebSocketHandler.lock_id = threading.current_thread().ident
                    self.send_json(dict(MASTER_STATUS=True));
                    print("Locking to thread: " ,WebSocketHandler.lock_id, "   :   ", self.id)
                    self.broadcast_all(dict(SLAVE=True))
                else:
                    WebSocketHandler.lock_id = None
                    self.send_json(dict(MASTER_STATUS=False))
                    self.broadcast_all(dict(SLAVE=False))
            #elif "MESSAGE" in msg_data:
            #    self.on_message(msg["MESSAGE"])
            #else:
            #   print("Unknown CMD, trashing: ", msg_data)
            self.on_message(msg_data)
        else:
            self.send_json(dict(SLAVE=True));
            print("Locked, trashing: ", msg) 
            
    def on_close(self):
        print("Server: Closing Connection for ", self.client_address)
        self.send_message("Server: Closing Connection")
        
    def send_message(self, message):
        print("Sending: ", message)
        self.send_json(dict(MESSAGE=message))
        
    def send_json(self, data):
        #sends a python dict as a json object
        self.request.sendall(self._pack(json.dumps(data)))
        
    def broadcast_all(self, data):
        #send a araay converted into JSON to every thread
        for t in WebSocketHandler.connections:
            if t.id == self.id:
                continue
            t.send_json(data)
    
#-------------------------------------------------------------------

    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    lock_id = None
    connections = []

    def _hasLock(self):
        #there is no lock or the current thread has it
        return (not WebSocketHandler.lock_id) or (WebSocketHandler.lock_id == self.id)
    
    
    
    def setup(self):
        #Overwrtien function from socketserver
        #Init some varibles
        print("\nConnection Established", self.client_address)
        self.closeHandle = False
        self.id = threading.current_thread().ident
        self.alive = threading.Event()
        self.alive.set()
        WebSocketHandler.connections.append(self)
    
    def handle(self):
        #handles the handshake with the server
        #Overwrtien function from socketserver
        try:
            self.handshake()
        except:
            print("HANDSHAKE ERROR! - Try using FireFox")
            #return
           
    def run(self):
        #runs the handler in a thread
        while self.alive.isSet():
            msg = self.request.recv(2)
            if not msg or self.closeHandle or msg[0] == 136: 
                print("Received Closed")
                break
            length = msg[1] & 127
            if length == 126:
                length = struct.unpack(">H", self.request.recv(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self.request.recv(8))[0]
            masks = self.request.recv(4)
            decoded = ""
            for char in self.request.recv(length):
                decoded += chr(char ^ masks[len(decoded) % 4])
            self.handle_message(decoded)
            
            #WebSocketHandler.broadcast_all.wait(0.01)
            
        self.close()
        
    def close(self, message="Cxn Closed"):
        self.closeHandle = True
        self.request.sendall(self._pack(message, True))
        self.on_close()
    
    def handshake(self):
        key = None
        data = self.request.recv(1024).strip()
        for line in data.splitlines():
            if b'Upgrade:' in line:
                upgrade = line.split(b': ')[1]
                if not upgrade == b'websocket':
                    raise Exception("Upgrade is Not a websocket!", data)
            if b'Sec-WebSocket-Key:' in line:
                key = line.split(b': ')[1]
                break
        if key is None:
            raise Exception("Couldn't find the key?:", data)
        print('Handshaking...   ', end = '')
        digest = self._websocketHash(key)
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
        self.handshake_done = self.request.send(response.encode())
        print("Sending Connected Message...   ", end = '')
        if self.handshake_done:
            self.send_message("Connected!")
        print("Connected!\n")
        
    def _websocketHash(self, key):
        result_string = key + self.magic
        sha1_digest = hashlib.sha1(result_string).digest()
        response_data = base64.encodestring(sha1_digest).strip()
        response_string = response_data.decode('utf8')
        return response_string

    def _get_framehead(self, close=False):
        #Gets the frame header for sending data, set final fragment & opcode
        frame_head = bytearray(2)
        frame_head[0] = frame_head[0] | (1 << 7)
        if close:
            # send the close connection frame
            frame_head[0] = frame_head[0] | (8 << 0)
        else:
            #send the default text frame
            frame_head[0] = frame_head[0] | (1 << 0)
        return frame_head
            
    def _pack(self, data ,close=False):
        #pack bytes for sending to client
        frame_head = self._get_framehead(close)        
        # payload length
        if len(data) < 126:
            frame_head[1] = len(data)
        elif len(data) < ((2**16) - 1):
            # First byte must be set to 126 to indicate the following 2 bytes
            # interpreted as a 16-bit unsigned integer are the payload length
            frame_head[1] = 126
            frame_head += int_to_bytes(len(data), 2)
        elif len(data) < (2**64) -1:
            # Use 8 bytes to encode the data length
            # First byte must be set to 127
            frame_head[1] = 127
            frame_head += int_to_bytes(len(data), 8)
        frame = frame_head + data.encode('utf-8')
        return frame
            
class HTTPServer(threading.Thread):
    def __init__(self, address_info=('',0)):
        threading.Thread.__init__(self)
        self.httpd = None
        self._start_server( address_info )
           
    def _start_server(self, address_info):
        #Starts the server at object init
        try:
            #Using std CGI Handler
            self.httpd = http.server.HTTPServer(address_info, QuiteCGIHandler)
            print("HTTP Server on : ", self.get_address() )
        except Exception as e:
            print("The HTTP server could not be started")
    
    def get_address(self):
        #returns string of the servers address or None
        if self.httpd is not None:
            return 'http://{host}:{port}/'.format(host=socket.gethostbyname(self.httpd.server_name), port=self.httpd.server_port)
        else:
            return None

    def run(self):
        #Overwrtien from Threading.Thread
        if self.httpd is not None :
            self.httpd.serve_forever()
        else:
            print("Error! - HTTP Server is NULL")

    def stop(self):
        #Overwrtien from Threading.Thread
        print("Killing Http Server ...")
        if self.httpd is not None:
            self.httpd.shutdown()
        print("Done")

class WebSocketTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    #Added a list of current handlers so they can be closed
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.handlers = []
        self.daemon_threads = True
        
    def finish_request(self, request, client_address):
        #Finish one request by instantiating RequestHandlerClass
        print("launching a new request")
        t = self.RequestHandlerClass(request, client_address, self)
        print("Request:" , t)
        self.handlers.append(t)
        print("Num request:" ,len(self.handlers))
        t.run()
        
    # def process_request(self, request, client_address):
        # #Start a new thread to process the request
        # t = threading.Thread(target = self.process_request_thread, args = (request, client_address))
        # t.daemon = True
        # t.start() 
        
    def get_handlers(self):
        #returns the list of handlers
        return self.handlers
    
class WebsocketServer(threading.Thread):
    def __init__(self, handler, address_info=('',0)):
        threading.Thread.__init__(self)
        self.wsd = None
        self.handler = handler
        self._start_server(address_info)

    def _start_server(self, address_info):
        #Starts the server at object init
        try:
            self.wsd = WebSocketTCPServer( address_info, self.handler)
            print( self.get_address())
        except Exception as e:
            print("Error! - Websocket Server Not Started!", e)
            
    def get_address(self):
        #returns string of the servers address or None
        if self.wsd is not None:
            return 'ws://{host}:{port}/'.format(host=socket.gethostbyname(self.wsd.server_name), port=self.wsd.server_port)
        else:
            return None
            
    def run(self):
        if self.wsd is not None:
            self.wsd.serve_forever()
        else:
            print("The WebSocket Server is NULL")

    def stop(self):
        print("Killing WebSocket Server ...")
        if self.wsd is not None:
            for h in self.wsd.handlers:
                h.alive.clear()
                
            self.wsd.shutdown()
        print("Done")
        
    def get_handlers(self):
        #returns the list of handlers
        return self.wsd.get_handlers()
        
    def send(self, msg):
        for h in self.wsd.get_handlers():
            h.send_message(msg)
        
class WebSocketHttpServer():
    def __init__(self, handler_class = WebSocketHandler, http_address=('',0), ws_address=('',0) ):
        self.http_address = http_address
        self.ws_address = ws_address
        self.handler = handler_class
        self.httpServer = None
        self.wsServer = None

    def _clean_server_temp_dir(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.tempdir)
        os.rmdir(self.tempdir)
        
    def _make_server_temp_dir(self):
        #make the new temp directory
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)
        print("New temp dir:", self.tempdir)
    
    def _make_webpage(self):
        writeWebsite(self.tempdir + "/index.html" , self.wsServer.get_address())
        
    def stop(self):
        try:
            self.httpServer.stop()
            self.wsServer.stop()
            self._clean_server_temp_dir()
        except Exception as e:
            print("The Servers were never started")
        
    def start(self):
        try:
            # make directory and copy files
            self._make_server_temp_dir()
            self.httpServer = HTTPServer(self.http_address)
            self.wsServer = WebsocketServer(self.handler, self.ws_address)
            if self.wsServer is not None and self.httpServer is not None:
                self.httpServer.start()
                self.wsServer.start()
                self._make_webpage()
                return True
            else:
                print("Error Starting The Servers, Something is not Initialized!")
                return False
        except Exception as e:
            print()
            print("Error!!!, There is some error!")
            print(e)
            print()
            return False
    
    def send(self, msg):
        self.wsServer.send(msg)
    
    def launch_webpage(self):
        #Copies all the resource over to the temp dir
        webbrowser.open(self.httpServer.get_address() + "index.html")
        
    def status(self):
        if self.wsServer is None or self.httpServer is None:
            return False
        else:
            return True
            
if __name__ == '__main__':
    print("No Main Program!")

