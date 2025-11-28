/**
 * Mathematics Text to Animation Script
 */

const API_BASE = 'http://localhost:5000/api/tta';
const SUBJECT = 'maths';

document.addEventListener('DOMContentLoaded', () => {
  const generateBtn = document.getElementById('generate-btn');
  const topicInput = document.getElementById('topic-input');
  const loadingOverlay = document.getElementById('loading-overlay');
  const inputSection = document.getElementById('input-section');
  const previewSection = document.getElementById('preview-section');
  const quizSection = document.getElementById('quiz-section');
  
  generateBtn.addEventListener('click', async () => {
    const topic = topicInput.value.trim();
    if (!topic) {
      alert('Please enter a topic');
      return;
    }
    
    await generateAnimation(topic);
  });
  
  topicInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      generateBtn.click();
    }
  });
});

async function generateAnimation(topic) {
  const loadingOverlay = document.getElementById('loading-overlay');
  const inputSection = document.getElementById('input-section');
  const previewSection = document.getElementById('preview-section');
  const quizSection = document.getElementById('quiz-section');
  
  try {
    // Show loading
    loadingOverlay.style.display = 'flex';
    previewSection.style.display = 'none';
    quizSection.style.display = 'none';
    
    // Call backend
    const response = await fetch(`${API_BASE}/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic: topic,
        subject: SUBJECT
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    }
    
    const data = await response.json();
    
    // Hide input, show preview
    inputSection.style.display = 'none';
    previewSection.style.display = 'block';
    
    // Display results
    displayResults(data);
    
    // Start rendering video
    await renderVideo(data.manim_code, topic);
    
    // Hide loading
    loadingOverlay.style.display = 'none';
    
    // Scroll to preview
    previewSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Parse and display quiz after a delay (to show after animation)
    setTimeout(() => {
      parseAndDisplayQuiz(data.questions);
      quizSection.style.display = 'block';
      quizSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 2000);
    
  } catch (error) {
    console.error('Error generating animation:', error);
    alert('Failed to generate animation. Please check backend connection and try again.');
    loadingOverlay.style.display = 'none';
  }
}

async function renderVideo(manimCode, topic) {
  const videoElement = document.getElementById('animation-video');
  const videoPlaceholder = document.getElementById('video-placeholder');
  
  if (!manimCode || manimCode.startsWith('# Error')) {
    videoPlaceholder.innerHTML = '<p>⚠️ Manim code not available. Please try again.</p>';
    return;
  }
  
  // Start rendering
  try {
    const response = await fetch(`${API_BASE}/render-video`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        manim_code: manimCode,
        topic: topic
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      const videoPath = data.video_path;
      
      // Show rendering message
      videoPlaceholder.innerHTML = '<p>🎬 Rendering animation video...</p><p style="font-size: 0.9em; margin-top: 0.5rem; opacity: 0.7;">This may take a few minutes. The video will appear here when ready.</p>';
      
      // Poll for video availability
      const pollInterval = setInterval(async () => {
        try {
          const videoResponse = await fetch(`http://localhost:5000${videoPath}`);
          if (videoResponse.ok) {
            // Video is ready
            clearInterval(pollInterval);
            videoPlaceholder.style.display = 'none';
            videoElement.src = `http://localhost:5000${videoPath}`;
            videoElement.style.display = 'block';
            videoElement.load();
          }
        } catch (error) {
          // Video not ready yet, continue polling
        }
      }, 3000); // Poll every 3 seconds
      
      // Stop polling after 5 minutes
      setTimeout(() => {
        clearInterval(pollInterval);
        if (videoPlaceholder.style.display !== 'none') {
          videoPlaceholder.innerHTML = '<p>⏳ Video is still rendering...</p><p style="font-size: 0.9em; margin-top: 0.5rem; opacity: 0.7;">Check the backend console for progress. The page will auto-update when ready.</p>';
        }
      }, 300000); // 5 minutes
    }
  } catch (error) {
    console.error('Error rendering video:', error);
    videoPlaceholder.innerHTML = '<p>⚠️ Could not start video rendering. Check backend logs.</p>';
  }
}

function displayResults(data) {
  console.log('Displaying results:', data);
  
  // Display summary
  const summaryContent = document.getElementById('summary-content');
  summaryContent.textContent = data.summary || 'No summary available';
  
  // Display audio if available
  const audioPlayer = document.getElementById('audio-player');
  if (data.audio) {
    audioPlayer.src = data.audio;
    audioPlayer.style.display = 'block';
  } else {
    audioPlayer.style.display = 'none';
  }
}

function parseAndDisplayQuiz(questionsText) {
  const quizContainer = document.getElementById('quiz-container');
  quizContainer.innerHTML = '';
  
  if (!questionsText || questionsText.startsWith('Error')) {
    quizContainer.innerHTML = '<p>No questions available.</p>';
    return;
  }
  
  // Parse MCQ questions from text format
  // Format: "1) Question?\nA) Option\nB) Option\nC) Option\nD) Option\nAnswer: X"
  const questionBlocks = questionsText.split(/\n(?=\d+\))/);
  
  questionBlocks.forEach((block, index) => {
    if (!block.trim()) return;
    
    const lines = block.trim().split('\n').filter(l => l.trim());
    if (lines.length < 6) return; // Need question + 4 options + answer
    
    // Extract question
    const questionMatch = lines[0].match(/^\d+\)\s*(.+)/);
    if (!questionMatch) return;
    const questionText = questionMatch[1];
    
    // Extract options
    const options = [];
    for (let i = 1; i < 5; i++) {
      const optionMatch = lines[i]?.match(/^([A-D])\)\s*(.+)/);
      if (optionMatch) {
        options.push({
          letter: optionMatch[1],
          text: optionMatch[2]
        });
      }
    }
    
    // Extract answer
    const answerMatch = lines.find(l => l.includes('Answer:'))?.match(/Answer:\s*([A-D])/i);
    const correctAnswer = answerMatch ? answerMatch[1].toUpperCase() : null;
    
    if (!correctAnswer || options.length < 4) return;
    
    // Create question card
    const questionCard = document.createElement('div');
    questionCard.className = 'quiz-question';
    questionCard.innerHTML = `
      <div class="question-text">${index + 1}. ${questionText}</div>
      <div class="options-container">
        ${options.map(opt => `
          <button class="option-btn" data-letter="${opt.letter}" data-question="${index}">
            ${opt.letter}) ${opt.text}
          </button>
        `).join('')}
      </div>
      <div class="answer-feedback" id="feedback-${index}"></div>
    `;
    
    quizContainer.appendChild(questionCard);
    
    // Add click handlers
    const optionButtons = questionCard.querySelectorAll('.option-btn');
    optionButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const selectedLetter = btn.dataset.letter;
        const questionIndex = parseInt(btn.dataset.question);
        const feedback = document.getElementById(`feedback-${questionIndex}`);
        
        // Disable all buttons for this question
        optionButtons.forEach(b => b.disabled = true);
        
        // Show feedback
        if (selectedLetter === correctAnswer) {
          btn.classList.add('correct');
          feedback.textContent = '✅ Correct!';
          feedback.className = 'answer-feedback correct show';
        } else {
          btn.classList.add('incorrect');
          // Highlight correct answer
          optionButtons.forEach(b => {
            if (b.dataset.letter === correctAnswer) {
              b.classList.add('correct');
            }
          });
          feedback.textContent = `❌ Incorrect. The correct answer is ${correctAnswer}.`;
          feedback.className = 'answer-feedback incorrect show';
        }
      });
    });
  });
}
