// MAIN FUNCTION

// Whose turns it is
var currentPawn = 0;
var windowWidth, windowHeight;
const view =
	{
		near: 1,
		far: 10000,
		background: new THREE.Color(255, 255, 255),

		// The camera's position
		eye: [-100, -100, 100],
		// The up vector (defines the human perspective)
		up: [0, 0, 1],
		fov: 30,

		updateCamera: function (camera, scene) {
			// Look the board's center once its created
			if (scene.children[2] != null) {
				camera.lookAt(scene.children[2].position)
			} else {
				camera.lookAt(scene.position)
			}
		}
	};

const closeView =
	{
		near: 0.1,
		far: 1000,
		background: new THREE.Color(255, 255, 255),

		// The camera's position
		eye: [55, 55, 30],
		// The up vector (defines the human perspective)
		up: [0, 0, 1],
		fov: 20,

		updateCamera: function (camera, scene) {
			// Look the board's center once its created
			if (currentPawn >= 0) {
				camera.lookAt(scene.children[3].children[currentPawn].position)
			}
		}
	};


// Ratio of graphics on the main page
const graphicsRatio = 1 - 0.167;

// Cardboard
const cardboardHeight = 0.03;
const cardboardWidth = 110;
// Number of boxes
const numberOfBoxes = 40;
// Pawns
var numberOfPawns = 0;

const pawnHeight = 2;
const pawnRadius = 0.5;
// House Ratio
const houseRatio = 1 / 7;
const houseColor = 0x00ff00;
// Box
const coverRatio = 0.7;
const boxWidth = cardboardWidth / 12.2;
const boxHeight = 1.6 * boxWidth;
const boxHeightHouse = boxHeight * (1 - houseRatio);
const boxHeightHouseBand = boxHeight * houseRatio;
const maxNumberOfHouse = 4;
// House band width
const houseWidthBox = boxHeight * houseRatio;
// House
const houseWidth = 1;
const houseHeight = houseWidth / 2;
const roofAngle = Math.PI / 4;
// Box positions
var boxes = getBoxesPositions(cardboardWidth);
// Accuracy for pawn motion
const epsilon = 1;
const coverMotion = 0.8;
// Pawn motion
const tMotion = 3; // duration to go to next case (seconds)

// Incrementing boolean to avoid multi-calls
var incrementing = false;
// CloseView activation boolean
var closeViewDisplay = false;
const closeViewRatio = 0.35;
const closeViewHeight = 50;
const closeViewFurtherRatio = 2;
// House relative position
const houseRelativePos = getHouseRelativePositions();
var housePositions = getHousesPositions(cardboardWidth);
// The ratio the card travels to towards the player
const cardUserRatio = 0.5;
var movingCard = false;
const cardAxis = new THREE.Vector3(0,-1,0).normalize();
// The angle the cards has rotated when it reaches the player
const revealAngle = 2*Math.PI/5;
const tReveal = 1;
const tTravel = 2;
// Number of house per box
// var numberOfHousesPerBox = noHousesPerBox();
// Hotel
const hotelHouseRatio = 3;
// Deck stuff
const deckRatio = 1.587;
const heightRatio = 5.827;
const deckSize = 20;

/*
 * Build scene
 */
// General camera
var container = document.getElementById('container');
view.camera = new THREE.PerspectiveCamera(view.fov, window.innerWidth / window.innerHeight, view.near, view.far);
view.camera.position.fromArray(view.eye);
view.camera.up.fromArray(view.up);
// Close camera
closeView.camera = new THREE.PerspectiveCamera(closeView.fov, window.innerWidth / window.innerHeight, closeView.near, closeView.far);
closeView.camera.position.fromArray(closeView.eye);
closeView.camera.up.fromArray(closeView.up);
// Scene
const scene = new THREE.Scene();
const loader = new THREE.TextureLoader();
loader.load('static/js/graphics/textures/clearSky.jpg', function (texture) {
	scene.background = texture;
});
scene.background = new THREE.Color(0x0000ff);

/*
 * Renderer Settings
 */
const renderer = new THREE.WebGLRenderer({antialias: true});
// Enable extension
renderer.getContext().getExtension('EXT_color_buffer_half_float');
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight - 54);
renderer.shadowMap.enabled = true;
renderer.shadowMapSoft = true;
renderer.shadowMapDebug = true;
renderer.domElement.style += "; position:relative; z-index:0; width:100%; height:100%";
container.appendChild(renderer.domElement);

// Orbit controls
const controls = new THREE.OrbitControls(view.camera, renderer.domElement);

/*
 * Instantiate and add the objects
 */
// Add a light
addALight(scene);
// Add a ground
createGround(scene);
// Add the cardboard
const cardboard = createCardboard(cardboardWidth, scene);
cardboard.rotateZ(Math.PI / 2);
cardboard.castShadow = true;
cardboard.receiveShadow = true;

