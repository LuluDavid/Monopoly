// INIT FUNCTION

function init() {
	// parameters
	cardboardWidth = 110
	pawnHeight = 2
	pawnRadius = 0.5
	coverRatio = 0.7
	epsilon = 1
	currentPawn = 0

	caseWidth = cardboardWidth/12.2
	caseHeight = 1.6*caseWidth
	numberOfPawns = 18
	caseCenter = new THREE.Vector2(caseHeight/2,caseHeight/2)

	boxes = getBoxesPositions(cardboardWidth)

	// Build scene
	container = document.getElementById( 'container' );

	view.camera = new THREE.PerspectiveCamera( view.fov, window.innerWidth / window.innerHeight, view.near, view.far );
	view.camera.position.fromArray( view.eye );
	view.camera.up.fromArray( view.up );

	scene = new THREE.Scene();
	controls = new THREE.OrbitControls( view.camera );

	// renderer settings
	renderer = new THREE.WebGLRenderer( { antialias: true} );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	renderer.shadowMap.enabled = true;
	renderer.shadowMapSoft = true;
	renderer.shadowMapDebug = true;

	container.appendChild( renderer.domElement );

	// add a light
	addALight(scene);

	// create ground
	ground = createGround(scene);
	// create cardboard
	cardboard = createCardboard(cardboardWidth, scene);
	cardboard.rotateZ(Math.PI/2);
	cardboard.castShadow = true;
	cardboard.receiveShadow = true;
	// create one pawn
	let pawns = createPawns(numberOfPawns, caseCenter, caseHeight, caseHeight);
	addPawns(pawns, scene);
	positions = initPositions();

	$(document).on('click',() => incrementPositions());

	controls.update();
	animate();

}

// ANIMATE AND UPDATE FUNCTIONS

function initPositions(){
	var positions = {}
	positions[0] = Array.from(Array(numberOfPawns).keys())
	for (let i = 1; i<numberOfPawns; i++){
		positions[i] = []
	}
	return positions
}

function emptyPositions(){
	var positions = {}
	for (let i = 0; i<40; i++){
		positions[i] = []
	}
	return positions
}

function updatePositions(){
	positions = emptyPositions();
	for (let i = 0; i<numberOfPawns; i++){
		let box = Object.assign(scene.children[3+i].currentCase);
		positions[box].push(i);
	}
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * Math.floor(max-min+1))+min;
}

function randomDices(){
	return getRandomInt(1,12); 
}

function incrementPositions(){

	var dices = randomDices();

	console.log("Vous obtenez un score de "+dices)

	var pawn = Object.assign(scene.children[3+currentPawn])
	var currentCase = Object.assign(pawn.currentCase)

	currentCase += dices;
	if (currentCase >= 40){
		currentCase -= 40;
	}

	translateCase(currentPawn, currentCase);

	currentPawn++;
	if (currentPawn == numberOfPawns){
		currentPawn = 0;
	}
}

function animate(){

	render();
	requestAnimationFrame( animate );
}

function distance(v1, v2){
	return v1.clone().distanceTo(v2.clone());
}

function translateCase(i, j){
	let box = boxes[j]
	dt = 1 // duration to go to next case
	translate(i, new THREE.Vector3(box.x, box.y, pawnHeight/2 + 0.05), dt)
	scene.children[3+i].currentCase = j;
	updatePositions();
}

function translate(i, goalPosition, duration){
	var fps = 60;           // seconds
	var step = 1 / (duration * fps);  // t-step per frame
	var t = 0;
	object = scene.children[3+i];
	console.log(object.position)

	function translation(a, b, t) {return a + (b - a) * t}

	function loop() {
	  var newX = translation(object.position.x, goalPosition.x, ease(t));   // interpolate between a and b where
	  var newY = translation(object.position.y, goalPosition.y, ease(t));   // t is first passed through a easing
	  var newZ = translation(object.position.z, goalPosition.z, ease(t));   // function in this example.
	  object.position.set(newX, newY, newZ);  // set new position
	  t += step;
	  if (t <= 0 || t >=1) { console.log("Tour fini"); return; }
	  requestAnimationFrame(loop)
	}

	function ease(t) { return 4*(t-t*t)} // add inertia

	loop();
	renderer.render(scene, view.camera);
}

function render() {

	updateSize();

	// First view
	view.updateCamera(view.camera,scene);

	var left = Math.floor( windowWidth * view.left );
	var top = Math.floor( windowHeight * view.top );
	var width = Math.floor( windowWidth * view.width );
	var height = Math.floor( windowHeight * view.height );

	renderer.setViewport( left, top, width, height );
	renderer.setScissor( left, top, width, height );
	renderer.setScissorTest( true );
	renderer.setClearColor( view.background );

	view.camera.aspect = width / height;
	view.camera.updateProjectionMatrix();
	
	renderer.render( scene, view.camera );
}

function updateSize() {

	if ( windowWidth != window.innerWidth ) {

		windowWidth = window.innerWidth;
		windowHeight = window.innerHeight;

		renderer.setSize( windowWidth, windowHeight );
	}
}


// FUNCTIONS TO BUILD OBJECTS

function addPawns(pawns, parentNode){
	for (let i = 0; i<pawns.length; i++){
		pawns[i].currentCase = 0;
		parentNode.add(pawns[i]);
	}
}

function createPawns(number, caseCenter, width, height){
	var positions = getPawnPositions(number, caseCenter, width, height);
	let pawns = []
	for (var i = 0; i<number; i++){
		var pawn = createPawn(positions[i]);
		pawn.castShadow = true;
		pawn.receiveShadow = true;
		pawns[i] = pawn;
	}
	return pawns;
}

function getPawnPositions(number, caseCenter, width, height){
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
	widthRatio = coverRatio*width
	heightRatio = coverRatio*height
	let nbLines = Math.ceil(Math.sqrt(number));
	let nbPawnsPerLine = number/nbLines;
	let nbPawnsLastLine;
	if (nbPawnsPerLine == Math.ceil(nbPawnsPerLine)){
		nbPawnsLastLine = nbPawnsPerLine;
	}
	else {
		nbPawnsPerLine = Math.ceil(nbPawnsPerLine)
		nbPawnsLastLine = number - (nbLines-1)*nbPawnsPerLine
	}
	let initialX = caseCenter.x-heightRatio/2
	let initialY = caseCenter.y-widthRatio/2

	let stepX = widthRatio/nbPawnsPerLine
	let stepY = heightRatio/nbPawnsPerLine
	var positions = []
	for (let j=0; j<nbLines-1; j++){
		for (let k=0; k<nbPawnsPerLine; k++){
			positions.push(new THREE.Vector2(initialX + stepX*j,initialY + stepY*k))
		}
	}

	let stepY2 = height/nbPawnsLastLine
	for (let k=0; k<nbPawnsLastLine; k++){
		positions.push(new THREE.Vector2(initialX + stepX*(nbLines-1),initialY + stepY2*k))
	}
	return positions
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
	let groundGeometry = new THREE.PlaneGeometry(1000,1000)
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












console.log("DBG: helperFns.js loaded");
