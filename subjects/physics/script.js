/**
 * EduVision Physics Subject Page Script
 */

import { showModal } from '../../shared/components/modal.js';
import { createEl } from '../../shared/libs/utils.js';

const API_BASE = 'http://localhost:5000/api/tta';

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀🚀🚀 PAGE LOADED - INITIALIZING...');
  
  // TEST: Add visible indicator that script loaded
  const testDiv = document.createElement('div');
  testDiv.id = 'script-test';
  testDiv.style.cssText = 'position: fixed; top: 10px; right: 10px; background: green; color: white; padding: 10px; z-index: 9999; border-radius: 5px; font-size: 12px;';
  testDiv.textContent = '✅ Script Loaded!';
  document.body.appendChild(testDiv);
  
  setTimeout(() => {
    const el = document.getElementById('script-test');
    if (el) el.remove();
  }, 3000);
  
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

  // Generate Button - CRITICAL SETUP
  const generateBtn = document.getElementById('generate-btn');
  const topicInput = document.getElementById('topic-input');
  
  console.log('🔍 Checking generate button:', generateBtn);
  console.log('🔍 Checking topic input:', topicInput);
  console.log('🔍 Checking audio box:', document.getElementById('audio-box-content'));
  console.log('🔍 Checking summary box:', document.getElementById('summary-box-content'));
  console.log('🔍 Checking MCQ box:', document.getElementById('mcq-box-content'));
  
  if (generateBtn && topicInput) {
    console.log('✅✅✅ Generate button and input found, adding listeners');
    
    // Remove any existing listeners
    const newGenerateBtn = generateBtn.cloneNode(true);
    generateBtn.parentNode.replaceChild(newGenerateBtn, generateBtn);
    
    newGenerateBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const topic = topicInput.value.trim();
      console.log('🎯🎯🎯 Generate button clicked, topic:', topic);
      
      if (!topic) {
        alert('Please enter a topic');
        return;
      }
      
      // Show immediate visual feedback
      let feedback = document.getElementById('generating-feedback');
      if (!feedback) {
        feedback = document.createElement('div');
        feedback.id = 'generating-feedback';
        feedback.style.cssText = 'position: fixed; top: 50px; right: 10px; background: #FFAA00; color: white; padding: 15px; z-index: 9999; border-radius: 5px; font-weight: bold;';
        document.body.appendChild(feedback);
      }
      feedback.textContent = '🔄 Generating...';
      feedback.style.display = 'block';
      
      console.log('🚀🚀🚀 Starting content generation...');
      
      try {
        await generateContent(topic);
        feedback.textContent = '✅ Generated!';
        feedback.style.background = 'green';
        setTimeout(() => {
          if (feedback) feedback.style.display = 'none';
        }, 2000);
      } catch (error) {
        feedback.textContent = '❌ Error!';
        feedback.style.background = 'red';
        setTimeout(() => {
          if (feedback) feedback.style.display = 'none';
        }, 3000);
      }
    });

    topicInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        console.log('⏎ Enter key pressed');
        newGenerateBtn.click();
      }
    });
    
    console.log('✅✅✅ Event listeners attached!');
  } else {
    console.error('❌❌❌ Generate button or topic input not found!');
    console.error('Generate button:', generateBtn);
    console.error('Topic input:', topicInput);
  }

  // TODO: Initialize animation canvas when backend is integrated
  // const canvas = document.getElementById('preview-canvas');
  // initializeAnimationCanvas(canvas);

  // TODO: Connect to gesture controller API
  // connectGestureController('physics');
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
      <p>Use hand gestures to control physics simulations:</p>
      
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
//   // Example: const engine = new PhysicsAnimationEngine(canvas);
// }

// TODO: Connect to gesture controller
// async function connectGestureController(subject) {
//   // This will connect to the backend gesture API
//   // Example: const controller = await GestureController.connect(subject);
// }

/**
 * Generate content for the three boxes (Audio, Summary, MCQ)
 */