// Pawn positions per box (where to put them to make them fit in)
var pawnsPositionsPerBox = getPawnsPositionsBoxes(cardboardWidth);
// To fill in when players start the game
var pawns = new THREE.Group();
// Fill empty
updatePawns();
// Represents the current state for all players
var stateArray = initState();
var idsToPawns = {};
var idsToPossessions = initPossessions();
// Instantiate empty houses group
updateAllHouses();
// Set the positions of the pawns on the cardboard in positions (fast access to positions)
var positions = initPositions();
var new_positions = initPositions();
// Create the deck of community cards
const communityDeck = createCommunityDeck();
scene.add(communityDeck);
// Create the deck of chance cards
const chanceDeck = createChanceDeck();
scene.add(chanceDeck);

function updatePawns(){
	pawnsPositionsPerBox = getPawnsPositionsBoxes(cardboardWidth);
	let pawnObjects = createPawns(numberOfPawns);
	pawns = new THREE.Group();
	addPawns(pawnObjects, pawns);
	// Replace previous pawns with the new ones, or just create them
	scene.children[3] = pawns;
}

function initPossessions(){
	let ids = Object.keys(idsToPawns);
	let res = {};
	let initialPossession = {"money":initialMoney, "houses":{"brown":0, "lightBlue":0, "magenta":0, "orange":0,
			"red":0, "yellow":0, "green":0, "blue":0}, "station":0, "electricity":0, "water":0};
	for (let i = 0; i<numberOfPawns; i++){
		res[ids[i]] = initialPossession;
	}
	return res;
}

function createCommunityCard() {
	let cardGeometry = new THREE.PlaneGeometry(deckSize/deckRatio, deckSize);
	let topMaterial = new THREE.MeshBasicMaterial(
		{map: new THREE.TextureLoader().load('static/js/graphics/textures/Community.jpg'), side:2});
	let card = new THREE.Mesh(cardGeometry, topMaterial);
	card.position.set(8/11*cardboardWidth, 8/11*cardboardWidth, cardboardHeight+deckSize/heightRatio-0.1); // Quick fix
	card.rotateZ(Math.PI/4);
	return card;
}

function createChanceCard() {
	let cardGeometry = new THREE.PlaneGeometry(deckSize/deckRatio, deckSize);
	let topMaterial = new THREE.MeshBasicMaterial(
		{map: new THREE.TextureLoader().load('static/js/graphics/textures/Chance.jpg'), side:2});
	let card = new THREE.Mesh(cardGeometry, topMaterial);
	card.position.set(3/11*cardboardWidth, 3/11*cardboardWidth, cardboardHeight+deckSize/heightRatio-0.1);
	card.rotateZ(Math.PI/4);
	return card;
}

function disableControls(){
	controls.enabled = false;
	controls.autoRotate = false;
}

// TODO: maybe also rotate the card horizontally and allow full autoRotation in ObritControls
function animateCard(type){
	disableControls();
	if (movingCard){
		console.log("A card is already moving currently");
		return;
	}
	// First, create the card to lift
	let card = (type === "community-fund")?createCommunityCard():createChanceCard();
	scene.add(card);
	render();
	// Then, lift the card towards the camera
	let fps = 60;           // seconds
	let tau = tTravel;
	let step = 1 / (tau * fps);  // t-step per frame
	let finalAngle = Math.PI/2 - Math.asin(view.camera.position.z/norm(view.camera.position));
	let angleStep = finalAngle*step;
	let t = 0;
	var object = scene.children[7];
	let initialPosition = object.position.clone();
	let goalPosition = new THREE.Vector3(view.camera.position.x,
										 view.camera.position.y,
										 view.camera.position.z);
	movingCard = true;
	loopCard(object, initialPosition, goalPosition, step, t, angleStep);
}

// Loop function
function loopCard(object, initialPosition, goalPosition, step, t, angleStep) {
	// Update the pawn's position
	let X = translation(initialPosition.x, goalPosition.x, ease(cardUserRatio*t));   // interpolate between a and b where
	let Y = translation(initialPosition.y, goalPosition.y, ease(cardUserRatio*t));   // t is first passed through a easing
	let Z = translation(initialPosition.z, goalPosition.z, ease(cardUserRatio*t));   // function in this example.
	object.position.set(X, Y, Z);  // set new position
	object.rotateOnAxis(cardAxis, angleStep);
	// Increment the time and loop back
	t = t + step;
	if (t >= 1) {
		return loopCard2(step, t);
	}
	requestAnimationFrame(() => loopCard(object, initialPosition, goalPosition, step, t, angleStep))
}

function loopCard2(step, t) {
	t = t + step;
	if (t >= 1 / coverRatio) {
		let fps = 60;           // seconds
		let dt = tReveal;
		let step = 1 / (dt * fps);  // t-step per frame
		let angleStep = -revealAngle*step;
		return semiReveal(scene.children[7], step, 0, angleStep);
	}
	requestAnimationFrame(() => loopCard2(step, t));
}

