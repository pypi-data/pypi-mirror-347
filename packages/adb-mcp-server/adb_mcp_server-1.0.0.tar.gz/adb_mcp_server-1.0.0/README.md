# ADB MCP Server

A Message Control Protocol (MCP) server implementation that uses stdio transport to communicate with Large Language Models (LLMs). This server is designed to work seamlessly with Cherry Studio for enhanced LLM interactions.

## Features

- Implements MCP protocol for standardized communication
- Uses stdio transport for efficient data transfer
- Compatible with Cherry Studio integration
- Supports ADB (Android Debug Bridge) communications

## Prerequisites

- Python 3.12 or higher
- Cherry Studio installed
- ADB tools (if working with Android devices)

## Installation

```bash
pip install adb-mcp-server
```

## Usage

### Using with Cherry Studio

1. Download and install [Cherry Studio](https://cherry.studio)
2. Open Cherry Studio settings
3. Navigate to the MCP server settings page
4. Add a new MCP server with the following configuration:
   - Name: Any name of your choice
   - Command: `uvx`
   - Parameter: `adb-mcp-server@latest`

## Development

### Requirements

- Python 3.12+
- MCP >= 1.6.0

### Building from Source

```bash
git clone https://github.com/yourusername/adb-mcp-server.git
cd adb-mcp-server
pip install -e .
```

## License

[Add your license information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/adb-mcp-server/issues) on GitHub.