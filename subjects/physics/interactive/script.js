/**
 * EduVision Physics Interactive Learning Script
 * Connects to backend API for physics simulators
 */

const API_BASE = 'http://localhost:5000/api/physics';
let currentSimulator = null;
let currentSessionId = null;
let animationFrameId = null;
let cameraStream = null;
let gestureProcessor = null;
let gestureInterval = null;
let isCameraEnabled = false;
let isManualControl = false; // Flag to prevent gesture updates when user manually controls
let lastGestureUpdate = {}; // Store last gesture values for smoothing

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
  loadSimulators();
  setupEventListeners();
});

/**
 * Load available simulators from backend
 */
async function loadSimulators() {
  const grid = document.getElementById('simulator-grid');
  if (!grid) {
    console.error('Simulator grid not found');
    return;
  }
  
  // Show loading state
  grid.innerHTML = '<p style="color: var(--text-secondary);">Loading simulators...</p>';
  
  try {
    const response = await fetch(`${API_BASE}/simulators`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    grid.innerHTML = ''; // Clear loading message
    
    if (data.simulators && data.simulators.length > 0) {
      data.simulators.forEach(sim => {
        const card = document.createElement('div');
        card.className = 'simulator-card';
        card.innerHTML = `
          <h3>${sim.name}</h3>
          <p>${sim.description}</p>
        `;
        card.addEventListener('click', () => startSimulator(sim.id, sim.name));
        grid.appendChild(card);
      });
    } else {
      grid.innerHTML = '<p style="color: var(--text-secondary);">No simulators available</p>';
    }
  } catch (error) {
    console.error('Failed to load simulators:', error);
    // Show fallback simulators even if backend is down
    grid.innerHTML = '';
    const fallbackSimulators = [
      { id: 'projectile', name: 'Projectile Motion', description: 'Gesture-controlled projectile simulation' },
      { id: 'optics', name: 'Optics Simulator', description: 'Lens and mirror ray tracing' },
      { id: 'wave', name: 'Wave Interference', description: 'Wave interference patterns' },
      { id: 'rotational', name: 'Rotational Motion', description: 'Circular motion visualization' }
    ];
    
    fallbackSimulators.forEach(sim => {
      const card = document.createElement('div');
      card.className = 'simulator-card';
      card.innerHTML = `
        <h3>${sim.name}</h3>
        <p>${sim.description}</p>
      `;
      card.addEventListener('click', () => startSimulator(sim.id, sim.name));
      grid.appendChild(card);
    });
    
    // Show warning but don't block
    const status = document.createElement('div');
    status.style.cssText = 'margin-top: 1rem; padding: 1rem; background: rgba(255,170,0,0.1); border: 1px solid var(--physics); border-radius: 0.5rem; color: var(--text-secondary);';
    status.innerHTML = '<strong>Note:</strong> Backend server not connected. Simulators may not work. Start backend_server.py to enable full functionality.';
    grid.parentElement.appendChild(status);
  }
}

/**
 * Start a simulator
 */
async function startSimulator(simulatorId, simulatorName) {
  try {
    // Stop current simulator if any
    if (currentSimulator) {
      await stopSimulator();
    }
    
    currentSimulator = simulatorId;
    currentSessionId = `session_${Date.now()}`;
    
    // Start simulator on backend
    const response = await fetch(`${API_BASE}/simulator/${simulatorId}/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: currentSessionId })
    });
    
    if (!response.ok) {
      throw new Error('Failed to start simulator');
    }
    
    // Show simulator view and hide selection
    const selection = document.querySelector('.simulator-selection');
    const view = document.getElementById('simulator-view');
    const nameEl = document.getElementById('simulator-name');
    
    if (selection) selection.style.display = 'none';
    if (view) view.style.display = 'block';
    if (nameEl) nameEl.textContent = simulatorName;
    
    // Setup controls
    setupControls(simulatorId);
    
    // Start animation loop
    startAnimationLoop();
    
  } catch (error) {
    console.error('Failed to start simulator:', error);
    showError('Failed to start simulator. Check backend connection.');
  }
}

/**
 * Setup controls for specific simulator
 */
function setupControls(simulatorId) {
  const controlInputs = document.getElementById('control-inputs');
  const paramDisplay = document.getElementById('parameter-display');
  
  controlInputs.innerHTML = '';
  paramDisplay.innerHTML = '';
  
  if (simulatorId === 'projectile') {
    controlInputs.innerHTML = `
      <div class="control-input">
        <label>Velocity (m/s): <span id="velocity-value">60</span></label>
        <input type="range" id="velocity-slider" min="0" max="100" value="60" step="1">
      </div>
      <div class="control-input">
        <label>Angle (degrees): <span id="angle-value">45</span></label>
        <input type="range" id="angle-slider" min="0" max="90" value="45" step="1">
      </div>
      <button class="btn-primary" id="launch-btn">Launch Projectile</button>
    `;
    
    document.getElementById('velocity-slider').addEventListener('input', (e) => {
      document.getElementById('velocity-value').textContent = e.target.value;
      isManualControl = true;
      setTimeout(() => { isManualControl = false; }, 2000); // Reset after 2 seconds
    });
    
    document.getElementById('angle-slider').addEventListener('input', (e) => {
      document.getElementById('angle-value').textContent = e.target.value;
      isManualControl = true;
      setTimeout(() => { isManualControl = false; }, 2000); // Reset after 2 seconds
    });
    
    document.getElementById('launch-btn').addEventListener('click', () => {
      const velocity = parseFloat(document.getElementById('velocity-slider').value);
      const angle = parseFloat(document.getElementById('angle-slider').value);
      launchProjectile(velocity, angle);
    });
    
    // Show gesture control for projectile
    const gestureGroup = document.querySelector('.control-group:nth-of-type(2)');
    if (gestureGroup && gestureGroup.querySelector('h3').textContent === 'Gesture Control') {
      gestureGroup.style.display = 'block';
      // Setup camera button if not already set up
      const cameraBtn = document.getElementById('enable-camera-btn');
      if (cameraBtn && !cameraBtn.hasAttribute('data-listener-added')) {
        cameraBtn.setAttribute('data-listener-added', 'true');
        cameraBtn.addEventListener('click', enableCamera);
      }
    }
    
  } else if (simulatorId === 'optics') {
    controlInputs.innerHTML = `
      <div class="control-input">
        <label>Object X: <span id="obj-x-value">200</span></label>
        <input type="range" id="obj-x-slider" min="50" max="400" value="200" step="1">
      </div>
      <div class="control-input">
        <label>Object Height: <span id="obj-h-value">80</span></label>
        <input type="range" id="obj-h-slider" min="20" max="150" value="80" step="1">
      </div>
      <div class="control-input">
        <label>Focal Length: <span id="focal-value">120</span></label>
        <input type="range" id="focal-slider" min="50" max="250" value="120" step="1">
      </div>
      <div class="control-input">
        <label>Mode:</label>
        <select id="mode-select" class="control-select">
          <option value="0">Lens</option>
          <option value="1">Mirror</option>
        </select>
      </div>
      <div class="control-input">
        <label>
          <input type="checkbox" id="show-rays-checkbox" checked style="margin-right: 0.5rem;">
          Show Rays
        </label>
      </div>
    `;
    
    ['obj-x', 'obj-h', 'focal'].forEach(id => {
      const slider = document.getElementById(`${id}-slider`);
      const value = document.getElementById(`${id}-value`);
      slider.addEventListener('input', (e) => {
        value.textContent = e.target.value;
        isManualControl = true;
        setTimeout(() => { isManualControl = false; }, 2000);
        updateOptics();
      });
    });
    
    document.getElementById('mode-select').addEventListener('change', updateOptics);
    
    document.getElementById('show-rays-checkbox').addEventListener('change', (e) => {
      updateOptics();
    });
    
    // Hide gesture control for optics
    const gestureGroup = document.querySelector('.control-group:nth-of-type(2)');
    if (gestureGroup && gestureGroup.querySelector('h3').textContent === 'Gesture Control') {
      gestureGroup.style.display = 'none';
    }
    
  } else if (simulatorId === 'wave') {
    controlInputs.innerHTML = `
      <div class="control-input">
        <label>Frequency: <span id="freq-value">1.2</span> Hz</label>
        <input type="range" id="freq-slider" min="0.2" max="6.0" value="1.2" step="0.1">
      </div>
      <div class="control-input">
        <label>Amplitude: <span id="amp-value">0.9</span></label>
        <input type="range" id="amp-slider" min="0.1" max="1.5" value="0.9" step="0.1">
      </div>
      <button class="btn-primary" id="pause-btn">Pause</button>
    `;
    
    // Show gesture control for wave
    const gestureGroup = document.querySelector('.control-group:nth-of-type(2)');
    if (gestureGroup && gestureGroup.querySelector('h3').textContent === 'Gesture Control') {
      gestureGroup.style.display = 'block';
    }
    
    document.getElementById('freq-slider').addEventListener('input', (e) => {
      document.getElementById('freq-value').textContent = e.target.value;
      isManualControl = true;
      setTimeout(() => { isManualControl = false; }, 2000);
      updateWave();
    });
    
    document.getElementById('amp-slider').addEventListener('input', (e) => {
      document.getElementById('amp-value').textContent = e.target.value;
      isManualControl = true;
      setTimeout(() => { isManualControl = false; }, 2000);
      updateWave();
    });
    
    document.getElementById('pause-btn').addEventListener('click', () => {
      const paused = document.getElementById('pause-btn').textContent === 'Pause';
      updateWave({ paused: !paused });
      document.getElementById('pause-btn').textContent = paused ? 'Resume' : 'Pause';
    });
    
  } else if (simulatorId === 'rotational') {
    controlInputs.innerHTML = `
      <div class="control-input">
        <label>Radius: <span id="radius-value">1.0</span> m</label>
        <input type="range" id="radius-slider" min="0.1" max="3.0" value="1.0" step="0.1">
      </div>
      <div class="control-input">
        <label>Angular Velocity: <span id="omega-value">2.0</span> rad/s</label>
        <input type="range" id="omega-slider" min="0" max="10" value="2.0" step="0.1">
      </div>
    `;
    
    // Show gesture control for rotational
    const gestureGroup = document.querySelector('.control-group:nth-of-type(2)');
    if (gestureGroup && gestureGroup.querySelector('h3').textContent === 'Gesture Control') {
      gestureGroup.style.display = 'block';
    }
    
    document.getElementById('radius-slider').addEventListener('input', (e) => {
      document.getElementById('radius-value').textContent = e.target.value;
      isManualControl = true;
      setTimeout(() => { isManualControl = false; }, 2000);
      updateRotational();
    });
    
    document.getElementById('omega-slider').addEventListener('input', (e) => {
      document.getElementById('omega-value').textContent = e.target.value;
      isManualControl = true;
      setTimeout(() => { isManualControl = false; }, 2000);
      updateRotational();
    });
  }
}

/**
 * Start animation loop
 */
function startAnimationLoop() {
  const canvas = document.getElementById('simulator-canvas');
  const ctx = canvas.getContext('2d');
  
  async function animate() {
    if (!currentSimulator || !currentSessionId) return;
    
    try {
      const response = await fetch(`${API_BASE}/simulator/${currentSimulator}/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          session_id: currentSessionId,
          params: getCurrentParams()
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to update simulator');
      }
      
      const data = await response.json();
      
      // Load and draw image
      const img = new Image();
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        document.getElementById('canvas-overlay').style.display = 'none';
      };
      img.src = data.frame;
      
    } catch (error) {
      console.error('Animation error:', error);
    }
    
    animationFrameId = requestAnimationFrame(animate);
  }
  
  animate();
}

