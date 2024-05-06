import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { gsap } from "gsap";
import { Button } from "../components/ui/button";

const InfiniteTweetGraph = () => {
  const containerRef = useRef(null);
  const camera = useRef(new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000));
  const rendererRef = useRef(null);
  const controlsRef = useRef(null);

  useEffect(() => {
    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    // Scene
    const scene = new THREE.Scene();

    // Initialize renderer if it doesn't exist yet
    if (!rendererRef.current) {
      rendererRef.current = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    }
    const renderer = rendererRef.current;
    renderer.setSize(width, height);
    if (!containerRef.current.contains(renderer.domElement)) {
      containerRef.current.appendChild(renderer.domElement);
    }

    // Set initial camera position
    if (camera.current.position.z === 0) {
      camera.current.position.set(0, 0, 5);
    }

    // Set up OrbitControls for mouse panning
    const controls = new OrbitControls(camera.current, renderer.domElement);
    controlsRef.current = controls;
    controls.enableZoom = true;
    controls.enableDamping = true;

    const TWEET_DISTANCE = 10; // Fixed distance between tweets

    // Create 3D Grid Background using BufferGeometry
    const gridMaterial = new THREE.LineBasicMaterial({ color: 0x444444 });
    const gridSize = 100;
    const gridDivisions = 10;

    for (let z = -gridSize / 2; z <= gridSize / 2; z += gridDivisions) {
      const gridGeometry = new THREE.BufferGeometry();
      const vertices = [];

      for (let i = -gridSize / 2; i <= gridSize / 2; i += gridDivisions) {
        // Horizontal lines
        vertices.push(-gridSize / 2, i, z, gridSize / 2, i, z);

        // Vertical lines
        vertices.push(i, -gridSize / 2, z, i, gridSize / 2, z);
      }

      gridGeometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      const gridLines = new THREE.LineSegments(gridGeometry, gridMaterial);
      //scene.add(gridLines);
    }

    function wrapText(context, text, x, y, maxWidth, lineHeight) {
      const words = text.split(' ');
      let line = '';
      const lines = [];
      
      for (const word of words) {
        const testLine = line + word + ' ';
        const metrics = context.measureText(testLine);
        const testWidth = metrics.width;
    
        if (testWidth > maxWidth && line !== '') {
          lines.push(line);
          line = word + ' ';
        } else {
          line = testLine;
        }
      }
      
      lines.push(line);
    
      for (const l of lines) {
        context.fillText(l, x, y);
        y += lineHeight;
      }
    }
    
    // Function to create tweet planes
    const createTweetPlane = (i, j, link, text) => {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      const canvasWidth = 512;
      const canvasHeight = 256;
      canvas.width = canvasWidth;
      canvas.height = canvasHeight;
    
      // Set background color
      context.fillStyle = '#ffffff';
      context.fillRect(0, 0, canvasWidth, canvasHeight);
    
      // Set text properties
      context.font = '30px Arial';
      context.fillStyle = '#000000';
    
      // Draw wrapped text
      const lineHeight = 40; // Adjust line height
      const padding = 50; // Adjust padding
      wrapText(context, text, padding, padding, canvasWidth - 2 * padding, lineHeight);
    
      // Create a texture from the canvas
      const texture = new THREE.CanvasTexture(canvas);
    
      // Create a material with the texture
      const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
    
      // Create a plane geometry
      const planeGeometry = new THREE.PlaneGeometry(6, 3);
    
      // Create a mesh
      const planeMesh = new THREE.Mesh(planeGeometry, material);
    
      planeMesh.position.set(i * TWEET_DISTANCE, j * TWEET_DISTANCE, 0);
    
      // Add interactivity: Open tweet link on click
      planeMesh.userData = { url: link };
      planeMesh.cursor = 'pointer';
    
      scene.add(planeMesh);
    };

    // Sample tweet data, replace with your actual data
    const tweets = [
      { id: '1', link: 'https://twitter.com/example/status/1', text: 'This is the first tweet fnasdkfnsalfnldsafnsdanfals' },
      { id: '2', link: 'https://twitter.com/example/status/1', text: 'This is the first tweet fnasdkfnsalfnldsafnsdanfals' },
    ];

    for (let i = 0; i < tweets.length; i++) {
      createTweetPlane(i, 0, tweets[i].link, tweets[i].text);
    }

    // Lighting

    // Handle keyboard input for camera movement
    const handleKeyDown = (event) => {
      const moveAmount = TWEET_DISTANCE;
      const newPosition = { x: camera.current.position.x, y: camera.current.position.y };
      switch (event.key) {
        case 'ArrowLeft':
          newPosition.x -= moveAmount;
          break;
        case 'ArrowRight':
          newPosition.x += moveAmount;
          break;
        case 'ArrowUp':
          newPosition.y += moveAmount;
          break;
        case 'ArrowDown':
          newPosition.y -= moveAmount;
          break;
        default:
          break;
      }
      gsap.to(camera.current.position, {
        x: newPosition.x,
        y: newPosition.y,
        duration: 1, // Transition duration in seconds
      });
    };

    window.addEventListener('keydown', handleKeyDown);

    // Handle clicks on tweets
    const handleMouseClick = (event) => {
      const mouse = new THREE.Vector2();
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera.current);

      const intersects = raycaster.intersectObjects(scene.children);
      if (intersects.length > 0) {
        const intersectedObject = intersects[0].object;
        if (intersectedObject.userData.url) {
          window.open(intersectedObject.userData.url, '_blank');
        }
      }
    };

    window.addEventListener('click', handleMouseClick);

    // Render Loop
    const animate = () => {
      requestAnimationFrame(animate);
      renderer.render(scene, camera.current);
    };
    animate();

    // Cleanup
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('click', handleMouseClick);
    };
  }, []);

  const resetCameraPosition = () => {
    gsap.to(camera.current.position, {
      x: 0,
      y: 0,
      z: 5,
      duration: 1,
      onComplete: () => {
        controlsRef.current.target.set(0, 0, 0); // Reset the target
        controlsRef.current.update();
      }
    });
  };

  return (
    <div className="relative w-full h-screen">
      {/* This is the 3D Visualization Container */}
      <div ref={containerRef} className="absolute inset-0"></div>
      {/* This is the Sticky Button */}
      <div className="fixed top-2 left-2 z-00">
        <Button variant="inputMatch" onClick={resetCameraPosition}>
          Reset Position
        </Button>
      </div>
    </div>
  );
};

export default InfiniteTweetGraph;
