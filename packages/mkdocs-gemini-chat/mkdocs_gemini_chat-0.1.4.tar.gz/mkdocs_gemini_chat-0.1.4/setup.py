from setuptools import setup, find_packages
import os

readme_file = "README.md" if os.path.exists("README.md") else "readme.md"
with open(readme_file, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-gemini-chat',
    version='0.1.4',
    description='A Material for MkDocs plugin that adds a Gemini-powered chat window to documentation pages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nolan Blevins',
    author_email='',
    url='https://github.com/nolanblevins/mkdocs-gemini-chat',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mkdocs>=1.0.0',
        'google-generativeai>=0.3.0',
        'fastapi>=0.68.0,<0.69.0',
        'uvicorn>=0.15.0,<0.16.0',
        'pydantic>=1.8.0,<2.0.0',
        'python-dotenv>=0.19.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-asyncio>=0.15.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'isort>=5.0',
            'flake8>=3.9',
            'mypy>=0.910',
            'httpx>=0.24.0',  # Required for FastAPI TestClient
        ]
    },
    entry_points={
        'mkdocs.plugins': [
            'gemini-chat = mkdocs_gemini_chat:GeminiChatPlugin',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: MkDocs',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
    python_requires='>=3.8',
    project_urls={
        'Bug Reports': 'https://github.com/nolanblevins/mkdocs-gemini-chat/issues',
        'Source': 'https://github.com/nolanblevins/mkdocs-gemini-chat',
        'Documentation': 'https://github.com/nolanblevins/mkdocs-gemini-chat#readme',
    }
) 