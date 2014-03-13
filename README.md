Blender Web Controller
=============================

Short Description
-----------------

This is a [Blender](http://blender.org) add-on that use your smartphone to control the view of model in the Blender Game Engine.

Feature Description
---------------------
This Blender add-on allows someone to present a 3D model and to control the camera positioning using a website. The add-on will create a new camera in the Blender scene and all the necessary scripts and logic to control it. It then create server to host the controlling website and a web-socket to communicate with the BGE. The website also also master/everyone locking, so a unique user or everyone can control the model. 

This add-on is developed at the University of Toledo as a research project. The goal of this project is to make a piece of software that would make it easy for professor to present a 3D model and control it in front of students. The master/everyone control is so the professor can lock control allowing only himself or any one of his students to control the model.

**Main Features:**

 1. Control the BGE using your smartphone!
 2. Everything included in the add-on, use only the standard python modules (website does use CDN so internet connection is required)
 3. Create new objects in blender, so it won't modify anything
 4. Uses python to create a web host to launch the controlling website
 5. The website features button, keyboard, and touch controls
 6. The website has a QR code for the connection information to easily share with others
 7. Master/Everyone control modes; Switch on will only allow that user to control the model, Off will allow anyone to control it.


 How to use
-------------------------
 8. Install and enable the "WebControllerAddon.py" add-on into blender. _Search Google for how to do this_ 
 9. Under Render Settings tab, there should now be a "Web Control" panel. Click on the "Setup" button. This will generate all the needed objects, scripts and logic.
 10. Reposition the camera and empty as needed
 11. Click "p" to start the game engine
 12. Use website to control the model

FAQ
------
**Not Connect Banner on website load**

There is a nasty bug that is preventing the website from using the correct web-socket address. If you have the console open you will see that Blender has started the web-socket on port #####. Under the connections tab on the website, enter that number into the web-socket input field and click on connect

 **I can't connect to website.**

The machine that Blender is running on and the device you are trying to connect with have to be on the same network. Otherwise you would have to set some kind of 3rd party server. 

**The Website looks like crap**

In order minimize the file size, improve  make this script easy to edit, he website uses CDN's to get some JavaScript files. Make sure you have external internet connection so you device can fetch those files. 

**Why are there funny play buttons on the bottom of the website?**

They are for later use. I hope enable animation play back one day and this buttons are a place holder for that. They do nothing.

**My question is not answered! / I have found an bug! / Can you make it do this?**

Please submit a GitHub issues!

**License**
This project is licensed under the the MIT license. See included file for more details

Copyright (c) <2014, Joseph Livecchi>
