/**
 * EduVision Button Component
 * Accessible button with primary/secondary variants
 */

import { createEl } from '../libs/utils.js';

/**
 * Create a button element
 * @param {Object} props - Button properties
 * @param {string} props.text - Button text
 * @param {string} props.variant - 'primary' or 'secondary'
 * @param {string} props.href - Optional link destination
 * @param {Function} props.onClick - Optional click handler
 * @param {string} props.className - Additional CSS classes
 * @param {string} props.ariaLabel - ARIA label for accessibility
 * @returns {HTMLElement}
 */
export function createButton({
  text,
  variant = 'primary',
  href = null,
  onClick = null,
  className = '',
  ariaLabel = null
}) {
  const button = createEl(href ? 'a' : 'button', {
    className: `btn btn-${variant} ${className}`.trim(),
    textContent: text,
    ...(href && { href }),
    ...(ariaLabel && { 'aria-label': ariaLabel }),
    ...(href ? {} : { type: 'button' })
  });
  
  if (onClick && !href) {
    button.addEventListener('click', onClick);
  }
  
  return button;
}

