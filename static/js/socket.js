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
        let newPlayerName = data["new_player"];
        console.log(newPlayerName + " a rejoint la partie");
        let playersInGameNames = data["players_in_game_names"];
        console.log(playersInGameNames);
        if(playerName === newPlayerName){
            let playerNamesToAdd = playersInGameNames.filter(name => name !== newPlayerName);
            playerNamesToAdd.forEach(nameToAdd => addPlayerNameToSidebar(nameToAdd));
        }
        else{
            addPlayerNameToSidebar(newPlayerName, playerName);
        }
    });

    function addPlayerNameToSidebar(nameToAdd){
        let playerHtmlLine = '<div class="list-group-item list-group-item-action bg-light" id="'+nameToAdd+'">';
        playerHtmlLine += nameToAdd;
        playerHtmlLine += '<svg class="bi bi-x" style="float : right" width="2em" height="2em" viewBox="0 0 16 16" fill="red" xmlns="http://www.w3.org/2000/svg">';
        playerHtmlLine += '<path fill-rule="evenodd" d="M11.854 4.146a.5.5 0 010 .708l-7 7a.5.5 0 01-.708-.708l7-7a.5.5 0 01.708 0z" clip-rule="evenodd"/>';
        playerHtmlLine += '<path fill-rule="evenodd" d="M4.146 4.146a.5.5 0 000 .708l7 7a.5.5 0 00.708-.708l-7-7a.5.5 0 00-.708 0z" clip-rule="evenodd"/>';
        playerHtmlLine += '</svg></div>';
        $("#player_list").append(playerHtmlLine);
    }


    $("#startGame").click(function(){
        console.log("Adding a new player to the game");
        $("#startGame").hide();
        socket.emit('start_game', {game_id: gameId, player_id: playerId});
    });

    socket.on('start_game', function(data) {
        console.log("New player added to the game");
        // Add a new pawn for the new player
        numberOfPawns++;
        // Change the page state
        updatePawns();
        stateArray = initState();
        // Once all players have clicked start game, display the play turn
        // TODO: add a "game joined" symbol near a player's name
        // TODO: display play turn only if it is your turn
        if (numberOfPawns === $("#player_list").children().length){
            if(playerId === data["player_turn"]) {
                $("#playTurnModal").modal({
                keyboard: false,
                backdrop: 'static'
                });
            }
        }
        else {
            console.log(numberOfPawns+"/"+$("#player_list").children().length+" players are ready to play")
        }
    });

    $("#playTurn").click(function(){
        if (incrementing) console.log("Last turn's animation is not finished yet");
        else socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "play_turn"});
    });
    
    socket.on('play_turn', function(data) {
        console.log(data);
        stateArray = data["state_array"];
        updateAllPlayers();

        if(playerId === data["player_turn"]) {
            if (data["action"] === "play_turn") {
                $("#playTurnModal").modal({
                    keyboard: false,
                    backdrop: 'static'
                });
            }
            else if (data["action"] === "ask_buy") {
                let questionData = {
                label: "Acheter un terrain",
                content: `Voulez vous acheter ${data["box_name"]} pour ${data["box_price"]} euros ?`,
                prop1: "J'achète le terrain",
                prop2: "Je n'achète pas le terrain",
                action: "buy"
                };
            showQuestionModal(questionData);
            }
        }
    });

    function showQuestionModal(questionData){
        $("#modalQuestionLabel").text(questionData["label"]);
        $("#modalQuestionContent").text(questionData["content"]);
        $("#modalQuestion1").text(questionData["prop1"]);
        $("#modalQuestion2").text(questionData["prop2"]);
        $("#modalQuestion1").attr("data-action", questionData["action"]);
        $("#modalQuestion2").attr("data-action", questionData["action"]);
        $('#modalQuestion').modal({
          keyboard: false,
          backdrop: 'static'
        });
    }

    $("#modalQuestion1").click(function(){
        let action = $(this).attr("data-action");
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: action, action_value: true});
    });
    $("#modalQuestion2").click(function(){
        let action = $(this).attr("data-action");
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: action, action_value: false});
    });



    // Subsidiary functions (chat...)

    $('#msgInput').on('keypress', function (e) {
        if(e.keyCode === 13){
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

    /*
    $("#question").on('click', function(){
        //C'est juste un example, ce sera générique une fois qu'on aura les infos depuis le back (titre, contenu, ...)
        $("#modalQuestionLabel").text('Acheter un terrain');
        $("#modalQuestionContent").text('Voulez vous acheter le terrain : Rue de Paradis, pour 3 cacahuètes ?');
        $("#modalQuestion1").text('J\'achète le terrain');
        $("#modalQuestion2").text('Je n\'achète pas le terrain');
        $('#modalQuestion').modal({
          keyboard: false,
          backdrop: 'static'
        });
    });



    $("#information").on('click', function(){
        //C'est juste un example, ce sera générique une fois qu'on aura les infos depuis le back (titre, contenu, ...)
        $("#modalInfoLabel").text('Caisse de communauté');
        $("#modalInfoContent").text('Félicitations, vous héritez de .... ah bah rien en fait, tout va à la banque');
        $('#modalInfo').modal({
          keyboard: false,
          backdrop: 'static'
        });
    });
    */

});