async function generateContent(topic) {
  const generateBtn = document.getElementById('generate-btn');
  const originalText = generateBtn ? generateBtn.textContent : 'Generate';
  
  try {
    console.log('📝 generateContent called with topic:', topic);
    
    // Show loading state
    if (generateBtn) {
      generateBtn.disabled = true;
      generateBtn.textContent = 'Generating...';
    }
    
    // Clear previous content
    console.log('🧹 Clearing previous content...');
    clearBoxes();
    
    // Call backend API
    console.log('🌐 Calling API:', `${API_BASE}/process`);
    const response = await fetch(`${API_BASE}/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic: topic,
        subject: 'physics'
      })
    });
    
    console.log('📡 Response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ API Error:', response.status, errorText);
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('✅✅✅ API Response received:', {
      hasSummary: !!data.summary,
      hasAudio: !!data.audio,
      hasQuestions: !!data.questions,
      summaryLength: data.summary?.length || 0,
      questionsLength: data.questions?.length || 0,
      summaryPreview: data.summary?.substring(0, 50),
      questionsPreview: data.questions?.substring(0, 50),
      audioUrl: data.audio_url,
      audioFilename: data.audio_filename
    });
    
    // Validate data before populating
    if (!data.summary || data.summary.trim().length === 0) {
      console.warn('⚠️ Summary is empty or missing');
    }
    if (!data.questions || data.questions.trim().length === 0) {
      console.warn('⚠️ Questions are empty or missing');
    }
    if (!data.audio && !data.audio_url && !data.audio_filename) {
      console.warn('⚠️ No audio data available');
    }
    
    // Populate the three boxes with real-time data IMMEDIATELY
    console.log('📦📦📦 Populating boxes NOW...');
    console.log('📦 Data received:', {
      hasSummary: !!data.summary,
      hasAudio: !!data.audio,
      hasAudioUrl: !!data.audio_url,
      hasAudioFilename: !!data.audio_filename,
      hasQuestions: !!data.questions
    });
    
    // Populate immediately - NO DELAY
    try {
      populateSummaryBox(data.summary || 'No summary available');
      console.log('✅ Summary box populated');
    } catch (e) {
      console.error('❌ Error populating summary:', e);
    }
    
    try {
      populateMCQBox(data.questions || 'No questions available');
      console.log('✅ MCQ box populated');
    } catch (e) {
      console.error('❌ Error populating MCQ:', e);
    }
    
    try {
      populateAudioBox(topic, data.audio, data.audio_url, data.audio_filename);
      console.log('✅ Audio box populated');
    } catch (e) {
      console.error('❌ Error populating audio:', e);
    }
    
    // Start polling for video and display in preview box
    if (data.video_path) {
      console.log('🎬 Starting video polling for:', data.video_path);
      pollAndDisplayVideo(data.video_path, topic);
    }
    
    console.log('✅✅✅ All boxes populated immediately!');
    
  } catch (error) {
    console.error('❌ Error generating content:', error);
    alert(`Failed to generate content: ${error.message}\n\nPlease check:\n1. Backend server is running on http://localhost:5000\n2. Check browser console for details`);
  } finally {
    if (generateBtn) {
      generateBtn.disabled = false;
      generateBtn.textContent = originalText;
    }
  }
}

/**
 * Populate Audio Box
 */
function populateAudioBox(topic, audioData, audioUrl, audioFilename) {
  console.log('🔊🔊🔊 populateAudioBox called with topic:', topic);
  console.log('🔊 Audio data exists:', !!audioData);
  console.log('🔊 Audio URL:', audioUrl);
  console.log('🔊 Audio filename:', audioFilename);
  
  const audioBoxContent = document.getElementById('audio-box-content');
  
  if (!audioBoxContent) {
    console.error('❌❌❌ audio-box-content not found!');
    return;
  }
  
  // COMPLETELY REPLACE THE CONTENT with status and player
  audioBoxContent.innerHTML = `
    <div id="audio-status" style="margin-bottom: 8px; padding: 8px; background: rgba(255, 170, 0, 0.1); border-radius: 4px; font-size: 14px; color: #FFAA00;">
      🎵 Preparing audio...
    </div>
    <div class="audio-player-container" style="display: none; width: 100%; margin-bottom: 8px;">
      <audio id="physics-audio-player" controls style="width: 100%; display: block; height: 40px;">
        Your browser does not support the audio element.
      </audio>
    </div>
    <div id="audio-download" style="display: none; margin-top: 8px;">
      <a id="audio-download-link" href="#" download style="color: #FFAA00; text-decoration: none; font-size: 14px;">⬇️ Download Audio</a>
    </div>
  `;
  
  const audioStatus = document.getElementById('audio-status');
  const audioPlayer = document.getElementById('physics-audio-player');
  const audioContainer = audioBoxContent.querySelector('.audio-player-container');
  const audioDownload = document.getElementById('audio-download');
  const audioDownloadLink = document.getElementById('audio-download-link');
  
  // Function to set audio source and play
  const setAudioAndPlay = (audioSource) => {
    if (!audioPlayer) {
      console.error('❌ Audio player not found!');
      return;
    }
    
    audioPlayer.src = audioSource;
    audioPlayer.load();
    
    console.log('✅✅✅ Audio player configured, src:', audioPlayer.src);
    
    // Show player
    if (audioContainer) {
      audioContainer.style.display = 'block';
    }
    
    // Update status
    if (audioStatus) {
      audioStatus.textContent = '✅ Audio ready to play';
      audioStatus.style.background = 'rgba(0, 255, 0, 0.1)';
      audioStatus.style.color = '#00ff00';
    }
    
    // Show download link (use the audioUrl parameter from outer scope)
    if (audioDownload && audioDownloadLink) {
      const downloadUrl = audioUrl ? `http://localhost:5000${audioUrl}` : audioSource;
      audioDownload.style.display = 'block';
      audioDownloadLink.href = downloadUrl;
      audioDownloadLink.download = audioFilename || 'audio.mp3';
    }
    
    // Try to play automatically
    setTimeout(() => {
      audioPlayer.play().catch(err => {
        console.log('⚠️ Audio autoplay prevented:', err);
        if (audioStatus) {
          audioStatus.textContent = '▶️ Click play button to start audio';
          audioStatus.style.background = 'rgba(255, 170, 0, 0.1)';
          audioStatus.style.color = '#FFAA00';
        }
      });
    }, 1000);
    
    // Also try when audio is ready
    audioPlayer.addEventListener('canplay', () => {
      console.log('✅ Audio can play, attempting playback');
      audioPlayer.play().catch(() => {});
    }, { once: true });
  };
  
  // Priority 1: Use base64 audio data if available (immediate)
  if (audioData && audioData.startsWith('data:audio')) {
    console.log('✅ Using base64 audio data');
    setAudioAndPlay(audioData);
    return;
  }
  
  // Priority 2: Use audio_url if provided
  if (audioUrl) {
    const fullAudioUrl = `http://localhost:5000${audioUrl}`;
    console.log('✅ Using audio URL:', fullAudioUrl);
    
    // Try immediately first (file might already be ready)
    fetch(fullAudioUrl, { method: 'HEAD' })
      .then(response => {
        if (response.ok) {
          console.log('✅ Audio file is ready immediately!');
          setAudioAndPlay(fullAudioUrl);
        } else {
          // If not ready, start polling
          console.log('⏳ Audio file not ready yet, starting to poll...');
          pollForAudio(fullAudioUrl);
        }
      })
      .catch(error => {
        console.log('⏳ Error on immediate check, starting to poll...', error);
        pollForAudio(fullAudioUrl);
      });
    
    // Poll function
    const pollForAudio = (url) => {
      let pollCount = 0;
      const maxPolls = 30; // 15 seconds max (30 * 500ms)
      const pollInterval = setInterval(async () => {
        pollCount++;
        try {
          const response = await fetch(url, { method: 'HEAD' });
          if (response.ok) {
            clearInterval(pollInterval);
            console.log('✅ Audio file is ready after polling!');
            setAudioAndPlay(url);
          } else if (pollCount >= maxPolls) {
            clearInterval(pollInterval);
            console.error('❌ Audio file not available after polling');
            if (audioStatus) {
              audioStatus.textContent = '❌ Audio file not found. Please try again.';
              audioStatus.style.background = 'rgba(255, 0, 0, 0.1)';
              audioStatus.style.color = '#ff0000';
            }
          } else {
            // Update status during polling
            if (audioStatus && pollCount % 4 === 0) {
              audioStatus.textContent = `🎵 Preparing audio... (${pollCount}/${maxPolls})`;
            }
          }
        } catch (error) {
          if (pollCount >= maxPolls) {
            clearInterval(pollInterval);
            console.error('❌ Error polling for audio:', error);
            if (audioStatus) {
              audioStatus.textContent = '❌ Error loading audio. Please check backend connection.';
              audioStatus.style.background = 'rgba(255, 0, 0, 0.1)';
              audioStatus.style.color = '#ff0000';
            }
          }
        }
      }, 500); // Poll every 500ms
    };
    
    return;
  }
  
  // Priority 3: Fallback to topic-based filename
  const safeTopic = topic.replace(/[^A-Za-z0-9_]/g, '_');
  const fallbackUrl = `http://localhost:5000/temp_audio/${safeTopic}.mp3`;
  console.log('⚠️ Using fallback audio URL:', fallbackUrl);
  setAudioAndPlay(fallbackUrl);
}

/**
 * Populate Summary Box
 */
function populateSummaryBox(summary) {
  console.log('📄📄📄 populateSummaryBox called, summary length:', summary?.length || 0);
  
  const summaryBoxContent = document.getElementById('summary-box-content');
  
  if (!summaryBoxContent) {
    console.error('❌❌❌ summary-box-content not found!');
    return;
  }
  
  // Remove placeholder
  const placeholder = summaryBoxContent.querySelector('.box-placeholder');
  if (placeholder) {
    placeholder.remove();
  }
  
  console.log('📄 Summary text preview:', summary?.substring(0, 100) + '...');
  
  // COMPLETELY REPLACE THE CONTENT - FORCE VISIBLE
  if (summary && summary.trim() && !summary.startsWith('Error')) {
    // Escape HTML but preserve line breaks
    const escapedSummary = summary
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');
    
    summaryBoxContent.innerHTML = `<div style="margin: 0 !important; padding: 12px !important; color: #FFFFFF !important; line-height: 1.8 !important; white-space: pre-wrap !important; word-wrap: break-word !important; font-size: 16px !important; display: block !important; visibility: visible !important; opacity: 1 !important;">${escapedSummary}</div>`;
    console.log('✅✅✅ Summary HTML set, length:', summaryBoxContent.innerHTML.length);
  } else {
    console.log('⚠️ No summary available or error');
    summaryBoxContent.innerHTML = '<p style="color: #FFFFFF !important; text-align: center !important; padding: 20px !important; display: block !important; visibility: visible !important;">No summary available. Please try again.</p>';
  }
  
  // Force visibility
  summaryBoxContent.style.display = 'block';
  summaryBoxContent.style.visibility = 'visible';
  summaryBoxContent.style.opacity = '1';
  
  console.log('✅ Summary box updated successfully');
}

/**
 * Populate MCQ Box
 */
function populateMCQBox(questionsText) {
  const mcqBoxContent = document.getElementById('mcq-box-content');
  
  if (!mcqBoxContent) {
    console.error('MCQ box element not found');
    return;
  }
  
  console.log('❓ Populating MCQ questions:', questionsText?.substring(0, 100) + '...');
  
  // Remove placeholder
  const mcqPlaceholder = mcqBoxContent.querySelector('.box-placeholder');
  if (mcqPlaceholder) {
    mcqPlaceholder.remove();
  }
  
  if (!questionsText || questionsText.trim().length === 0 || questionsText.startsWith('Error')) {
    mcqBoxContent.innerHTML = '<p style="color: #FFFFFF !important; text-align: center !important; padding: 20px !important; display: block !important;">No questions available. Please try again.</p>';
    return;
  }
  
  // Parse MCQ questions from text format
  // Format: "1) Question?\nA) Option\nB) Option\nC) Option\nD) Option\nAnswer: X"
  // Try multiple parsing strategies
  let questionBlocks = questionsText.split(/\n(?=\d+\))/);
  
  // If that doesn't work, try splitting by double newlines
  if (questionBlocks.length === 1) {
    questionBlocks = questionsText.split(/\n\n+/);
  }
  
  // If still doesn't work, try splitting by "Answer:" pattern
  if (questionBlocks.length === 1) {
    questionBlocks = questionsText.split(/(?=Answer:)/);
  }
  
  console.log('📊 Found question blocks:', questionBlocks.length);
  console.log('📊 First block preview:', questionBlocks[0]?.substring(0, 200));
  
  // FORCE CLEAR
  mcqBoxContent.innerHTML = '';
  mcqBoxContent.style.display = 'flex';
  mcqBoxContent.style.flexDirection = 'column';
  mcqBoxContent.style.gap = 'var(--spacing-md)';
  
  let questionCount = 0;
  
  questionBlocks.forEach((block, index) => {
    if (!block || !block.trim()) return;
    
    const lines = block.trim().split('\n').filter(l => l.trim());
    console.log(`📋 Block ${index} has ${lines.length} lines`);
    
    if (lines.length < 3) {
      console.log(`⚠️ Block ${index} too short, skipping`);
      return;
    }
    
    // Extract question - try multiple patterns
    let questionText = null;
    let questionMatch = lines[0].match(/^\d+\)\s*(.+)/);
    if (!questionMatch) {
      questionMatch = lines[0].match(/^Question\s*\d+[:.]?\s*(.+)/i);
    }
    if (!questionMatch) {
      // Just take the first line as question if it doesn't match patterns
      questionText = lines[0].replace(/^\d+\)\s*/, '').replace(/^Question\s*\d+[:.]?\s*/i, '');
    } else {
      questionText = questionMatch[1];
    }
    
    if (!questionText || !questionText.trim()) {
      console.log(`⚠️ Block ${index} - no question text found`);
      return;
    }
    
    // Extract options - look for A), B), C), D) patterns
    const options = [];
    for (let i = 0; i < lines.length; i++) {
      const optionMatch = lines[i]?.match(/^([A-D])[\)\.]\s*(.+)/i);
      if (optionMatch) {
        options.push({
          letter: optionMatch[1].toUpperCase(),
          text: optionMatch[2].trim()
        });
      }
    }
    
    // Extract answer - look for "Answer:" pattern
    let correctAnswer = null;
    const answerLine = lines.find(l => l.toLowerCase().includes('answer'));
    if (answerLine) {
      const answerMatch = answerLine.match(/answer[:.]?\s*([A-D])/i);
      if (answerMatch) {
        correctAnswer = answerMatch[1].toUpperCase();
      }
    }
    
    console.log(`❓ Question ${index + 1}: "${questionText.substring(0, 40)}..."`);
    console.log(`   Options found: ${options.length}`);
    console.log(`   Correct answer: ${correctAnswer}`);
    
    if (!correctAnswer) {
      console.log(`⚠️ Question ${index + 1} has no correct answer, skipping`);
      return;
    }
    
    if (options.length < 2) {
      console.log(`⚠️ Question ${index + 1} has too few options (${options.length}), skipping`);
      return;
    }
    
    questionCount++;
    
    // Create question card - FORCE VISIBLE WITH INLINE STYLES
    const escapedQuestion = questionText.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const escapedOptions = options.map(opt => ({
      letter: opt.letter,
      text: opt.text.replace(/</g, '&lt;').replace(/>/g, '&gt;'),
      isCorrect: opt.letter === correctAnswer
    }));
    
    const questionCard = document.createElement('div');
    questionCard.style.cssText = 'padding: 16px !important; background: rgba(0, 0, 0, 0.2) !important; border-radius: 8px !important; border-left: 3px solid #FFAA00 !important; margin-bottom: 12px !important; display: block !important; visibility: visible !important; opacity: 1 !important;';
    questionCard.innerHTML = `
      <div style="color: #FFFFFF !important; font-weight: 600 !important; margin-bottom: 12px !important; font-size: 16px !important; display: block !important; visibility: visible !important;">${questionCount}. ${escapedQuestion}</div>
      <div style="display: flex !important; flex-direction: column !important; gap: 8px !important;">
        ${escapedOptions.map(opt => `
          <div class="mcq-option" data-letter="${opt.letter}" data-correct="${opt.isCorrect}" style="color: #FFFFFF !important; padding: 8px 16px !important; background: rgba(255, 255, 255, 0.05) !important; border-radius: 4px !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; cursor: pointer !important; display: block !important; visibility: visible !important; opacity: 1 !important;">
            ${opt.letter}) ${opt.text}
          </div>
        `).join('')}
      </div>
    `;
    
    mcqBoxContent.appendChild(questionCard);
    console.log(`✅✅✅ Question ${questionCount} added to DOM, HTML length:`, questionCard.innerHTML.length);
    
    // Add click handlers
    const optionElements = questionCard.querySelectorAll('.mcq-option');
    optionElements.forEach(opt => {
      opt.addEventListener('click', () => {
        const isCorrect = opt.dataset.correct === 'true';
        const selectedLetter = opt.dataset.letter;
        
        // Disable all options for this question
        optionElements.forEach(o => {
          o.style.pointerEvents = 'none';
          if (o.dataset.correct === 'true') {
            o.classList.add('correct');
          } else if (o === opt && !isCorrect) {
            o.classList.add('incorrect');
          }
        });
        
        // Show feedback
        const feedback = document.createElement('div');
        feedback.style.marginTop = 'var(--spacing-xs)';
        feedback.style.padding = 'var(--spacing-xs)';
        feedback.style.borderRadius = 'var(--radius-sm)';
        feedback.style.fontSize = 'var(--font-size-sm)';
        
        if (isCorrect) {
          feedback.textContent = '✅ Correct!';
          feedback.style.background = 'rgba(0, 255, 0, 0.15)';
          feedback.style.color = '#00ff00';
        } else {
          feedback.textContent = `❌ Incorrect. The correct answer is ${correctAnswer}.`;
          feedback.style.background = 'rgba(255, 0, 0, 0.15)';
          feedback.style.color = '#ff0000';
        }
        
        questionCard.appendChild(feedback);
      });
    });
  });
  
  if (questionCount === 0) {
    console.log('⚠️ No questions parsed, showing raw text');
    // Show raw text so user can see what was received
    const rawText = questionsText.substring(0, 500);
    mcqBoxContent.innerHTML = `<div style="padding: 16px; color: #FFFFFF !important; background: rgba(255, 0, 0, 0.1); border: 1px solid red; border-radius: 8px;">
      <p style="color: #FFFFFF !important; font-weight: 600; margin-bottom: 8px;">Could not parse questions. Showing raw text:</p>
      <pre style="color: #FFFFFF !important; white-space: pre-wrap; font-size: 12px;">${rawText}</pre>
    </div>`;
  } else {
    console.log(`✅✅✅ Successfully loaded ${questionCount} questions!`);
    // Force visibility
    mcqBoxContent.style.display = 'flex';
    mcqBoxContent.style.visibility = 'visible';
    mcqBoxContent.style.opacity = '1';
  }
}

