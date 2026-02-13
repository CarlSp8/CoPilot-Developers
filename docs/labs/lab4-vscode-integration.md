# Lab 4: Integration with VS Code

**Duration**: 45-60 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Labs 1-3, VS Code with GitHub Copilot installed

## Learning Objectives

- Configure MCP servers in VS Code
- Use MCP tools in GitHub Copilot Chat
- Debug MCP server integration issues
- Create user-friendly tool descriptions
- Handle environment variables securely

## Introduction

Learn how to integrate your custom MCP servers with VS Code and GitHub Copilot to create a seamless development experience.

## Part 1: VS Code Configuration (15 minutes)

### Understanding VS Code Settings

VS Code uses settings.json to configure MCP servers for GitHub Copilot. The configuration tells Copilot:
- Where to find your MCP server
- How to launch it
- What environment variables to provide

### Configuration Location

Open your VS Code settings:
- **Mac**: `~/Library/Application Support/Code/User/settings.json`
- **Windows**: `%APPDATA%\Code\User\settings.json`
- **Linux**: `~/.config/Code/User/settings.json`

Or use VS Code UI:
1. Press `Cmd/Ctrl + Shift + P`
2. Type "Preferences: Open User Settings (JSON)"

### Basic Configuration

Add your MCP server to the configuration:

```json
{
  "github.copilot.chat.mcp.servers": {
    "calculator": {
      "command": "node",
      "args": ["/absolute/path/to/calculator-mcp-server/dist/index.js"]
    }
  }
}
```

### Advanced Configuration with Environment Variables

```json
{
  "github.copilot.chat.mcp.servers": {
    "weather": {
      "command": "node",
      "args": ["${workspaceFolder}/weather-server/dist/index.js"],
      "env": {
        "WEATHER_API_KEY": "your-api-key-here",
        "NODE_ENV": "production",
        "LOG_LEVEL": "debug"
      }
    },
    "database": {
      "command": "npx",
      "args": [
        "tsx",
        "${workspaceFolder}/database-server/src/index.ts"
      ],
      "env": {
        "DB_PATH": "${workspaceFolder}/data/app.db",
        "DB_READONLY": "false"
      }
    }
  }
}
```

### Using Variables

VS Code supports several variables in configurations:

- `${workspaceFolder}` - The workspace root path
- `${workspaceFolderBasename}` - Workspace folder name
- `${file}` - Current opened file
- `${fileBasename}` - Current file name
- `${env:NAME}` - Environment variable

## Part 2: Testing Your Integration (15 minutes)

### Step 1: Restart VS Code

After changing configuration, restart VS Code:
```
Cmd/Ctrl + Shift + P → Developer: Reload Window
```

### Step 2: Open Copilot Chat

Open Copilot Chat panel:
```
Cmd/Ctrl + Shift + I
```

Or click the chat icon in the activity bar.

### Step 3: Verify MCP Server Connection

In Copilot Chat, type:
```
@workspace List the available MCP tools
```

You should see your server's tools listed.

### Step 4: Test a Tool

Try using one of your tools:
```
@workspace Use the calculator to add 42 and 58
```

### Step 5: Check for Errors

If tools don't appear, check:

1. **VS Code Output Panel** (`Cmd/Ctrl + Shift + U`):
   - Select "GitHub Copilot Chat" from dropdown
   - Look for connection errors

2. **Server Logs**:
   - Add logging to your server
   - Check if server is starting correctly

3. **Path Issues**:
   - Use absolute paths
   - Ensure file exists and is executable

## Part 3: Creating User-Friendly Tools (15 minutes)

### Good Tool Descriptions

Tools should be self-documenting for the AI to use them effectively.

**Bad Example:**
```typescript
{
  name: "calc",
  description: "Does math",
  inputSchema: {
    type: "object",
    properties: {
      x: { type: "number" },
      y: { type: "number" },
      op: { type: "string" }
    }
  }
}
```

**Good Example:**
```typescript
{
  name: "calculate",
  description: "Perform mathematical operations on two numbers. " +
    "Supports: add, subtract, multiply, divide, power, and modulo. " +
    "Example: calculate(a=10, b=5, operation='multiply') returns 50",
  inputSchema: {
    type: "object",
    properties: {
      a: {
        type: "number",
        description: "First operand (any real number)"
      },
      b: {
        type: "number",
        description: "Second operand (any real number, cannot be 0 for division)"
      },
      operation: {
        type: "string",
        enum: ["add", "subtract", "multiply", "divide", "power", "modulo"],
        description: "Mathematical operation to perform",
        default: "add"
      }
    },
    required: ["a", "b"]
  }
}
```

### Response Formatting

Make responses easy to parse:

**For Structured Data:**
```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({
      result: 50,
      operation: "multiply",
      formula: "10 × 5 = 50"
    }, null, 2)
  }]
};
```

**For User-Friendly Messages:**
```typescript
return {
  content: [{
    type: "text",
    text: "✓ Book successfully added to catalog\n\n" +
          "Title: The Great Gatsby\n" +
          "Author: F. Scott Fitzgerald\n" +
          "ISBN: 978-0743273565\n" +
          "Status: Available"
  }]
};
```

## Part 4: Debugging and Troubleshooting (15 minutes)

