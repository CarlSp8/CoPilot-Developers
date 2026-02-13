# How to Build Your Own Copilot

A comprehensive, MIT-level guide to building AI coding assistants using the Model Context Protocol (MCP).

![MCP Architecture](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [MCP Protocol Fundamentals](#mcp-protocol-fundamentals)
4. [Building Your First MCP Server](#building-your-first-mcp-server)
5. [Advanced Features](#advanced-features)
6. [Integration with VS Code](#integration-with-vs-code)
7. [Best Practices](#best-practices)
8. [Labs and Examples](#labs-and-examples)

## Introduction

GitHub Copilot and similar AI assistants are powerful, but what if you could build your own custom AI assistant tailored to your specific needs? This guide will teach you how to create custom copilot-style tools using the Model Context Protocol (MCP).

### What You'll Learn

- Understanding the MCP architecture and protocol
- Building custom MCP servers
- Creating tools and resources for AI assistants
- Integrating with popular IDEs like VS Code
- Deploying and scaling your copilot
- Security and best practices

### Prerequisites

- Basic understanding of Python or TypeScript
- Familiarity with RESTful APIs and JSON
- Experience with AI/LLM concepts (helpful but not required)
- Node.js 18+ or Python 3.10+

## Architecture Overview

The Model Context Protocol enables AI assistants to interact with external services through a standardized interface. Think of it as "USB-C for AI."

```
┌─────────────┐
│   Client    │  (Your IDE/Editor)
│  (Copilot)  │
└──────┬──────┘
       │ MCP Protocol
       │ (JSON-RPC 2.0)
       │
┌──────▼──────────────────────────────┐
│       MCP Server Layer              │
│  ┌──────────┐  ┌─────────────────┐ │
│  │  Tools   │  │   Resources     │ │
│  │          │  │                 │ │
│  └──────────┘  └─────────────────┘ │
└──────┬──────────────────────────────┘
       │
┌──────▼──────┐
│   External  │
│   Services  │
│ (GitHub,DB) │
└─────────────┘
```

### Key Components

1. **MCP Client**: The AI assistant (e.g., GitHub Copilot, Claude)
2. **MCP Server**: Your custom backend that provides tools and resources
3. **Tools**: Functions that the AI can call to perform actions
4. **Resources**: Data sources that provide context to the AI
5. **Prompts**: Pre-defined conversation templates

## MCP Protocol Fundamentals

MCP uses JSON-RPC 2.0 over standard input/output (stdio) or HTTP/SSE (Server-Sent Events).

### Protocol Messages

#### 1. Initialize Connection

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "clientInfo": {
      "name": "my-client",
      "version": "1.0.0"
    }
  }
}
```

#### 2. List Available Tools

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

#### 3. Call a Tool

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "San Francisco"
    }
  }
}
```

### Transport Layers

MCP supports two primary transport mechanisms:

1. **stdio**: Standard input/output (best for local processes)
2. **HTTP/SSE**: Server-Sent Events (best for remote servers)

## Building Your First MCP Server

Let's build a simple MCP server that provides weather information.

### Step 1: Setup Project

```bash
mkdir my-mcp-server
cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk
```

### Step 2: Create Server

```typescript
// server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create server instance
const server = new Server(
  {
    name: "weather-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Register tool listing handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_weather",
        description: "Get current weather for a city",
        inputSchema: {
          type: "object",
          properties: {
            city: {
              type: "string",
              description: "The city name",
            },
          },
          required: ["city"],
        },
      },
    ],
  };
});

// Register tool call handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_weather") {
    const city = request.params.arguments?.city as string;
    
    // In a real implementation, you'd call a weather API
    const weatherData = {
      city: city,
      temperature: 72,
      condition: "Sunny",
      humidity: 45,
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(weatherData, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP server running on stdio");
}

main().catch(console.error);
```

### Step 3: Build and Test

```bash
npx tsx server.ts
```

## Advanced Features

### 1. Resources

Resources provide contextual data to the AI assistant.

```typescript
import { ListResourcesRequestSchema, ReadResourceRequestSchema } from "@modelcontextprotocol/sdk/types.js";

// List available resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "weather://current",
        name: "Current Weather Data",
        description: "Real-time weather information",
        mimeType: "application/json",
      },
    ],
  };
});

// Read resource content
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  
  if (uri === "weather://current") {
    const data = await fetchCurrentWeather();
    return {
      contents: [
        {
          uri: uri,
          mimeType: "application/json",
          text: JSON.stringify(data),
        },
      ],
    };
  }
  
  throw new Error(`Unknown resource: ${uri}`);
});
```

### 2. Prompts

Pre-defined conversation templates for common tasks.

```typescript
import { ListPromptsRequestSchema, GetPromptRequestSchema } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "weather_report",
        description: "Generate a weather report for a city",
        arguments: [
          {
            name: "city",
            description: "City name",
            required: true,
          },
        ],
      },
    ],
  };
});

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  if (request.params.name === "weather_report") {
    const city = request.params.arguments?.city;
    
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please provide a detailed weather report for ${city}`,
          },
        },
      ],
    };
  }
  
  throw new Error(`Unknown prompt: ${request.params.name}`);
});
```

### 3. Progress Notifications

For long-running operations, send progress updates.

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "analyze_data") {
    // Send progress notifications
    await server.notification({
      method: "notifications/progress",
      params: {
        progressToken: request.params._meta?.progressToken,
        progress: 0,
        total: 100,
      },
    });

    // Perform work
    for (let i = 0; i <= 100; i += 10) {
      await performWork(i);
      await server.notification({
        method: "notifications/progress",
        params: {
          progressToken: request.params._meta?.progressToken,
          progress: i,
          total: 100,
        },
      });
    }

    return {
      content: [{ type: "text", text: "Analysis complete" }],
    };
  }
});
```

