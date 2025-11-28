/**
 * EduVision Chemistry Subject Page Script
 */

import { showModal } from '../../shared/components/modal.js';
import { createEl } from '../../shared/libs/utils.js';

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
  // Gesture Guide Modal
  const gestureGuideBtn = document.getElementById('gesture-guide-btn');
  if (gestureGuideBtn) {
    gestureGuideBtn.addEventListener('click', () => {
      showGestureGuide();
    });
  }

  // Scene Breakdown Collapse
  const collapseBtn = document.querySelector('.collapse-btn');
  const breakdownContent = document.getElementById('breakdown-content');
  
  if (collapseBtn && breakdownContent) {
    collapseBtn.addEventListener('click', () => {
      const isExpanded = collapseBtn.getAttribute('aria-expanded') === 'true';
      breakdownContent.classList.toggle('collapsed', isExpanded);
      collapseBtn.setAttribute('aria-expanded', !isExpanded);
      collapseBtn.textContent = isExpanded ? '+' : '−';
    });
  }

  // TODO: Initialize animation canvas when backend is integrated
  // const canvas = document.getElementById('preview-canvas');
  // initializeAnimationCanvas(canvas);

  // TODO: Connect to gesture controller API
  // connectGestureController('chemistry');
});

/**
 * Show gesture guide modal
 */
function showGestureGuide() {
  const content = createEl('div', {
    className: 'gesture-guide-content'
  });

  const guideHTML = `
    <div class="gesture-guide">
      <h3>Interactive Lab Gesture Controls</h3>
      <p>Use hand gestures to control chemistry experiments:</p>
      
      <div class="gesture-item">
        <div class="gesture-icon">👈</div>
        <div class="gesture-info">
          <strong>Left Hand</strong>
          <p>Control angle or parameter A</p>
        </div>
      </div>
      
      <div class="gesture-item">
        <div class="gesture-icon">👉</div>
        <div class="gesture-info">
          <strong>Right Hand</strong>
          <p>Control velocity or parameter B</p>
        </div>
      </div>
      
      <div class="gesture-item">
        <div class="gesture-icon">✊</div>
        <div class="gesture-info">
          <strong>Pinch Gesture</strong>
          <p>Launch or trigger action</p>
        </div>
      </div>
      
      <div class="gesture-tip">
        <small>💡 Tip: Ensure good lighting and keep hands visible to the camera</small>
      </div>
    </div>
  `;

  content.innerHTML = guideHTML;

  showModal({
    title: 'Gesture Guide',
    content: content,
    onClose: () => {
      console.log('Gesture guide closed');
    }
  });
}

// TODO: Initialize animation canvas
// function initializeAnimationCanvas(canvas) {
//   // This will be integrated with the backend animation engine
//   // Example: const engine = new ChemistryAnimationEngine(canvas);
// }

// TODO: Connect to gesture controller
// async function connectGestureController(subject) {
//   // This will connect to the backend gesture API
//   // Example: const controller = await GestureController.connect(subject);
// }