function norm(v) {
	return Math.sqrt(v.x*v.x+v.y*v.y+v.z*v.z);
}

function semiReveal(object, step, t, angleStep){
	t += step;
	if (t >= 1) {
		console.log("Done");
		removeCard();
		movingCard = false;
		controls.enabled = true;
		controls.autoRotate = true;
		return;
	}
	object.rotateOnAxis(cardAxis, angleStep);
	requestAnimationFrame(() => semiReveal(object, step, t, angleStep));
}

function removeCard() {
	scene.remove(scene.children[7]);
}

function init() {
	animate();
}


/*
 * Loop functions
 */

function animate() {
	controls.update();
	render();
	requestAnimationFrame(animate);
}

// Render the camera
function render() {

	updateSize();

	if (!closeViewDisplay) updateView();
	else {
		updateView();
		updateCloseView()
	}
}

function updateView(vleft = 0, vtop = 0, vwidth = graphicsRatio, vheight = 1) {
	// First view
	view.updateCamera(view.camera, scene);

	var left = Math.floor(windowWidth * vleft);
	var top = Math.floor(windowHeight * vtop);
	var width = Math.floor(windowWidth * vwidth);
	var height = Math.floor(windowHeight * vheight);

	renderer.setViewport(left, top, width, height);
	renderer.setScissor(left, top, width, height);
	renderer.setScissorTest(true);
	renderer.setClearColor(view.background);

	view.camera.aspect = width / height;
	view.camera.updateProjectionMatrix();

	renderer.render(scene, view.camera);
}

function updateCloseView(vleft = (graphicsRatio - closeViewRatio), vtop = (1 - closeViewRatio),
						 vwidth = closeViewRatio, vheight = closeViewRatio) {
	// Second view
	closeView.updateCamera(closeView.camera, scene);

	var leftCloseView = Math.floor(windowWidth * vleft);
	var topCloseView = Math.floor(windowHeight * vtop);
	var widthCloseView = Math.floor(windowWidth * vwidth);
	var heightCloseView = Math.floor(windowHeight * vheight);

	renderer.setViewport(leftCloseView, topCloseView, widthCloseView, heightCloseView);
	renderer.setScissor(leftCloseView, topCloseView, widthCloseView, heightCloseView);
	renderer.setScissorTest(true);
	renderer.setClearColor(closeView.background);

	closeView.camera.aspect = widthCloseView / heightCloseView;
	closeView.camera.updateProjectionMatrix();

	renderer.render(scene, closeView.camera);
}

// Adapt to the screen size
function updateSize() {
	if (windowWidth !== window.innerWidth) {
		windowWidth = window.innerWidth;
		windowHeight = window.innerHeight - 54;
		renderer.setSize(windowWidth, windowHeight);
	}
}

/*
 * Loop Utils
 */

function updateAllPlayers(){
	for (let i = 0; i<numberOfBoxes; i++){
		let pawns = stateArray[i][0];
		for (let j = 0; j<pawns.length; j++){
			let playerId = pawns[j];
			console.log("Updating playerId "+playerId);
			let pawnNumber = idsToPawns[playerId];
			console.log("Found pawn number "+pawnNumber);
			let pawn = scene.children[3].children[pawnNumber];
			if (pawn.currentBox !== i){
				translatePawnToBox(pawnNumber, i);
			}
		}
	}
}

// Translate pawn n°i to box n°j
function translatePawnToBox(i, j) {
	let boxCardinal = Math.max(positions[j].length, new_positions[j].length);
	let pawnPosition = pawnsPositionsPerBox[j][boxCardinal];
	let deltaT = tMotion * Math.pow(j / numberOfBoxes, 1 / 3);
	scene.children[3].children[i].currentBox = j;
	updateNewPositions();
	translate(i, new THREE.Vector3(pawnPosition.x, pawnPosition.y, pawnHeight / 2 + cardboardHeight), deltaT);
}

// Translate pawn n°i to goalPosition
function translate(i, goalPosition, deltaT) {
	incrementing = true;
	closeViewDisplay = true;
	render();
	let fps = 60;           // seconds
	let step = 1 / (deltaT * fps);  // t-step per frame
	let t = 0;
	var object = scene.children[3].children[i];
	let initialPosition = object.position.clone();
	let initialCameraPosition = closeView.camera.position.clone();
	let goalPositionCamera = new THREE.Vector3(goalPosition.x, goalPosition.y, goalPosition.z + closeViewHeight);
	addCanvas();
	loop(object, initialPosition, initialCameraPosition, goalPosition, goalPositionCamera, step, t);
}

// Translation from a to b's parametric equation
function translation(a, b, t) {
	return a + (b - a) * t
}