/**
 * Get current parameters based on simulator type
 */
function getCurrentParams() {
  if (currentSimulator === 'projectile') {
    return {}; // Launch handled separately
  } else if (currentSimulator === 'optics') {
    return {
      obj_x: parseInt(document.getElementById('obj-x-slider')?.value || 200),
      obj_h: parseInt(document.getElementById('obj-h-slider')?.value || 80),
      focal: parseInt(document.getElementById('focal-slider')?.value || 120),
      mode: parseInt(document.getElementById('mode-select')?.value || 0),
      show_rays: document.getElementById('show-rays-checkbox')?.checked !== false
    };
  } else if (currentSimulator === 'wave') {
    return {
      freq: parseFloat(document.getElementById('freq-slider')?.value || 1.2),
      amp: parseFloat(document.getElementById('amp-slider')?.value || 0.9),
      paused: document.getElementById('pause-btn')?.textContent === 'Resume'
    };
  } else if (currentSimulator === 'rotational') {
    return {
      radius: parseFloat(document.getElementById('radius-slider')?.value || 1.0),
      omega: parseFloat(document.getElementById('omega-slider')?.value || 2.0)
    };
  }
  return {};
}

/**
 * Launch projectile
 */
async function launchProjectile(velocity, angle) {
  try {
    await fetch(`${API_BASE}/simulator/projectile/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: currentSessionId,
        params: {
          launch: { velocity, angle }
        }
      })
    });
  } catch (error) {
    console.error('Failed to launch:', error);
  }
}

/**
 * Update optics simulator
 */
function updateOptics() {
  // Parameters are sent in animation loop
  // This function is called when controls change
}

/**
 * Update wave simulator
 */
function updateWave(params = {}) {
  // Parameters are sent in animation loop
}

/**
 * Update rotational simulator
 */
function updateRotational() {
  // Parameters are sent in animation loop
}

/**
 * Stop current simulator
 */
async function stopSimulator() {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  
  // Disable camera if enabled
  if (isCameraEnabled) {
    disableCamera();
  }
  
  // Reset gesture tracking
  lastGestureUpdate = {};
  isManualControl = false;
  
  if (currentSimulator && currentSessionId) {
    try {
      await fetch(`${API_BASE}/simulator/${currentSimulator}/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: currentSessionId })
      });
    } catch (error) {
      console.error('Failed to stop simulator:', error);
    }
  }
  
  currentSimulator = null;
  currentSessionId = null;
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
  const closeBtn = document.getElementById('close-simulator');
  if (closeBtn) {
    closeBtn.addEventListener('click', async () => {
      await stopSimulator();
      // Go back to simulator selection, not main page
      const selection = document.querySelector('.simulator-selection');
      const view = document.getElementById('simulator-view');
      if (selection) selection.style.display = 'block';
      if (view) view.style.display = 'none';
      // Scroll to top to show selection
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}

/**
 * Enable camera for gesture control
 */
async function enableCamera() {
  // If already enabled, disable it
  if (isCameraEnabled) {
    disableCamera();
    return;
  }
  
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'user', width: 640, height: 480 } 
    });
    
    cameraStream = stream;
    isCameraEnabled = true;
    
    // Get the preview video element
    const preview = document.getElementById('camera-preview');
    if (preview) {
      preview.srcObject = stream;
      preview.style.display = 'block';
      // Ensure video plays
      preview.play().catch(err => console.error('Video play error:', err));
    }
    
    // Create a hidden video element to capture frames for processing
    let video = document.getElementById('camera-video-source');
    if (!video) {
      video = document.createElement('video');
      video.id = 'camera-video-source';
      video.style.display = 'none';
      video.autoplay = true;
      video.playsinline = true;
      video.muted = true;
      document.body.appendChild(video);
    }
    video.srcObject = stream;
    video.play().catch(err => console.error('Hidden video play error:', err));
    
    const btn = document.getElementById('enable-camera-btn');
    if (btn) {
      btn.textContent = 'Disable Camera';
      // Remove old event listeners and add new one
      btn.replaceWith(btn.cloneNode(true));
      const newBtn = document.getElementById('enable-camera-btn');
      newBtn.addEventListener('click', disableCamera);
      newBtn.classList.add('btn-active');
    }
    
    const status = document.getElementById('gesture-status');
    if (status) {
      status.innerHTML = '<p style="color: #ffaa00;">Camera enabled - Show hands to control</p>';
    }
    
    // Start gesture processing
    startGestureProcessing(video);
    
  } catch (error) {
    console.error('Failed to enable camera:', error);
    showError('Failed to access camera. Please check permissions.');
    isCameraEnabled = false;
    
    const btn = document.getElementById('enable-camera-btn');
    if (btn) {
      btn.textContent = 'Enable Camera';
      btn.replaceWith(btn.cloneNode(true));
      const newBtn = document.getElementById('enable-camera-btn');
      newBtn.addEventListener('click', enableCamera);
      newBtn.classList.remove('btn-active');
    }
  }
}