### Common Issues

#### Issue 1: Server Not Found

**Error**: "MCP server 'myserver' failed to start"

**Solutions**:
- Use absolute paths: `"/Users/you/projects/server/dist/index.js"`
- Or use workspace variable: `"${workspaceFolder}/server/dist/index.js"`
- Check file permissions: `chmod +x dist/index.js`

#### Issue 2: Tools Not Appearing

**Symptoms**: Server starts but tools don't show up

**Debug Steps**:
1. Add logging to your server:
```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  console.error("Tools requested"); // Logs to VS Code output
  const tools = [...];
  console.error(`Returning ${tools.length} tools`);
  return { tools };
});
```

2. Check VS Code output panel for errors

3. Verify tool schema is valid JSON Schema

#### Issue 3: Tool Call Errors

**Symptoms**: Tool calls fail or return errors

**Debug**:
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  console.error("Tool call:", JSON.stringify(request.params, null, 2));
  
  try {
    // Your tool logic
    const result = executeTool(request.params);
    console.error("Success:", result);
    return { content: [{ type: "text", text: result }] };
  } catch (error) {
    console.error("Error:", error);
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true
    };
  }
});
```

### Enabling Debug Mode

Add debug logging to your server:

```typescript
const DEBUG = process.env.DEBUG === "true";

function debug(...args: any[]) {
  if (DEBUG) {
    console.error("[DEBUG]", ...args);
  }
}

// Usage
debug("Server initialized");
debug("Received request:", request);
```

Configure in settings.json:
```json
{
  "github.copilot.chat.mcp.servers": {
    "myserver": {
      "command": "node",
      "args": ["dist/index.js"],
      "env": {
        "DEBUG": "true"
      }
    }
  }
}
```

### Testing Standalone

Test your server independently before VS Code integration:

```bash
# Test with MCP inspector
npx @modelcontextprotocol/inspector node dist/index.js

# Or create a simple test client
node test-client.js
```

## Part 5: Best Practices (10 minutes)

### 1. Security

**Never hardcode secrets:**
```json
// ❌ Bad
{
  "env": {
    "API_KEY": "sk-1234567890abcdef"
  }
}

// ✅ Good - Use environment variables
{
  "env": {
    "API_KEY": "${env:MY_API_KEY}"
  }
}
```

Set environment variables in your shell:
```bash
export MY_API_KEY="sk-1234567890abcdef"
```

### 2. Error Messages

Provide actionable error messages:

```typescript
// ❌ Bad
throw new Error("Invalid input");

// ✅ Good
throw new Error(
  "Invalid input: 'priority' must be one of: low, medium, high, urgent. " +
  "Received: '${priority}'"
);
```

### 3. Tool Organization

Group related tools:

```json
{
  "github.copilot.chat.mcp.servers": {
    "database-tools": {
      "command": "node",
      "args": ["${workspaceFolder}/servers/database/dist/index.js"]
    },
    "api-tools": {
      "command": "node", 
      "args": ["${workspaceFolder}/servers/api/dist/index.js"]
    },
    "devops-tools": {
      "command": "node",
      "args": ["${workspaceFolder}/servers/devops/dist/index.js"]
    }
  }
}
```

### 4. Performance

- Keep tools fast (< 5 seconds)
- Cache when appropriate
- Show progress for long operations

### 5. Documentation

Document your server for team members:

Create `README.md`:
```markdown
# Project MCP Servers

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Build servers:
   ```bash
   npm run build
   ```

3. Configure VS Code:
   Copy `vscode-settings-template.json` to your VS Code settings

4. Set environment variables:
   ```bash
   export MY_API_KEY="..."
   ```

## Available Tools

### database-tools
- `query_database` - Execute SQL queries
- `get_schema` - View database schema

### api-tools
- `call_api` - Make HTTP requests
- `validate_response` - Check API responses
```

## Exercises

### Exercise 1: Multi-Server Setup

Configure three different MCP servers:
1. Calculator (from Lab 1)
2. Task manager (from Lab 2)
3. Library system (from Lab 3)

Test that all tools are available in Copilot Chat.

### Exercise 2: Create a Debug Config

Create a launch configuration for debugging your MCP server:

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug MCP Server",
      "program": "${workspaceFolder}/src/index.ts",
      "runtimeArgs": ["-r", "tsx"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Exercise 3: Create a Settings Template

Create a `vscode-settings-template.json` for your team:
- Include all server configurations
- Use variables for paths
- Document required environment variables
- Add comments explaining each setting

## Verification Checklist

- [ ] Server starts without errors
- [ ] Tools appear in Copilot Chat
- [ ] Tools execute successfully
- [ ] Errors are handled gracefully
- [ ] No secrets in configuration files
- [ ] Documentation is complete

## Next Steps

- [Lab 5: Advanced Features and Optimization](lab5-advanced-features.md)
- Review [Integration Patterns](../examples/integration-patterns.md)

## Additional Resources

- [VS Code Settings Documentation](https://code.visualstudio.com/docs/getstarted/settings)
- [GitHub Copilot MCP Guide](https://docs.github.com/copilot/using-github-copilot/using-mcp-with-github-copilot)
- [Environment Variables Best Practices](https://12factor.net/config)