// Loop function
function loop(object, initialPosition, initialPositionCam, goalPosition, goalPositionCam, step, t) {
	// Update the pawn's position
	let X = translation(initialPosition.x, goalPosition.x, ease(t));   // interpolate between a and b where
	let Y = translation(initialPosition.y, goalPosition.y, ease(t));   // t is first passed through a easing
	let Z = translation(initialPosition.z, goalPosition.z, ease(t));   // function in this example.
	object.position.set(X, Y, Z);  // set new position
	// Update the camera's positions
	let XCam = translation(initialPositionCam.x, goalPositionCam.x, soonerFaster(t * closeViewFurtherRatio));
	let YCam = translation(initialPositionCam.y, goalPositionCam.y, soonerFaster(t * closeViewFurtherRatio));
	let ZCam = translation(initialPositionCam.z, goalPositionCam.z, soonerFaster(t * closeViewFurtherRatio));
	closeView.camera.position.set(XCam, YCam, ZCam);
	// Increment the time and loop back
	t = t + step;
	if (t >= 1) {
		loop2(step, t);
	}
	else{
		requestAnimationFrame(() => loop(object, initialPosition, initialPositionCam, goalPosition, goalPositionCam, step, t))
	}
}

function loop2(step, t) {
	t = t + step;
	if (t >= 1 / coverRatio) {
		removeCanvas();
		console.log("Tour fini");
		incrementing = false;
		closeViewDisplay = false;
		currentPawn++;
		closeView.camera.position.set(closeView.eye[0], closeView.eye[1], closeView.eye[2]);
		updatePositions();
		if (currentPawn === numberOfPawns) {
			currentPawn = 0;
		}
	}
	else{
		requestAnimationFrame(() => loop2(step, t))
	}
}


// Empty constructor for the positions dictionary
function emptyPositions() {
	let positions = {};
	for (let i = 0; i < numberOfBoxes; i++) {
		positions[i] = []
	}
	return positions
}

// Use the currentBox param stored in every pawn to fill the positions dictionary
function updateNewPositions() {
	new_positions = emptyPositions();
	for (let i = 0; i < numberOfPawns; i++) {
		let box = scene.children[3].children[i].currentBox;
		new_positions[box].push(i);
	}
}



function updatePositions() {
	positions = $.extend(true, {}, new_positions);
}

// Random int in [min,max]
function getRandomInt(min, max) {
	return Math.floor(Math.random() * Math.floor(max - min + 1)) + min;
}

// Distance between two points
function distance(v1, v2) {
	return v1.clone().distanceTo(v2.clone());
}


function addCanvas() {
	let height = Math.floor(windowHeight * closeViewRatio);
	let width = Math.floor(windowWidth * closeViewRatio);
	console.log(width);
	let canvas = "<canvas id = 'closeView' width='" + width + "' height='" + height + "' style=\"border:3px solid #000000; position:fixed; top: 56px; right: 0px; z-index:2;\"></canvas>"
	$("#container").append(canvas);
}

function removeCanvas() {
	$("#closeView").remove();
}

// Parabole to describe the motion inertia
function ease(t) {
	return -t * t + 2 * t
}

function soonerFaster(t) {
	return Math.pow(t, 1 / 5);
}

function getHouseRelativePositions() {

	let space = (boxWidth - maxNumberOfHouse * houseWidth) / (maxNumberOfHouse + 1);
	let offset = space - boxWidth / 2;
	let housePos = [];

	for (let i = 0; i < maxNumberOfHouse; i++) {
		let newPos = offset + houseWidth / 2;
		housePos.push(newPos);
		offset += houseWidth + space;
	}

	return housePos
}


function getPawnPositions(i) {
	/*
	_____________________________
	|		 					|
	|  ||| <-> ...  <->	 |||	|
	|							|
	|							|
	|							|
	|							|
	|							|
	|							|
	|	||| <-> ...  <-> |||	|
	|___________________________|

	*/
	// Get the box parameters
	let box = boxes[i];
	let width, height;
	if (box.isW) {
		if (box.isH) {
			width = boxHeight;
			height = boxHeight;
		} else {
			width = boxHeightHouse;
			height = boxWidth;
		}
	} else if (box.isH) {
		width = boxWidth;
		height = boxHeightHouse;
	}

	// Just take the ratio-ed width and height to spread the pawns
	let widthRatio = coverRatio * width;
	let heightRatio = coverRatio * height;

	// Count the number of lines necessary to spread them equally across the square
	let nbLines = Math.ceil(Math.sqrt(numberOfPawns));
	let nbPawnsPerLine = numberOfPawns / nbLines;
	let nbPawnsLastLine;
	// If the number of pawns is square, same number of pawns on each line
	if (nbPawnsPerLine === Math.ceil(nbPawnsPerLine)) {
		nbPawnsLastLine = nbPawnsPerLine;
	}
	// else, the last line will have less pawns
	else {
		nbPawnsPerLine = Math.ceil(nbPawnsPerLine);
		nbPawnsLastLine = numberOfPawns - (nbLines - 1) * nbPawnsPerLine
	}
	// Where to begin on the X axis
	let initialX = box.x - heightRatio / 2;
	let initialY = box.y - widthRatio / 2;
	// The step between each piece is the remaining width divided by the number of pawns on the line
	let stepX = heightRatio / nbPawnsPerLine;
	let stepY = widthRatio / nbPawnsPerLine;
	let positions = [];
	// All but last line
	for (let j = 0; j < nbLines - 1; j++) {
		for (let k = 0; k < nbPawnsPerLine; k++) {
			positions.push(new THREE.Vector2(initialX + stepX * j, initialY + stepY * k))
		}
	}
	// Last line (potentially less pawns)
	let stepY2 = width / nbPawnsLastLine;
	for (let k = 0; k < nbPawnsLastLine; k++) {
		positions.push(new THREE.Vector2(initialX + stepX * (nbLines - 1), initialY + stepY2 * k));
	}
	return positions;
}

