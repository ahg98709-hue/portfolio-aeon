const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const voiceBtn = document.getElementById('voice-btn');
const voiceOutputToggle = document.getElementById('voice-output-toggle');

// State
let isRecording = false;

// Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onstart = () => {
        isRecording = true;
        voiceBtn.classList.add('recording');
    };

    recognition.onend = () => {
        isRecording = false;
        voiceBtn.classList.remove('recording');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendMessage(); // Auto-send on voice end
    };
    
    recognition.onerror = (event) => {
        console.error("Speech error", event.error);
        isRecording = false;
        voiceBtn.classList.remove('recording');
    };
} else {
    voiceBtn.style.display = 'none';
    console.warn("Speech Recognition not supported");
}

voiceBtn.addEventListener('click', () => {
    if (!recognition) return;
    if (isRecording) {
        recognition.stop();
    } else {
        recognition.start();
    }
});

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';

    // Show typical "thinking" state if desired, but waiting is fine
    // addMessage("...", 'assistant', true); 

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        const data = await response.json();
        const aeonResponse = data.response;
        
        addMessage(aeonResponse, 'assistant');
        
        if (voiceOutputToggle.checked) {
            speak(aeonResponse);
        }

    } catch (error) {
        addMessage("Communication Error: " + error, 'system');
    }
}

function addMessage(text, type, loading=false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    msgDiv.innerHTML = `<div class="content">${formatText(text)}</div>`;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function formatText(text) {
    if (!text) return "";
    // Basic formatting
    // Remove "Thinking..." blocks if they leaked, ideally backend handles it
    let cleanText = text.replace(/Thinking\.\.\./g, "").trim();
    
    // Simple markdown replacement
    cleanText = cleanText
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/`([^`]+)`/g, '<code style="background:rgba(255,255,255,0.1);padding:2px 4px;border-radius:4px;">$1</code>');
        
    return cleanText;
}

function speak(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        
        // Strip markdown for speech
        const speechText = text.replace(/[*`#]/g, '');
        
        const utterance = new SpeechSynthesisUtterance(speechText);
        const voices = window.speechSynthesis.getVoices();
        // Prefer a female/soft voice typically for "AI" or whatever default
        // Just pick default or first
        // If we wait for voiceschanged it works better, but simple is ok
        
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

// Preload voices
speechSynthesis.getVoices();
