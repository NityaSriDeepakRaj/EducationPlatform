/**
 * EduVision Card Component
 * Reusable subject card with hover effects and accent colors
 */

import { createEl } from '../libs/utils.js';

/**
 * Create a subject card element
 * @param {Object} props - Card properties
 * @param {string} props.title - Card title
 * @param {string} props.accent - Accent color (chemistry, physics, cs, math)
 * @param {string} props.icon - SVG icon string or path
 * @param {string} props.href - Link destination
 * @returns {HTMLElement}
 */
export function createCard({ title, accent, icon, href }) {
  const card = createEl('a', {
    href,
    className: 'subject-card',
    'data-accent': accent,
    'aria-label': `Navigate to ${title}`
  });
  
  // Card content wrapper
  const content = createEl('div', {
    className: 'card-content'
  });
  
  // Icon container
  const iconContainer = createEl('div', {
    className: 'card-icon'
  });
  
  if (icon) {
    if (icon.startsWith('<svg')) {
      iconContainer.innerHTML = icon;
    } else {
      const img = createEl('img', {
        src: icon,
        alt: `${title} icon`,
        loading: 'lazy'
      });
      iconContainer.appendChild(img);
    }
  }
  
  // Title
  const titleEl = createEl('h3', {
    className: 'card-title',
    textContent: title
  });
  
  content.appendChild(iconContainer);
  content.appendChild(titleEl);
  card.appendChild(content);
  
  // Add hover effect with accent color
  card.addEventListener('mouseenter', () => {
    document.documentElement.style.setProperty('--cursor-accent', `var(--${accent})`);
  });
  
  card.addEventListener('mouseleave', () => {
    document.documentElement.style.removeProperty('--cursor-accent');
  });
  
  return card;
}