/*
 * Update houses per box
 */

function updateAllHouses() {
	scene.children[4] = updateHouseGroup();
}

function updateHouseGroup() {
	var housesPerBox = new THREE.Group();
	for (let i = 0; i < numberOfBoxes; i++) {
		let houses = updateHouses(i);
		housesPerBox.add(houses);
	}
	return housesPerBox;
}

function updateHouses(i) {
	let houses = new THREE.Group();
	if (boxes[i].isFull) {
		return scene.children[4].children[i];
	} else if (stateArray[i][1] === 5) {
		let hotel = createHotelPos(i);
		houses.add(hotel);
		boxes[i].isFull = true;
	} else {
		for (let j = 0; j < stateArray[i][1]; j++) {
			let house = setUpHouse(i, j);
			houses.add(house);
		}
	}
	return houses
}

function createHotelPos(i) {
	let hotel = createHotel();
	hotel.position.set(housePositions[i].x, housePositions[i].y, cardboardHeight);
	hotel.rotateZ(Math.PI / 2);
	return hotel
}

function createHotel() {
	let clr = 0xff0000;
	return createHouse(clr, houseWidth * hotelHouseRatio, houseHeight * hotelHouseRatio);
}

function setUpHouse(i, j) {
	let box = boxes[i];
	let house = createHouse(houseColor, houseWidth, houseHeight);
	if (box.isH) {
		house.position.set(housePositions[i].x, housePositions[i].y + houseRelativePos[j], cardboardHeight)
	} else if (box.isW) {
		house.position.set(housePositions[i].x + houseRelativePos[j], housePositions[i].y, cardboardHeight)
	}
	return house
}


/*
 * Functions used only to initialize objects
 */

function addPawns(pawns, parentNode) {
	for (let i = 0; i < pawns.length; i++) {
		pawns[i].currentBox = 0;
		parentNode.add(pawns[i]);
	}
}

function createPawns(number, j = 0) {
	let positions = pawnsPositionsPerBox[j];
	let pawns = [];
	for (let i = 0; i < number; i++) {
		let pawn = createPawn(positions[i]);
		pawns[i] = pawn;
	}
	return pawns;
}

function createPawn(position) {
	let clr = getRandomColor();
	let geometry = new THREE.CylinderGeometry(pawnRadius, pawnRadius, pawnHeight, 32);
	let material = new THREE.MeshPhongMaterial({color: clr});
	let pawn = new THREE.Mesh(geometry, material);
	pawn.rotateX(Math.PI / 2);
	pawn.position.set(position.x, position.y, pawnHeight / 2 + cardboardHeight);
	pawn.castShadow = true;
	pawn.receiveShadow = true;
	return pawn;
}

