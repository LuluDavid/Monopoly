$( document ).ready(function() {
    let socket = io.connect('https://' + document.domain + ':' + location.port, {secure: true});

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
        idsToPawns[newPlayerId] = Object.keys(idsToPawns).length;
        let playersInGame = data["players_in_game"];
        let ids = Object.keys(playersInGame);
        let names = Object.values(playersInGame);
        if(playerName === newPlayerName){
            for (let i = 0; i<ids.length; i++){
                // Rebuild the mapping for the new player
                idsToPawns[ids[i]] = i;
                let id = ids[i];
                if (parseInt(id) !== playerId){
                    addPlayerNameToSidebar(names[i], id);
                }
            }
        }
        else{
            addPlayerNameToSidebar(newPlayerName, newPlayerId);
        }
    });

    function addPlayerNameToSidebar(nameToAdd, id){
        let playerHtmlLine = '<div id="'+id+'" class="list-group-item list-group-item-action bg-light"><div id="top-info" style="color: black; font-size: 18px">';
        playerHtmlLine += nameToAdd;
        playerHtmlLine += uncheck+'</div>'+frontGoods+'</div>';
        $("#player_list").append(playerHtmlLine);
    }


    $("#startGame").click(function(){
        console.log("Adding a new player to the game");
        $("#startGame").hide();
        socket.emit('start_game', {game_id: gameId, player_id: playerId, player_name: playerName});
    });

    socket.on('start_game', function(data) {
        let newPlayerId = data["newPlayer"]["id"];
        let newPlayerName = data["newPlayer"]["name"];

        $("#"+newPlayerId+" svg").remove();
        $("#"+newPlayerId+" #top-info").append(check);

        data = data["gameState"];
        console.log("Player "+newPlayerName+" is ready to play");
        // Add a new pawn for the new player
        numberOfPawns++;
        idsToPossessions = initPossessions();
        // Change the page state
        updatePawns();
        stateArray = initState();
        // Once all players have clicked start game, display the play turn
        if (numberOfPawns === $("#player_list").children().length){
            if(playerId === data["player_turn"]) {
                $("#modalPlayTurn").modal({
                keyboard: false,
                backdrop: 'static'
                });
            }
        }
    });
    
    socket.on('play_turn', async function(data) {
        let changedPlayers = data["changed_players"];
        if (changedPlayers != null) {
            for (let pid of Object.keys(changedPlayers)) {
                let playerChanges = changedPlayers[pid];
                for (let prop of Object.keys(playerChanges)) {
                    let changes = {};
                    changes[prop] = playerChanges[prop];
                    idsToPossessions[pid] = Object.assign({}, idsToPossessions[pid], changes);
                    updateSidebarId(pid);
                }
            }
        }
        stateArray = data["state_array"];
        updateAllPlayers();
        updateAllHouses();
        await waitForModal(data);
    });

    async function waitForModal(data){
        // Block the following if still animating pawns
        if (!incrementing){
            await switchModal(data);
        }
        else{
            requestAnimationFrame(() => waitForModal(data));
        }
    }

    async function switchModal(data){
        if(playerId === data["player_turn"]) {
            if (data["action"] === "play_turn") {
                if (data["is_in_jail"] && data["jail_turn"] < 3){
                    if(data["player_money"]>50) $("#jailTurnPay").show(); else $("#jailTurnPay").hide();
                    if(data["card_leave_jail"]>0) $("#jailTurnCard").show(); else $("#jailTurnCard").hide();
                    $("#modalJailTurn").modal({
                        keyboard: false,
                        backdrop: 'static'
                    });
                }
                else {
                    $("#modalPlayTurn").modal({
                        keyboard: false,
                        backdrop: 'static'
                    });
                }
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
            else if (data["action"] === "ask_buy_houses") {
                let buyHousesData = {
                    content: `Voulez vous acheter des maisons sur ${data["box_name"]} (${data["house_price"]} l'unité)`,
                    buyable_houses: data["buyable_houses"],
                    action: "buy_houses"
                };
                showBuyHousesModal(buyHousesData);
            }
            else if (data["action"] === "draw_card") {
                animateCard(data["card_type"]);
                // Wait for the animation to stop
                await new Promise(r => setTimeout(r, 1000*(tReveal+tTravel/coverRatio)));
                console.log("Awaited executor");
                let labels = {"community-fund": "Caisse de communauté", "chance": "Chance"};
                let infoData = {
                    label: labels[data["card_type"]],
                    content: data["card_message"],
                    action: "execute_card"
                };
                showInfoModal(infoData);
            }
        }
    }

    function showInfoModal(infoData){
        $("#modalInfoLabel").text(infoData["label"]);
        $("#modalInfoContent").text(infoData["content"]);
        $("#modalInfoOk").attr("data-action", infoData["action"]);
        $('#modalInfo').modal({
          keyboard: false,
          backdrop: 'static'
        });
    }

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

    function showBuyHousesModal(buyHousesData){
        $("#modalBuyHousesContent").text(buyHousesData["content"]);
        $("#modalBuyHousesYes").attr("data-action", buyHousesData["action"]);
        $("#modalBuyHousesNo").attr("data-action", buyHousesData["action"]);
        $("#nbHousesInput").attr("max", buyHousesData["buyable_houses"]);
        $("#nbHousesInput").val(0);
        $('#modalBuyHouses').modal({
          keyboard: false,
          backdrop: 'static'
        });
    }

    $("#playTurn").click(function(){
        if (incrementing) console.log("Last turn's animation is not finished yet");
        else socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "play_turn"});
    });
    $("#jailTurnDouble").click(function(){
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "play_turn", action_value: "double"});
    });
    $("#jailTurnPay").click(function(){
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "play_turn", action_value: "pay"});
    });
    $("#jailTurnCard").click(function(){
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "play_turn", action_value: "card"});
    });
    $("#modalQuestion1").click(function(){
        let action = $(this).attr("data-action");
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: action, action_value: true});
    });
    $("#modalQuestion2").click(function(){
        let action = $(this).attr("data-action");
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: action, action_value: false});
    });
    $("#modalBuyHousesYes").click(function(){
        let action_value = $("#nbHousesInput").val();
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "buy_houses", action_value: action_value});
    });
    $("#modalBuyHousesNo").click(function(){
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: "buy_houses", action_value: 0});
    });
    $("#modalInfoOk").click(function(){
        let action = $(this).attr("data-action");
        socket.emit('play_turn', {game_id: gameId, player_id: playerId, action: action});
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

});



