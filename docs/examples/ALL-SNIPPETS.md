# 30+ MCP Code Snippets

A comprehensive collection of code snippets for building MCP servers.

## Basic Examples (Snippets 1-10)

### 1. Hello World Server
```typescript
const server = new Server({ name: "hello", version: "1.0.0" }, { capabilities: { tools: {} } });
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{ name: "greet", description: "Say hello", inputSchema: { type: "object", properties: { name: { type: "string" } } } }]
}));
```

### 2. Simple Calculator Tool
```typescript
{
  name: "add",
  description: "Add two numbers",
  inputSchema: {
    type: "object",
    properties: {
      a: { type: "number" },
      b: { type: "number" }
    },
    required: ["a", "b"]
  }
}
```

### 3. String Manipulation Tool
```typescript
{
  name: "reverse_string",
  description: "Reverse a string",
  inputSchema: {
    type: "object",
    properties: {
      text: { type: "string", description: "Text to reverse" }
    },
    required: ["text"]
  }
}
// Handler:
if (name === "reverse_string") {
  const text = args.text as string;
  return { content: [{ type: "text", text: text.split("").reverse().join("") }] };
}
```

### 4. Input Validation with Zod
```typescript
import { z } from "zod";

const EmailSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100)
});

// In handler:
const validated = EmailSchema.parse(args);
```

### 5. Error Handling Pattern
```typescript
try {
  const result = await performOperation(args);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
} catch (error) {
  return {
    content: [{ type: "text", text: `Error: ${error.message}` }],
    isError: true
  };
}
```

### 6. Environment Variables
```typescript
const CONFIG = {
  apiKey: process.env.API_KEY || "",
  port: parseInt(process.env.PORT || "8080"),
  debug: process.env.DEBUG === "true"
};

if (!CONFIG.apiKey) {
  throw new Error("API_KEY environment variable is required");
}
```

### 7. JSON Response Formatting
```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    }, null, 2)
  }]
};
```

### 8. File Read Tool
```typescript
import { readFileSync } from "fs";

{
  name: "read_file",
  description: "Read a file's contents",
  inputSchema: {
    type: "object",
    properties: {
      path: { type: "string", description: "File path" }
    },
    required: ["path"]
  }
}
// Handler:
const content = readFileSync(args.path as string, "utf-8");
return { content: [{ type: "text", text: content }] };
```

### 9. HTTP GET Request
```typescript
{
  name: "fetch_url",
  description: "Fetch content from a URL",
  inputSchema: {
    type: "object",
    properties: {
      url: { type: "string", format: "uri" }
    },
    required: ["url"]
  }
}
// Handler:
const response = await fetch(args.url as string);
const data = await response.text();
return { content: [{ type: "text", text: data }] };
```

### 10. Date/Time Tools
```typescript
{
  name: "current_time",
  description: "Get current time in various formats",
  inputSchema: {
    type: "object",
    properties: {
      format: {
        type: "string",
        enum: ["iso", "unix", "locale"],
        default: "iso"
      },
      timezone: { type: "string", description: "IANA timezone" }
    }
  }
}
// Handler:
const now = new Date();
const format = args.format || "iso";
if (format === "iso") return { content: [{ type: "text", text: now.toISOString() }] };
if (format === "unix") return { content: [{ type: "text", text: String(Math.floor(now.getTime() / 1000)) }] };
```

## Intermediate Examples (Snippets 11-20)

### 11. Resource Provider
```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [{
    uri: "config://app",
    name: "Application Config",
    mimeType: "application/json"
  }]
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  if (request.params.uri === "config://app") {
    return {
      contents: [{
        uri: request.params.uri,
        mimeType: "application/json",
        text: JSON.stringify(config)
      }]
    };
  }
});
```

### 12. Prompt Template
```typescript
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [{
    name: "code_review",
    description: "Review code for issues",
    arguments: [{
      name: "code",
      description: "Code to review",
      required: true
    }]
  }]
}));

server.setRequestHandler(GetPromptRequestSchema, async (request) => ({
  messages: [{
    role: "user",
    content: {
      type: "text",
      text: `Review this code:\n\n${request.params.arguments?.code}\n\nFocus on: security, performance, best practices`
    }
  }]
}));
```

