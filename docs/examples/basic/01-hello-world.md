# Example 1: Hello World Server

The simplest possible MCP server.

## Code

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create server
const server = new Server(
  {
    name: "hello-world",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "greet",
        description: "Returns a greeting message",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Name to greet",
            },
          },
          required: ["name"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "greet") {
    const name = request.params.arguments?.name as string;
    return {
      content: [
        {
          type: "text",
          text: `Hello, ${name}! Welcome to MCP.`,
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
  console.error("Hello World MCP server running");
}

main().catch(console.error);
```

## Key Concepts

1. **Server Initialization**: Create a `Server` instance with name and version
2. **Capabilities**: Declare what your server can do (tools, resources, prompts)
3. **Request Handlers**: Register handlers for different request types
4. **Transport**: Use `StdioServerTransport` for standard input/output communication

## Usage

After building and running the server, you can test it:

```bash
# In VS Code Copilot Chat
@workspace Use the greet tool to say hello to Alice
```

Expected output:
```
Hello, Alice! Welcome to MCP.
```

## Next Steps

- [Example 2: Single Tool](02-single-tool.md) - More detailed single tool implementation
- [Example 3: Multiple Tools](03-multiple-tools.md) - Adding multiple related tools
