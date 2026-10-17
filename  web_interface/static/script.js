// Jarvis Web Interface - JavaScript

let commandCount = 0;
let isListening = false;

// DOM Elements
const commandInput = document.getElementById('commandInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const messagesContainer = document.getElementById('messages');
const historyModal = document.getElementById('historyModal');
const commandCountDisplay = document.getElementById('commandCount');

// Event Listeners
sendBtn.addEventListener('click', () => {
    const command = commandInput.value.trim();
    if (command) {
        sendCommand(command);
        commandInput.value = '';
    }
});

commandInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const command = commandInput.value.trim();
        if (command) {
            sendCommand(command);
            commandInput.value = '';
        }
    }
});

voiceBtn.addEventListener('click', startVoiceInput);

// Send Command
function sendCommand(command) {
    if (!command) return;

    // Add user message
    addMessage(command, 'user');
    commandCount++;
    updateCommandCount();

    // Disable input while processing
    commandInput.disabled = true;
    sendBtn.disabled = true;

    // Send to server
    fetch('/api/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addMessage(data.response, 'bot');
            speakResponse(data.response);
        } else {
            addMessage('Error: ' + (data.error || 'Unknown error'), 'bot');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Connection error. Please try again.', 'bot');
    })
    .finally(() => {
        commandInput.disabled = false;
        sendBtn.disabled = false;
        commandInput.focus();
    });
}

// Add Message to Chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Start Voice Input
function startVoiceInput() {
    if (isListening) return;

    isListening = true;
    voiceBtn.style.background = 'var(--danger-color)';
    voiceBtn.textContent = '🛑';

    // Use Web Speech API if available
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert('Speech Recognition not supported in your browser');
        isListening = false;
        voiceBtn.style.background = 'var(--accent-color)';
        voiceBtn.textContent = '🎤';
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        addMessage('🎤 Listening...', 'bot');
    };

    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }

        if (transcript.trim()) {
            commandInput.value = transcript;
            sendCommand(transcript);
        }
    };

    recognition.onerror = (event) => {
        addMessage('Error listening: ' + event.error, 'bot');
    };

    recognition.onend = () => {
        isListening = false;
        voiceBtn.style.background = 'var(--accent-color)';
        voiceBtn.textContent = '🎤';
    };

    recognition.start();
}

// Text-to-Speech Response
function speakResponse(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        speechSynthesis.speak(utterance);
    }
}

// Load History
function loadHistory() {
    historyModal.style.display = 'block';

    fetch('/api/history?limit=20')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.interactions.length > 0) {
                let historyHTML = '';
                data.interactions.forEach(interaction => {
                    historyHTML += `
                        <div class="history-item">
                            <div class="history-item-user">👤 You: ${interaction.user}</div>
                            <div class="history-item-response">🤖 Jarvis: ${interaction.response}</div>
                            <div class="history-item-time">${new Date(interaction.timestamp).toLocaleString()}</div>
                        </div>
                    `;
                });
                document.getElementById('historyContent').innerHTML = historyHTML;
            } else {
                document.getElementById('historyContent').innerHTML = '<p>No history found</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('historyContent').innerHTML = '<p>Error loading history</p>';
        });
}

// Clear History
function clearHistory() {
    if (confirm('Are you sure you want to clear conversation history?')) {
        fetch('/api/clear-history', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messagesContainer.innerHTML = '';
                addMessage('💾 History cleared', 'bot');
                commandCount = 0;
                updateCommandCount();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Close Modal
function closeModal() {
    historyModal.style.display = 'none';
}

// Update Command Count
function updateCommandCount() {
    commandCountDisplay.textContent = `Commands: ${commandCount}`;
}

// Close modal on outside click
window.addEventListener('click', (event) => {
    if (event.target == historyModal) {
        closeModal();
    }
});

// Check Status on Load
window.addEventListener('load', () => {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ Jarvis is online');
                addMessage('✅ Connected to Jarvis', 'bot');
            }
        })
        .catch(error => {
            console.error('Connection Error:', error);
            addMessage('⚠️ Warning: Cannot connect to Jarvis server', 'bot');
        });

    commandInput.focus();
});