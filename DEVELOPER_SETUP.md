# Developer Setup Guide

This guide will help you set up your development environment to work on the CoPilot-Developers project and learn how to build your own AI-enhanced applications.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **VS Code**: [Download VS Code](https://code.visualstudio.com/)
- **GitHub Account**: [Sign up](https://github.com/signup)

### Recommended Extensions (VS Code)

1. **GitHub Copilot** - AI-powered code completion
2. **GitHub Copilot Chat** - Conversational AI assistance
3. **Python** - Python language support
4. **REST Client** or **Thunder Client** - API testing

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/CoPilot-Developers.git
cd CoPilot-Developers

# Add upstream remote
git remote add upstream https://github.com/CarlSp8/CoPilot-Developers.git
```

### 2. Set Up Python Environment

#### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using conda

```bash
# Create conda environment
conda create -n copilot-dev python=3.10
conda activate copilot-dev

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Navigate to src directory
cd src

# Run with uvicorn
python -m uvicorn app:app --reload

# Or use the shortcut
python app.py
```

The application will be available at:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 4. Set Up GitHub Copilot with MCP

1. **Install GitHub Copilot in VS Code**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
   - Search for "GitHub Copilot"
   - Install and sign in

2. **Create MCP Configuration**
   
   The `.vscode/mcp.json` file should already exist. If not, create it:
   
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

3. **Start MCP Server**
   - Open `.vscode/mcp.json` in VS Code
   - Click the "Start" button that appears
   - Authenticate with GitHub when prompted

4. **Verify Installation**
   - Open Copilot Chat panel
   - Click the tools icon (🛠️)
   - You should see GitHub tools available

## 🔧 Development Workflow

### Making Changes

1. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Edit files as needed
   - Test locally
   - Commit frequently

3. **Test Your Changes**
   ```bash
   # Run the application
   cd src
   python -m uvicorn app:app --reload
   
   # Test API endpoints
   curl http://localhost:8000/activities
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the description
   - Submit for review

### Using VS Code Debugger

The project includes a debug configuration. To use it:

1. Open the Run and Debug panel (Ctrl+Shift+D or Cmd+Shift+D)
2. Select "Python: FastAPI" from the dropdown
3. Press F5 or click the green play button
4. Set breakpoints by clicking left of line numbers
5. Debug your code interactively

## 🧪 Testing

### Manual API Testing

Using curl:

```bash
# Get all activities
curl http://localhost:8000/activities

# Sign up for an activity
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=test@mergington.edu"

# Unregister from an activity
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/unregister?email=test@mergington.edu"
```

Using VS Code REST Client extension:

Create a file `test.http`:

```http
### Get all activities
GET http://localhost:8000/activities

### Sign up for Chess Club
POST http://localhost:8000/activities/Chess%20Club/signup?email=test@mergington.edu

### Unregister from Chess Club
DELETE http://localhost:8000/activities/Chess%20Club/unregister?email=test@mergington.edu
```

### Interactive API Testing

Visit http://localhost:8000/docs for Swagger UI:
- View all endpoints
- Try API calls directly in the browser
- See request/response schemas

## 🎨 Project Structure

```
CoPilot-Developers/
├── .devcontainer/         # Development container configuration
├── .github/              # GitHub Actions and workflows
├── .vscode/              # VS Code settings and MCP config
│   ├── launch.json       # Debug configurations
│   └── mcp.json         # MCP server configuration
├── src/                  # Application source code
│   ├── static/          # Frontend files (HTML, CSS, JS)
│   ├── app.py           # Main FastAPI application
│   └── README.md        # Application documentation
├── ARCHITECTURE.md       # System architecture guide
├── CONTRIBUTING.md       # Contribution guidelines
├── DEVELOPER_SETUP.md    # This file
├── README.md            # Project overview
├── requirements.txt     # Python dependencies
└── LICENSE              # MIT License
```

## 📦 Dependencies

The project uses the following main dependencies:

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type hints

See `requirements.txt` for the complete list.

### Adding New Dependencies

1. Add the package to `requirements.txt`
2. Install it: `pip install -r requirements.txt`
3. Document why it's needed in your PR

## 🐛 Troubleshooting

### Common Issues

**Issue: Port 8000 already in use**

```bash
# Find the process
# On Windows:
netstat -ano | findstr :8000
# On macOS/Linux:
lsof -i :8000

# Kill the process or use a different port
python -m uvicorn app:app --reload --port 8001
```

**Issue: Module not found**

```bash
# Ensure you're in the virtual environment
# Install dependencies again
pip install -r requirements.txt
```

**Issue: MCP server not starting**

- Ensure you're signed in to GitHub Copilot
- Check that `.vscode/mcp.json` is properly formatted
- Try restarting VS Code
- Check VS Code output panel for errors

**Issue: Changes not reflecting**

- Ensure `--reload` flag is used with uvicorn
- Check the terminal for error messages
- Try clearing your browser cache

### Getting Help

If you encounter issues:

1. Check existing [Issues](https://github.com/CarlSp8/CoPilot-Developers/issues)
2. Search [Discussions](https://github.com/CarlSp8/CoPilot-Developers/discussions)
3. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

## 🔄 Keeping Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream changes into your main branch
git checkout main
git merge upstream/main

# Push updates to your fork
git push origin main
```

## 🌟 Tips for Success

1. **Use GitHub Copilot**: Ask it to explain code, suggest improvements, or generate boilerplate
2. **Read the Docs**: Familiarize yourself with FastAPI and MCP documentation
3. **Start Small**: Begin with minor changes to understand the codebase
4. **Ask Questions**: The community is here to help
5. **Have Fun**: Enjoy learning and building!

## 📚 Additional Resources

### Learning Materials

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Community

- [GitHub Discussions](https://github.com/CarlSp8/CoPilot-Developers/discussions)
- [FastAPI Discord](https://discord.com/invite/fastapi)
- [GitHub Community](https://github.community/)

## ✅ Checklist

Before you start developing:

- [ ] Python 3.8+ installed
- [ ] VS Code installed with required extensions
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application runs successfully
- [ ] MCP server configured and started
- [ ] GitHub Copilot working in VS Code

You're all set! Happy coding! 🚀

---

Need help? Check [CONTRIBUTING.md](CONTRIBUTING.md) or open an [issue](https://github.com/CarlSp8/CoPilot-Developers/issues).
