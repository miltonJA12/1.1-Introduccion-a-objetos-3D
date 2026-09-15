import * as THREE from 'three';


// =====================================================
// ESCENA
// =====================================================

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x080a0d);


// =====================================================
// CÁMARA
// =====================================================

const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

camera.position.set(8, 4, 8);


// =====================================================
// RENDERER
// =====================================================

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: "high-performance"
});

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
);

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);


// =====================================================
// SOMBRAS
// =====================================================

renderer.shadowMap.enabled = true;

renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;


// =====================================================
// COLOR
// =====================================================

renderer.outputColorSpace =
    THREE.SRGBColorSpace;


// =====================================================
// TONEMAPPING
// =====================================================

renderer.toneMapping =
    THREE.ACESFilmicToneMapping;

renderer.toneMappingExposure = 1.25;


// =====================================================
// ILUMINACIÓN FÍSICA
// =====================================================

renderer.useLegacyLights = false;


document.body.appendChild(
    renderer.domElement
);


// =====================================================
// PISO
// =====================================================

const floorGeometry =
    new THREE.PlaneGeometry(
        30,
        30
    );


const floorMaterial =
    new THREE.MeshStandardMaterial({

        color: 0x3a3d40,

        roughness: 0.78,

        metalness: 0.05

    });


const floor =
    new THREE.Mesh(
        floorGeometry,
        floorMaterial
    );


floor.rotation.x =
    -Math.PI / 2;

floor.position.y =
    -1.2;


// EL PISO RECIBE SOMBRAS

floor.receiveShadow = true;


scene.add(floor);


// =====================================================
// CUBO DE CRISTAL
// =====================================================

const cubeGeometry =
    new THREE.BoxGeometry(
        2,
        1.2,
        2.5
    );


const cubeMaterial =
    new THREE.MeshPhysicalMaterial({

        // Cristal ligeramente azul
        color: 0xb8f7ff,

        // Transmisión alta
        transmission: 0.98,

        // Transparencia
        transparent: true,

        opacity: 0.96,

        // Grosor
        thickness: 1.5,

        // Índice del vidrio
        ior: 1.52,

        // Superficie pulida
        roughness: 0.025,

        // No metálico
        metalness: 0,

        // Reflejos
        specularIntensity: 1,

        specularColor:
            new THREE.Color(0xffffff),

        // Tinte interno
        attenuationColor:
            new THREE.Color(0xb8f7ff),

        attenuationDistance: 8

    });


const cube =
    new THREE.Mesh(
        cubeGeometry,
        cubeMaterial
    );


cube.position.set(
    -1.5,
    -0.6,
    0
);


// =====================================================
// SOMBRAS DEL CUBO
// =====================================================

cube.castShadow = true;

cube.receiveShadow = true;


scene.add(cube);


// =====================================================
// ESFERA DE CRISTAL TRANSPARENTE
// =====================================================

const sphereGeometry =
    new THREE.SphereGeometry(
        1,
        96,
        96
    );


const sphereMaterial =
    new THREE.MeshPhysicalMaterial({

        // =============================================
        // CRISTAL TOTALMENTE TRANSPARENTE
        // =============================================

        color: 0xffffff,

        // Máxima transmisión
        transmission: 1.0,

        // Transparencia
        transparent: true,

        opacity: 0.95,

        // Grosor del cristal
        thickness: 1.5,

        // Índice de refracción realista
        // del vidrio
        ior: 1.52,

        // Cristal muy pulido
        roughness: 0.015,

        // No metálico
        metalness: 0,

        // Reflejos
        specularIntensity: 1,

        specularColor:
            new THREE.Color(0xffffff),

        // Cristal sin color
        attenuationColor:
            new THREE.Color(0xffffff),

        attenuationDistance: 10

    });


const sphere =
    new THREE.Mesh(
        sphereGeometry,
        sphereMaterial
    );


sphere.position.set(
    1.5,
    0,
    0
);


