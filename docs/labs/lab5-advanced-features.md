# Lab 5: Advanced Features and Optimization

**Duration**: 90-120 minutes  
**Difficulty**: Advanced  
**Prerequisites**: Labs 1-4, Understanding of async programming

## Learning Objectives

- Implement resources and prompts
- Add caching and performance optimization
- Handle concurrent requests
- Implement progress notifications
- Deploy MCP servers for production use

## Part 1: Resources (25 minutes)

Resources provide context to the AI assistant. They're read-only data sources.

### Example: File System Resource

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { readFileSync, readdirSync, statSync } from "fs";
import { join } from "path";

// List available resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "file:///config/app.json",
        name: "Application Configuration",
        description: "Main application config file",
        mimeType: "application/json",
      },
      {
        uri: "file:///logs/latest",
        name: "Latest Application Logs",
        description: "Most recent 100 log entries",
        mimeType: "text/plain",
      },
      {
        uri: "directory:///docs",
        name: "Documentation Directory",
        description: "Project documentation files",
        mimeType: "text/markdown",
      },
    ],
  };
});

// Read resource content
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri.startsWith("file://")) {
    const filePath = uri.replace("file://", "");
    try {
      const content = readFileSync(filePath, "utf-8");
      return {
        contents: [
          {
            uri: uri,
            mimeType: getMimeType(filePath),
            text: content,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Failed to read file: ${error.message}`);
    }
  }

  if (uri.startsWith("directory://")) {
    const dirPath = uri.replace("directory://", "");
    try {
      const files = readdirSync(dirPath);
      const fileList = files.map((file) => {
        const stats = statSync(join(dirPath, file));
        return `${file} (${stats.isDirectory() ? "dir" : "file"}, ${stats.size} bytes)`;
      });

      return {
        contents: [
          {
            uri: uri,
            mimeType: "text/plain",
            text: fileList.join("\n"),
          },
        ],
      };
    } catch (error) {
      throw new Error(`Failed to read directory: ${error.message}`);
    }
  }

  throw new Error(`Unknown resource URI: ${uri}`);
});

function getMimeType(filePath: string): string {
  if (filePath.endsWith(".json")) return "application/json";
  if (filePath.endsWith(".md")) return "text/markdown";
  if (filePath.endsWith(".txt")) return "text/plain";
  return "application/octet-stream";
}
```

### Dynamic Resources

Resources can be dynamic:

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  // Query database for available datasets
  const datasets = await db.query("SELECT name, description FROM datasets");

  return {
    resources: datasets.map((ds) => ({
      uri: `dataset://${ds.name}`,
      name: ds.name,
      description: ds.description,
      mimeType: "application/json",
    })),
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri.startsWith("dataset://")) {
    const datasetName = uri.replace("dataset://", "");
    const data = await db.query(
      "SELECT * FROM datasets WHERE name = ?",
      [datasetName]
    );

    return {
      contents: [
        {
          uri: uri,
          mimeType: "application/json",
          text: JSON.stringify(data, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

## Part 2: Prompts (20 minutes)

Prompts are pre-defined conversation templates.

```typescript
import {
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "analyze_code",
        description: "Analyze code for potential issues and improvements",
        arguments: [
          {
            name: "file_path",
            description: "Path to the code file",
            required: true,
          },
          {
            name: "focus",
            description: "What to focus on: security, performance, or style",
            required: false,
          },
        ],
      },
      {
        name: "generate_tests",
        description: "Generate unit tests for a given function",
        arguments: [
          {
            name: "function_name",
            description: "Name of the function to test",
            required: true,
          },
          {
            name: "test_framework",
            description: "Testing framework (jest, mocha, pytest, etc.)",
            required: false,
          },
        ],
      },
      {
        name: "explain_error",
        description: "Explain an error message and suggest fixes",
        arguments: [
          {
            name: "error_message",
            description: "The error message or stack trace",
            required: true,
          },
        ],
      },
    ],
  };
});

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "analyze_code": {
      const filePath = args?.file_path as string;
      const focus = (args?.focus as string) || "general";

      // Read the file
      const code = readFileSync(filePath, "utf-8");

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `Please analyze this code with a focus on ${focus}:\n\n\`\`\`\n${code}\n\`\`\`\n\n` +
                `Provide specific recommendations for improvement.`,
            },
          },
        ],
      };
    }

    case "generate_tests": {
      const functionName = args?.function_name as string;
      const framework = (args?.test_framework as string) || "jest";

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `Generate comprehensive unit tests for the function "${functionName}" ` +
                `using ${framework}. Include:\n` +
                `- Happy path tests\n` +
                `- Edge cases\n` +
                `- Error conditions\n` +
                `- Mock any dependencies`,
            },
          },
        ],
      };
    }

    case "explain_error": {
      const errorMessage = args?.error_message as string;

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `I'm getting this error:\n\n\`\`\`\n${errorMessage}\n\`\`\`\n\n` +
                `Please:\n` +
                `1. Explain what this error means\n` +
                `2. Identify the likely cause\n` +
                `3. Provide specific steps to fix it`,
            },
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown prompt: ${name}`);
  }
});
```

## Part 3: Performance Optimization (25 minutes)

### Caching

Implement intelligent caching:

```typescript
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  expiresIn: number;
}

class Cache<T> {
  private cache = new Map<string, CacheEntry<T>>();

  set(key: string, data: T, expiresIn: number = 300000) {
    // Default 5 minutes
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      expiresIn,
    });
  }

  get(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    if (Date.now() - entry.timestamp > entry.expiresIn) {
      this.cache.delete(key);
      return null;
    }

    return entry.data;
  }

  clear() {
    this.cache.clear();
  }

  size() {
    return this.cache.size;
  }
}

// Usage
const responseCache = new Cache<any>();

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  // Create cache key
  const cacheKey = `${name}:${JSON.stringify(args)}`;

  // Check cache
  const cached = responseCache.get(cacheKey);
  if (cached) {
    console.error(`Cache hit for ${name}`);
    return cached;
  }

  // Execute tool
  console.error(`Cache miss for ${name}`);
  const result = await executeTool(name, args);

  // Cache result (with appropriate TTL based on data type)
  const ttl = getCacheTTL(name);
  responseCache.set(cacheKey, result, ttl);

  return result;
});

function getCacheTTL(toolName: string): number {
  // Static data: 1 hour
  if (toolName === "get_config") return 3600000;

  // User data: 5 minutes
  if (toolName.startsWith("get_user")) return 300000;

  // Dynamic data: 30 seconds
  return 30000;
}
```

### Request Pooling

Handle concurrent requests efficiently:

```typescript
class RequestPool {
  private pending = new Map<string, Promise<any>>();

  async execute<T>(key: string, fn: () => Promise<T>): Promise<T> {
    // If already running, return existing promise
    const existing = this.pending.get(key);
    if (existing) {
      console.error(`Request pooling: reusing ${key}`);
      return existing;
    }

    // Execute and store promise
    const promise = fn()
      .finally(() => {
        this.pending.delete(key);
      });

    this.pending.set(key, promise);
    return promise;
  }
}

const requestPool = new RequestPool();

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const key = `${name}:${JSON.stringify(args)}`;

  return requestPool.execute(key, async () => {
    return await executeTool(name, args);
  });
});
```

### Streaming Large Responses

For large datasets, consider streaming:

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "export_data") {
    const totalRecords = await db.count();
    const batchSize = 1000;

    let processed = 0;
    const chunks: string[] = [];

    for (let i = 0; i < totalRecords; i += batchSize) {
      const batch = await db.getBatch(i, batchSize);
      chunks.push(JSON.stringify(batch));

      processed += batch.length;

      // Send progress notification
      if (request.params._meta?.progressToken) {
        await server.notification({
          method: "notifications/progress",
          params: {
            progressToken: request.params._meta.progressToken,
            progress: processed,
            total: totalRecords,
          },
        });
      }
    }

    return {
      content: [
        {
          type: "text",
          text: `[${chunks.join(",\n")}]`,
        },
      ],
    };
  }
});
```

## Part 4: Production Deployment (25 minutes)

### Environment Configuration

```typescript
// config.ts
import { config } from "dotenv";

