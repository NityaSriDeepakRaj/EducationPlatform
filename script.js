/**
 * EduVision Landing Page Script
 * Main entry point for index.html
 */

import { createCard } from './shared/components/card.js';

// Subject data
const subjects = [
  {
    title: 'Chemistry',
    slug: 'chemistry',
    accent: 'chemistry',
    icon: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="30" r="15" fill="currentColor"/>
      <path d="M 50 45 L 30 85 L 70 85 Z" fill="currentColor"/>
      <circle cx="50" cy="50" r="3" fill="var(--bg-primary)"/>
    </svg>`
  },
  {
    title: 'Physics',
    slug: 'physics',
    accent: 'physics',
    icon: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="25" fill="none" stroke="currentColor" stroke-width="3"/>
      <path d="M 50 25 L 50 50 L 65 65" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
      <circle cx="50" cy="50" r="3" fill="currentColor"/>
    </svg>`
  },
  {
    title: 'Computer Science',
    slug: 'computer-science',
    accent: 'cs',
    icon: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <rect x="20" y="25" width="60" height="45" rx="5" fill="none" stroke="currentColor" stroke-width="3"/>
      <rect x="25" y="30" width="50" height="35" fill="currentColor" opacity="0.3"/>
      <rect x="15" y="70" width="70" height="8" rx="4" fill="currentColor"/>
      <rect x="40" y="78" width="20" height="4" rx="2" fill="currentColor"/>
    </svg>`
  },
  {
    title: 'Mathematics',
    slug: 'maths',
    accent: 'math',
    icon: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <path d="M 30 30 L 50 50 L 70 30" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 30 70 L 50 50 L 70 70" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`
  }
];

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
  const grid = document.querySelector('.subjects-grid');
  
  if (!grid) {
    console.error('Subjects grid not found');
    return;
  }
  
  // Create and append subject cards
  subjects.forEach(subject => {
    const card = createCard({
      title: subject.title,
      accent: subject.accent,
      icon: subject.icon,
      href: `subjects/${subject.slug}/index.html`
    });
    
    grid.appendChild(card);
  });
  
  // Handle navigation button clicks (placeholders)
  const askQuestionBtn = document.querySelector('a[href="#ask-question"]');
  const interactiveLabBtn = document.querySelector('a[href="#interactive-lab"]');
  
  if (askQuestionBtn) {
    askQuestionBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // TODO: Route to question interface when backend is integrated
      console.log('Ask a Question clicked');
    });
  }
  
  if (interactiveLabBtn) {
    interactiveLabBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // TODO: Route to interactive lab selection when backend is integrated
      console.log('Interactive Lab clicked');
    });
  }
  
  // Add page transition on load
  document.body.style.opacity = '0';
  requestAnimationFrame(() => {
    document.body.style.transition = 'opacity 200ms ease-in';
    document.body.style.opacity = '1';
  });
});