/**
 * Disable camera
 */
function disableCamera() {
  console.log('Disabling camera...');
  
  // Set flag first to stop processing
  isCameraEnabled = false;
  
  // Clear gesture processing interval
  if (gestureInterval) {
    clearInterval(gestureInterval);
    gestureInterval = null;
    console.log('Gesture interval cleared');
  }
  
  // Stop all camera tracks
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => {
      track.stop();
      console.log('Camera track stopped');
    });
    cameraStream = null;
  }
  
  // Stop and hide preview video
  const preview = document.getElementById('camera-preview');
  if (preview) {
    preview.pause();
    preview.srcObject = null;
    preview.style.display = 'none';
    console.log('Preview video stopped');
  }
  
  // Remove annotated overlay if it exists
  const overlay = document.getElementById('camera-annotated-overlay');
  if (overlay) {
    overlay.remove();
    console.log('Annotated overlay removed');
  }
  
  // Stop and remove hidden video source
  const video = document.getElementById('camera-video-source');
  if (video) {
    video.pause();
    video.srcObject = null;
    video.remove();
    console.log('Hidden video source removed');
  }
  
  // Update button
  const btn = document.getElementById('enable-camera-btn');
  if (btn) {
    btn.textContent = 'Enable Camera';
    // Remove old event listeners and add new one
    btn.replaceWith(btn.cloneNode(true));
    const newBtn = document.getElementById('enable-camera-btn');
    newBtn.addEventListener('click', enableCamera);
    newBtn.classList.remove('btn-active');
  }
  
  // Update status
  const status = document.getElementById('gesture-status');
  if (status) {
    status.innerHTML = '<p>Camera disabled</p>';
  }
  
  console.log('Camera disabled successfully');
}

