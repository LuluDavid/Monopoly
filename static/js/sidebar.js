const check =
"<svg class=\"bi bi-check\" style=\"float : right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 16 16\" fill=\"green\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
"  <path fill-rule=\"evenodd\" d=\"M13.854 3.646a.5.5 0 010 .708l-7 7a.5.5 0 01-.708 0l-3.5-3.5a.5.5 0 11.708-.708L6.5 10.293l6.646-6.647a.5.5 0 01.708 0z\" clip-rule=\"evenodd\"/>\n" +
"</svg>";

const uncheck =
"<svg class=\"bi bi-x\" style=\"float : right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 16 16\" fill=\"red\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
"  <path fill-rule=\"evenodd\" d=\"M11.854 4.146a.5.5 0 010 .708l-7 7a.5.5 0 01-.708-.708l7-7a.5.5 0 01.708 0z\" clip-rule=\"evenodd\"/>\n" +
"  <path fill-rule=\"evenodd\" d=\"M4.146 4.146a.5.5 0 000 .708l7 7a.5.5 0 00.708-.708l-7-7a.5.5 0 00-.708 0z\" clip-rule=\"evenodd\"/>\n" +
"</svg>";


const color_hex = {
    "brown": "color:#8B4513",
    "light-blue": "color:#87CEEB",
    "pink": "color:#FF69B4",
    "orange": "color:#FF8C00",
    "red": "color:red",
    "yellow": "color:#FFD700",
    "green": "color:green",
    "dark-blue": "color:blue"
};

function frontMoney(money = initialMoney){
    return `<div id="player-money">
                <i class="fa fa-money" style="color:green">${money} $</i></div>`;
}

function street_icon(color, i){
    if (i === 0){
        return "";
    }
    let style = color_hex[color];
    return`<div id=`+color+`>
              <i class="fa fa-flag" style=${style}>${i}</i>
           </div>`;
}

function station_icon(i){
    if (i === 0){
        return "";
    }
    return`<div id="player-station">
              <i class="fa fa-train" aria-hidden="true" style="color:black">${i}</i>
           </div>`;
}

function electricity_icon(i){
    if (i === 0){
        return "";
    }
    return `<div id="electricity" style="margin-left: 10px">
                <i class="fa fa-lightbulb-o" style="color:black"></i>
            </div>`;
}

function water_icon(i){
    if (i === 0){
        return "";
    }
    return `<div id="water" style="margin-left: 10px">
                <i class="fa fa-tint" style="color:black"></i>
            </div>`;
}

function frontPossessions(brown = 0, lightBlue = 0, pink = 0, orange = 0,
                          red = 0, yellow = 0, green = 0, darkBlue = 0,
                          station = 0, electricity = 0, water = 0){
    // Street divs
    let brown_div = street_icon("brown", brown);
    let lightBlue_div = street_icon("light-blue", lightBlue);
    let pink_div = street_icon("pink", pink);
    let orange_div = street_icon("orange", orange);
    let red_div = street_icon("red", red);
    let yellow_div = street_icon("yellow", yellow);
    let green_div = street_icon("green", green);
    let dark_blue_div = street_icon("dark-blue", darkBlue);
    // Service divs
    let stations_div = station_icon(station);
    let electricity_div = electricity_icon(electricity);
    let water_div = water_icon(water);

    return `<div id="player-goods">
            <div id="player-houses" style="display : flex; flex-direction: row; font-size: 14.7px">
                ${brown_div}
                ${lightBlue_div}
                ${pink_div}
                ${orange_div}
                ${red_div}
                ${yellow_div}
                ${green_div}
                ${dark_blue_div}
            </div>
            <div id="player-station-services" style="display : flex; flex-direction: row">
                ${stations_div}
                ${electricity_div}
                ${water_div}
            </div>
        </div>` ;
}

const frontGoods = frontMoney()+frontPossessions();

function updateSidebar(){
    for (let pid of Object.keys(idsToPossessions)){
        updateSidebarId(pid);
    }
}
function updateSidebarId(pid){
    console.log("updateSidebarId for " + pid);
    let possessions;
    let money, brown, lightBlue, pink, orange, red, yellow, green, darkBlue, station, electricity, water;
    possessions = idsToPossessions[pid];
    money = possessions["money"];
    brown = possessions["brown"];
    lightBlue = possessions["light-blue"];
    pink = possessions["pink"];
    orange = possessions["orange"];
    red = possessions["red"];
    yellow = possessions["yellow"];
    green = possessions["green"];
    darkBlue = possessions["dark-blue"];
    station = possessions["station"];
    electricity = possessions["electricity"];
    water = possessions["water"];

    $("#"+pid+" #player-money").replaceWith(frontMoney(money));
    $("#"+pid+" #player-goods").replaceWith(frontPossessions(brown, lightBlue, pink, orange, red,
        yellow, green, darkBlue, station, electricity, water));
}