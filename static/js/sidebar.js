const check =
"<svg class=\"bi bi-check\" style=\"float : right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 16 16\" fill=\"green\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
"  <path fill-rule=\"evenodd\" d=\"M13.854 3.646a.5.5 0 010 .708l-7 7a.5.5 0 01-.708 0l-3.5-3.5a.5.5 0 11.708-.708L6.5 10.293l6.646-6.647a.5.5 0 01.708 0z\" clip-rule=\"evenodd\"/>\n" +
"</svg>";

const uncheck =
"<svg class=\"bi bi-x\" style=\"float : right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 16 16\" fill=\"red\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
"  <path fill-rule=\"evenodd\" d=\"M11.854 4.146a.5.5 0 010 .708l-7 7a.5.5 0 01-.708-.708l7-7a.5.5 0 01.708 0z\" clip-rule=\"evenodd\"/>\n" +
"  <path fill-rule=\"evenodd\" d=\"M4.146 4.146a.5.5 0 000 .708l7 7a.5.5 0 00.708-.708l-7-7a.5.5 0 00-.708 0z\" clip-rule=\"evenodd\"/>\n" +
"</svg>";

function frontMoney(money = initialMoney){
    return `<div id="player-money">
                <i class="fa fa-money" style="color:green"> ` + money + `$</i></div>`;
}

function frontPossessions(brown = 0, lightBlue = 0, magenta = 0, orange = 0,
                          red = 0, yellow = 0, green = 0, blue = 0,
                          station = 0, electricity = 0, water = 0){
    return `<div id="player-goods">
            <div id="player-houses" style="display : flex; flex-direction: row; font-size: 14.7px">
                <div id="brown">
                    <i class="fa fa-home" style="color:#8B4513"> `+ brown +`</i>
                </div>
                <div id="light-blue">
                    <i class="fa fa-home" style="color:#87CEEB"> `+ lightBlue +`</i>
                </div>
                <div id="magenta">
                    <i class="fa fa-home" style="color:#FF69B4"> `+ magenta +`</i>
                </div>
                <div id="orange">
                    <i class="fa fa-home" style="color:#FF8C00"> `+ orange +`</i>
                </div>
                <div id="red">
                    <i class="fa fa-home" style="color:red"> `+ red +`</i>
                </div>
                <div id="yellow">
                    <i class="fa fa-home" style="color:#FFD700"> `+ yellow +`</i>
                </div>
                <div id="green">
                    <i class="fa fa-home" style="color:green"> `+ green +`</i>
                </div>
                <div id="blue">
                    <i class="fa fa-home" style="color:blue"> `+ blue +`</i>
                </div>
            </div>
            <div id="player-station-services" style="display : flex; flex-direction: row">
                <div id=player-station" style="height:20px">
                    <i class="fa fa-train" aria-hidden="true" style="color:black"> `+ station +` </i>
                </div>
                <div id="electricity" style="margin-left: 10px">
                    <i class="fa fa-lightbulb-o" style="color:black"> `+ electricity +` </i>
                </div>
                <div id="water" style="margin-left: 10px">
                    <i class="fa fa-tint" style="color:black"> `+ water +`</i>
                </div>
            </div>
        </div>` ;
}

const frontGoods = frontMoney()+frontPossessions();

/* We suppose we have a mapping :
* dict : { "player1":{"money":int, "houses":{"brown":int, ...},
* "station":int, "electricity":bool, "water":bool} ... }
* */
function updateSidebar(){
    for (let pid of Object.keys(idsToPossessions)){
        updateSidebarId(pid);
    }
}
function updateSidebarId(pid){
    let possessions, houses;
    let money, brown, lightBlue, magenta, orange, red, yellow, green, blue, station, electricity, water;
    possessions = idsToPossessions[pid];
    money = possessions["money"];
    houses = possessions["houses"];
    brown = houses["brown"];
    lightBlue = houses["lightBlue"];
    magenta = houses["magenta"];
    orange = houses["orange"];
    red = houses["red"];
    yellow = houses["yellow"];
    green = houses["green"];
    blue = houses["blue"];
    station = possessions["station"];
    electricity = possessions["electricity"];
    water = possessions["water"];

    $("#"+pid+" #player-money").replaceWith(frontMoney(money));
    $("#"+pid+" #player-goods").replaceWith(frontPossessions(brown, lightBlue, magenta, orange, red,
        yellow, green, blue, station, electricity, water));
}