### 13. State Management
```typescript
class ServerState {
  private data = new Map<string, any>();
  
  set(key: string, value: any) {
    this.data.set(key, value);
  }
  
  get(key: string): any {
    return this.data.get(key);
  }
  
  has(key: string): boolean {
    return this.data.has(key);
  }
}

const state = new ServerState();
```

### 14. Async Queue Processing
```typescript
async function processQueue(items: any[]) {
  const results = [];
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
    
    // Send progress
    await server.notification({
      method: "notifications/progress",
      params: {
        progress: results.length,
        total: items.length
      }
    });
  }
  return results;
}
```

### 15. Progress Notifications
```typescript
async function longRunningOperation(request: any) {
  const total = 100;
  for (let i = 0; i <= total; i += 10) {
    await doWork();
    
    if (request.params._meta?.progressToken) {
      await server.notification({
        method: "notifications/progress",
        params: {
          progressToken: request.params._meta.progressToken,
          progress: i,
          total: total
        }
      });
    }
  }
}
```

### 16. Data Transformation Pipeline
```typescript
const transform = (data: any[]) => 
  data
    .filter(item => item.active)
    .map(item => ({
      id: item.id,
      name: item.name.toUpperCase(),
      processed: true
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
```

### 17. API Key Authentication
```typescript
function validateApiKey(apiKey: string): boolean {
  const validKeys = (process.env.VALID_API_KEYS || "").split(",");
  return validKeys.includes(apiKey);
}

// In tool handler:
const apiKey = args.apiKey as string;
if (!validateApiKey(apiKey)) {
  return {
    content: [{ type: "text", text: "Invalid API key" }],
    isError: true
  };
}
```

### 18. Rate Limiter
```typescript
class RateLimiter {
  private requests = new Map<string, number[]>();
  
  isAllowed(key: string, maxRequests: number, windowMs: number): boolean {
    const now = Date.now();
    const requests = this.requests.get(key) || [];
    
    // Remove old requests
    const recent = requests.filter(time => now - time < windowMs);
    
    if (recent.length >= maxRequests) {
      return false;
    }
    
    recent.push(now);
    this.requests.set(key, recent);
    return true;
  }
}

const limiter = new RateLimiter();
```

### 19. Batch Operations
```typescript
{
  name: "batch_create",
  description: "Create multiple items at once",
  inputSchema: {
    type: "object",
    properties: {
      items: {
        type: "array",
        items: {
          type: "object",
          properties: {
            name: { type: "string" },
            value: { type: "string" }
          }
        }
      }
    }
  }
}
// Handler:
const results = await Promise.all(
  (args.items as any[]).map(item => createItem(item))
);
```

### 20. Retry Logic
```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
    }
  }
  throw new Error("Max retries exceeded");
}
```

## Advanced Examples (Snippets 21-33)

### 21. Connection Pool
```typescript
import Database from "better-sqlite3";

class DatabasePool {
  private connections: Database.Database[] = [];
  private available: Database.Database[] = [];
  
  constructor(private dbPath: string, private maxConnections: number = 5) {
    for (let i = 0; i < maxConnections; i++) {
      const conn = new Database(dbPath);
      this.connections.push(conn);
      this.available.push(conn);
    }
  }
  
  async acquire(): Promise<Database.Database> {
    while (this.available.length === 0) {
      await new Promise(resolve => setTimeout(resolve, 10));
    }
    return this.available.pop()!;
  }
  
  release(conn: Database.Database) {
    this.available.push(conn);
  }
}
```

### 22. Transaction Management
```typescript
async function withTransaction<T>(
  db: Database.Database,
  fn: () => T
): Promise<T> {
  return db.transaction(() => {
    try {
      return fn();
    } catch (error) {
      throw error; // Transaction will be rolled back
    }
  })();
}
```

