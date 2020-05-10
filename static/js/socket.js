$( document ).ready(function() {
    let socket = io.connect('http://' + document.domain + ':' + location.port);
    $("#play_turn").hide();

    socket.on('connect', function() {
        console.log('Websocket connected!');
        joinGame();
    });

    function joinGame() {
      console.log('Game id : ' + gameId);
      socket.emit('join', {game_id: gameId, player_id: playerId});
    }

    socket.on('join_game', function(data) {
        let newPlayerName = data["new_player"]
        console.log(data)
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

    $("#start_game").click(function(){
        console.log("Starting Game...");
        $("#start_game").hide();
        socket.emit('start_game', {game_id: gameId, player_id: playerId});
    });

    socket.on('start_game', function(data) {
        console.log("Game started");
        $("#play_turn").show();
        console.log(data);
    });

    $("#play_turn").click(function(){
        socket.emit('play_turn', {game_id: gameId, player_id: playerId});
    });

    socket.on('play_turn', function(data) {
        console.log("Game played");
        console.log(data);
    });



    $('#msgInput').on('keypress', function (e) {
        if(e.keyCode == 13){
            let newMsg = escapeHtml($('#msgInput').val());
            $('#msgInput').val('');
            socket.emit('new_msg', {game_id: gameId, player_name: playerName, msg: newMsg});
        }
    });

    function escapeHtml(text) {
      return text
          .replace("&", "&amp;") // Necessary to do it first
          .replace("é", "&eacute;")
          .replace("è", "&egrave;")
          .replace("ê", "&ecirc;")
          .replace("à", "&agrave;")
          .replace("â", "&acirc;")
          .replace("ç","&ccedil;")
          .replace("ù", "&ugrave;")
          .replace("û", "&ucirc;")
          .replace("ô", "&ocirc;")
          .replace("î", "&icirc;")
          .replace("\"", "&quot;")
          .replace("\'", "&apos;")
          .replace(/<\/?[^>]+(>|$)/g, "");
    }

    socket.on('print_new_msg', function(data) {
        let newPlayerName = data["player_name"];
        console.log(newPlayerName + " a posté un message");
        let cleanMsg = data["msg"];
        $("#messages").append('<div>' + '<strong>' + newPlayerName + ': ' + '</strong>' + cleanMsg + '</div>');
        $("#messages").scrollTop($("#messages")[0].scrollHeight);
    });

    $("#copy").on('click', function() {
        let temp = $("<input>");
        $("body").append(temp);
        temp.val(gameId).select();
        document.execCommand("copy");
        temp.remove();
    });

});