config();

export const CONFIG = {
  // Server settings
  server: {
    name: process.env.SERVER_NAME || "my-mcp-server",
    version: process.env.SERVER_VERSION || "1.0.0",
  },

  // Database
  database: {
    path: process.env.DB_PATH || "./data/app.db",
    readonly: process.env.DB_READONLY === "true",
  },

  // API keys
  api: {
    openai: process.env.OPENAI_API_KEY,
    github: process.env.GITHUB_TOKEN,
  },

  // Performance
  cache: {
    enabled: process.env.CACHE_ENABLED !== "false",
    ttl: parseInt(process.env.CACHE_TTL || "300000"),
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || "info",
    pretty: process.env.LOG_PRETTY === "true",
  },
};

// Validation
if (!CONFIG.api.github) {
  throw new Error("GITHUB_TOKEN environment variable is required");
}
```

### Structured Logging

```typescript
enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

class Logger {
  constructor(private level: LogLevel = LogLevel.INFO) {}

  private log(level: LogLevel, message: string, meta?: any) {
    if (level < this.level) return;

    const timestamp = new Date().toISOString();
    const levelName = LogLevel[level];

    const logEntry = {
      timestamp,
      level: levelName,
      message,
      ...meta,
    };

    console.error(JSON.stringify(logEntry));
  }