// =====================================================
// SOMBRAS DE LA ESFERA
// =====================================================

sphere.castShadow = true;

sphere.receiveShadow = true;


scene.add(sphere);


// =====================================================
// LUZ AMBIENTE
// =====================================================

const ambientLight =
    new THREE.AmbientLight(
        0xffffff,
        0.06
    );


scene.add(
    ambientLight
);


// =====================================================
// LUZ DE RELLENO
// =====================================================

const fillLight =
    new THREE.HemisphereLight(

        // Luz superior
        0xbfdfff,

        // Luz inferior
        0x080808,

        // Intensidad
        0.22

    );


scene.add(
    fillLight
);


// =====================================================
// FOCO / LÁMPARA PRINCIPAL
// =====================================================
//
// Este foco se mueve junto con la cámara.
//

const flashlight =
    new THREE.SpotLight(

        // Color
        0xffffff,

        // =============================================
        // INTENSIDAD
        // =============================================

        1000,

        // =============================================
        // DISTANCIA
        // =============================================

        60,

        // =============================================
        // ÁNGULO
        // =============================================

        Math.PI / 5,

        // =============================================
        // DIFUMINADO
        // =============================================

        0.40,

        // =============================================
        // DECAIMIENTO
        // =============================================

        2

    );


// =====================================================
// SOMBRAS DEL FOCO
// =====================================================

flashlight.castShadow = true;


// =====================================================
// RESOLUCIÓN DE SOMBRAS
// =====================================================

flashlight.shadow.mapSize.width =
    4096;

flashlight.shadow.mapSize.height =
    4096;


// =====================================================
// CÁMARA DE SOMBRAS
// =====================================================

flashlight.shadow.camera.near =
    0.1;

flashlight.shadow.camera.far =
    70;


// =====================================================
// CALIDAD DE SOMBRAS
// =====================================================

flashlight.shadow.bias =
    -0.0001;

flashlight.shadow.normalBias =
    0.025;


// =====================================================
// SUAVIDAD DE SOMBRAS
// =====================================================

flashlight.shadow.radius =
    4;


scene.add(
    flashlight
);


// =====================================================
// TARGET DEL FOCO
// =====================================================

const flashlightTarget =
    new THREE.Object3D();


scene.add(
    flashlightTarget
);


flashlight.target =
    flashlightTarget;


// =====================================================
// LUZ DE REBOTE
// =====================================================

const bounceLight =
    new THREE.PointLight(

        // Color
        0x9fdcff,

        // Intensidad
        8,

        // Distancia
        12,

        // Decaimiento
        2

    );


bounceLight.position.set(
    0,
    3,
    0
);


scene.add(
    bounceLight
);


// =====================================================
// CONTROLES
// =====================================================

const keys = {};

let mouseDown = false;


// =====================================================
// ROTACIÓN HORIZONTAL
// =====================================================

let yaw =
    -Math.PI / 4;


// =====================================================
// ROTACIÓN VERTICAL
// =====================================================

let pitch =
    -0.20;


// =====================================================
// VELOCIDAD
// =====================================================

const moveSpeed =
    0.12;


// =====================================================
// SENSIBILIDAD DEL MOUSE
// =====================================================

const mouseSensitivity =
    0.002;


// =====================================================
// TECLADO
// =====================================================

window.addEventListener(
    'keydown',
    (event) => {

        keys[event.code] = true;

    }
);


window.addEventListener(
    'keyup',
    (event) => {

        keys[event.code] = false;

    }
);


// =====================================================
// MOUSE - PRESIONAR
// =====================================================

renderer.domElement.addEventListener(
    'mousedown',
    () => {

        mouseDown = true;

    }
);


// =====================================================
// MOUSE - SOLTAR
// =====================================================

window.addEventListener(
    'mouseup',
    () => {

        mouseDown = false;

    }
);


// =====================================================
// MOVIMIENTO DEL MOUSE
// =====================================================

