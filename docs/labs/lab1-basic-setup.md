# Lab 1: Basic MCP Server Setup

**Duration**: 45-60 minutes  
**Difficulty**: Beginner  
**Prerequisites**: Node.js 18+, basic TypeScript knowledge

## Learning Objectives

By the end of this lab, you will be able to:
- Set up a basic MCP server project
- Understand the MCP server lifecycle
- Implement a simple tool
- Test your MCP server locally

## Introduction

In this lab, you'll create your first MCP (Model Context Protocol) server. This server will provide a simple calculator tool that can perform basic arithmetic operations.

## Part 1: Project Setup (10 minutes)

### Step 1: Create Project Directory

```bash
mkdir calculator-mcp-server
cd calculator-mcp-server
```

### Step 2: Initialize Node.js Project

```bash
npm init -y
```

### Step 3: Install Dependencies

```bash
npm install @modelcontextprotocol/sdk
npm install --save-dev typescript @types/node tsx
```

### Step 4: Configure TypeScript

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### Step 5: Update package.json

Add the following scripts:

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

## Part 2: Basic Server Implementation (20 minutes)

### Step 1: Create Server File

Create `src/index.ts`:

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create server instance
const server = new Server(
  {
    name: "calculator-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool: Add two numbers
function add(a: number, b: number): number {
  return a + b;
}

// Tool: Subtract two numbers
function subtract(a: number, b: number): number {
  return a - b;
}

// Tool: Multiply two numbers
function multiply(a: number, b: number): number {
  return a * b;
}

// Tool: Divide two numbers
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Cannot divide by zero");
  }
  return a / b;
}

// Register tool listing handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add",
        description: "Add two numbers together",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "First number",
            },
            b: {
              type: "number",
              description: "Second number",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "subtract",
        description: "Subtract second number from first number",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "First number",
            },
            b: {
              type: "number",
              description: "Second number",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "multiply",
        description: "Multiply two numbers together",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "First number",
            },
            b: {
              type: "number",
              description: "Second number",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "divide",
        description: "Divide first number by second number",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "Numerator",
            },
            b: {
              type: "number",
              description: "Denominator (cannot be zero)",
            },
          },
          required: ["a", "b"],
        },
      },
    ],
  };
});

// Register tool call handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (!args) {
    throw new Error("No arguments provided");
  }

  const a = args.a as number;
  const b = args.b as number;

  let result: number;

  switch (name) {
    case "add":
      result = add(a, b);
      break;
    case "subtract":
      result = subtract(a, b);
      break;
    case "multiply":
      result = multiply(a, b);
      break;
    case "divide":
      result = divide(a, b);
      break;
    default:
      throw new Error(`Unknown tool: ${name}`);
  }

  return {
    content: [
      {
        type: "text",
        text: `Result: ${result}`,
      },
    ],
  };
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Calculator MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
```

## Part 3: Testing Your Server (15 minutes)

### Step 1: Build the Server

```bash
npm run build
```

### Step 2: Test with MCP Inspector

Install the MCP Inspector (if not already installed):

```bash
npm install -g @modelcontextprotocol/inspector
```

Run the inspector:

```bash
mcp-inspector node dist/index.js
```

This will open a web interface where you can:
- View available tools
- Call tools with different parameters
- See the responses

### Step 3: Manual Testing

Create a test script `test-client.js`:

```javascript
import { spawn } from 'child_process';

const server = spawn('node', ['dist/index.js']);

// Send initialize request
const initRequest = {
  jsonrpc: '2.0',
  id: 1,
  method: 'initialize',
  params: {
    protocolVersion: '2024-11-05',
    capabilities: { tools: {} },
    clientInfo: { name: 'test-client', version: '1.0.0' }
  }
};

server.stdin.write(JSON.stringify(initRequest) + '\n');

// List tools
setTimeout(() => {
  const listRequest = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/list',
    params: {}
  };
  server.stdin.write(JSON.stringify(listRequest) + '\n');
}, 100);

// Call add tool
setTimeout(() => {
  const callRequest = {
    jsonrpc: '2.0',
    id: 3,
    method: 'tools/call',
    params: {
      name: 'add',
      arguments: { a: 5, b: 3 }
    }
  };
  server.stdin.write(JSON.stringify(callRequest) + '\n');
}, 200);

server.stdout.on('data', (data) => {
  console.log('Response:', data.toString());
});

server.stderr.on('data', (data) => {
  console.error('Server log:', data.toString());
});

// Clean up after 2 seconds
setTimeout(() => {
  server.kill();
  process.exit(0);
}, 2000);
```

Run the test:

```bash
node test-client.js
```

## Part 4: Exercises (15 minutes)

### Exercise 1: Add More Operations

Extend the calculator with these operations:
- `power`: Raise first number to the power of second number
- `modulo`: Get remainder of division
- `sqrt`: Calculate square root (takes one argument)

**Solution Hint**: Add new tool definitions and implement the functions.

### Exercise 2: Add Input Validation

Improve the tool handlers to validate inputs:
- Check if inputs are valid numbers
- Add range constraints (e.g., numbers between -1000 and 1000)
- Provide helpful error messages

### Exercise 3: Add a History Feature

Create a tool that returns the last 5 calculations performed.

**Hint**: Maintain an array to store calculation history.

## Verification

Your server is working correctly if:
1. ✅ All four calculator tools are listed
2. ✅ Each tool returns correct results
3. ✅ Division by zero is handled gracefully
4. ✅ Invalid tool names return an error
5. ✅ The server continues running after errors

## Common Issues and Solutions

### Issue 1: Server won't start

**Error**: `Cannot find module '@modelcontextprotocol/sdk'`

**Solution**: Make sure you installed dependencies:
```bash
npm install
```

### Issue 2: TypeScript compilation errors

**Error**: `Cannot find name 'Server'`

**Solution**: Check your imports and ensure SDK is installed correctly.

### Issue 3: Tools not showing up

**Problem**: Tools list returns empty array

**Solution**: Make sure your `ListToolsRequestSchema` handler is properly registered before connecting the transport.

## Key Takeaways

- MCP servers use JSON-RPC 2.0 protocol
- Servers communicate via stdio or HTTP/SSE
- Tools must be registered with proper schemas
- Input validation is essential for robust servers
- Error handling prevents server crashes

## Next Steps

Congratulations! You've built your first MCP server. Continue to:
- [Lab 2: Tool Definition and Registration](lab2-tool-registration.md)
- Explore the [examples directory](../examples/)
- Read the [MCP Protocol Specification](https://modelcontextprotocol.io/specification)

## Additional Resources

- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [JSON Schema Reference](https://json-schema.org/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