function createHouse(clr, width, height) {
	let roofSize = width / (2 * Math.cos(roofAngle));
	let house = new THREE.Group();
	let wallGeometry = new THREE.PlaneGeometry(width, height);
	let roofGeometry = new THREE.PlaneGeometry(width, roofSize);
	let roofFrontGeometry = new THREE.Geometry();
	roofFrontGeometry.vertices.push(new THREE.Vector3(-width / 2, width / 2, height));
	roofFrontGeometry.vertices.push(new THREE.Vector3(-width / 2, -width / 2, height));
	roofFrontGeometry.vertices.push(new THREE.Vector3(-width / 2, 0, height + width * Math.tan(roofAngle) / 2));
	let normalVectorFront = new THREE.Vector3(-1, 0, 0);
	roofFrontGeometry.faces.push(new THREE.Face3(0, 1, 2, normalVectorFront));
	let roofBackGeometry = new THREE.Geometry();
	roofBackGeometry.vertices.push(new THREE.Vector3(width / 2, width / 2, height));
	roofBackGeometry.vertices.push(new THREE.Vector3(width / 2, -width / 2, height));
	roofBackGeometry.vertices.push(new THREE.Vector3(width / 2, 0, height + width * Math.tan(roofAngle) / 2));
	let normalVectorBack = new THREE.Vector3(-1, 0, 0);
	roofBackGeometry.faces.push(new THREE.Face3(0, 1, 2, normalVectorBack));

	var material = new THREE.MeshPhongMaterial({color: clr, side: 2});
	let frontWall = new THREE.Mesh(wallGeometry, material);
	let backWall = new THREE.Mesh(wallGeometry, material);
	let leftWall = new THREE.Mesh(wallGeometry, material);
	let rightWall = new THREE.Mesh(wallGeometry, material);
	let leftRoof = new THREE.Mesh(roofGeometry, material);
	let rightRoof = new THREE.Mesh(roofGeometry, material);
	let roofFront = new THREE.Mesh(roofFrontGeometry, material);
	let roofBack = new THREE.Mesh(roofBackGeometry, material);

	frontWall.receiveShadow = true;
	backWall.receiveShadow = true;
	leftWall.receiveShadow = true;
	rightWall.receiveShadow = true;
	leftRoof.receiveShadow = true;
	rightRoof.receiveShadow = true;
	roofFront.receiveShadow = true;
	roofBack.receiveShadow = true;

	frontWall.position.set(-width / 2, 0, height / 2);
	backWall.position.set(width / 2, 0, height / 2);
	leftWall.position.set(0, width / 2, height / 2);
	rightWall.position.set(0, -width / 2, height / 2);
	leftRoof.position.set(0, width / 4, height + width / 4 * Math.tan(roofAngle));
	rightRoof.position.set(0, -width / 4, height + width / 4 * Math.tan(roofAngle));
	frontWall.rotateX(Math.PI / 2);
	frontWall.rotateY(Math.PI / 2);
	backWall.rotateX(Math.PI / 2);
	backWall.rotateY(Math.PI / 2);
	leftWall.rotateX(Math.PI / 2);
	rightWall.rotateX(-Math.PI / 2);
	leftRoof.rotateX(-roofAngle);
	rightRoof.rotateX(roofAngle);
	house.add(frontWall);
	house.add(backWall);
	house.add(leftWall);
	house.add(rightWall);
	house.add(leftRoof);
	house.add(rightRoof);
	house.add(roofFront);
	house.add(roofBack);

	return house;
}

function createCardboard(width, parentNode) {
	let cardboardGeometry = new THREE.PlaneGeometry(width, width);
	let texture = new THREE.TextureLoader().load('static/js/graphics/textures/monopoly.jpg');
	let cardboardMaterial = new THREE.MeshPhongMaterial({map: texture});
	let cardboard = new THREE.Mesh(cardboardGeometry, cardboardMaterial);
	cardboard.position.set(cardboardWidth / 2, cardboardWidth / 2, cardboardHeight);
	cardboard.castShadow = true;
	cardboard.receiveShadow = true;
	parentNode.add(cardboard);
	return cardboard;
}

function createGround(parentNode) {
	let groundGeometry = new THREE.PlaneGeometry(2000, 2000);
	let texture = new THREE.TextureLoader().load('static/js/graphics/textures/herbe.jpg');
	texture.wrapS = THREE.RepeatWrapping;
	texture.wrapT = THREE.RepeatWrapping;
	texture.repeat.set(20, 20);
	let groundMaterial = new THREE.MeshPhongMaterial({map: texture});
	let ground = new THREE.Mesh(groundGeometry, groundMaterial);
	parentNode.add(ground);
	return ground;
}

function createCommunityDeck() {
	let deckGeometry = new THREE.BoxGeometry(deckSize/deckRatio, deckSize, deckSize/heightRatio);
	let sideMaterial = new THREE.MeshBasicMaterial(
		{map: new THREE.TextureLoader().load('static/js/graphics/textures/pack.jpg')
		});
	let topMaterial = new THREE.MeshBasicMaterial(
		{map: new THREE.TextureLoader().load('static/js/graphics/textures/Community.jpg')
		});
	let materials =
		[sideMaterial,
			sideMaterial,
			sideMaterial,
			sideMaterial,
			topMaterial,
			new THREE.MeshBasicMaterial()];
	let deck = new THREE.Mesh(deckGeometry, materials);
	deck.position.set(8/11*cardboardWidth, 8/11*cardboardWidth, cardboardHeight+deckSize/(2*heightRatio));
	deck.rotateZ(Math.PI/4);
	return deck;
}

