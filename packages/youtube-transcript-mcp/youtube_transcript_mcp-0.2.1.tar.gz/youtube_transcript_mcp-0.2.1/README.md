# YouTube Transcript MCP Server

[![PyPI version](https://img.shields.io/pypi/v/youtube-transcript-mcp.svg)](https://pypi.org/project/youtube-transcript-mcp/)

A Model Context Protocol server that allows you to download subtitles from YouTube and connect them to a LLM. This is just a thin wrapper on the youtube-transcript-api package.

## Features

- Download transcripts of YouTube videos
- Optionally include timestamps
- Works with any MCP-compatible client

## Installation

### Option 1: Using uv (Recommended)

Install [uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option 2: Using pip

If you prefer not to use uv, you can install using standard pip:

```bash
pip install youtube-transcript-mcp
```

## Usage

### In your MCP client configuration:

#### If using uv:

The `uvx` command is provided by uv and allows you to run Python packages directly:

```json
"mcpServers": {
    "youtube": {
      "command": "uvx",
      "args": ["youtube-transcript-mcp"]
    },
}
```

#### If using standard Python:

```json
"mcpServers": {
    "youtube": {
      "command": "python",
      "args": ["-m", "youtube_transcript_mcp"]
    },
}
```

## License

MIT