### 23. Multi-Level Cache
```typescript
class MultiLevelCache {
  private l1 = new Map<string, any>(); // In-memory
  private l2: Database.Database; // Disk
  
  constructor(dbPath: string) {
    this.l2 = new Database(dbPath);
    this.l2.exec("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT, expires INTEGER)");
  }
  
  get(key: string): any | null {
    // Check L1
    if (this.l1.has(key)) return this.l1.get(key);
    
    // Check L2
    const stmt = this.l2.prepare("SELECT value, expires FROM cache WHERE key = ? AND expires > ?");
    const row = stmt.get(key, Date.now()) as any;
    if (row) {
      const value = JSON.parse(row.value);
      this.l1.set(key, value); // Promote to L1
      return value;
    }
    
    return null;
  }
  
  set(key: string, value: any, ttl: number = 300000) {
    this.l1.set(key, value);
    const stmt = this.l2.prepare("INSERT OR REPLACE INTO cache (key, value, expires) VALUES (?, ?, ?)");
    stmt.run(key, JSON.stringify(value), Date.now() + ttl);
  }
}
```

### 24. Circuit Breaker
```typescript
enum CircuitState {
  CLOSED,
  OPEN,
  HALF_OPEN
}

class CircuitBreaker {
  private state = CircuitState.CLOSED;
  private failureCount = 0;
  private lastFailureTime = 0;
  
  constructor(
    private threshold: number = 5,
    private timeout: number = 60000
  ) {}
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = CircuitState.HALF_OPEN;
      } else {
        throw new Error("Circuit breaker is OPEN");
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess() {
    this.failureCount = 0;
    this.state = CircuitState.CLOSED;
  }
  
  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.failureCount >= this.threshold) {
      this.state = CircuitState.OPEN;
    }
  }
}
```

### 25. Request Deduplication
```typescript
class RequestDeduplicator {
  private pending = new Map<string, Promise<any>>();
  
  async dedupe<T>(key: string, fn: () => Promise<T>): Promise<T> {
    const existing = this.pending.get(key);
    if (existing) return existing;
    
    const promise = fn().finally(() => {
      this.pending.delete(key);
    });
    
    this.pending.set(key, promise);
    return promise;
  }
}
```

### 26. Streaming Large Data
```typescript
async function* streamData(query: string) {
  const batchSize = 1000;
  let offset = 0;
  
  while (true) {
    const batch = await db.query(`${query} LIMIT ${batchSize} OFFSET ${offset}`);
    if (batch.length === 0) break;
    
    for (const item of batch) {
      yield item;
    }
    
    offset += batchSize;
  }
}
```

### 27. Message Queue Integration
```typescript
import { Queue } from "bullmq";

const taskQueue = new Queue("tasks", {
  connection: {
    host: "localhost",
    port: 6379
  }
});

// Add job to queue
await taskQueue.add("process-data", {
  data: largeDataset,
  priority: 1
});
```

### 28. Metrics Collection
```typescript
class Metrics {
  private counters = new Map<string, number>();
  private histograms = new Map<string, number[]>();
  
  increment(name: string, value: number = 1) {
    this.counters.set(name, (this.counters.get(name) || 0) + value);
  }
  
  recordTiming(name: string, duration: number) {
    if (!this.histograms.has(name)) {
      this.histograms.set(name, []);
    }
    this.histograms.get(name)!.push(duration);
  }
  
  getStats(name: string) {
    const values = this.histograms.get(name) || [];
    return {
      count: values.length,
      avg: values.reduce((a, b) => a + b, 0) / values.length,
      min: Math.min(...values),
      max: Math.max(...values)
    };
  }
}

const metrics = new Metrics();

// Usage:
const start = Date.now();
await executeTool(name, args);
metrics.recordTiming(`tool.${name}`, Date.now() - start);
metrics.increment(`tool.${name}.calls`);
```

### 29. Distributed Tracing
```typescript
interface Span {
  traceId: string;
  spanId: string;
  parentSpanId?: string;
  name: string;
  startTime: number;
  endTime?: number;
  tags: Record<string, any>;
}

class Tracer {
  private spans: Span[] = [];
  
  startSpan(name: string, traceId?: string, parentSpanId?: string): Span {
    const span: Span = {
      traceId: traceId || this.generateId(),
      spanId: this.generateId(),
      parentSpanId,
      name,
      startTime: Date.now(),
      tags: {}
    };
    this.spans.push(span);
    return span;
  }
  
  endSpan(span: Span) {
    span.endTime = Date.now();
  }
  
  private generateId(): string {
    return Math.random().toString(36).substring(2);
  }
}
```

