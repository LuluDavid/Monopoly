// INIT FUNCTION

function init() {
	/* 
	 * Global parameters 
	 */

	// Cardboard
	cardboardWidth = 110
	// Number of boxes
	numberOfBoxes = 40
	// Pawns
	numberOfPawns = 6
	pawnHeight = 2
	pawnRadius = 0.5
	// Box
	coverRatio = 0.7
	boxWidth = cardboardWidth/12.2
	boxHeight = 1.6*boxWidth
	// Box positions
	boxes = getBoxesPositions(cardboardWidth)
	// Accuracy for pawn motion
	epsilon = 1
	coverMotion = 0.8
	// Whose turns it is
	currentPawn = 0
	// Pawn motion
	tMotion = 3 // duration to go to next case (seconds)
	// Pawn positions on boxes
	boxes = getBoxesPositions(cardboardWidth);
	// Pawn positions per box (where to put them to make them fit in)
	pawnsPositionsPerBox = getPawnsPositionsBoxes(cardboardWidth);
	// Incrementing boolean to avoid multi-calls
	incrementing = false;
	// CloseView activation boolean
	closeViewDisplay = false
	closeViewRatio = 0.4
	closeViewHeight = 50
	closeViewFurtherRatio = 2


	/*
	 * Build scene
	 */
	// General camera
	container = document.getElementById( 'container' );
	view.camera = new THREE.PerspectiveCamera( view.fov, window.innerWidth / window.innerHeight, view.near, view.far );
	view.camera.position.fromArray( view.eye );
	view.camera.up.fromArray( view.up );
	// Close camera
	closeView.camera = new THREE.PerspectiveCamera( closeView.fov, window.innerWidth / window.innerHeight, closeView.near, closeView.far );
	closeView.camera.position.fromArray( closeView.eye );
	closeView.camera.up.fromArray( closeView.up );
	// Scene
	scene = new THREE.Scene();
	const loader = new THREE.TextureLoader();
	loader.load('textures/clearSky.jpg' , function(texture)
            { scene.background = texture;  });
	scene.background = new THREE.Color( 0x0000ff );
	// Orbit controls
	controls = new THREE.OrbitControls( view.camera );

	/*
	 * Renderer Settings
	 */
	renderer = new THREE.WebGLRenderer( { antialias: true} );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	renderer.shadowMap.enabled = true;
	renderer.shadowMapSoft = true;
	renderer.shadowMapDebug = true;
	renderer.domElement.style += "; position:relative; z-index:0; "
	container.appendChild( renderer.domElement );

	/*
	 * Instantiate and add the objects
	 */
	// Add a light
	addALight(scene);
	// Add a ground
	ground = createGround(scene);
	// Add the cardboard
	cardboard = createCardboard(cardboardWidth, scene);
	cardboard.rotateZ(Math.PI/2);
	cardboard.castShadow = true;
	cardboard.receiveShadow = true;
	// Create and add the pawns
	let pawns = createPawns(numberOfPawns);
	addPawns(pawns, scene);
	// Set the positions of the pawns on the cardboard in positions (fast access to positions)
	positions = initPositions();
	new_positions = initPositions();

	/*
	 * First test to move successfully pawns around the board
	 */
	$(document).on('click',() => incrementPositionsAux());

	/*
	 * Basic update functions : update OrbiteControls, update the camera
	 */
	controls.update();
	animate();

}





/*
 * Loop functions
 */

