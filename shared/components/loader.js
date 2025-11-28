/**
 * EduVision Loader Component
 * Subtle glass spinner for async states
 */

import { createEl } from '../libs/utils.js';

/**
 * Create a loader element
 * @param {Object} props - Loader properties
 * @param {string} props.size - 'sm', 'md', 'lg'
 * @param {string} props.className - Additional CSS classes
 * @returns {HTMLElement}
 */
export function createLoader({ size = 'md', className = '' }) {
  const loader = createEl('div', {
    className: `loader loader-${size} ${className}`.trim(),
    'aria-label': 'Loading',
    role: 'status'
  });
  
  const spinner = createEl('div', {
    className: 'loader-spinner'
  });
  
  // Create spinner segments
  for (let i = 0; i < 8; i++) {
    const segment = createEl('div', {
      className: 'loader-segment'
    });
    segment.style.setProperty('--segment-index', i);
    spinner.appendChild(segment);
  }
  
  loader.appendChild(spinner);
  
  return loader;
}

/**
 * Show loader in a container
 * @param {HTMLElement|string} container - Container element or selector
 * @param {Object} options - Loader options
 */
export function showLoader(container, options = {}) {
  const containerEl = typeof container === 'string' 
    ? document.querySelector(container) 
    : container;
  
  if (!containerEl) return null;
  
  const loader = createLoader(options);
  containerEl.appendChild(loader);
  return loader;
}

/**
 * Hide loader
 * @param {HTMLElement} loader - Loader element to remove
 */
export function hideLoader(loader) {
  if (loader && loader.parentNode) {
    loader.remove();
  }
}

