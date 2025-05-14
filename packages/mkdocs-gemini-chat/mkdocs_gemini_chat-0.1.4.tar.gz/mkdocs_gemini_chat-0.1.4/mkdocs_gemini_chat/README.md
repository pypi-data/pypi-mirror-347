# MkDocs Gemini Chat Plugin

A Material for MkDocs plugin that adds a Gemini-powered chat window to documentation pages, allowing users to ask questions about the documentation content.

## Features

- Interactive chat window powered by Google's Gemini 2.5 Pro
- Context-aware responses based on documentation content
- Support for multiple languages
- Version-specific documentation context
- Chat history support
- Copy chat to clipboard
- Download chat history as a file
- Customizable UI position
- Error handling and user feedback
- Loading states and animations

## Installation

```bash
pip install mkdocs-gemini-chat
```

## Configuration

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - gemini-chat:
      api_key: your-gemini-api-key  # Required
      ui_position: bottom-right      # Optional (default: bottom-right)
      default_language: en           # Optional (default: en)
      default_version: latest        # Optional (default: latest)
      chat_history_length: 10        # Optional (default: 10)
```

### Configuration Options

| Option | Description | Default | Required |
|--------|-------------|---------|----------|
| `api_key` | Your Gemini API key | None | Yes |
| `ui_position` | Position of chat window (`bottom-right`, `bottom-left`, `top-right`, `top-left`) | `bottom-right` | No |
| `default_language` | Default documentation language | `en` | No |
| `default_version` | Default documentation version | `latest` | No |
| `chat_history_length` | Number of messages to keep in chat history | 10 | No |

### Supported Languages

The plugin supports the following languages:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Russian (ru)
- Portuguese (pt)
- Italian (it)

To add support for additional languages, modify the language selector options in the chat window HTML.

### Version Support

The plugin can handle any version string specified in your documentation. Common patterns include:
- Semantic versioning (e.g., "1.0.0", "2.1.3")
- Named versions (e.g., "latest", "stable", "dev")
- Date-based versions (e.g., "2024.1", "24.01")

## Security Best Practices

1. API Key Management:
   - Store your Gemini API key as an environment variable
   - Use a secrets management system in production
   - Never commit API keys to version control

Example using environment variables:
```yaml
plugins:
  - gemini-chat:
      api_key: !ENV GEMINI_API_KEY
```

2. Access Control:
   - Consider implementing rate limiting
   - Monitor API usage
   - Implement user authentication if needed

## Usage

1. Get a Gemini API key from the [Google AI Studio](https://makersuite.google.com/app/apikey).

2. Add your API key to the plugin configuration in `mkdocs.yml`.

3. The chat window will automatically appear on all documentation pages.

4. Users can:
   - Ask questions about the documentation
   - Specify file paths for context
   - Select documentation language
   - Select documentation version
   - Copy chat history to clipboard
   - Download chat history as a file

### Example Questions

The chat window can handle various types of questions, such as:
- "What are the installation requirements?"
- "How do I configure feature X?"
- "Can you explain the difference between version 1.0 and 2.0?"
- "Show me examples of using this API"

## Requirements

- Python >= 3.8
- MkDocs >= 1.0.0
- google-generativeai >= 0.3.0

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mkdocs-gemini-chat.git
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run tests:
```bash
python -m pytest tests/
```

## Error Handling

The plugin provides clear error messages for common issues:
- API key validation errors
- File access issues
- Network connectivity problems
- Rate limiting errors
- Invalid input errors

Error messages are displayed in the chat window with appropriate styling and icons.

## Deployment

### Local Development
1. Clone and install:
```bash
git clone https://github.com/yourusername/mkdocs-gemini-chat.git
cd mkdocs-gemini-chat
pip install -e .[dev]
```

2. Set up environment variables:
```bash
export GEMINI_API_KEY=your-api-key
export REDIS_URL=redis://localhost:6379  # For rate limiting
```

3. Run the development server:
```bash
uvicorn mkdocs_gemini_chat.server:app --reload
```

### Production Deployment

1. Install the package:
```bash
pip install mkdocs-gemini-chat
```

2. Configure environment variables in your production environment:
```bash
GEMINI_API_KEY=your-api-key
REDIS_URL=your-redis-url
```

3. Configure CORS in `mkdocs.yml`:
```yaml
plugins:
  - gemini-chat:
      api_key: !ENV GEMINI_API_KEY
      allowed_origins:
        - https://your-docs-site.com
```

4. Use a production ASGI server:
```bash
gunicorn mkdocs_gemini_chat.server:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment

1. Build the image:
```bash
docker build -t mkdocs-gemini-chat .
```

2. Run with Docker:
```bash
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your-api-key \
  -e REDIS_URL=redis://redis:6379 \
  mkdocs-gemini-chat
```

## Troubleshooting

### Common Issues

1. API Key Issues
- Error: "Invalid API key"
  - Solution: Check if GEMINI_API_KEY is properly set in environment variables
  - Verify API key is valid in Google AI Studio

2. Rate Limiting
- Error: "Too many requests"
  - Solution: Check Redis connection
  - Adjust rate limits in configuration
  - Consider upgrading API quota

3. File Access Issues
- Error: "File not found" or "Permission denied"
  - Solution: Check file paths are relative to docs directory
  - Verify file permissions
  - Ensure paths don't traverse outside allowed directory

4. CORS Issues
- Error: "Access blocked by CORS policy"
  - Solution: Add your domain to allowed_origins in configuration
  - Check if protocol (http/https) matches
  - Verify port numbers in development

5. Redis Connection
- Error: "Could not connect to Redis"
  - Solution: Verify Redis is running
  - Check Redis URL configuration
  - Ensure Redis port is accessible

### Debugging

1. Enable debug logging:
```yaml
plugins:
  - gemini-chat:
      debug: true
```

2. Check logs:
```bash
tail -f /var/log/mkdocs-gemini-chat.log
```

3. Test API endpoints:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### Getting Help

1. Check the [FAQ](https://github.com/yourusername/mkdocs-gemini-chat/wiki/FAQ)
2. Search [existing issues](https://github.com/yourusername/mkdocs-gemini-chat/issues)
3. Join our [Discord community](https://discord.gg/your-invite)
4. Open a new issue with:
   - Plugin version
   - MkDocs version
   - Error messages
   - Steps to reproduce
   - Expected vs actual behavior

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Run the test suite
6. Submit a pull request

### Development Setup

1. Install development dependencies:
```bash
pip install -e .[dev]
```

2. Run tests:
```bash
pytest tests/
```

3. Check code style:
```bash
black .
isort .
flake8 .
mypy mkdocs_gemini_chat
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused and small
- Add tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.