/**
 * Start gesture processing with landmark visualization
 */
function startGestureProcessing(video) {
  if (!video) {
    console.error('Video element not found');
    return;
  }
  
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 640;
  canvas.height = 480;
  
  let frameCount = 0;
  
  gestureInterval = setInterval(async () => {
    if (!isCameraEnabled || !video || video.readyState !== video.HAVE_ENOUGH_DATA) {
      return;
    }
    
    try {
      // Draw video frame to canvas
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // Get image data for processing
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      
      // Process gesture frame
      const gestureData = await processGestureFrame(imageData);
      
      // Debug: Log gesture data periodically
      if (gestureData && frameCount % 30 === 0) { // Log every 3 seconds
        console.log('Gesture data received:', {
          hands_detected: gestureData.hands_detected,
          left_dist: gestureData.left_dist,
          right_dist: gestureData.right_dist,
          pinch: gestureData.pinch
        });
      }
      
      // Display annotated frame with landmarks if available
      if (gestureData && gestureData.annotated_frame) {
        const preview = document.getElementById('camera-preview');
        if (preview) {
          // Create an overlay image element to show annotated frame
          let overlay = document.getElementById('camera-annotated-overlay');
          if (!overlay) {
            overlay = document.createElement('img');
            overlay.id = 'camera-annotated-overlay';
            overlay.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; pointer-events: none; transform: scaleX(-1); z-index: 2;';
            const previewContainer = preview.parentElement;
            if (previewContainer) {
              previewContainer.style.position = 'relative';
              previewContainer.appendChild(overlay);
            }
          }
          overlay.src = gestureData.annotated_frame;
          overlay.style.display = 'block';
        }
      } else {
        // Hide overlay if no annotated frame
        const overlay = document.getElementById('camera-annotated-overlay');
        if (overlay) {
          overlay.style.display = 'none';
        }
      }
      
      // Only update simulator when hands are actually detected
      if (gestureData && gestureData.hands_detected) {
        updateSimulatorFromGestures(gestureData);
        
        // Update status every frame for immediate feedback
        frameCount++;
        const status = document.getElementById('gesture-status');
        if (status) {
          let statusText = '✅ Hands detected - Controlling simulator';
          if (gestureData.left_dist !== null) {
            statusText += ` | Left: ${gestureData.left_dist.toFixed(2)}`;
          }
          if (gestureData.right_dist !== null) {
            statusText += ` | Right: ${gestureData.right_dist.toFixed(2)}`;
          }
          if (gestureData.pinch) {
            statusText += ' | 👌 Pinch!';
          }
          status.innerHTML = `<p style="color: #00ff00; font-weight: bold;">${statusText}</p>`;
        }
      } else {
        // No hands detected
        frameCount++;
        if (frameCount % 10 === 0) {
          const status = document.getElementById('gesture-status');
          if (status) {
            status.innerHTML = '<p style="color: #ffaa00;">📹 Camera enabled - Show hands to control</p>';
          }
        }
      }
    } catch (error) {
      console.error('Gesture processing error:', error);
    }
  }, 100); // Process every 100ms
}

