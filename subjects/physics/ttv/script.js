/**
 * Physics Text to Animation Script
 */

import { showModal } from '../../../shared/components/modal.js';

const API_BASE = 'http://localhost:5000/api/tta';
const SUBJECT = 'physics';

let videoModal = null;

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
    
    // Display results (summary)
    displayResults(data);
    
    // IMMEDIATELY play audio automatically after generation
    // User just clicked button, so autoplay should work
    playAudioAutomatically(topic);
    
    // Video is already being rendered by backend automatically!
    // Just show the modal and poll for the video
    const videoPath = data.video_path || `/api/tta/video/${topic.replace(/[^A-Za-z0-9_]/g, '_')}`;
    showVideoModalAndPoll(topic, videoPath);
    
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

function playAudioAutomatically(topic) {
  // Generate the expected filename from topic (same as backend does)
  const safeTopic = topic.replace(/[^A-Za-z0-9_]/g, '_');
  const audioFilename = `${safeTopic}.mp3`;
  const audioUrl = `http://localhost:5000/temp_audio/${audioFilename}`;
  
  console.log('🎵🎵🎵 Playing audio automatically:', audioUrl);
  
  // Get the audio player element
  const audioPlayer = document.getElementById('audio-player');
  if (!audioPlayer) {
    console.error('❌ Audio player element not found!');
    return;
  }
  
  // Wait a moment for file to be fully written (backend just created it)
  setTimeout(() => {
    // Set the source
    audioPlayer.src = audioUrl;
    audioPlayer.volume = 1.0;
    
    // Function to play audio - called multiple times to ensure it plays
    const playAudio = () => {
      try {
        const playPromise = audioPlayer.play();
        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              console.log('✅✅✅✅✅ AUDIO IS NOW PLAYING AUTOMATICALLY!');
            })
            .catch(err => {
              console.log('⚠️ Play attempt:', err.name);
            });
        }
      } catch (err) {
        console.log('⚠️ Play error:', err);
      }
    };
    
    // Set up event listeners for when audio is ready
    const handleCanPlay = () => {
      console.log('✅ Audio ready - playing now!');
      playAudio();
    };
    
    audioPlayer.addEventListener('canplay', handleCanPlay, { once: true });
    
    audioPlayer.addEventListener('canplaythrough', () => {
      console.log('✅ Audio can play through - playing now!');
      playAudio();
    }, { once: true });
    
    audioPlayer.addEventListener('loadeddata', () => {
      console.log('✅ Audio data loaded - playing now!');
      playAudio();
    }, { once: true });
    
    // Load the audio (this triggers the events)
    audioPlayer.load();
    
    // Try playing immediately (user just clicked, so autoplay should work)
    playAudio();
    
    // Retry attempts - user interaction context is still valid
    setTimeout(playAudio, 500);
    setTimeout(playAudio, 1000);
    setTimeout(playAudio, 2000);
  }, 800); // Wait 800ms for file to be fully written
}

function showVideoModalAndPoll(topic, videoPath) {
  // Create video modal content
  const videoContainer = document.createElement('div');
  videoContainer.className = 'video-modal-container';
  videoContainer.innerHTML = `
    <video id="animation-video" controls autoplay style="display: none;">
      Your browser does not support the video tag.
    </video>
    <div class="video-placeholder" id="video-placeholder">
      <p>🎬 Rendering animation video...</p>
      <p style="font-size: 0.9em; margin-top: 0.5rem; opacity: 0.7;">Video is being rendered automatically. This may take a few minutes. The video will appear here when ready.</p>
      <div class="render-progress">
        <div class="progress-bar"></div>
      </div>
    </div>
  `;
  
  // Show modal immediately
  videoModal = showModal({
    title: `Animation: ${topic}`,
    content: videoContainer,
    className: 'video-modal',
    onClose: () => {
      videoModal = null;
      // Pause video when modal closes
      const video = document.getElementById('animation-video');
      if (video) {
        video.pause();
      }
    }
  });
  
  console.log('✅ Video modal opened, polling for video at:', videoPath);
  
  // Get video elements from modal
  const modalVideo = videoContainer.querySelector('#animation-video');
  const modalPlaceholder = videoContainer.querySelector('#video-placeholder');
  
  // Poll for video availability (backend is already rendering!)
  let pollCount = 0;
  const pollInterval = setInterval(async () => {
    pollCount++;
    try {
      const videoResponse = await fetch(`http://localhost:5000${videoPath}`);
      if (videoResponse.ok) {
        // Video is ready!
        clearInterval(pollInterval);
        modalPlaceholder.style.display = 'none';
        modalVideo.src = `http://localhost:5000${videoPath}`;
        modalVideo.style.display = 'block';
        modalVideo.load();
        modalVideo.play().catch(err => {
          console.log('Video autoplay prevented:', err);
        });
        console.log(`✅✅✅ Video loaded successfully after ${pollCount} polls!`);
      } else {
        if (pollCount % 10 === 0) { // Log every 10 polls to avoid spam
          console.log(`Poll ${pollCount}: Video not ready yet (${videoResponse.status}) - still rendering...`);
        }
      }
    } catch (error) {
      // Video not ready yet, continue polling
      if (pollCount % 10 === 0) {
        console.log(`Poll ${pollCount}: Video not ready yet, continuing...`);
      }
    }
  }, 3000); // Poll every 3 seconds
  
  // Stop polling after 10 minutes
  setTimeout(() => {
    clearInterval(pollInterval);
    if (modalPlaceholder && modalPlaceholder.style.display !== 'none') {
      modalPlaceholder.innerHTML = '<p>⏳ Video is still rendering...</p><p style="font-size: 0.9em; margin-top: 0.5rem; opacity: 0.7;">Check the backend console for progress. The page will auto-update when ready.</p>';
    }
  }, 600000); // 10 minutes
}

function displayResults(data) {
  console.log('Displaying results:', data);
  
  // Display summary
  const summaryContent = document.getElementById('summary-content');
  summaryContent.textContent = data.summary || 'No summary available';
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
