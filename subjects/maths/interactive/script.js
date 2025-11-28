/**
 * EduVision Mathematics Interactive Learning Script
 * Connects to backend API for mathematics simulators
 */

const API_BASE = 'http://localhost:5000/api/maths';
let currentSimulator = null;
let currentSessionId = null;
let animationFrameId = null;

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
    // Show fallback simulator
    grid.innerHTML = '';
    const fallbackSimulator = {
      id: 'trig',
      name: 'Trigonometric Visualizer',
      description: 'Interactive trigonometric graph with angle marker'
    };
    
    const card = document.createElement('div');
    card.className = 'simulator-card';
    card.innerHTML = `
      <h3>${fallbackSimulator.name}</h3>
      <p>${fallbackSimulator.description}</p>
    `;
    card.addEventListener('click', () => startSimulator(fallbackSimulator.id, fallbackSimulator.name));
    grid.appendChild(card);
    
    // Show warning but don't block
    const status = document.createElement('div');
    status.style.cssText = 'margin-top: 1rem; padding: 1rem; background: rgba(0,140,255,0.1); border: 1px solid var(--math); border-radius: 0.5rem; color: var(--text-secondary);';
    status.innerHTML = '<strong>Note:</strong> Backend server not connected. Start backend_server.py to enable full functionality.';
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
    
    // Initialize parameter display for trig
    if (simulatorId === 'trig') {
      updateTrig();
    }
    
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
  
  if (simulatorId === 'trig') {
    controlInputs.innerHTML = `
      <div class="control-input">
        <label>Function:</label>
        <select id="func-select" class="control-select">
          <option value="sin">sin</option>
          <option value="cos">cos</option>
          <option value="tan">tan</option>
          <option value="csc">csc</option>
          <option value="sec">sec</option>
          <option value="cot">cot</option>
        </select>
      </div>
      <div class="control-input">
        <label>Angle (degrees): <span id="angle-value">30</span>°</label>
        <input type="range" id="angle-slider" min="-720" max="720" value="30" step="1">
      </div>
      <div class="control-input">
        <label>X Range:</label>
        <select id="x-range-select" class="control-select">
          <option value="-360,360">-360 to 360</option>
          <option value="-180,180">-180 to 180</option>
          <option value="-90,90">-90 to 90</option>
          <option value="0,360">0 to 360</option>
        </select>
      </div>
      <div class="control-input">
        <label>Y-axis Clip: <span id="y-clip-value">5.0</span></label>
        <input type="range" id="y-clip-slider" min="1.0" max="20.0" value="5.0" step="0.5">
      </div>
      <div class="control-input">
        <label>
          <input type="checkbox" id="show-grid-checkbox" checked style="margin-right: 0.5rem;">
          Show Grid
        </label>
      </div>
    `;
    
    document.getElementById('func-select').addEventListener('change', (e) => {
      updateTrig();
    });
    
    document.getElementById('angle-slider').addEventListener('input', (e) => {
      document.getElementById('angle-value').textContent = e.target.value;
      updateTrig();
    });
    
    document.getElementById('x-range-select').addEventListener('change', (e) => {
      updateTrig();
    });
    
    document.getElementById('y-clip-slider').addEventListener('input', (e) => {
      document.getElementById('y-clip-value').textContent = e.target.value;
      updateTrig();
    });
    
    document.getElementById('show-grid-checkbox').addEventListener('change', (e) => {
      updateTrig();
    });
    
    // Update parameter display
    paramDisplay.innerHTML = `
      <div class="parameter-item">
        <strong>Function:</strong> <span id="param-func">sin</span>
      </div>
      <div class="parameter-item">
        <strong>Angle:</strong> <span id="param-angle">30°</span>
      </div>
      <div class="parameter-item">
        <strong>Value:</strong> <span id="param-value">-</span>
      </div>
    `;
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
  if (currentSimulator === 'trig') {
    const xRange = document.getElementById('x-range-select')?.value || '-360,360';
    const [xLeft, xRight] = xRange.split(',').map(Number);
    
    return {
      func: document.getElementById('func-select')?.value || 'sin',
      angle_deg: parseFloat(document.getElementById('angle-slider')?.value || 30),
      x_left: xLeft,
      x_right: xRight,
      y_clip: parseFloat(document.getElementById('y-clip-slider')?.value || 5.0),
      show_grid: document.getElementById('show-grid-checkbox')?.checked !== false
    };
  }
  return {};
}

/**
 * Update trig simulator
 */
function updateTrig() {
  // Parameters are sent in animation loop
  // Update parameter display
  if (currentSimulator === 'trig') {
    const func = document.getElementById('func-select')?.value || 'sin';
    const angle = document.getElementById('angle-slider')?.value || 30;
    
    const paramFunc = document.getElementById('param-func');
    const paramAngle = document.getElementById('param-angle');
    
    if (paramFunc) paramFunc.textContent = func;
    if (paramAngle) paramAngle.textContent = `${angle}°`;
    
    // Calculate value (simplified - would be better from backend)
    const angleRad = (parseFloat(angle) * Math.PI) / 180;
    let value = 0;
    if (func === 'sin') value = Math.sin(angleRad);
    else if (func === 'cos') value = Math.cos(angleRad);
    else if (func === 'tan') value = Math.tan(angleRad);
    else if (func === 'csc') value = 1 / Math.sin(angleRad);
    else if (func === 'sec') value = 1 / Math.cos(angleRad);
    else if (func === 'cot') value = 1 / Math.tan(angleRad);
    
    const paramValue = document.getElementById('param-value');
    if (paramValue) {
      if (isFinite(value) && Math.abs(value) < 1e5) {
        paramValue.textContent = value.toFixed(4);
      } else {
        paramValue.textContent = '∞';
      }
    }
  }
}

/**
 * Stop current simulator
 */
async function stopSimulator() {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  
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
 * Show error message
 */
function showError(message) {
  const overlay = document.getElementById('canvas-overlay');
  overlay.style.display = 'flex';
  document.getElementById('status-text').textContent = message;
  document.getElementById('status-text').style.color = '#ff4444';
}

