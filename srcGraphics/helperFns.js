// INIT FUNCTION

function init() {
	// parameters
	cardboardWidth = 110
	pawnHeight = 2
	pawnRadius = 0.5
	coverRatio = 0.7

	caseWidth = (cardboardWidth/12.25)
	caseHeight = 1.625*caseWidth
	numberOfPawns = 18
	caseCenter = new THREE.Vector2(caseHeight/2,caseHeight/2)

	boxes = getBoxesPositions(cardboardWidth)

	// Build scene
	container = document.getElementById( 'container' );

	view.camera = new THREE.PerspectiveCamera( view.fov, window.innerWidth / window.innerHeight, view.near, view.far );
	view.camera.position.fromArray( view.eye );
	view.camera.up.fromArray( view.up );

	scene = new THREE.Scene();
	var controls = new THREE.OrbitControls( view.camera );

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
	cardboard.rotateZ(-Math.PI/2);
	cardboard.castShadow = true;
	cardboard.receiveShadow = true;
	// create one pawn
	let pawns = createPawns(numberOfPawns, caseCenter, caseHeight, caseHeight);
	addPawns(pawns, scene);

	$(document).on('click',() => incrementPositions());

	controls.update();
	animate();

}

// ANIMATE AND UPDATE FUNCTIONS

function incrementPositions(){
	currentCase++;
	if (currentCase == 40){
		currentCase = 0;
	}
	let box = boxes[currentCase]
	let center = new THREE.Vector2(box.x, box.y);
	let height = box.isW?caseWidth:caseHeight;
	let width = box.isH?caseHeight:caseWidth;

	newPawns  = createPawns(numberOfPawns, center, width, height);
	for (let i = 3; i<scene.children.length; i++){
		scene.children[i] = newPawns[i-3];
	}
}

function animate(){

	render();
	requestAnimationFrame( animate );
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
		parentNode.add(pawns[i]);
	}
}

function createPawns(number, caseCenter, width, height){
	var positions = getPawnPositions(number, caseCenter, width*coverRatio, height*coverRatio);
	let pawns = []
	for (var i = 0; i<number; i++){
		let clr = getRandomColor();
		var pawn = createPawn(clr, positions[i]);
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
	let initialX = caseCenter.x-height/2
	let initialY = caseCenter.y-width/2

	let stepX = width/nbPawnsPerLine
	let stepY = height/nbPawnsPerLine
	var positions = []
	for (let j=0; j<nbLines-1; j++){
		for (let k=0; k<nbPawnsPerLine; k++){
			positions.push(new THREE.Vector2(initialX + stepX*j,initialY + stepY*k))
		}
	}

	let stepY2 = width/nbPawnsLastLine
	for (let k=0; k<nbPawnsLastLine; k++){
		positions.push(new THREE.Vector2(initialX + stepX*(nbLines-1),initialY + stepY2*k))
	}
	return positions
}

function createPawn(clr, position){
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
    var l = L / 12.25
    var h = l * 1.625

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
