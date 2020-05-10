# Monopoly



## Project's Architecture
```
Monopoly  
|  webbapp.py : server controler for the web application
└──templates : jinja2 templates for the web application
└──game : python module with the game algorithm
└──tests : unittests for the game module
└──static : static files download by the user while loaing the page
    └──css
    └──js
        |  sockets.js : file managing all the socket communication beetwen server and clients
        └──graphics : js module with all the graphic interface
```


## How to test

### Game unittests
In the root folder :
```
export PYTHONPATH=.
python -m unittest discover -s tests -t tests
```

### Graphics
Run `python -m http.server`. Then go into your webbrowser like Firefox and search for :
```
http://localhost:8000/static/js/graphics/main.html
```      

### Share your URL
Install ngrok (https://ngrok.com/download), run webapp.py (on port X) and run ```ngrok http X```.
Ngrok then gives you the public URL which you can connect on from other devices.
You just need to create a game from one end, and then use the "Copier l'id" button to copy the game
id, which you can use from other devices to connect to the same game.


## Game

### Types of boxes

`start`, `street`, `station`, `public-service`, `community-fund`, `chance`, `tax`, `jail`, `park`, `to-jail`
