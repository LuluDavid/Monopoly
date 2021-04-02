# Monopoly

<p align="center">
  <img src="./pictures/moving.png" width = 850>
</p>

This project is a web implementation of the famous Monopoly game. It relies on [three.js](https://threejs.org/) for the graphics, [Flask](https://flask.palletsprojects.com/en/1.1.x/) for the web framework & [websockets](https://socket.io/) for the realtime updates with the backend. The application is hosted on Heroku at the following [address](https://monolopy.herokuapp.com/) if you want to test the game (sorry for non-french users).

## External features

This project uses the Github repo [threejs-dice](https://github.com/byWulf/threejs-dice) from byWulf, which allows us to throw predetermined dices in the game.
<p align="center">
  <img src="./pictures/property.png" width=430 height=400>  <img src="./pictures/dices.png" width=430 height=400>
</p>
Because of that, we also use [cannon.js](https://schteppe.github.io/cannon.js/) for physics simulation on the dice throw.  
Finally, we use [notify.js](https://notifyjs.jpillora.com/) to notify other players of the game changes.

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

## How to play

The master branch is deployed on heroku at [this link](https://monolopy.herokuapp.com). It is not persistent yet, so you will need to avoid refreshing the page. You just need to create a game, share the id with the other players, and all click the ready button.
Once this is done, the game will run between different pages. The trading system is not implemented yet, and the game lacks a bit of information (notifications), but it is coming soon.

## How to test it locally

You just need to run webapp.py and connect to localhost:8000.

## TODO-list

* Add an ending scenario to the game
* Version the used libs (not possible for three-dices, but for the rest it should be alright)
* Implement a persistent interface to save the game on refresh (cookie uid)
* Refactor most of the socket interface to make it more readable
* Handle more seriously asynchronous features (the notifications come sometimes early/late for instance)
* Play A LOT to detect side effects
* Integrate google-ads (but we'll get copyrighted right ?)
* Integrate a proximity-chat (just kidding)