function createChanceDeck() {
	let deckGeometry = new THREE.BoxGeometry(deckSize/deckRatio, deckSize, deckSize/heightRatio);
	let sideMaterial = new THREE.MeshBasicMaterial(
		{map: new THREE.TextureLoader().load('static/js/graphics/textures/pack.jpg')
		});
	let topMaterial = new THREE.MeshBasicMaterial(
		{map: new THREE.TextureLoader().load('static/js/graphics/textures/Chance.jpg')
		});
	let materials =
		[sideMaterial,
			sideMaterial,
			sideMaterial,
			sideMaterial,
			topMaterial,
			new THREE.MeshBasicMaterial()];
	let deck = new THREE.Mesh(deckGeometry, materials);
	deck.position.set(3/11*cardboardWidth, 3/11*cardboardWidth, cardboardHeight+deckSize/(2*heightRatio));
	deck.rotateZ(Math.PI/4);
	return deck;
}

function addALight(parentNode) {
	let light = new THREE.DirectionalLight(0xffffff, 1);
	light.position.set(-1, -1, 10);
	light.castShadow = true;
	light.shadow.mapSize.width = 2048;
	light.shadow.mapSize.height = 2048;
	light.shadow.mapSize.darkness = 0.75;
	light.shadow.camera.near = 1;
	light.shadow.camera.far = 1000;
	light.shadow.darkness = 0.75;

	/* since you have a directional light */
	light.shadow.camera.left = -50;
	light.shadow.camera.right = 50;
	light.shadow.camera.top = 50;
	light.shadow.camera.bottom = -50;
	parentNode.add(light);
}

function initPositions() {
	let positions = {};
	positions[0] = Array.from(Array(numberOfPawns).keys());
	for (let i = 1; i < numberOfBoxes; i++) {
		positions[i] = [];
	}
	return positions;
}

function getRandomColor() {
	let red = Math.floor(Math.random() * 255);
	let blue = Math.floor(Math.random() * 255);
	let green = Math.floor(Math.random() * 255);
	let color_string = "rgb(" + red + ", " + green + ", " + blue + ")";
	return new THREE.Color(color_string);
}


function getHousesPositions(L) {
	let l = L / 12.2;
	let h = l * 1.6;

	let axCoords = {
		0: h - houseWidthBox,
		1: h + l / 2,
		2: h + 3 * l / 2,
		3: h + 5 * l / 2,
		4: h + 7 * l / 2,
		5: h + 9 * l / 2,
		6: h + 11 * l / 2,
		7: h + 13 * l / 2,
		8: h + 15 * l / 2,
		9: h + 17 * l / 2,
		10: L - h + houseWidthBox
	};
	return {
		0: {},
		1: {x: axCoords[0], y: axCoords[1]},
		2: {x: axCoords[0], y: axCoords[2]},
		3: {x: axCoords[0], y: axCoords[3]},
		4: {x: axCoords[0], y: axCoords[4]},
		5: {x: axCoords[0], y: axCoords[5]},
		6: {x: axCoords[0], y: axCoords[6]},
		7: {x: axCoords[0], y: axCoords[7]},
		8: {x: axCoords[0], y: axCoords[8]},
		9: {x: axCoords[0], y: axCoords[9]},
		10: {},
		11: {x: axCoords[1], y: axCoords[10]},
		12: {x: axCoords[2], y: axCoords[10]},
		13: {x: axCoords[3], y: axCoords[10]},
		14: {x: axCoords[4], y: axCoords[10]},
		15: {x: axCoords[5], y: axCoords[10]},
		16: {x: axCoords[6], y: axCoords[10]},
		17: {x: axCoords[7], y: axCoords[10]},
		18: {x: axCoords[8], y: axCoords[10]},
		19: {x: axCoords[9], y: axCoords[10]},
		20: {},
		21: {x: axCoords[10], y: axCoords[9]},
		22: {x: axCoords[10], y: axCoords[8]},
		23: {x: axCoords[10], y: axCoords[7]},
		24: {x: axCoords[10], y: axCoords[6]},
		25: {x: axCoords[10], y: axCoords[5]},
		26: {x: axCoords[10], y: axCoords[4]},
		27: {x: axCoords[10], y: axCoords[3]},
		28: {x: axCoords[10], y: axCoords[2]},
		29: {x: axCoords[10], y: axCoords[1]},
		30: {},
		31: {x: axCoords[9], y: axCoords[0]},
		32: {x: axCoords[8], y: axCoords[0]},
		33: {x: axCoords[7], y: axCoords[0]},
		34: {x: axCoords[6], y: axCoords[0]},
		35: {x: axCoords[5], y: axCoords[0]},
		36: {x: axCoords[4], y: axCoords[0]},
		37: {x: axCoords[3], y: axCoords[0]},
		38: {x: axCoords[2], y: axCoords[0]},
		39: {x: axCoords[1], y: axCoords[0]}
	};
}


