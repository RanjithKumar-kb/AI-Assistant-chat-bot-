let currentSessionId = null;

// Initialize the app when the window loads
window.onload = () => {
    loadSidebar();
};

// 1. Sidebar Management: Fetches all saved chat sessions
async function loadSidebar() {
    try {
        const res = await fetch('/sessions');
        const sessions = await res.json();
        const sidebarList = document.getElementById('chat-list');
        
        // Clear current list but keep the header label
        sidebarList.innerHTML = '<p class="history-label">Recent Conversations</p>';

        const sessionIds = Object.keys(sessions).reverse();
        
        sessionIds.forEach(id => {
            // Create a container for the chat item and delete button
            const container = document.createElement('div');
            container.className = 'chat-item-container';

            const item = document.createElement('div');
            item.className = 'chat-item';
            item.innerText = sessions[id].title || "Untitled Chat";
            item.onclick = () => loadExistingChat(id);

            // Create Delete Button (×)
            const delBtn = document.createElement('button');
            delBtn.className = 'delete-btn';
            delBtn.innerHTML = '&times;';
            delBtn.title = "Delete Chat";
            delBtn.onclick = (e) => {
                e.stopPropagation(); // Stop from opening the chat when clicking delete
                deleteChat(id);
            };

            container.appendChild(item);
            container.appendChild(delBtn);
            sidebarList.appendChild(container);
        });
    } catch (err) {
        console.warn("Sidebar could not be loaded.");
    }
}

// NEW: Delete Chat Logic
async function deleteChat(id) {
    if (confirm("Are you sure you want to delete this chat?")) {
        try {
            const res = await fetch(`/delete_session/${id}`, { method: 'DELETE' });
            const data = await res.json();
            
            if (data.success) {
                // If we deleted the chat we are currently looking at, start a new one
                if (currentSessionId === id) {
                    startNewChat();
                }
                loadSidebar(); // Refresh the list
            }
        } catch (err) {
            alert("Could not delete the chat.");
        }
    }
}

// 2. Chat Switching: Loads a specific session
async function loadExistingChat(id) {
    currentSessionId = id;
    const box = document.getElementById('chat-box');
    box.innerHTML = '<div class="msg ai"><b>Lumina:</b> Loading history...</div>';
    
    try {
        const res = await fetch('/sessions');
        const sessions = await res.json();
        const messages = sessions[id].messages;

        box.innerHTML = ''; 
        messages.filter(m => m.role !== 'system').forEach(m => {
            const roleClass = m.role === 'user' ? 'user' : 'ai';
            const senderName = m.role === 'user' ? 'You' : 'Lumina';
            
            const msgDiv = document.createElement('div');
            msgDiv.className = `msg ${roleClass}`;
            msgDiv.innerHTML = `<b>${senderName}:</b> <div>${marked.parse(m.content)}</div>`;
            box.appendChild(msgDiv);
        });
        
        scrollToBottom();
    } catch (err) {
        box.innerHTML = '<div class="msg ai">Error loading chat.</div>';
    }
}

// 3. New Chat Logic
function startNewChat() {
    currentSessionId = null;
    const box = document.getElementById('chat-box');
    box.innerHTML = `
        <div class="msg ai">
            <b>Lumina:</b> New session started. What's on your mind?
        </div>
    `;
}

// 4. Send Message Logic
async function sendMessage() {
    const input = document.getElementById('user-input');
    const box = document.getElementById('chat-box');
    const text = input.value.trim();
    
    if (!text) return;

    box.innerHTML += `<div class="msg user"><b>You:</b> ${text}</div>`;
    input.value = ''; 
    scrollToBottom();

    const aiDiv = document.createElement('div');
    aiDiv.className = 'msg ai';
    aiDiv.innerHTML = '<b>Lumina:</b> <span class="tokens"></span>';
    box.appendChild(aiDiv);
    const contentSpan = aiDiv.querySelector('.tokens');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                message: text, 
                session_id: currentSessionId 
            })
        });

        const newId = response.headers.get("X-Session-ID");
        if (newId) currentSessionId = newId;

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullText = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            fullText += decoder.decode(value, { stream: true });
            contentSpan.innerHTML = marked.parse(fullText);
            scrollToBottom();
        }
        
        loadSidebar(); 

    } catch (err) {
        contentSpan.innerText = "Connection Error. Please ensure Ollama and Flask are running.";
    }
}

function scrollToBottom() {
    const box = document.getElementById('chat-box');
    box.scrollTop = box.scrollHeight;
}

function handleKey(event) {
    if (event.key === "Enter") {
        event.preventDefault(); 
        sendMessage();
    }
}