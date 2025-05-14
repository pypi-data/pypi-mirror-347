import pytest
from mkdocs_gemini_chat import GeminiChatPlugin
from mkdocs.config.base import Config

@pytest.fixture
def plugin():
    return GeminiChatPlugin()

@pytest.fixture
def mock_config():
    return Config(schema=[])

def test_plugin_initialization(plugin):
    assert plugin.chat_history == []
    assert plugin.docs_context == {}

def test_plugin_config(plugin, mock_config):
    # Test with default values
    config = plugin.on_config(mock_config)
    assert isinstance(config, Config)

def test_chat_window_html_generation(plugin):
    html = plugin._generate_chat_window_html()
    assert 'gemini-chat-window' in html
    assert 'chat-header' in html
    assert 'chat-body' in html
    assert 'chat-input' in html

def test_chat_js_generation(plugin):
    js = plugin._generate_chat_js()
    assert 'addMessage' in js
    assert 'sendMessage' in js
    assert 'chatHistory' in js

def test_page_content_modification(plugin, mock_config):
    original_html = '<div>Test content</div>'
    modified_html = plugin.on_page_content(original_html, None, mock_config, None)
    assert original_html in modified_html
    assert 'gemini-chat-window' in modified_html 