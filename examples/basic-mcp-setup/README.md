# Basic MCP Setup Tutorial

This tutorial will guide you through setting up Model Context Protocol (MCP) with GitHub Copilot from scratch.

## 🎯 Learning Objectives

By the end of this tutorial, you will:
- Understand what MCP is and why it's useful
- Set up an MCP server configuration
- Connect GitHub Copilot to external services
- Test the integration
- Use MCP tools in your development workflow

## 📋 Prerequisites

- VS Code installed
- GitHub Copilot subscription and extension installed
- Basic understanding of JSON
- GitHub account

## ⏱️ Estimated Time: 15 minutes

---

## Step 1: Understanding MCP (5 minutes)

**What is Model Context Protocol (MCP)?**

MCP is like "USB-C for AI" - a universal connector that allows GitHub Copilot to interact with external services seamlessly.

**Why use MCP?**

Without MCP:
```
Developer → Manual API calls → External Service
           ↓
        Copy/paste data
           ↓
        Manually write code
```

With MCP:
```
Developer → Natural language request → Copilot → MCP → External Service
                                         ↓
                                  Automatic code generation
```

**Benefits**:
- Less context switching
- Faster development
- Consistent patterns
- AI-powered automation

---

## Step 2: Create MCP Configuration (3 minutes)

1. **Open VS Code** in your project directory

2. **Create the `.vscode` directory** if it doesn't exist:
   ```bash
   mkdir -p .vscode
   ```

3. **Create `.vscode/mcp.json`** with this content:

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

**What does this configuration do?**

- `servers`: Defines available MCP servers
- `github`: Name identifier for this server
- `type`: Protocol type (http, stdio, etc.)
- `url`: Endpoint for the MCP server

---

## Step 3: Start the MCP Server (2 minutes)

1. **Open `.vscode/mcp.json`** in VS Code

2. You should see a **"Start"** button appear at the top of the file
   
   ![MCP Start Button](https://github.com/user-attachments/assets/15a3d885-1c13-40b4-8d59-87b478ddd8a0)

3. **Click "Start"**

4. **Authenticate with GitHub** when prompted
   - A browser window will open
   - Sign in to GitHub
   - Authorize the connection

5. **Verify success** - You should see a green indicator

---

## Step 4: Explore Available Tools (3 minutes)

1. **Open GitHub Copilot Chat** (Ctrl+Shift+I or Cmd+Shift+I)

2. **Enable Agent Mode** - Look for the toggle at the top

3. **Click the tools icon** (🛠️) to see available capabilities

You should see GitHub-related tools like:
- List issues
- Create issues
- Search repositories
- Get file contents
- And more!

---

## Step 5: Test the Integration (2 minutes)

Let's test it! Try these prompts in Copilot Chat:

### Test 1: List Issues
```
@workspace List all open issues in this repository
```

Expected: Copilot uses GitHub MCP to fetch and display issues

### Test 2: Search Code
```
@workspace Find all Python files in this repository
```

Expected: Copilot searches using GitHub tools

### Test 3: Create Content
```
@workspace Help me create a README for this project
```

Expected: Copilot generates README with repository context

---

## 🎉 Congratulations!

You've successfully set up MCP with GitHub Copilot!

## 🚀 Next Steps

Now that you have MCP configured, you can:

1. **Explore more capabilities**: Try different prompts and see what Copilot can do
2. **Build an API**: Move to the [Simple API tutorial](../simple-api/)
3. **Add more MCP servers**: Connect to other services
4. **Customize your workflow**: Integrate MCP into your daily development

## 📚 Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Full Application Example](../../src/)

## 💡 Pro Tips

1. **Use Agent Mode**: Always enable Agent mode for complex tasks
2. **Be Specific**: Clear prompts get better results
3. **Iterate**: If you don't get what you want, refine your prompt
4. **Explore Tools**: Click the 🛠️ icon to see what's available
5. **Context Matters**: Copilot works better with good documentation

## 🐛 Troubleshooting

**MCP server won't start?**
- Ensure you're signed in to GitHub Copilot
- Check your internet connection
- Try restarting VS Code

**Don't see GitHub tools?**
- Verify the MCP server is running (green indicator)
- Check the VS Code output panel for errors
- Ensure your GitHub Copilot subscription is active

**Authentication fails?**
- Clear browser cache and try again
- Ensure you're using the correct GitHub account
- Check if you need 2FA

## ❓ Questions?

- Check the main [README](../../README.md)
- Open an [issue](https://github.com/CarlSp8/CoPilot-Developers/issues)
- Ask in [discussions](https://github.com/CarlSp8/CoPilot-Developers/discussions)

---

**Ready for more?** Continue to the [Simple API tutorial](../simple-api/) to build something with your new MCP powers!
