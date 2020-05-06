$( document ).ready(function() {
    let socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('Websocket connected!');
        joinGame();
    });

    function joinGame() {
      console.log('Game id : ' + gameId);
      socket.emit('join', {game_id: gameId, player_id: playerId});
    }

    socket.on('join_game', function(data) {
        let newPlayerName = data["new_player"]["name"]
        console.log(newPlayerName + " a rejoint la partie");
        let playersInGameNames = data["players_in_game_names"];
        console.log(playersInGameNames);
        if(playerName == newPlayerName){
            let playerNamesToAdd = playersInGameNames.filter(name => name != newPlayerName);
            playerNamesToAdd.forEach(nameToAdd => addPlayerNameToSidebar(nameToAdd));
        }
        else{
            addPlayerNameToSidebar(newPlayerName, playerName);
        }
    });


    function addPlayerNameToSidebar(nameToAdd){
        let playerHtmlLine = '<div class="list-group-item list-group-item-action bg-light" id="player_list">';
        playerHtmlLine += nameToAdd + '</div>';
        $("#player_list").append(playerHtmlLine);
    }
});