/**
 * Process gesture frame (sends to backend for processing)
 */
async function processGestureFrame(imageData) {
  try {
    // Convert imageData to base64
    const canvas = document.createElement('canvas');
    canvas.width = imageData.width;
    canvas.height = imageData.height;
    const ctx = canvas.getContext('2d');
    ctx.putImageData(imageData, 0, 0);
    
    const dataUrl = canvas.toDataURL('image/jpeg', 0.5);
    const base64 = dataUrl.split(',')[1];
    
    // Send to backend for gesture processing
    const response = await fetch(`${API_BASE}/gesture/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image: base64,
        width: imageData.width,
        height: imageData.height
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      throw new Error(`HTTP ${response.status}`);
    }
  } catch (error) {
    console.warn('Gesture processing failed, using fallback:', error);
    // Fallback: return null to indicate no gesture detected
    // This prevents errors but doesn't simulate fake data
    return null;
  }
}

/**
 * Smooth gesture value using exponential moving average
 */
function smoothGestureValue(currentValue, lastValue, smoothingFactor = 0.3) {
  if (lastValue === null || lastValue === undefined) {
    return currentValue;
  }
  return lastValue + (currentValue - lastValue) * smoothingFactor;
}

/**
 * Update simulator based on gesture data (only when hands are detected)
 */
function updateSimulatorFromGestures(gestureData) {
  // Only process if hands are actually detected and not manually controlling
  if (!gestureData || !gestureData.hands_detected || !currentSimulator || !currentSessionId) {
    return;
  }
  
  if (isManualControl) {
    console.log('Manual control active, skipping gesture update');
    return;
  }
  
  console.log('Updating simulator from gestures:', {
    left_dist: gestureData.left_dist,
    right_dist: gestureData.right_dist,
    pinch: gestureData.pinch,
    simulator: currentSimulator
  });
  
  if (currentSimulator === 'projectile') {
    // Map gestures to velocity and angle with smoothing
    if (gestureData.left_dist !== null && !isNaN(gestureData.left_dist)) {
      const rawAngle = gestureData.left_dist * 90;
      const smoothedAngle = smoothGestureValue(rawAngle, lastGestureUpdate.angle || rawAngle, 0.3);
      const angle = Math.max(0, Math.min(90, smoothedAngle));
      lastGestureUpdate.angle = angle;
      
      const angleSlider = document.getElementById('angle-slider');
      const angleValue = document.getElementById('angle-value');
      if (angleSlider && angleValue) {
        const oldValue = angleSlider.value;
        angleSlider.value = angle;
        angleValue.textContent = Math.round(angle);
        console.log(`Gesture: Angle updated from ${oldValue} to ${angle}`);
        // The animation loop will pick up the new value via getCurrentParams()
      }
    }
    
    if (gestureData.right_dist !== null && !isNaN(gestureData.right_dist)) {
      const rawVelocity = gestureData.right_dist * 100;
      const smoothedVelocity = smoothGestureValue(rawVelocity, lastGestureUpdate.velocity || rawVelocity, 0.3);
      const velocity = Math.max(0, Math.min(100, smoothedVelocity));
      lastGestureUpdate.velocity = velocity;
      
      const velocitySlider = document.getElementById('velocity-slider');
      const velocityValue = document.getElementById('velocity-value');
      if (velocitySlider && velocityValue) {
        const oldValue = velocitySlider.value;
        velocitySlider.value = velocity;
        velocityValue.textContent = Math.round(velocity);
        console.log(`Gesture: Velocity updated from ${oldValue} to ${velocity}`);
      }
    }
    
    // Launch on pinch (only trigger once per pinch)
    if (gestureData.pinch === true && !lastGestureUpdate.pinchTriggered) {
      lastGestureUpdate.pinchTriggered = true;
      const velocity = parseFloat(document.getElementById('velocity-slider')?.value || 60);
      const angle = parseFloat(document.getElementById('angle-slider')?.value || 45);
      console.log(`Gesture: Launching projectile with velocity=${velocity}, angle=${angle}`);
      launchProjectile(velocity, angle);
    } else if (gestureData.pinch === false) {
      lastGestureUpdate.pinchTriggered = false;
    }
  } else if (currentSimulator === 'wave') {
    // Map gestures for wave simulator with smoothing
    if (gestureData.left_dist !== null && !isNaN(gestureData.left_dist)) {
      const rawFreq = gestureData.left_dist * 6.0;
      const smoothedFreq = smoothGestureValue(rawFreq, lastGestureUpdate.freq || rawFreq, 0.3);
      const freq = Math.max(0.2, Math.min(6.0, smoothedFreq));
      lastGestureUpdate.freq = freq;
      
      const freqSlider = document.getElementById('freq-slider');
      const freqValue = document.getElementById('freq-value');
      if (freqSlider && freqValue) {
        freqSlider.value = freq;
        freqValue.textContent = freq.toFixed(1);
        console.log(`Gesture: Frequency updated to ${freq}`);
      }
    }
    
    if (gestureData.right_dist !== null && !isNaN(gestureData.right_dist)) {
      const rawAmp = gestureData.right_dist * 1.5;
      const smoothedAmp = smoothGestureValue(rawAmp, lastGestureUpdate.amp || rawAmp, 0.3);
      const amp = Math.max(0.1, Math.min(1.5, smoothedAmp));
      lastGestureUpdate.amp = amp;
      
      const ampSlider = document.getElementById('amp-slider');
      const ampValue = document.getElementById('amp-value');
      if (ampSlider && ampValue) {
        ampSlider.value = amp;
        ampValue.textContent = amp.toFixed(1);
        console.log(`Gesture: Amplitude updated to ${amp}`);
      }
    }
  } else if (currentSimulator === 'rotational') {
    // Map gestures for rotational simulator with smoothing
    if (gestureData.left_dist !== null && !isNaN(gestureData.left_dist)) {
      const rawRadius = gestureData.left_dist * 3.0;
      const smoothedRadius = smoothGestureValue(rawRadius, lastGestureUpdate.radius || rawRadius, 0.3);
      const radius = Math.max(0.1, Math.min(3.0, smoothedRadius));
      lastGestureUpdate.radius = radius;
      
      const radiusSlider = document.getElementById('radius-slider');
      const radiusValue = document.getElementById('radius-value');
      if (radiusSlider && radiusValue) {
        radiusSlider.value = radius;
        radiusValue.textContent = radius.toFixed(1);
        console.log(`Gesture: Radius updated to ${radius}`);
      }
    }
    
    if (gestureData.right_dist !== null && !isNaN(gestureData.right_dist)) {
      const rawOmega = gestureData.right_dist * 10;
      const smoothedOmega = smoothGestureValue(rawOmega, lastGestureUpdate.omega || rawOmega, 0.3);
      const omega = Math.max(0, Math.min(10, smoothedOmega));
      lastGestureUpdate.omega = omega;
      
      const omegaSlider = document.getElementById('omega-slider');
      const omegaValue = document.getElementById('omega-value');
      if (omegaSlider && omegaValue) {
        omegaSlider.value = omega;
        omegaValue.textContent = omega.toFixed(1);
        console.log(`Gesture: Angular velocity updated to ${omega}`);
      }
    }
  }
}

/**
 * Show error message
 */
function showError(message) {
  const overlay = document.getElementById('canvas-overlay');
  overlay.style.display = 'flex';
  document.getElementById('status-text').textContent = message;
  document.getElementById('status-text').style.color = '#ff4444';
}

