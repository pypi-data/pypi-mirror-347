"""
API handler for the Gemini chat functionality.
"""

import google.generativeai as genai
from typing import List, Dict, Any
import os
from dataclasses import dataclass
from enum import Enum

class ChatError(Exception):
    """Base exception for chat-related errors"""
    pass

class FileAccessError(ChatError):
    """Raised when there are issues accessing documentation files"""
    pass

class ModelError(ChatError):
    """Raised when there are issues with the Gemini model"""
    pass

class ConfigError(ChatError):
    """Raised when there are configuration issues"""
    pass

@dataclass
class ChatResponse:
    """Structured response from chat handler"""
    text: str
    success: bool
    error: str = None
    metadata: Dict[str, Any] = None

class ChatHandler:
    def __init__(self, api_key: str):
        if not api_key:
            raise ConfigError("Gemini API key is required")
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-pro-preview-05-06')
            self.chat = None
            self.reset_chat()
        except Exception as e:
            raise ModelError(f"Failed to initialize Gemini model: {str(e)}")

    def reset_chat(self):
        """Reset the chat session."""
        try:
            self.chat = self.model.start_chat(history=[])
        except Exception as e:
            raise ModelError(f"Failed to start new chat session: {str(e)}")

    def get_doc_context(self, file_path: str = None) -> str:
        """
        Get the documentation context for the given file path.
        If no file path is provided, use the current page context.
        
        Raises:
            FileAccessError: If there are issues reading the documentation file
        """
        if not file_path:
            return ""
        
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileAccessError(f"Documentation file not found: {file_path}")
        except PermissionError:
            raise FileAccessError(f"Permission denied accessing file: {file_path}")
        except Exception as e:
            raise FileAccessError(f"Error reading documentation file {file_path}: {str(e)}")

    async def handle_message(self, message: str, file_path: str = None, 
                           language: str = 'en', version: str = 'latest',
                           history: List[Dict[str, str]] = None) -> ChatResponse:
        """
        Handle a chat message and return the response.
        
        Args:
            message: The user's question or message
            file_path: Optional path to specific documentation file
            language: Documentation language (default: 'en')
            version: Documentation version (default: 'latest')
            history: Optional chat history
            
        Returns:
            ChatResponse object containing the response and metadata
            
        Raises:
            ModelError: If there are issues with the Gemini model
            FileAccessError: If there are issues accessing documentation
            ChatError: For other chat-related errors
        """
        try:
            # Get documentation context
            doc_context = self.get_doc_context(file_path)
            
            # Prepare the prompt with context
            prompt = f"""
            Language: {language}
            Version: {version}
            Documentation Context: {doc_context}
            
            User Question: {message}
            
            Please provide a helpful response based on the documentation context.
            If the context doesn't contain relevant information, say so.
            """
            
            # Update chat history if provided
            if history:
                self.chat.history = [
                    genai.types.ContentDict(role=msg['role'], parts=[msg['content']])
                    for msg in history
                ]
            
            # Get response from Gemini
            response = await self.chat.send_message_async(prompt)
            
            return ChatResponse(
                text=response.text,
                success=True,
                metadata={
                    'language': language,
                    'version': version,
                    'has_context': bool(doc_context)
                }
            )
            
        except FileAccessError as e:
            raise e
        except Exception as e:
            raise ModelError(f"Error getting response from Gemini: {str(e)}")

    def update_history(self, history: List[Dict[str, str]]):
        """
        Update the chat history.
        
        Args:
            history: List of message dictionaries with 'role' and 'content' keys
            
        Raises:
            ChatError: If there are issues updating the history
        """
        try:
            self.chat.history = [
                genai.types.ContentDict(role=msg['role'], parts=[msg['content']])
                for msg in history
            ]
        except Exception as e:
            raise ChatError(f"Failed to update chat history: {str(e)}") 