function getBoxesPositions(L) {
	let l = L / 12.2;
	let h = l * 1.6;

	let axCoords = {
		0: h / 2 - houseWidthBox,
		1: h + l / 2,
		2: h + 3 * l / 2,
		3: h + 5 * l / 2,
		4: h + 7 * l / 2,
		5: h + 9 * l / 2,
		6: h + 11 * l / 2,
		7: h + 13 * l / 2,
		8: h + 15 * l / 2,
		9: h + 17 * l / 2,
		10: L - h / 2 + houseWidthBox
	};
	return {
		0: {x: h / 2, y: h / 2, isW: true, isH: true},
		1: {x: axCoords[0], y: axCoords[1], isW: false, isH: true, isFull: false},
		2: {x: axCoords[0], y: axCoords[2], isW: false, isH: true, isFull: false},
		3: {x: axCoords[0], y: axCoords[3], isW: false, isH: true, isFull: false},
		4: {x: axCoords[0], y: axCoords[4], isW: false, isH: true, isFull: false},
		5: {x: axCoords[0], y: axCoords[5], isW: false, isH: true, isFull: false},
		6: {x: axCoords[0], y: axCoords[6], isW: false, isH: true, isFull: false},
		7: {x: axCoords[0], y: axCoords[7], isW: false, isH: true, isFull: false},
		8: {x: axCoords[0], y: axCoords[8], isW: false, isH: true, isFull: false},
		9: {x: axCoords[0], y: axCoords[9], isW: false, isH: true, isFull: false},
		10: {x: h / 2, y: L - h / 2, isW: true, isH: true, isFull: false},
		11: {x: axCoords[1], y: axCoords[10], isW: true, isH: false, isFull: false},
		12: {x: axCoords[2], y: axCoords[10], isW: true, isH: false, isFull: false},
		13: {x: axCoords[3], y: axCoords[10], isW: true, isH: false, isFull: false},
		14: {x: axCoords[4], y: axCoords[10], isW: true, isH: false, isFull: false},
		15: {x: axCoords[5], y: axCoords[10], isW: true, isH: false, isFull: false},
		16: {x: axCoords[6], y: axCoords[10], isW: true, isH: false, isFull: false},
		17: {x: axCoords[7], y: axCoords[10], isW: true, isH: false, isFull: false},
		18: {x: axCoords[8], y: axCoords[10], isW: true, isH: false, isFull: false},
		19: {x: axCoords[9], y: axCoords[10], isW: true, isH: false, isFull: false},
		20: {x: L - h / 2, y: L - h / 2, isW: true, isH: true, isFull: false},
		21: {x: axCoords[10], y: axCoords[9], isW: false, isH: true, isFull: false},
		22: {x: axCoords[10], y: axCoords[8], isW: false, isH: true, isFull: false},
		23: {x: axCoords[10], y: axCoords[7], isW: false, isH: true, isFull: false},
		24: {x: axCoords[10], y: axCoords[6], isW: false, isH: true, isFull: false},
		25: {x: axCoords[10], y: axCoords[5], isW: false, isH: true, isFull: false},
		26: {x: axCoords[10], y: axCoords[4], isW: false, isH: true, isFull: false},
		27: {x: axCoords[10], y: axCoords[3], isW: false, isH: true, isFull: false},
		28: {x: axCoords[10], y: axCoords[2], isW: false, isH: true, isFull: false},
		29: {x: axCoords[10], y: axCoords[1], isW: false, isH: true, isFull: false},
		30: {x: L - h / 2, y: h / 2, isW: true, isH: true, isFull: false},
		31: {x: axCoords[9], y: axCoords[0], isW: true, isH: false, isFull: false},
		32: {x: axCoords[8], y: axCoords[0], isW: true, isH: false, isFull: false},
		33: {x: axCoords[7], y: axCoords[0], isW: true, isH: false, isFull: false},
		34: {x: axCoords[6], y: axCoords[0], isW: true, isH: false, isFull: false},
		35: {x: axCoords[5], y: axCoords[0], isW: true, isH: false, isFull: false},
		36: {x: axCoords[4], y: axCoords[0], isW: true, isH: false, isFull: false},
		37: {x: axCoords[3], y: axCoords[0], isW: true, isH: false, isFull: false},
		38: {x: axCoords[2], y: axCoords[0], isW: true, isH: false, isFull: false},
		39: {x: axCoords[1], y: axCoords[0], isW: true, isH: false, isFull: false}
	};
}

function getPawnsPositionsBoxes() {
	let pawnsPositionsPerBox = {};
	for (let i = 0; i < numberOfBoxes; i++) {
		pawnsPositionsPerBox[i] = getPawnPositions(i);
	}
	return pawnsPositionsPerBox;
}

function initState(){
	let players = [];
	for (let i = 0; i<numberOfPawns; i++){
		players.push(i);
	}
	let res = {0:[players,0]};
	for (let i = 1; i<numberOfBoxes; i++){
		res[i]=[[], 0];
	}
	return res;
}

console.log("DBG: helperFns.js loaded");