/**
 * Clear all boxes
 */
/**
 * Poll for video and display in animation preview box
 */
function pollAndDisplayVideo(videoPath, topic) {
  console.log('🎬🎬🎬 Starting video polling...');
  
  const previewCanvas = document.getElementById('preview-canvas');
  if (!previewCanvas) {
    console.error('❌ preview-canvas not found!');
    return;
  }
  
  // Replace placeholder with loading message
  previewCanvas.innerHTML = `
    <div style="text-align: center; color: #FFAA00; padding: 40px;">
      <div style="font-size: 48px; margin-bottom: 16px;">🎬</div>
      <p style="font-size: 18px; margin-bottom: 8px;">Rendering animation video...</p>
      <p style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">This may take a few minutes</p>
      <div id="video-progress" style="margin-top: 16px; font-size: 12px; color: rgba(255, 255, 255, 0.5);"></div>
    </div>
  `;
  
  const videoUrl = `http://localhost:5000${videoPath}`;
  console.log('🎬 Video URL:', videoUrl);
  
  // Function to display video
  const displayVideo = () => {
    console.log('🎬🎬🎬 Displaying video in preview box!');
    
    // Clear and create video element
    previewCanvas.innerHTML = '';
    const videoElement = document.createElement('video');
    videoElement.id = 'animation-video';
    videoElement.controls = true;
    videoElement.autoplay = false; // Don't autoplay, let user control
    videoElement.playsInline = true; // Important for mobile
    videoElement.style.cssText = 'width: 100% !important; height: 100% !important; object-fit: contain !important; background: #000 !important; display: block !important; border-radius: 8px;';
    videoElement.src = videoUrl;
    videoElement.type = 'video/mp4';
    
    previewCanvas.appendChild(videoElement);
    
    // Load video
    videoElement.load();
    
    // Event listeners
    videoElement.addEventListener('loadedmetadata', () => {
      console.log('✅ Video metadata loaded!');
    });
    
    videoElement.addEventListener('canplay', () => {
      console.log('✅ Video can play!');
    });
    
    videoElement.addEventListener('error', (e) => {
      console.error('❌ Video error:', e);
      previewCanvas.innerHTML = `
        <div style="text-align: center; color: #ff0000; padding: 40px;">
          <div style="font-size: 48px; margin-bottom: 16px;">❌</div>
          <p style="font-size: 18px;">Error loading video</p>
          <p style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">Please try again</p>
        </div>
      `;
    });
    
    console.log('✅✅✅ Video element created and added to preview box!');
  };
  
  let pollCount = 0;
  const maxPolls = 300; // 5 minutes max (300 * 1s = 5 minutes)
  const pollInterval = setInterval(async () => {
    pollCount++;
    
    // Update progress
    const progressDiv = document.getElementById('video-progress');
    if (progressDiv) {
      const minutes = Math.floor(pollCount / 60);
      const seconds = pollCount % 60;
      progressDiv.textContent = `Checking... (${minutes}m ${seconds}s)`;
    }
    
    try {
      const response = await fetch(videoUrl, { method: 'HEAD' });
      if (response.ok) {
        clearInterval(pollInterval);
        console.log('✅✅✅ Video is ready! Status:', response.status);
        displayVideo();
      } else if (pollCount >= maxPolls) {
        clearInterval(pollInterval);
        console.error('❌ Video not available after polling');
        previewCanvas.innerHTML = `
          <div style="text-align: center; color: #ff0000; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 16px;">❌</div>
            <p style="font-size: 18px; margin-bottom: 8px;">Video rendering failed or timed out</p>
            <p style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">Please try again</p>
          </div>
        `;
      }
    } catch (error) {
      if (pollCount >= maxPolls) {
        clearInterval(pollInterval);
        console.error('❌ Error polling for video:', error);
        previewCanvas.innerHTML = `
          <div style="text-align: center; color: #ff0000; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 16px;">❌</div>
            <p style="font-size: 18px; margin-bottom: 8px;">Error loading video</p>
            <p style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">Please check backend connection</p>
          </div>
        `;
      }
    }
  }, 1000); // Poll every 1 second
}

