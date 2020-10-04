let socket = io.connect(window.location.protocol+'//' + document.domain + ':' + location.port, {secure: true});

$( document ).ready(function() {

    socket.on('connect', function() {
        console.log('Websocket connected!');
        joinGame();
    });

    function joinGame() {
      console.log('Game id : ' + gameId);
      socket.emit('join', {game_id: gameId, player_id: playerId});
    }

    socket.on('error', function(data){
            console.log(data['error']);
        });

    socket.on('join_game', function(data) {
        console.log("Joining game "+gameId);
        let newPlayer = data["new_player"];
        let newPlayerName = newPlayer["name"];
        let newPlayerId = newPlayer["id"];
        idsToNames[newPlayerId] = newPlayerName;
        let playersInGame = data["players_in_game"];
        let ids = Object.keys(playersInGame);
        let names = Object.values(playersInGame);
        if(playerName === newPlayerName){
            for (let i = 0; i<ids.length; i++){
                // Rebuild the mapping for the new player
                // idsToPawns[ids[i]] = i;
                idsToNames[ids[i]] = names[i];
                let id = ids[i];
                let name = names[i];
                if (parseInt(id) !== playerId){
                    addPlayerNameToSidebar(name, id);
                    addPlayerNameToNavbar(name, id);
                }
            }
        }
        else{
            console.log("New player "+newPlayerName);
            addPlayerNameToSidebar(newPlayerName, newPlayerId);
            addPlayerNameToNavbar(newPlayerName, newPlayerId);
        }
    });

    function addPlayerNameToNavbar(pn, pid){
        $("#properties").append('<a href = "#" id = "possessions'+pid+'"' +
            'onclick=\"return openPropositionModal('+ pid +');\"' +
            '>'+pn+'</a><div class="dropdown-divider"></div>')
    }

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
        idsToPawns[newPlayerId] = Object.keys(idsToPawns).length;
        idsToPossessions[newPlayerId] = initPossessions();
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

    socket.on('accepted', function(data){
        let sender = data["sender"];
        let receiver = data["receiver"];
        let money = parseInt(data["money"]);
        let offered = data["offered"];
        let wanted = data["wanted"];
        let display = "Le joueur "+idsToNames[sender]+" vient d'échanger ses propriétés "+offered;
        if (money > 0)
            display += " et de donner "+money+"€";
        display += " au joueur "+idsToNames[receiver]+" en échange";
        if (money < 0)
            display += " de "+(-1)*money+ " et ";
        if (wanted.length !== 0)
            display += " des propriéts "+wanted;
        console.log(display);
    });

    socket.on("offer", function(data){
        let target = data["receiver"];
        if (playerId === target){
            let pid = data["player_id"];
            let offeredProperties = data["offered_properties"];
            let wantedProperties = data["wanted_properties"];
            let money = data["money"];
            openOfferModal(pid, money, offeredProperties, wantedProperties);
        }
    });

    socket.on("trade", function(data) {
        // Update sidebar
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
    });

    socket.on('play_turn', async function(data) {
        // Add user <-> property dep
        let bought = data["bought"];
        if (bought != null){
            let id = Object.keys(bought)[0];
            let newPossession = bought[id];
            let new_pos = "<div class=\"form-check\">" +
                "<input class=\"form-check-input\" type=\"checkbox\" value=\""+newPossession+"\">\n" +
                "  <label class=\"form-check-label\" for=\"defaultCheck1\">" + newPossession + "</label></div>";
            if (parseInt(data["previous_player"]) === playerId) {
                $("#properties_to_offer").append(new_pos);
            }
            if (possessions[id] === undefined){
                possessions[id] = [newPossession];
            }
            else{
                possessions[id].push(newPossession);
                // $("#properties"+id).append(item); TODO
            }
        }
        // Update sidebar
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
        let dices = data["dices"];
        if (dices != null){
            console.log("dices");
            await randomDiceThrow(dices);
            await waitDices(data);
        }
        else{
            await updatePawn(data);
        }
    });

    async function waitDices(data){
        if (!scene.children[7].visible){
            await updatePawn(data);
        }
        else{
            requestAnimationFrame(() => waitDices(data));
        }
    }

    async function updatePawn(data){
        // Update current pawn and array
        currentPawn = idsToPawns[data["player_turn"]];
        stateArray = data["state_array"];
        updateAllHouses();
        let goToPrison = data["go_to_prison"];
        let previousPlayer = data["previous_player"];
        if (goToPrison){
            // First go to the jail box
            stateArray[10][0].pop();
            stateArray[30][0].push(previousPlayer);
            updateAllPlayers();
            // Then go to jail
            stateArray[30][0].pop();
            stateArray[10][0].push(previousPlayer);
        }
        waitForMotion();
        await waitForModal(data);
    }

    function waitForMotion(){
        // Block the following if still animating pawns
        if (!incrementing){
            updateAllPlayers();
        }
        else{
            requestAnimationFrame(() => waitForMotion());
        }
    }

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
                if (data["card_type"]==="street"){
                    updateModalCardProperty(data["box_name"], data["box_rent"][0], data["box_rent"][1], data["box_rent"][2],
                    data["box_rent"][3], data["box_rent"][4], data["box_rent"][5], data["house_price"],
                    parseInt(data["box_price"])/2, data["box_color"]);
                }
                else if (data["card_type"]=== "station"){
                    updateModalCardStation(data["box_name"]);
                }
                else if (data["card_type"] === "public-company"){
                    updateModalCardCompany(data["box_name"]);
                }
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

function openPropositionModal(id){
    let currentMoney = idsToPossessions[playerId]["money"];
    let otherMoney = idsToPossessions[id]["money"];
    $("#text-offer").replaceWith("<p>Vous pouvez échanger plusieurs propriétés au joueur "
        + idsToNames[id] + " contre une ou plusieurs propriétés et/ou de l'argent.</p>");
    $("#myRange").attr("max", currentMoney);
    $("#myRange").attr("min", -parseInt(otherMoney));
    $("properties_to_buy").innerHTML = '';
    let posses =  possessions[id];
    for (let i = 0; i < posses.length; i++) {
        let pos = posses[i];
        let new_pos = "<div class=\"form-check\">" +
            "<input class=\"form-check-input\" type=\"checkbox\" value=\""+pos+"\">\n" +
            "  <label class=\"form-check-label\" for=\"defaultCheck1\">" + pos + "</label></div>";
        $("#properties_to_buy").append(new_pos);
    }
    $("#modalMakeOffer").modal({ keyboard: false, backdrop: 'static' });
    $("#modalSendOffer").click(
        function(){
            let money = $("#myRange")[0].value;
            let buy = [];
            let checked_prop = $("#properties_to_buy input:checked:enabled");
            for (let i = 0; i<checked_prop.length; i++){
                let prop = checked_prop[i];
                buy.push(prop["value"]);
            }
            let offer = [];
            checked_prop = $("#properties_to_offer input:checked:enabled");
            for (let i = 0; i<checked_prop.length; i++){
                let prop = checked_prop[i];
                offer.push(prop["value"]);
            }
            socket.emit('offer',
                {game_id: gameId, player_id: playerId, receiver: id,
                    money: money,
                    offered_properties: buy,
                    wanted_properties: offer,
                    action: "offer"});
    });
}

function openOfferModal(pid, money, offered, wanted){
    let offer = "Le joueur <b>"+idsToNames[pid]+"</b> veut acquérir vos propriétés" +
        "<ul class=\"list-group\">";
    for (let i = 0; i<offered.length; i++){
        let prop = offered[i];
        offer += "<li class=\"list-group-item\">"+prop+"</li>";
    }
    offer += "</ul>";
    if (money >= 0) {
        offer += "<br>En te proposant la modique somme de <b>" + money +"€</b><br>";
    }
    else{
        offer += "<br>En te réclamant en plus la somme de <b>" + money +"€</b><br>";
    }
    if (wanted.length>0) {
        offer += "Et en échange des propriétés";
        offer += "<ul class=\"list-group\">";
        for (let i = 0; i < wanted.length; i++) {
            let prop = wanted[i];
            offer += "<li class=\"list-group-item\">" + prop + "</li>";
        }
        offer += "</ul>"
    }
    offer += "Acceptes-tu ?";
    $("#proposition").replaceWith(offer);
    $("#modalReceiveOffer").modal({ keyboard: false, backdrop: 'static' });
    $("#acceptOffer").click(
        function(){
            socket.emit('accepted',
                {game_id: gameId, sender: pid, receiver:playerId, money:money,
                    offered:offered, wanted:wanted, action:'accepted'});
        }
    );
}