### 4. Error Handling

Proper error handling is crucial for robust MCP servers.

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Validate input
    if (!request.params.arguments?.city) {
      return {
        content: [
          {
            type: "text",
            text: "Error: city parameter is required",
          },
        ],
        isError: true,
      };
    }

    // Perform operation
    const result = await getWeather(request.params.arguments.city);
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result),
        },
      ],
    };
  } catch (error) {
    console.error("Error in get_weather:", error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});
```

## Integration with VS Code

To use your MCP server with GitHub Copilot in VS Code, you need to configure it in your settings.

### Configuration

Edit your `settings.json` (VS Code):

```json
{
  "github.copilot.chat.mcp.servers": {
    "weather": {
      "command": "node",
      "args": ["/path/to/your/server/dist/server.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Using Your Server

Once configured, you can use your tools in Copilot Chat:

```
@workspace Use the weather tool to get the current weather in San Francisco
```

## Best Practices

### 1. Security

- **Never expose sensitive data** in tool responses
- **Validate all inputs** before processing
- **Use environment variables** for API keys and secrets
- **Implement rate limiting** to prevent abuse
- **Sanitize user inputs** to prevent injection attacks

```typescript
function validateCity(city: string): string {
  // Remove special characters
  const sanitized = city.replace(/[^a-zA-Z0-9\s-]/g, '');
  
  // Limit length
  if (sanitized.length > 100) {
    throw new Error('City name too long');
  }
  
  return sanitized;
}
```

### 2. Performance

- **Cache frequently accessed data**
- **Use async/await** for I/O operations
- **Implement timeouts** for external API calls
- **Batch requests** when possible

```typescript
// Simple caching example
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function getCachedWeather(city: string) {
  const cached = cache.get(city);
  
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  
  const data = await fetchWeather(city);
  cache.set(city, { data, timestamp: Date.now() });
  
  return data;
}
```

### 3. Error Handling

- **Provide clear error messages**
- **Log errors for debugging**
- **Handle network failures gracefully**
- **Return partial results when possible**

### 4. Documentation

- **Document all tools** with clear descriptions
- **Provide examples** in tool descriptions
- **Include parameter constraints**
- **Specify return value formats**

```typescript
{
  name: "calculate_distance",
  description: "Calculate distance between two cities. Example: calculate_distance(city1='New York', city2='Los Angeles')",
  inputSchema: {
    type: "object",
    properties: {
      city1: {
        type: "string",
        description: "First city name (e.g., 'New York')"
      },
      city2: {
        type: "string",
        description: "Second city name (e.g., 'Los Angeles')"
      },
      unit: {
        type: "string",
        enum: ["miles", "kilometers"],
        description: "Unit of measurement (default: 'miles')"
      }
    },
    required: ["city1", "city2"]
  }
}
```

### 5. Testing

Always test your MCP server thoroughly:

```typescript
// test/server.test.ts
import { describe, it, expect } from 'vitest';
import { Server } from '../src/server';

describe('Weather MCP Server', () => {
  it('should list available tools', async () => {
    const tools = await server.listTools();
    expect(tools).toHaveLength(1);
    expect(tools[0].name).toBe('get_weather');
  });

  it('should get weather for a city', async () => {
    const result = await server.callTool('get_weather', {
      city: 'San Francisco'
    });
    expect(result.content[0].text).toContain('San Francisco');
  });

  it('should handle invalid city names', async () => {
    const result = await server.callTool('get_weather', {
      city: 'InvalidCity123!@#'
    });
    expect(result.isError).toBe(true);
  });
});
```

## Labs and Examples

This guide includes hands-on labs and over 30 code snippets to help you master MCP development:

### Labs

1. [Lab 1: Basic MCP Server Setup](labs/lab1-basic-setup.md)
2. [Lab 2: Tool Definition and Registration](labs/lab2-tool-registration.md)
3. [Lab 3: Building a Database MCP Server](labs/lab3-database-server.md)
4. [Lab 4: Integration with VS Code](labs/lab4-vscode-integration.md)
5. [Lab 5: Advanced Features and Optimization](labs/lab5-advanced-features.md)

### Code Examples

Browse over 30 practical examples in the [examples directory](examples/):

- **Basic**: Simple tool implementations (10 examples)
- **Intermediate**: Resources, prompts, and state management (10 examples)
- **Advanced**: Error handling, caching, and performance optimization (10+ examples)

## Additional Resources

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [GitHub MCP Registry](https://github.com/mcp)
- [MCP SDK Reference](https://github.com/modelcontextprotocol/sdk)
- [Community Examples](https://github.com/topics/model-context-protocol)

## Contributing

Found an issue or want to contribute? Please see our [Contributing Guide](../CONTRIBUTING.md).

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

**Ready to build?** Start with [Lab 1: Basic MCP Server Setup](labs/lab1-basic-setup.md) →