function clearBoxes() {
  const audioBoxContent = document.getElementById('audio-box-content');
  const summaryBoxContent = document.getElementById('summary-box-content');
  const mcqBoxContent = document.getElementById('mcq-box-content');
  const previewCanvas = document.getElementById('preview-canvas');
  const audioPlayer = document.getElementById('physics-audio-player');
  const audioContainer = audioBoxContent?.querySelector('.audio-player-container');
  
  // Reset audio
  if (audioPlayer) {
    audioPlayer.src = '';
    audioPlayer.pause();
  }
  
  if (audioContainer) {
    audioContainer.style.display = 'none';
  }
  
  // Reset summary
  if (summaryBoxContent) {
    summaryBoxContent.innerHTML = '<p class="box-placeholder">Summary of the animated video will appear here</p>';
  }
  
  // Reset MCQ
  if (mcqBoxContent) {
    mcqBoxContent.innerHTML = '<p class="box-placeholder">MCQ questions related to the topic will appear here</p>';
  }
  
  // Reset video preview
  if (previewCanvas) {
    previewCanvas.innerHTML = `
      <div class="canvas-placeholder">
        <p>Animation canvas will appear here</p>
        <small>Ready for gesture control integration</small>
      </div>
    `;
  }
  
  // Show placeholder for audio
  if (audioBoxContent && !audioBoxContent.querySelector('.box-placeholder')) {
    const placeholder = document.createElement('p');
    placeholder.className = 'box-placeholder';
    placeholder.textContent = 'Audio narration will appear here after generating animation';
    audioBoxContent.appendChild(placeholder);
  }
}

