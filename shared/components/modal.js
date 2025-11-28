/**
 * EduVision Modal Component
 * Accessible modal with focus trap and keyboard navigation
 */

import { createEl } from '../libs/utils.js';

/**
 * Create a modal element
 * @param {Object} props - Modal properties
 * @param {string} props.title - Modal title
 * @param {HTMLElement|string} props.content - Modal content
 * @param {Function} props.onClose - Close handler
 * @param {string} props.className - Additional CSS classes
 * @returns {HTMLElement}
 */
export function createModal({ title, content, onClose, className = '' }) {
  const overlay = createEl('div', {
    className: 'modal-overlay',
    role: 'dialog',
    'aria-modal': 'true',
    'aria-labelledby': 'modal-title'
  });
  
  const modal = createEl('div', {
    className: `modal ${className}`.trim()
  });
  
  const header = createEl('div', {
    className: 'modal-header'
  });
  
  const titleEl = createEl('h2', {
    id: 'modal-title',
    className: 'modal-title',
    textContent: title
  });
  
  const closeButton = createEl('button', {
    className: 'modal-close',
    'aria-label': 'Close modal',
    type: 'button',
    innerHTML: '<span aria-hidden="true">&times;</span>'
  });
  
  header.appendChild(titleEl);
  header.appendChild(closeButton);
  
  const body = createEl('div', {
    className: 'modal-body'
  });
  
  if (typeof content === 'string') {
    body.innerHTML = content;
  } else if (content instanceof Node) {
    body.appendChild(content);
  }
  
  modal.appendChild(header);
  modal.appendChild(body);
  overlay.appendChild(modal);
  
  // Close handlers
  const close = () => {
    overlay.classList.add('closing');
    setTimeout(() => {
      overlay.remove();
      if (onClose) onClose();
    }, 200);
  };
  
  closeButton.addEventListener('click', close);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) close();
  });
  
  // Keyboard navigation
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      close();
    }
    
    // Focus trap: Tab key
    if (e.key === 'Tab') {
      const focusableElements = modal.querySelectorAll(
        'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
      );
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    }
  };
  
  overlay.addEventListener('keydown', handleKeyDown);
  
  // Focus first focusable element
  setTimeout(() => {
    const firstFocusable = modal.querySelector(
      'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
    if (firstFocusable) firstFocusable.focus();
  }, 100);
  
  return overlay;
}

/**
 * Show a modal
 * @param {Object} props - Modal properties
 */
export function showModal(props) {
  const modal = createModal(props);
  document.body.appendChild(modal);
  document.body.style.overflow = 'hidden';
  
  // Remove overflow lock when modal closes
  const originalClose = props.onClose;
  props.onClose = () => {
    document.body.style.overflow = '';
    if (originalClose) originalClose();
  };
  
  return modal;
}

