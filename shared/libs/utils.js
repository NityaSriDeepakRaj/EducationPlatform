/**
 * EduVision Utility Functions
 * Helper functions for DOM manipulation and common operations
 */

/**
 * Create a DOM element with attributes and children
 * @param {string} tag - HTML tag name
 * @param {Object} attrs - Attributes object (id, class, style, etc.)
 * @param {Array|string} children - Child elements or text content
 * @returns {HTMLElement}
 */
export function createEl(tag, attrs = {}, children = []) {
  const el = document.createElement(tag);
  
  // Set attributes
  Object.entries(attrs).forEach(([key, value]) => {
    if (key === 'className') {
      el.className = value;
    } else if (key === 'textContent') {
      el.textContent = value;
    } else if (key === 'innerHTML') {
      el.innerHTML = value;
    } else if (key.startsWith('data-')) {
      el.setAttribute(key, value);
    } else {
      el.setAttribute(key, value);
    }
  });
  
  // Append children
  if (typeof children === 'string') {
    el.textContent = children;
  } else if (Array.isArray(children)) {
    children.forEach(child => {
      if (typeof child === 'string') {
        el.appendChild(document.createTextNode(child));
      } else if (child instanceof Node) {
        el.appendChild(child);
      }
    });
  } else if (children instanceof Node) {
    el.appendChild(children);
  }
  
  return el;
}

/**
 * Mount a component to a container
 * @param {HTMLElement|string} container - Container element or selector
 * @param {HTMLElement|string} content - Content to mount
 */
export function mount(container, content) {
  const containerEl = typeof container === 'string' 
    ? document.querySelector(container) 
    : container;
  
  if (!containerEl) {
    console.warn('Container not found:', container);
    return;
  }
  
  if (typeof content === 'string') {
    containerEl.innerHTML = content;
  } else if (content instanceof Node) {
    containerEl.innerHTML = '';
    containerEl.appendChild(content);
  }
}

/**
 * Fetch JSON placeholder (for future API integration)
 * @param {string} url - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<Object>}
 */
export async function fetchJSONPlaceholder(url, options = {}) {
  // TODO: Replace with actual API call when backend is integrated
  // This is a placeholder that returns mock data structure
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        status: 'success',
        data: {
          message: 'Placeholder response',
          url,
          timestamp: new Date().toISOString()
        }
      });
    }, 100);
  });
}

/**
 * Navigate to a URL with page transition
 * @param {string} url - Target URL
 * @param {number} delay - Transition delay in ms
 */
export function navigate(url, delay = 200) {
  // Add fade-out transition
  document.body.style.opacity = '0';
  document.body.style.transition = `opacity ${delay}ms ease-out`;
  
  setTimeout(() => {
    window.location.href = url;
  }, delay);
}

/**
 * Get subject accent color
 * @param {string} subject - Subject slug (chemistry, physics, cs, math)
 * @returns {string} CSS variable name
 */
export function getSubjectColor(subject) {
  const colors = {
    chemistry: 'var(--chemistry)',
    physics: 'var(--physics)',
    cs: 'var(--cs)',
    math: 'var(--math)'
  };
  return colors[subject] || 'var(--text-primary)';
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function}
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Check if reduced motion is preferred
 * @returns {boolean}
 */
export function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

