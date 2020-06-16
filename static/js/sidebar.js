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
function propertyCard(name, rent, oneHouse, twoHouses, threeHouses, fourHouses, hotel, housePrice,
                      hypotheque, color){
    return `<div id="card" class="border border-dark" style="width:220px; margin-left: auto; margin-right: auto; margin-top: 10px">
        <div id="box-title" class = "border border-dark" align="center" style="background-` + color_hex[color] +
        `; width : 200px; margin-top: 10px; margin-left: 10px">
        <h6><strong> ` + name +` </strong></h6>
		</div>
		<div id="rent" style="margin-left: 10px; font-size: 13px">
			<div id="no-house" style="margin-top: 8px">
                <span style="text-align:left;">
                    <strong> Loyer : </strong>
                    <span style="float:right;">`+rent+`€</span>
                </span>
			</div>
			<div id="one-house">
			    <span style="text-align:left;">
                    <strong> Avec 1 maison :</strong>
                    <span style="float:right;">`+ oneHouse +` € </span>
                </span>
			</div>
			<div id="two-houses">
			    <span style="text-align:left;">
                    <strong> Avec 2 maisons :</strong>
                    <span style="float:right;"> `+ twoHouses +` € </span>
                </span>
			</div>
			<div id="three-houses">
			    <span style="text-align:left;">
                    <strong> Avec 3 maisons :</strong>
                    <span style="float:right;">`+ threeHouses + ` € </span>
                </span>
			</div>
			<div id="four-houses">
			    <span style="text-align:left;">
                    <strong> Avec 4 maisons :</strong>
                    <span style="float:right;"> `+ fourHouses + ` € </span>
                </span>
			</div>
			<div id="five-houses">
			    <span style="text-align:left;">
                    <strong> Avec Hotel :</strong>
                    <span style="float:right;"> `+ hotel + ` € </span>
                </span>
			</div>
		</div>
		<!--<div class="border-top border-dark" style="font-size: 11px; margin-top: 5px; margin-left: 4px; margin-right: 4px">
			<div class="text-justify" style="margin-top: 4px; margin-bottom: 4px">
				Si un joueur possede <strong>TOUS</strong> les terrains d'un Groupe de couleur quelconque,
				le loyer des terrains nus de ce groupe est double.
			</div>
		</div>-->
		<div class="border-top border-dark" style="font-size: 12px; margin-left: 4px; margin-right: 4px">
			<div style="margin-top: 5px">
				<strong> Prix des maisons : </strong>
				<span> `+ housePrice +` € </span>
			</div>
			<div>
				<strong> Prix d'un Hotel : </strong>
				<span> `+ housePrice+` € + 4 maisons</span>
			</div>
		</div>
		<div id="hypotheque" align="center" style="font-size: 12px; margin-top: 6px; margin-bottom: 6px">
			<span> Valeur hypothecaire du terrain : </span>
			<span> `+ hypotheque+` € </span>
		</div>
	</div>`;
}

function companyCard(name){
    let first;
    if (name === "Compagnie de distribution d'electricite") {
        first = `<div id="card" class="border border-dark" style="width:220px; margin-left: auto; margin-right: auto; margin-top: 10px">
            <div id="icon" style="font-size: 60px">
                <p style="text-align:center; margin:0; padding:0"><i class="fa fa-lightbulb-o" style="text-align :center"/>
                </p></div>`;
    }
    else {
        first = `<div id="card" class="border border-dark" style="width:220px; margin-left: auto; margin-right: auto; margin-top: 10px">
            <div id="icon" style="font-size: 60px">
                <p style="text-align:center; margin:0; padding:0"><i class="fa fa-tint" style="text-align :center"/>
                </p></div>`;
    }
    let second = `<div style="font-size: 17px; text-align : center">
            <span><strong>`+ name +`  </strong></span>
        <div>
        </div>
            <div class="text-center" style="margin-right: 5px; margin-left: 5px; font-size: 11.5px">
                Si l'on possede UNE carte de compagnie de Service Public, le loyer est 4 fois le montant indique par les des.
            </div>
            <div class="text-center" style="margin-right: 5px; margin-left: 5px; font-size: 11.5px; margin-top: 6px">
                Si l'on possede les DEUX cartes de compagnie de Service Public, le loyer est 10 fois le montant indique par les des. 
            </div>
            <div style="font-size : 13px; text-align : center; margin-top: 8px">
                <span> Valeur Hypothecaire : 75 €</span>
            </div>
        </div>
    </div>`;
    return first + second;
}

function stationCard(name){
    return `<div id="card" class="border border-dark" style="width:220px; margin-left: auto; margin-right: auto; margin-top: 10px">
        <div id="icon" style="font-size: 70px">
            <p style="text-align:center"><i class="fa fa-train" style="text-align :center"/></p>
        <div style="font-size: 20px; text-align : center">
            <span><strong> `+ name +` </strong></span>
        </div>
        </div>
        <div style="font-size: 13px; margin-top: 15px; margin-left:5px; margin-right: 5px">
            <div>
				<span style="text-align:left;">
				    Loyer : 
				    <span style="float:right;">
				        25 €
				    </span>
				</span>
            </div>
            <div>
				<span style="text-align:left;">
				     Si vous avez 2 gares : 
				    <span style="float:right;">
				        50 €
				    </span>
				</span>
            </div>
            <div>
				<span style="text-align:left;">
				     Si vous avez 3 gares : 
				    <span style="float:right;">
				        100 €
				    </span>
				</span>
            </div>
            <div>
				<span style="text-align:left;">
				     Si vous avez 4 gares : 
				    <span style="float:right;">
				        200 €
				    </span>
				</span>
            </div>
        </div>
        <div style="font-size : 15px; text-align : center; margin-top: 15px">
            <span> Valeur Hypothecaire : 100 €</span>
        </div>
    </div>`;
}


function updateModalCardProperty(name, rent, oneHouse, twoHouses, threeHouses, fourHouses, hotel, housePrice, hypotheque, color){
    $("#card").replaceWith(propertyCard(name, rent,oneHouse,twoHouses,threeHouses,fourHouses,hotel,housePrice,hypotheque, color));
}

function updateModalCardStation(name){
    $("#card").replaceWith(stationCard(name));
}

function updateModalCardCompany(name){
    $("#card").replaceWith(companyCard(name));
}

function frontMoney(money = initialMoney){
    return `<div id="player-money">
                <i class="fa fa-money" style="color:green"> ` + money + `€</i></div>`;
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
                <i class="fa fa-lightbulb-o" style="color:black"/>
            </div>`;
}

function water_icon(i){
    if (i === 0){
        return "";
    }
    return `<div id="water" style="margin-left: 10px">
                <i class="fa fa-tint" style="color:black"/>
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
