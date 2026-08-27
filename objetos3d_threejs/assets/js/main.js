import * as THREE from 'three';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x07111f);

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);

camera.position.set(8, 6, 8);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);

document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(2, 1.2, 2.5);

const material = new THREE.MeshBasicMaterial({
  color: 0x22d3ee,
  wireframe: false
});

const cube = new THREE.Mesh(geometry, material);
cube.position.x = -1.5;

scene.add(cube);

const sphereGeometry = new THREE.SphereGeometry(1, 32, 32);

const sphereMaterial = new THREE.MeshBasicMaterial({
  color: 0xff4d6d,
  wireframe: false
});

const sphere = new THREE.Mesh(
  sphereGeometry,
  sphereMaterial
);

sphere.position.x = 1.5;

scene.add(sphere);

function animate(time) {
  cube.rotation.x = time / 3000;
  cube.rotation.y = time / 1500;

  sphere.rotation.x = time / 2000;
  sphere.rotation.y = time / 2500;

  renderer.render(scene, camera);
}

renderer.setAnimationLoop(animate);

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(
    window.innerWidth,
    window.innerHeight
  );
});