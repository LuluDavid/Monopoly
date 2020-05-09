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

## Game

### Types of boxes

`start`, `street`, `station`, `public-service`, `community-fund`, `chance`, `tax`, `jail`, `park`, `to-jail`