  debug(message: string, meta?: any) {
    this.log(LogLevel.DEBUG, message, meta);
  }

  info(message: string, meta?: any) {
    this.log(LogLevel.INFO, message, meta);
  }

  warn(message: string, meta?: any) {
    this.log(LogLevel.WARN, message, meta);
  }

  error(message: string, error?: Error, meta?: any) {
    this.log(LogLevel.ERROR, message, {
      error: error ? {
        message: error.message,
        stack: error.stack,
      } : undefined,
      ...meta,
    });
  }
}

const logger = new Logger(
  LogLevel[CONFIG.logging.level.toUpperCase() as keyof typeof LogLevel]
);

// Usage
logger.info("Server started", { tools: tools.length });
logger.error("Tool execution failed", error, { tool: name });
```

### Health Checks

```typescript
// Add a health check tool
{
  name: "health_check",
  description: "Check server health and status",
  inputSchema: {
    type: "object",
    properties: {}
  }
}

// Handler
case "health_check": {
  const health = {
    status: "healthy",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    cache: {
      size: responseCache.size(),
    },
    database: {
      connected: await db.ping(),
    },
  };

  return {
    content: [{
      type: "text",
      text: JSON.stringify(health, null, 2)
    }]
  };
}
```

### Error Tracking

```typescript
interface ErrorLog {
  timestamp: string;
  tool: string;
  error: string;
  stack?: string;
  args?: any;
}

const errorLog: ErrorLog[] = [];
const MAX_ERROR_LOG = 100;

function logError(tool: string, error: Error, args?: any) {
  errorLog.unshift({
    timestamp: new Date().toISOString(),
    tool,
    error: error.message,
    stack: error.stack,
    args,
  });

  // Keep only last N errors
  if (errorLog.length > MAX_ERROR_LOG) {
    errorLog.length = MAX_ERROR_LOG;
  }
}

// Add diagnostic tool
{
  name: "get_recent_errors",
  description: "Get recent error logs for debugging",
  inputSchema: {
    type: "object",
    properties: {
      limit: {
        type: "integer",
        default: 10,
        description: "Number of recent errors to return"
      }
    }
  }
}
```

## Part 5: Exercises (20 minutes)

### Exercise 1: Implement Rate Limiting

Add rate limiting to prevent abuse:
- Limit requests per minute per tool
- Return appropriate error messages
- Log rate limit violations

### Exercise 2: Add Metrics Collection

Track:
- Tool call counts
- Average response times
- Error rates
- Cache hit rates

Create a `get_metrics` tool to retrieve this data.

### Exercise 3: Implement Circuit Breaker

For external API calls:
- Track failure rates
- Open circuit after threshold
- Automatically recover after cooldown

## Key Takeaways

- Resources provide read-only context to AI
- Prompts enable consistent conversation patterns
- Caching dramatically improves performance
- Proper logging enables debugging in production
- Health checks and metrics are essential for monitoring

## Final Project

Combine everything you've learned to build a complete MCP server with:
- Multiple tools across different categories
- Resources for documentation and configuration
- Prompts for common tasks
- Caching and performance optimization
- Production-ready logging and monitoring
- Comprehensive error handling
- Full test coverage

## Congratulations!

You've completed all five labs. You now have the skills to build production-ready MCP servers for GitHub Copilot.

## Additional Resources

- [MCP Best Practices](https://modelcontextprotocol.io/docs/best-practices)
- [Production Deployment Guide](../examples/production-deployment.md)
- [Community Examples](https://github.com/topics/model-context-protocol)
