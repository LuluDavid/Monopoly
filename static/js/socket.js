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
        let newPlayer = data["new_player"];
        let newPlayerName = newPlayer["name"];
        let newPlayerId = newPlayer["id"];
        console.log(newPlayerName + " a rejoint la partie");
        let playersInGame = data["players_in_game"];
        let ids = Object.keys(playersInGame);
        let names = Object.values(playersInGame);
        if(playerName === newPlayerName){
            for (let i = 0; i<ids.length; i++){
                let id = ids[i];
                if (parseInt(id) !== playerId){
                    console.log("id "+id+" different from "+playerId);
                    addPlayerNameToSidebar(names[i], id);
                }
            }
        }
        else{
            addPlayerNameToSidebar(newPlayerName, newPlayerId);
        }
    });

    function addPlayerNameToSidebar(nameToAdd, id){
        let playerHtmlLine = '<div id="'+id+'" class="list-group-item list-group-item-action bg-light">';
        playerHtmlLine += nameToAdd;
        playerHtmlLine += uncheck+'</div>';
        $("#player_list").append(playerHtmlLine);
    }


    $("#startGame").click(function(){
        console.log("Adding a new player to the game");
        $("#startGame").hide();
        $("#"+playerId+" svg").remove();
        $("#"+playerId).append(check);
        socket.emit('start_game', {game_id: gameId, player_id: playerId});
    });

    socket.on('start_game', function(data) {
        let playerReady = data["playerReady"];

        $("#"+playerReady+" svg").remove();
        $("#"+playerReady).append(check);

        data = data["gameState"];
        console.log("Player "+playerReady+" is ready to play");
        // Add a new pawn for the new player
        numberOfPawns++;
        // Change the page state
        updatePawns();
        // TODO: create a map id <-> pawn number here would be easy as fuck
        stateArray = data;
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
    });

    $("#playTurn").click(function(){
        if (incrementing) console.log("Last turn's animation is not finished yet");
        else socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "play_turn"});
    });
    
    socket.on('play_turn', async function(data) {
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
             // Wait 2 seconds
            await new Promise(r => setTimeout(r, 2000));
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



