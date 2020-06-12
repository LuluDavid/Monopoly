const check =
"<svg class=\"bi bi-check\" style=\"float : right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 16 16\" fill=\"green\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
"  <path fill-rule=\"evenodd\" d=\"M13.854 3.646a.5.5 0 010 .708l-7 7a.5.5 0 01-.708 0l-3.5-3.5a.5.5 0 11.708-.708L6.5 10.293l6.646-6.647a.5.5 0 01.708 0z\" clip-rule=\"evenodd\"/>\n" +
"</svg>";

const uncheck =
"<svg class=\"bi bi-x\" style=\"float : right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 16 16\" fill=\"red\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
"  <path fill-rule=\"evenodd\" d=\"M11.854 4.146a.5.5 0 010 .708l-7 7a.5.5 0 01-.708-.708l7-7a.5.5 0 01.708 0z\" clip-rule=\"evenodd\"/>\n" +
"  <path fill-rule=\"evenodd\" d=\"M4.146 4.146a.5.5 0 000 .708l7 7a.5.5 0 00.708-.708l-7-7a.5.5 0 00-.708 0z\" clip-rule=\"evenodd\"/>\n" +
"</svg>";


function propertyCard(name, rent, oneHouse, twoHouses, threeHouses, fourHouses, hotel, housePrice,
                      hypotheque){
    return `<div id="card" class="border border-dark" style="width:220px; margin-left: auto; margin-right: auto; margin-top: 10px">
        <div id="box-title" class = "border border-dark" align="center" style="background-color: yellow; width : 200px; margin-top: 10px; margin-left: 10px">
        <h6><strong> ` + name +` </strong></h6>
		</div>
		<div id="rent" style="margin-left: 10px; font-size: 13px">
			<div id="no-house" style="margin-top: 8px">
				<strong> Terrain nu : </strong>
				<span>`+rent+`€</span>
			</div>
			<div id="one-house">
				<strong> Avec 1 maison : </strong>
				<span> `+ oneHouse +` €</span>
			</div>
			<div id="two-houses">
				<strong> Avec 2 maisons : </strong>
				<span> `+ twoHouses+` € </span>
			</div>
			<div id="three-houses">
				<strong> Avec 3 maisons : </strong>
				<span> `+ threeHouses +`€</span>
			</div>
			<div id="four-houses">
				<strong> Avec 4 maisons : </strong>
				<span> `+ fourHouses+` €</span>
			</div>
			<div id="five-houses">
				<strong> Avec Hotel : </strong>
				<span> `+ hotel +` € </span>
			</div>
		</div>
		<div class="border-top border-dark" style="font-size: 11px; margin-top: 5px; margin-left: 4px; margin-right: 4px">
			<div class="text-justify" style="margin-top: 4px; margin-bottom: 4px">
				Si un joueur possede <strong>TOUS</strong> les terrains d'un Groupe de couleur quelconque,
				le loyer des terrains nus de ce groupe est double.
			</div>
		</div>
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

function servicesCard(){
    return `<div id="serviceCard" className="border border-dark"
                style="width:220px; height:313px; margin-top: 10px; margin-left: 10px">
        <div id="icon" style="font-size: 60px">
            <p style="text-align:center; margin:0; padding:0"><i className="fa fa-tint" style="text-align :center"></i>
            </p>
            <!--<p style="text-align:center"><i class="fa fa-lightbulb-o" style="text-align :center"></i></p>-->
        </div>
        <div style="font-size: 17px; text-align : center">
            <span><strong> Compagnie de distribution des eaux </strong></span>
        </div>
        <div>
            <div className="text-center" style="margin-right: 5px; margin-left: 5px; font-size: 11.5px">
                Si l'on possede UNE carte de compagnie de Service Public, le loyer est 4 fois le montant indique par les
                des.
            </div>
            <div className="text-center"
                 style="margin-right: 5px; margin-left: 5px; font-size: 11.5px; margin-top: 6px">
                Si l'on possede les DEUX cartes de compagnie de Service Public, le loyer est 10 fois le montant indique
                par les des.
            </div>
            <div style="font-size : 13px; text-align : center; margin-top: 8px">
                <span> Valeur Hypothecaire : 75 €</span>
            </div>
        </div>
    </div>`;
}

function stationCard(name){
    return `<div id="trainCard" className="border border-dark"
                style="width:220px; height:313px; margin-top: 10px; margin-left: 10px">
        <div id="icon" style="font-size: 70px">
            <p style="text-align:center"><i className="fa fa-train" style="text-align :center"></i></p>
        </div>
        <div style="font-size: 20px; text-align : center">
            <span><strong> `+ name +` </strong></span>
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


function updateModalCard(name, rent, oneHouse, twoHouses, threeHouses, fourHouses, hotel, housePrice, hypotheque){
    $("#card").replaceWith(propertyCard(name, rent,oneHouse,twoHouses,threeHouses,fourHouses,hotel,housePrice,hypotheque));
}


function frontMoney(money = initialMoney){
    return `<div id="player-money">
                <i class="fa fa-money" style="color:green"> ` + money + `€</i></div>`;
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
