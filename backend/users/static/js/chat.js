const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const fileInput = document.getElementById('fileInput');
const selectedFilesContainer = document.getElementById('selectedFiles');
const chatForm = document.getElementById('chatForm');
const sendButton = document.getElementById('sendButton');


document.getElementById('logoutButton').addEventListener('click', function() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear stored tokens
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        
        // Redirect to login
        window.location.href = '/user/login/';
    }
});
let selectedFiles = [];

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});

// Handle file selection
fileInput.addEventListener('change', function(e) {
    const files = Array.from(e.target.files);
    selectedFiles = [...selectedFiles, ...files];
    updateSelectedFilesDisplay();
    e.target.value = '';
});

function updateSelectedFilesDisplay() {
    selectedFilesContainer.innerHTML = '';
    selectedFiles.forEach((file, index) => {
        const fileElement = document.createElement('div');
        fileElement.className = 'selected-file';
        fileElement.innerHTML = `
            <span class="file-icon">📁</span>
            ${file.name}
            <span class="remove-file" onclick="removeFile(${index})">×</span>
        `;
        selectedFilesContainer.appendChild(fileElement);
    });
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateSelectedFilesDisplay();
}

function addMessage(type, content, files = []) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    let filesHtml = '';
    if (files.length > 0) {
        filesHtml = files.map(file => `
            <div class="file-attachment">
                <span class="file-icon">📁</span>
                ${file.name}
            </div>
        `).join('');
    }

    messageDiv.innerHTML = `
        <div class="message-avatar">${type === 'user' ? 'U' : 'AI'}</div>
        <div class="message-content ${type === 'assistant' && content.includes('error') ? 'error-message' : ''}">
            ${filesHtml}
            ${content}
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    const files = [...selectedFiles];

    if (!message && files.length === 0) {
        return;
    }

    // Create FormData
    const formData = new FormData();
    if (message) formData.append('message', message);
    files.forEach(file => formData.append('files', file));

    // Show user message
    if (message) {
        addMessage('user', message, files);
    } else if (files.length > 0) {
        addMessage('user', `Uploaded ${files.length} file(s)`, files);
    }

    // Clear inputs
    messageInput.value = '';
    messageInput.style.height = 'auto';
    selectedFiles = [];
    updateSelectedFilesDisplay();

    const token = localStorage.getItem('accessToken');
    if (!token) {
        addMessage('assistant', 'Please log in to continue.');
        return;
    }

    sendButton.disabled = true;

    try {
        const response = await fetch('/user/chat/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            addMessage('assistant', data.answer || 'No response');
        } else {
            addMessage('assistant', data.detail || 'Error occurred');
        }

    } catch (error) {
        addMessage('assistant', 'Connection error');
    } finally {
        sendButton.disabled = false;
    }
});

// Handle Enter key
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});