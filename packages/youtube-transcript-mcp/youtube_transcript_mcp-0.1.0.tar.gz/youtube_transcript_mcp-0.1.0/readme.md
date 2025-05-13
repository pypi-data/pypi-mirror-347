# YouTube Trascript MCP Server

A Model Context Protocol server that allows you to download subtitles from YouTube and connect them to a LLM. This is just a thin wrapper on the youtube-transcript-api package.

## Features

- Download transcripts of YouTube videos
- Optionally include timestamps
- Works with any MCP-compatible client

## Usage

### In your MCP client configuration:

```json
"mcpServers": {
    "youtube": {
      "command": "uvx",
      "args": ["youtube-transcript-mcp"]
    },
}
```

## License

MIT