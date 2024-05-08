import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { gsap } from "gsap";
import { Button } from "../components/ui/button";
import { MyContext } from "../MyContext";
import { useContext } from "react";
import { useState } from "react";
import { Link } from 'react-router-dom';


const InfiniteTweetGraph = () => {
  const containerRef = useRef(null);
  const camera = useRef(new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000));
  const rendererRef = useRef(null);
  const controlsRef = useRef(null);
  const [beginStatus, setBeginStatus] = useState(true);

  const {tweets, setTweets} = useContext(MyContext);

  useEffect(() => {
    console.log(tweets);
    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    // Scene
    const scene = new THREE.Scene();

    // Initialize renderer if it doesn't exist yet
    if (!rendererRef.current) {
      rendererRef.current = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    }
    const renderer = rendererRef.current;
    renderer.setPixelRatio(window.devicePixelRatio);
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

    function wrapText(context, text, x, y, maxWidth, lineHeight, maxY) {
      const words = text.split(' ');
      let line = '';
      const lines = [];
    
      for (const word of words) {
        const testLine = line + word + ' ';
        const metrics = context.measureText(testLine);
        const testWidth = metrics.width;
    
        if (testWidth > maxWidth - 40 && line !== '') {
          lines.push(line);
          line = word + ' ';
        } else {
          line = testLine;
        }
      }
    
      lines.push(line);
    
      for (const l of lines) {
        if (y + lineHeight > maxY) { // Check if adding another line would exceed the maxY
          break; // Stop adding lines if it would
        }
        context.fillText(l, x, y);
        y += lineHeight;
      }
    }
    
    // Function to create tweet planes
    const createTweetPlane = (i, j, tweet) => {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      const devicePixelRatio = window.devicePixelRatio || 1;
      const canvasWidth = 512;
      const canvasHeight = 256;
      const lineHeight = 24;
      const padding = 40;
      const footerHeight = 40; // Height reserved for footer text
      const borderRadius = 20; // Radius for rounded corners
      canvas.width = canvasWidth * devicePixelRatio;
      canvas.height = canvasHeight * devicePixelRatio;
    
      context.scale(devicePixelRatio, devicePixelRatio);

      function drawRoundedRect(x, y, width, height, radius) {
        context.beginPath();
        context.moveTo(x + radius, y);
        context.lineTo(x + width - radius, y);
        context.quadraticCurveTo(x + width, y, x + width, y + radius);
        context.lineTo(x + width, y + height - radius);
        context.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        context.lineTo(x + radius, y + height);
        context.quadraticCurveTo(x, y + height, x, y + height - radius);
        context.lineTo(x, y + radius);
        context.quadraticCurveTo(x, y, x + radius, y);
        context.closePath();
        context.fill();
      }
    
      // Draw rounded rectangle
      drawRoundedRect(context, 0, 0, canvasWidth, canvasHeight, borderRadius);
    
      // Background color
      context.fillStyle = '#070708';
      drawRoundedRect(0, 0, canvasWidth, canvasHeight, borderRadius);
    
      // Text properties for the username
      context.font = 'bold 18px Helvetica Neue';
      context.fillStyle = '#ffffff';
      context.fillText(tweet.user, padding, padding);
    
      // Text properties for the date
      context.textAlign = 'right';
      context.fillText(new Date(tweet.time).toLocaleDateString('en-US', {
        year: 'numeric', month: 'long', day: 'numeric'
      }), canvasWidth - padding, padding);
      context.textAlign = 'left';
    
      // Maximum Y coordinate for body text, to avoid overlapping with footer
      const maxY = canvasHeight - footerHeight;
    
      // Body text properties
      context.font = '16px Helvetica Neue';
      context.fillStyle = '#c1ebfb';
      wrapText(context, tweet.text, padding, padding + 60, canvasWidth - 2 * padding, lineHeight, maxY);
    
      // Footer text
      context.font = 'italic 16px Helvetica Neue';
      context.fillStyle = '#ffffff';
      context.fillText("Click to read more...", padding, canvasHeight - padding);
    
      const texture = new THREE.CanvasTexture(canvas);
      texture.generateMipmaps = true;
      texture.minFilter = THREE.LinearMipmapLinearFilter; // This can help with blurring at a distance

      const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
      const planeGeometry = new THREE.PlaneGeometry(6, 3);
      const planeMesh = new THREE.Mesh(planeGeometry, material);
      planeMesh.position.set(i * TWEET_DISTANCE, j * TWEET_DISTANCE/2, 0);
      planeMesh.userData = { url: tweet.link };
      planeMesh.cursor = 'pointer';
      scene.add(planeMesh);
    };
    
    

    // Sample tweet data, replace with your actual data
    // const tweets = [
    //   {
    //     "id": "1644498932242821120",
    //     "link": "https://www.twitter.com/SenBlumenthal/statuses/1644498932242821120",
    //     "similarity": 0.535,
    //     "text": "If allowed to go into effect, this is tantamount to a nationwide ban on the most common form of abortion care. Mifepristone has been used safely&amp;effectively for 20 yrs w/ FDA approval for abortion care &amp; miscarriage management—now recklessly overruled by an activist judge in TX. https://twitter.com/CBSNews/status/1644473061419147265 QT @CBSNews BREAKING: A federal judge has halted FDA approval of the abortion pill mifepristone. https://www.cbsnews.com/news/federal-judge-halts-fda-approval-of-abortion-pill-mifepristone/?ftag=CNM-00-10aab7e&linkId=208915865",
    //     "time": "2023-04-07T20:34:33-04:00",
    //     "user": "SenBlumenthal"
    //     },
    //     { id: '2', link: 'https://twitter.com/example/status/1', text: 'This is the first tweet fnasdkfnsalfnldsafnsdanfals' },
    // ];

    const weeks = [-2, -1, 0, 1, 2];
    console.log("Tweets: ", tweets);

    if (tweets["week_0"] !== undefined) {
      for (let i = 0; i < weeks.length; i++) {
        console.log(weeks[i]);
        console.log(tweets[`week_${weeks[i]}`]);
        for (let j = 0; j < tweets[`week_${weeks[i]}`].length; j++) {
            createTweetPlane(j, -weeks[i], tweets[`week_${weeks[i]}`][j])
        } // createTweetPlane(i, weeks[i], tweets[`week_${weeks[i]}`]);
      }
    }

    // for (let i = 0; i < tweets.length; i++) {
    //   createTweetPlane(i, 0, tweets[i]);
    // }

    // Lighting

    // Handle keyboard input for camera movement
    const handleKeyDown = (event) => {
      const moveAmount = TWEET_DISTANCE;
      const newPosition = { x: camera.current.position.x, y: camera.current.position.y };
      setBeginStatus(false);
      switch (event.key) {
        case 'ArrowLeft':
          newPosition.x -= moveAmount;
          break;
        case 'ArrowRight':
          newPosition.x += moveAmount;
          break;
        case 'ArrowUp':
          newPosition.y += moveAmount/2;
          break;
        case 'ArrowDown':
          newPosition.y -= moveAmount/2;
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

  const resetCameraPosition = () => {setBeginStatus(true);
    gsap.to(camera.current.position, {
      x: 0,
      y: 0,
      z: 5,
      duration: 1,
      onComplete: () => {
        controlsRef.current.target.set(0, 0, 0); // Reset the target
        controlsRef.current.update();
        setBeginStatus(true);
      }
    });
  };

  return (
    <div className="dark relative w-full h-screen">
      {/* This is the 3D Visualization Container */}
      <div ref={containerRef} className="absolute inset-0"></div>
      {/* This is the Sticky Button */}
      {beginStatus && <div className="fixed inset-x-0 top-20 flex justify-center">
          <h1 className="text-2xl font-extrabold tracking-tight lg:text-2xl text-accent-foreground text-center">
              Older Tweets ↑
          </h1>
      </div>}
      {beginStatus && <div className="fixed inset-x-0 bottom-20 flex justify-center">
          <h1 className="text-2xl font-extrabold tracking-tight lg:text-2xl text-accent-foreground text-center">
              Newer Tweets ↓
          </h1>
      </div>}
      {beginStatus && <div className="fixed inset-y-0 right-20 flex items-center">
          <h1 className="text-2xl font-extrabold tracking-tight lg:text-2xl text-accent-foreground text-center">
              Relevant Tweets →
          </h1>
      </div>}
      <div className="fixed top-5 right-5 z-00">
        <Button variant="inputMatch" onClick={resetCameraPosition}>
          Reset Position
        </Button>
      </div>
      <div className="fixed top-5 left-5 z-00">
        <Link to="/" className="text-2xl font-extrabold tracking-tight lg:text-2xl text-accent-foreground text-center">
          Home
        </Link>
      </div>
    </div>
  );
};

export default InfiniteTweetGraph;
