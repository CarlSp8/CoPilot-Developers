# Quick Start Guide

Get up and running with MCP development in 15 minutes.

## Prerequisites

- Node.js 18+ or Python 3.10+
- VS Code with GitHub Copilot installed
- Basic understanding of TypeScript/JavaScript or Python

## Step 1: Create Your First MCP Server (5 minutes)

```bash
# Create project directory
mkdir my-first-mcp-server
cd my-first-mcp-server

# Initialize project
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk
npm install --save-dev typescript @types/node tsx

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
EOF

# Create source directory
mkdir src
```

## Step 2: Write Your Server (5 minutes)

Create `src/index.ts`:

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "my-tools", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "echo",
      description: "Echo back the input text",
      inputSchema: {
        type: "object",
        properties: {
          text: { type: "string", description: "Text to echo" }
        },
        required: ["text"]
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "echo") {
    const text = request.params.arguments?.text as string;
    return {
      content: [{ type: "text", text: `Echo: ${text}` }]
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running on stdio");
}

main().catch(console.error);
```

Add to `package.json`:

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  }
}
```

## Step 3: Test Your Server (2 minutes)

```bash
# Build
npm run build

# Test with inspector
npx @modelcontextprotocol/inspector node dist/index.js
```

This opens a web interface where you can test your tool.

## Step 4: Configure VS Code (3 minutes)

Open VS Code settings (`Cmd/Ctrl + ,`), search for "settings.json", and add:

```json
{
  "github.copilot.chat.mcp.servers": {
    "my-tools": {
      "command": "node",
      "args": ["/absolute/path/to/my-first-mcp-server/dist/index.js"]
    }
  }
}
```

Replace `/absolute/path/to/` with your actual project path.

Restart VS Code: `Cmd/Ctrl + Shift + P` → "Developer: Reload Window"

## Step 5: Use in Copilot Chat

Open Copilot Chat (`Cmd/Ctrl + Shift + I`) and try:

```
@workspace Use the echo tool to repeat "Hello, MCP!"
```

You should see: `Echo: Hello, MCP!`

## Next Steps

✅ Congratulations! You've created your first MCP server.

Now explore:

1. **Learn More**: Read the [comprehensive guide](HOW-TO-BUILD-YOUR-OWN-COPILOT.md)
2. **Complete Labs**: Work through [Lab 1](labs/lab1-basic-setup.md) through [Lab 5](labs/lab5-advanced-features.md)
3. **Browse Examples**: Check out [30+ code snippets](examples/ALL-SNIPPETS.md)
4. **Build Something**: Create tools for your specific use case

## Common Issues

### Server won't start

**Error**: `Cannot find module '@modelcontextprotocol/sdk'`

**Fix**: Run `npm install`

### Tools don't appear in Copilot

**Fixes**:
1. Use absolute paths in settings.json
2. Restart VS Code after configuration changes
3. Check VS Code Output panel for errors

### Permission denied

**Error**: `EACCES: permission denied`

**Fix**: `chmod +x dist/index.js`

## Resources

- [Full Documentation](HOW-TO-BUILD-YOUR-OWN-COPILOT.md)
- [MCP Official Docs](https://modelcontextprotocol.io)
- [GitHub MCP Registry](https://github.com/mcp)
- [Community Examples](https://github.com/topics/model-context-protocol)

## Get Help

- Check the [troubleshooting section](labs/lab4-vscode-integration.md#debugging-and-troubleshooting)
- Review [common patterns](examples/ALL-SNIPPETS.md)
- Ask questions in the community

Happy coding! 🚀