window.addEventListener(
    'mousemove',
    (event) => {

        if (!mouseDown)
            return;


        yaw -=
            event.movementX *
            mouseSensitivity;


        pitch -=
            event.movementY *
            mouseSensitivity;


        // Limitar inclinación

        pitch =
            Math.max(

                -Math.PI / 2 + 0.1,

                Math.min(
                    Math.PI / 2 - 0.1,
                    pitch
                )

            );

    }
);


// =====================================================
// ACTUALIZAR CÁMARA
// =====================================================

function updateCamera() {


    // =================================================
    // DIRECCIÓN HACIA ADELANTE
    // =================================================

    const forward =
        new THREE.Vector3(

            Math.sin(yaw),

            0,

            Math.cos(yaw)

        );


    // =================================================
    // DIRECCIÓN LATERAL
    // =================================================

    const right =
        new THREE.Vector3(

            Math.cos(yaw),

            0,

            -Math.sin(yaw)

        );


    // =================================================
    // W
    // =================================================

    if (keys['KeyW']) {

        camera.position.addScaledVector(
            forward,
            moveSpeed
        );

    }


    // =================================================
    // S
    // =================================================

    if (keys['KeyS']) {

        camera.position.addScaledVector(
            forward,
            -moveSpeed
        );

    }


    // =================================================
    // A
    // =================================================

    if (keys['KeyA']) {

        camera.position.addScaledVector(
            right,
            -moveSpeed
        );

    }


    // =================================================
    // D
    // =================================================

    if (keys['KeyD']) {

        camera.position.addScaledVector(
            right,
            moveSpeed
        );

    }


    // =================================================
    // Q
    // =================================================

    if (keys['KeyQ']) {

        camera.position.y -=
            moveSpeed;

    }


    // =================================================
    // E
    // =================================================

    if (keys['KeyE']) {

        camera.position.y +=
            moveSpeed;

    }


    // =================================================
    // DIRECCIÓN DE LA VISTA
    // =================================================

    const direction =
        new THREE.Vector3();


    direction.x =
        Math.sin(yaw) *
        Math.cos(pitch);


    direction.y =
        Math.sin(pitch);


    direction.z =
        Math.cos(yaw) *
        Math.cos(pitch);


    direction.normalize();


    // =================================================
    // CÁMARA
    // =================================================

    camera.lookAt(

        camera.position.x +
        direction.x,

        camera.position.y +
        direction.y,

        camera.position.z +
        direction.z

    );


    // =================================================
    // POSICIÓN DEL FOCO
    // =================================================

    flashlight.position.set(

        camera.position.x +
        direction.x * 0.35,

        camera.position.y +
        direction.y * 0.35,

        camera.position.z +
        direction.z * 0.35

    );


    // =================================================
    // DIRECCIÓN DEL FOCO
    // =================================================

    flashlightTarget.position.set(

        camera.position.x +
        direction.x * 25,

        camera.position.y +
        direction.y * 25,

        camera.position.z +
        direction.z * 25

    );

}


// =====================================================
// ANIMACIÓN
// =====================================================

function animate(time) {


    // =================================================
    // ACTUALIZAR CÁMARA Y FOCO
    // =================================================

    updateCamera();


    // =================================================
    // ROTACIÓN DEL CUBO
    // =================================================

    cube.rotation.x =
        time / 3000;

    cube.rotation.y =
        time / 1500;


    // =================================================
    // ROTACIÓN DE LA ESFERA
    // =================================================

    sphere.rotation.x =
        time / 2000;

    sphere.rotation.y =
        time / 2500;


    // =================================================
    // RENDER
    // =================================================

    renderer.render(
        scene,
        camera
    );

}


// =====================================================
// LOOP DE ANIMACIÓN
// =====================================================

renderer.setAnimationLoop(
    animate
);


// =====================================================
// RESPONSIVE
// =====================================================

window.addEventListener(
    'resize',
    () => {

        camera.aspect =
            window.innerWidth /
            window.innerHeight;


        camera.updateProjectionMatrix();


        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );

    }
);