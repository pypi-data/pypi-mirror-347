"""
Material for MkDocs plugin that adds a Gemini-powered chat window to documentation pages.
"""

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import os
import json

class GeminiChatPlugin(BasePlugin):
    config_scheme = (
        ('ui_position', config_options.Type(str, default='bottom-right')),
        ('api_key', config_options.Type(str, required=True)),
        ('default_language', config_options.Type(str, default='en')),
        ('default_version', config_options.Type(str, default='latest')),
        ('chat_history_length', config_options.Type(int, default=10)),
    )

    def __init__(self):
        self.chat_history = []
        self.docs_context = {}

    def on_config(self, config):
        """
        Initialize plugin with configuration from mkdocs.yml
        """
        return config

    def on_page_content(self, html, page, config, files):
        """
        Add chat window HTML and required JavaScript to each documentation page.
        """
        # Add chat window HTML
        chat_window_html = self._generate_chat_window_html()
        html += chat_window_html

        # Add required JavaScript
        chat_js = self._generate_chat_js()
        html += f'<script>{chat_js}</script>'

        return html

    def on_post_build(self, config):
        """
        Clean up any resources after build.
        """
        pass

    def _generate_chat_window_html(self):
        """
        Generate the HTML for the chat window UI.
        """
        return """
        <div id="gemini-chat-window" class="gemini-chat">
            <div class="chat-header">
                <h3>Documentation Chat</h3>
                <div class="chat-controls">
                    <button id="download-chat" title="Download chat">📥</button>
                    <button id="copy-chat" title="Copy to clipboard">📋</button>
                    <button id="toggle-chat" title="Toggle chat">➖</button>
                </div>
            </div>
            <div class="chat-body">
                <div id="chat-messages"></div>
                <div class="chat-input-area">
                    <input type="text" id="file-path" placeholder="File path (optional)">
                    <select id="doc-language">
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <!-- Add more languages as needed -->
                    </select>
                    <select id="doc-version">
                        <option value="latest">Latest</option>
                        <!-- Add more versions dynamically -->
                    </select>
                    <div class="chat-input-container">
                        <textarea id="chat-input" placeholder="Ask a question..."></textarea>
                        <button id="send-message">Send</button>
                    </div>
                </div>
            </div>
        </div>
        <style>
        .gemini-chat {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            z-index: 1000;
        }
        .chat-header {
            padding: 10px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-header h3 {
            margin: 0;
        }
        .chat-controls button {
            background: none;
            border: none;
            cursor: pointer;
            padding: 5px;
        }
        .chat-body {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        #chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }
        .chat-input-area {
            padding: 10px;
            border-top: 1px solid #eee;
        }
        #file-path {
            width: 100%;
            margin-bottom: 5px;
            padding: 5px;
        }
        #doc-language, #doc-version {
            width: 48%;
            margin-bottom: 5px;
            padding: 5px;
        }
        .chat-input-container {
            display: flex;
            gap: 5px;
        }
        #chat-input {
            flex: 1;
            padding: 5px;
            resize: none;
            height: 60px;
        }
        #send-message {
            padding: 5px 15px;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .message {
            margin: 5px 0;
            padding: 8px;
            border-radius: 5px;
        }
        .user-message {
            background: #e3f2fd;
            margin-left: 20px;
        }
        .bot-message {
            background: #f5f5f5;
            margin-right: 20px;
        }
        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            font-size: 14px;
        }

        .success-message {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            font-size: 14px;
            opacity: 0.9;
        }

        .loading-spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #ffffff;
            border-radius: 50%;
            border-top-color: transparent;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to {transform: rotate(360deg);}
        }

        #send-message:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .chat-input:disabled {
            background: #f5f5f5;
            cursor: not-allowed;
        }
        </style>
        """

    def _generate_chat_js(self):
        """
        Generate the JavaScript code for chat functionality.
        """
        return """
        document.addEventListener('DOMContentLoaded', function() {
            let chatHistory = [];
            const chatMessages = document.getElementById('chat-messages');
            const chatInput = document.getElementById('chat-input');
            const sendButton = document.getElementById('send-message');
            const filePathInput = document.getElementById('file-path');
            const langSelect = document.getElementById('doc-language');
            const versionSelect = document.getElementById('doc-version');
            const copyButton = document.getElementById('copy-chat');
            const downloadButton = document.getElementById('download-chat');
            const toggleButton = document.getElementById('toggle-chat');
            const chatWindow = document.getElementById('gemini-chat-window');

            function showError(message) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'message error-message';
                errorDiv.innerHTML = `❌ ${message}`;
                chatMessages.appendChild(errorDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function showSuccess(message) {
                const successDiv = document.createElement('div');
                successDiv.className = 'message success-message';
                successDiv.innerHTML = `✅ ${message}`;
                chatMessages.appendChild(successDiv);
                successDiv.scrollIntoView({ behavior: 'smooth' });
                setTimeout(() => successDiv.remove(), 3000);
            }

            function setLoading(isLoading) {
                sendButton.disabled = isLoading;
                sendButton.innerHTML = isLoading ? 
                    '<span class="loading-spinner"></span>' : 
                    'Send';
                chatInput.disabled = isLoading;
            }

            function addMessage(message, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                messageDiv.textContent = message;
                chatMessages.appendChild(messageDiv);
                messageDiv.scrollIntoView({ behavior: 'smooth' });
                chatHistory.push({ role: isUser ? 'user' : 'assistant', content: message });
            }

            async function sendMessage() {
                const message = chatInput.value.trim();
                if (!message) {
                    showError('Please enter a message');
                    return;
                }

                setLoading(true);
                addMessage(message, true);
                chatInput.value = '';

                // Prepare request data
                const requestData = {
                    message: message,
                    filePath: filePathInput.value,
                    language: langSelect.value,
                    version: versionSelect.value,
                    history: chatHistory
                };

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(requestData)
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();
                    
                    if (!data.success) {
                        throw new Error(data.error || 'Unknown error occurred');
                    }

                    addMessage(data.text, false);

                    // Show metadata if available
                    if (data.metadata) {
                        const contextInfo = data.metadata.has_context ? 
                            'Using documentation context' : 
                            'No specific documentation context';
                        showSuccess(`${contextInfo} (${data.metadata.language}, v${data.metadata.version})`);
                    }

                } catch (error) {
                    console.error('Error:', error);
                    showError(error.message || 'Failed to get response. Please try again.');
                } finally {
                    setLoading(false);
                }
            }

            // Event listeners
            sendButton.addEventListener('click', sendMessage);
            chatInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            copyButton.addEventListener('click', async function() {
                try {
                    const chatText = chatHistory
                        .map(msg => `${msg.role}: ${msg.content}`)
                        .join('\n');
                    await navigator.clipboard.writeText(chatText);
                    showSuccess('Chat copied to clipboard');
                } catch (error) {
                    showError('Failed to copy chat');
                }
            });

            downloadButton.addEventListener('click', function() {
                try {
                    const chatText = chatHistory
                        .map(msg => `${msg.role}: ${msg.content}`)
                        .join('\n');
                    const blob = new Blob([chatText], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'chat-history.txt';
                    a.click();
                    URL.revokeObjectURL(url);
                    showSuccess('Chat downloaded successfully');
                } catch (error) {
                    showError('Failed to download chat');
                }
            });

            toggleButton.addEventListener('click', function() {
                const chatBody = document.querySelector('.chat-body');
                if (chatBody.style.display === 'none') {
                    chatBody.style.display = 'flex';
                    toggleButton.textContent = '➖';
                } else {
                    chatBody.style.display = 'none';
                    toggleButton.textContent = '➕';
                }
            });
        });
        """ 