function animate(){

	render();
	requestAnimationFrame( animate );
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

function updateView(vleft = 0, vtop = 0, vwidth = 1, vheight = 1){
	// First view
	view.updateCamera(view.camera,scene);

	var left = Math.floor( windowWidth * vleft );
	var top = Math.floor( windowHeight * vtop );
	var width = Math.floor( windowWidth * vwidth );
	var height = Math.floor( windowHeight * vheight );

	renderer.setViewport( left, top, width, height );
	renderer.setScissor( left, top, width, height );
	renderer.setScissorTest( true );
	renderer.setClearColor( view.background );

	view.camera.aspect = width / height;
	view.camera.updateProjectionMatrix();
	
	renderer.render( scene, view.camera );
}

function updateCloseView(vleft = 1-closeViewRatio, vtop = 1-closeViewRatio, vwidth = closeViewRatio, vheight = closeViewRatio){
	// Second view
	closeView.updateCamera(closeView.camera,scene);

	var leftcloseView = Math.floor( windowWidth * vleft );
	var topcloseView = Math.floor( windowHeight * vtop );
	var widthcloseView = Math.floor( windowWidth * vwidth );
	var heightcloseView = Math.floor( windowHeight * vheight );

	renderer.setViewport( leftcloseView, topcloseView, widthcloseView, heightcloseView );
	renderer.setScissor( leftcloseView, topcloseView, widthcloseView, heightcloseView );
	renderer.setScissorTest( true );
	renderer.setClearColor( closeView.background );

	closeView.camera.aspect = widthcloseView / heightcloseView;
	closeView.camera.updateProjectionMatrix();
	
	renderer.render(scene,closeView.camera);
}

// Adapt to the screen size
function updateSize() {

	if ( windowWidth != window.innerWidth ) {

		windowWidth = window.innerWidth;
		windowHeight = window.innerHeight;

		renderer.setSize( windowWidth, windowHeight );
	}
}






/*
 * Loop Utils
 */

// Empty constructor for the positions dictionary
function emptyPositions(){
	var positions = {}
	for (let i = 0; i<numberOfBoxes; i++){
		positions[i] = []
	}
	return positions
}

// Use the currentBox param stored in every pawn to fill the positions dictionary
function updateNewPositions(){
	new_positions = emptyPositions();
	for (let i = 0; i<numberOfPawns; i++){
		let box = scene.children[3+i].currentBox;
		new_positions[box].push(i);
	}
}

function updatePositions(){ 
	positions = $.extend( true, {}, new_positions );
}

// Random int in [min,max]
function getRandomInt(min, max) {
  return Math.floor(Math.random() * Math.floor(max-min+1))+min;
}

// Random int in [1,12]
function randomDices(){
	return getRandomInt(1,12); 
}

// Aux function to ensure we do not multithread on incrementPositions
function incrementPositionsAux(){
	if (incrementing == false){
		incrementing = true;
		incrementPositions();
	}
	else {
		console.log("Previous increment is not over.")
	}
}

// Main function to update next pawn's position (throw of dice, move the pawn)
function incrementPositions(){
	// Pass to next pawn for next call (modulo numberOfPawns)
	var dices = randomDices();
	console.log("Vous obtenez un score de "+dices)
	// Copies
	var pawn = Object.assign(scene.children[3+currentPawn])
	var currentBox = Object.assign(pawn.currentBox)
	// Update the box where the pawn is (modulo numberOfBoxes) 
	currentBox += dices;
	if (currentBox >= numberOfBoxes){
		currentBox -= numberOfBoxes;
	}
	// Translate the pawn to this box
	translatePawnToBox(currentPawn, currentBox);
}

// Distance between two points
function distance(v1, v2){
	return v1.clone().distanceTo(v2.clone());
}

// Translate pawn n°i to box n°j
function translatePawnToBox(i, j){
	let boxCardinal = Math.max(positions[j].length, new_positions[j].length)
	let pawnPosition = pawnsPositionsPerBox[j][boxCardinal]
	let deltaT = tMotion*Math.pow(j/numberOfBoxes, 1/3)
	scene.children[3+i].currentBox = j;
	updateNewPositions();
	addCanvas();
	translate(i, new THREE.Vector3(pawnPosition.x, pawnPosition.y, pawnHeight/2 + 0.05), deltaT)
}

function addCanvas(){
	let height = windowHeight*closeViewRatio;
	let width = windowWidth*closeViewRatio;
	let canvas = "<canvas id = 'closeView' width='"+ width +"' height='"+ height +"' style=\"border:3px solid #000000; position:fixed; top: 0px; right: 0px; z-index:2;\"></canvas>"
	$("#container").append(canvas);
}

function removeCanvas(){
	$("#closeView").remove();
}

// Parabole to describe the motion inertia
function ease(t) { return -t*t+2*t}

function soonerFaster(t) { return Math.pow(t,1/5); }

// Translate pawn n°i to goalPosition
function translate(i, goalPosition, deltaT){
	closeViewDisplay = true;
	render();
	var fps = 60;           // seconds
	var step = 1 / (deltaT * fps);  // t-step per frame
	var t = 0;
	object = scene.children[3+i];
	var initialPosition = object.position.clone()
	var initialCameraPosition = closeView.camera.position.clone()
	var goalPositionCamera = new THREE.Vector3(goalPosition.x, goalPosition.y, goalPosition.z + closeViewHeight)
	loop(initialPosition, initialCameraPosition, goalPosition, goalPositionCamera, step, t)
}

// Translation from a to b's parametric equation
function translation(a, b, t) { return a+(b - a)*t }

// Loop function
function loop(initialPosition, initialPositionCam, goalPosition, goalPositionCam, step, t) {
	// Update the pawn's position
  	var X = translation(initialPosition.x, goalPosition.x, ease(t));   // interpolate between a and b where
    var Y = translation(initialPosition.y, goalPosition.y, ease(t));   // t is first passed through a easing
  	var Z = translation(initialPosition.z, goalPosition.z, ease(t));   // function in this example.
  	object.position.set(X, Y, Z);  // set new position
  	// Update the camera's positions
  	var XCam = translation(initialPositionCam.x, goalPositionCam.x, soonerFaster(t*closeViewFurtherRatio));
  	var YCam = translation(initialPositionCam.y, goalPositionCam.y, soonerFaster(t*closeViewFurtherRatio));
  	var ZCam = translation(initialPositionCam.z, goalPositionCam.z, soonerFaster(t*closeViewFurtherRatio));
  	closeView.camera.position.set(XCam, YCam, ZCam);
  	// Increment the time and loop back
  	t = t + step;
  	if (t >= 1) { return loop2(step, t); } 
  	requestAnimationFrame(() => loop(initialPosition, initialPositionCam, goalPosition, goalPositionCam, step, t))
}

function loop2(step, t) {
	t = t + step;
	if (t >=1/coverRatio){
		console.log("Tour fini"); 
		incrementing = false; 
		closeViewDisplay = false;
		currentPawn++;
		closeView.camera.position.set(closeView.eye[0], closeView.eye[1], closeView.eye[2]);
		removeCanvas();
		updatePositions(); 
		if (currentPawn == numberOfPawns) {
			currentPawn = 0;
		}
		return;
	}
	requestAnimationFrame(() => loop2(step, t))
}



/*
 * Get positions adapted to share a box for number pawns on box n°i
 */



// TODO: externalize the common part (the first lines) for the three different cases (corner, width, height)
function getPawnPositions(i){
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
	let box = boxes[i]
	let width = boxWidth;
	let height = boxWidth;
	if (box.isW) width = boxHeight;
	if (box.isH) height = boxHeight;

	// Just take the ratio-ed width and height to spread the pawns
	widthRatio = coverRatio*width
	heightRatio = coverRatio*height

	// Count the number of lines necessary to spread them equally across the square
	let nbLines = Math.ceil(Math.sqrt(numberOfPawns));
	let nbPawnsPerLine = numberOfPawns/nbLines;
	let nbPawnsLastLine;
	// If the number of pawns is square, same number of pawns on each line
	if (nbPawnsPerLine == Math.ceil(nbPawnsPerLine)){
		nbPawnsLastLine = nbPawnsPerLine;
	}
	// else, the last line will have less pawns
	else {
		nbPawnsPerLine = Math.ceil(nbPawnsPerLine)
		nbPawnsLastLine = numberOfPawns - (nbLines-1)*nbPawnsPerLine
	}
	// Where to begin on the X axis
	let initialX = box.x-heightRatio/2
	let initialY = box.y-widthRatio/2
	// The step between each piece is the remaining width divided by the number of pawns on the line
	let stepX = heightRatio/nbPawnsPerLine
	let stepY = widthRatio/nbPawnsPerLine
	var positions = []
	// All but last line
	for (let j=0; j<nbLines-1; j++){
		for (let k=0; k<nbPawnsPerLine; k++){
			positions.push(new THREE.Vector2(initialX + stepX*j,initialY + stepY*k))
		}
	}
	// Last line (potentially less pawns)
	let stepY2 = width/nbPawnsLastLine
	for (let k=0; k<nbPawnsLastLine; k++){
		positions.push(new THREE.Vector2(initialX + stepX*(nbLines-1),initialY + stepY2*k))
	}
	return positions
}




/* 
 * Functions used only to initialize objects
 */

function addPawns(pawns, parentNode){
	for (let i = 0; i<pawns.length; i++){
		pawns[i].currentBox = 0;
		parentNode.add(pawns[i]);
	}
}

function createPawns(number, i = 0){
	var positions = pawnsPositionsPerBox[i];
	let pawns = [];
	for (var i = 0; i<number; i++){
		var pawn = createPawn(positions[i]);
		pawn.castShadow = true;
		pawn.receiveShadow = true;
		pawns[i] = pawn;
	}
	return pawns;
}

function createPawn(position){
	let clr = getRandomColor();
	let geometry = new THREE.CylinderGeometry( pawnRadius, pawnRadius, pawnHeight, 32);
	let material = new THREE.MeshPhongMaterial({color: clr});
	let pawn = new THREE.Mesh( geometry, material );
	pawn.rotateX(Math.PI/2);
	pawn.position.set(position.x, position.y, pawnHeight/2 + 0.05);
	return pawn;
}

function createCardboard(width, parentNode){
	let cardboardGeometry = new THREE.PlaneGeometry(width,width);
	let texture = new THREE.TextureLoader().load('textures/monopoly.jpg');
	let cardboardMaterial = new THREE.MeshPhongMaterial({map:texture});
	let cardboard = new THREE.Mesh(cardboardGeometry,cardboardMaterial);
	cardboard.position.set(cardboardWidth/2,cardboardWidth/2,0.03);
	parentNode.add(cardboard);
	return cardboard;
}

function createGround(parentNode){
	let groundGeometry = new THREE.PlaneGeometry(2000,2000)
	let texture = new THREE.TextureLoader().load( 
		'textures/herbe.jpg' );
	texture.wrapS = THREE.RepeatWrapping;
	texture.wrapT = THREE.RepeatWrapping;
	texture.repeat.set( 20, 20 );
	let groundMaterial = new THREE.MeshPhongMaterial({map:texture});
	let ground = new THREE.Mesh(groundGeometry,groundMaterial);
	parentNode.add(ground);
	return ground;
}

function addALight(parentNode){
	let light = new THREE.DirectionalLight(0xffffff,1);
	light.position.set(0,10,10)
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

function initPositions(){
	var positions = {}
	positions[0] = Array.from(Array(numberOfPawns).keys())
	for (let i = 1; i<numberOfBoxes; i++){
		positions[i] = []
	}
	return positions
}

function getRandomColor() {
	let red = Math.floor(Math.random()*255);
	let blue = Math.floor(Math.random()*255);
	let green = Math.floor(Math.random()*255);
	let color_string = "rgb("+red+", "+green+", "+blue+")"
	let res = new THREE.Color(color_string);
	return res;
	}


function getBoxesPositions(L) {
    var l = L / 12.2
    var h = l * 1.6

    var axCoords = {
      0: h/2,
      1: h+l/2,
      2: h+3*l/2,
      3: h+5*l/2,
      4: h+7*l/2,
      5: h+9*l/2,
      6: h+11*l/2,
      7: h+13*l/2,
      8: h+15*l/2,
      9: h+17*l/2,
      10: L-h/2
    }

    positions = {
        0: {x: axCoords[0], y: axCoords[0], isW:true, isH:true},
        1: {x: axCoords[0], y: axCoords[1], isW:false, isH:true},
        2: {x: axCoords[0], y: axCoords[2], isW:false, isH:true},
        3: {x: axCoords[0], y: axCoords[3], isW:false, isH:true},
        4: {x: axCoords[0], y: axCoords[4], isW:false, isH:true},
        5: {x: axCoords[0], y: axCoords[5], isW:false, isH:true},
        6: {x: axCoords[0], y: axCoords[6], isW:false, isH:true},
        7: {x: axCoords[0], y: axCoords[7], isW:false, isH:true},
        8: {x: axCoords[0], y: axCoords[8], isW:false, isH:true},
        9: {x: axCoords[0], y: axCoords[9], isW:false, isH:true},
        10: {x: axCoords[0], y: axCoords[10], isW:true, isH:true},
        11: {x: axCoords[1], y: axCoords[10], isW:true, isH:false},
        12: {x: axCoords[2], y: axCoords[10], isW:true, isH:false},
        13: {x: axCoords[3], y: axCoords[10], isW:true, isH:false},
        14: {x: axCoords[4], y: axCoords[10], isW:true, isH:false},
        15: {x: axCoords[5], y: axCoords[10], isW:true, isH:false},
        16: {x: axCoords[6], y: axCoords[10], isW:true, isH:false},
        17: {x: axCoords[7], y: axCoords[10], isW:true, isH:false},
        18: {x: axCoords[8], y: axCoords[10], isW:true, isH:false},
        19: {x: axCoords[9], y: axCoords[10], isW:true, isH:false},
        20: {x: axCoords[10], y: axCoords[10], isW:true, isH:true},
        21: {x: axCoords[10], y: axCoords[9], isW:false, isH:true},
        22: {x: axCoords[10], y: axCoords[8], isW:false, isH:true},
        23: {x: axCoords[10], y: axCoords[7], isW:false, isH:true},
        24: {x: axCoords[10], y: axCoords[6], isW:false, isH:true},
        25: {x: axCoords[10], y: axCoords[5], isW:false, isH:true},
        26: {x: axCoords[10], y: axCoords[4], isW:false, isH:true},
        27: {x: axCoords[10], y: axCoords[3], isW:false, isH:true},
        28: {x: axCoords[10], y: axCoords[2], isW:false, isH:true},
        29: {x: axCoords[10], y: axCoords[1], isW:false, isH:true},
        30: {x: axCoords[10], y: axCoords[0], isW:true, isH:true},
        31: {x: axCoords[9], y: axCoords[0], isW:true, isH:false},
        32: {x: axCoords[8], y: axCoords[0], isW:true, isH:false},
        33: {x: axCoords[7], y: axCoords[0], isW:true, isH:false},
        34: {x: axCoords[6], y: axCoords[0], isW:true, isH:false},
        35: {x: axCoords[5], y: axCoords[0], isW:true, isH:false},
        36: {x: axCoords[4], y: axCoords[0], isW:true, isH:false},
        37: {x: axCoords[3], y: axCoords[0], isW:true, isH:false},
        38: {x: axCoords[2], y: axCoords[0], isW:true, isH:false},
        39: {x: axCoords[1], y: axCoords[0], isW:true, isH:false}
    };
  return positions;
}

function getPawnsPositionsBoxes(L) {
	var pawnsPositionsPerBox = {}
	for (let i = 0; i<numberOfBoxes; i++){
		pawnsPositionsPerBox[i] = getPawnPositions(i);
	}
	return pawnsPositionsPerBox;
}











console.log("DBG: helperFns.js loaded");