### 30. Plugin System
```typescript
interface Plugin {
  name: string;
  version: string;
  tools: any[];
  initialize?: () => Promise<void>;
  cleanup?: () => Promise<void>;
}

class PluginManager {
  private plugins = new Map<string, Plugin>();
  
  async loadPlugin(pluginPath: string) {
    const plugin = await import(pluginPath) as Plugin;
    
    if (plugin.initialize) {
      await plugin.initialize();
    }
    
    this.plugins.set(plugin.name, plugin);
  }
  
  getAllTools(): any[] {
    const tools: any[] = [];
    for (const plugin of this.plugins.values()) {
      tools.push(...plugin.tools);
    }
    return tools;
  }
}
```

### 31. Multi-Tenancy Support
```typescript
class TenantManager {
  private tenants = new Map<string, {
    id: string;
    name: string;
    config: any;
    db: Database.Database;
  }>();
  
  getTenant(tenantId: string) {
    return this.tenants.get(tenantId);
  }
  
  async executeTenantQuery(tenantId: string, query: string, params: any[]) {
    const tenant = this.getTenant(tenantId);
    if (!tenant) throw new Error(`Tenant ${tenantId} not found`);
    
    return tenant.db.prepare(query).all(...params);
  }
}
```

### 32. Encryption for Sensitive Data
```typescript
import crypto from "crypto";

class Encryptor {
  private algorithm = "aes-256-gcm";
  private key: Buffer;
  
  constructor(secretKey: string) {
    this.key = crypto.scryptSync(secretKey, "salt", 32);
  }
  
  encrypt(text: string): string {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);
    
    let encrypted = cipher.update(text, "utf8", "hex");
    encrypted += cipher.final("hex");
    
    const authTag = cipher.getAuthTag();
    
    return JSON.stringify({
      iv: iv.toString("hex"),
      data: encrypted,
      tag: authTag.toString("hex")
    });
  }
  
  decrypt(encryptedData: string): string {
    const { iv, data, tag } = JSON.parse(encryptedData);
    
    const decipher = crypto.createDecipheriv(
      this.algorithm,
      this.key,
      Buffer.from(iv, "hex")
    );
    
    decipher.setAuthTag(Buffer.from(tag, "hex"));
    
    let decrypted = decipher.update(data, "hex", "utf8");
    decrypted += decipher.final("utf8");
    
    return decrypted;
  }
}
```

### 33. Production Deployment Setup
```typescript
// server.ts - Production-ready server
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { config } from "dotenv";

// Load environment variables
config();

// Setup logging
const logger = setupLogger();

// Setup monitoring
const metrics = new Metrics();
const tracer = new Tracer();

// Setup error tracking
process.on("uncaughtException", (error) => {
  logger.error("Uncaught exception", error);
  process.exit(1);
});

process.on("unhandledRejection", (reason) => {
  logger.error("Unhandled rejection", reason);
});

// Health check
setInterval(() => {
  const health = {
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    metrics: metrics.getAll()
  };
  logger.debug("Health check", health);
}, 60000);

// Graceful shutdown
process.on("SIGTERM", async () => {
  logger.info("SIGTERM received, shutting down gracefully");
  await cleanup();
  process.exit(0);
});

// Start server
async function main() {
  const server = createServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  logger.info("Server started successfully");
}

main().catch((error) => {
  logger.error("Failed to start server", error);
  process.exit(1);
});
```

## Usage Tips

1. **Start Simple**: Begin with basic examples and gradually add complexity
2. **Test Thoroughly**: Use the MCP inspector to test each tool
3. **Handle Errors**: Always include proper error handling
4. **Document Well**: Clear descriptions help the AI use your tools correctly
5. **Monitor Performance**: Track metrics in production

## Next Steps

- Review the [main guide](../HOW-TO-BUILD-YOUR-OWN-COPILOT.md)
- Complete the [labs](../labs/)
- Join the [MCP community](https://github.com/topics/model-context-protocol)
