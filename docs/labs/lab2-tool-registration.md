# Lab 2: Tool Definition and Registration

**Duration**: 60-75 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Completion of Lab 1, understanding of JSON Schema

## Learning Objectives

By the end of this lab, you will be able to:
- Design comprehensive tool schemas
- Implement complex input validation
- Handle multiple tool categories
- Use TypeScript types for type safety
- Create reusable tool patterns

## Introduction

In Lab 1, you created simple calculator tools. In this lab, you'll build a more sophisticated MCP server with multiple categories of tools, complex input schemas, and proper TypeScript typing.

## Part 1: Project Setup (10 minutes)

### Create New Project

```bash
mkdir task-manager-mcp
cd task-manager-mcp
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install --save-dev typescript @types/node tsx
```

We're adding `zod` for runtime validation.

### TypeScript Configuration

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
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

## Part 2: Define Type-Safe Tool Schemas (20 minutes)

### Step 1: Create Type Definitions

Create `src/types.ts`:

```typescript
import { z } from "zod";

// Task priority levels
export enum Priority {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  URGENT = "urgent",
}

// Task status
export enum Status {
  TODO = "todo",
  IN_PROGRESS = "in_progress",
  DONE = "done",
  BLOCKED = "blocked",
}

// Task interface
export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: Priority;
  status: Status;
  dueDate?: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

// Zod schemas for validation
export const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().max(1000).optional(),
  priority: z.nativeEnum(Priority).default(Priority.MEDIUM),
  dueDate: z.string().datetime().optional(),
  tags: z.array(z.string()).default([]),
});

export const UpdateTaskSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(200).optional(),
  description: z.string().max(1000).optional(),
  priority: z.nativeEnum(Priority).optional(),
  status: z.nativeEnum(Status).optional(),
  dueDate: z.string().datetime().optional(),
  tags: z.array(z.string()).optional(),
});

export const ListTasksSchema = z.object({
  status: z.nativeEnum(Status).optional(),
  priority: z.nativeEnum(Priority).optional(),
  tag: z.string().optional(),
  limit: z.number().int().positive().max(100).default(10),
});

export const DeleteTaskSchema = z.object({
  id: z.string().uuid(),
});
```

### Step 2: Create Task Storage

Create `src/storage.ts`:

```typescript
import { Task, Priority, Status } from "./types.js";
import { randomUUID } from "crypto";

class TaskStorage {
  private tasks: Map<string, Task> = new Map();

  create(data: Omit<Task, "id" | "createdAt" | "updatedAt" | "status">): Task {
    const now = new Date().toISOString();
    const task: Task = {
      id: randomUUID(),
      ...data,
      status: Status.TODO,
      createdAt: now,
      updatedAt: now,
    };
    this.tasks.set(task.id, task);
    return task;
  }

  get(id: string): Task | undefined {
    return this.tasks.get(id);
  }

  update(id: string, data: Partial<Task>): Task | undefined {
    const task = this.tasks.get(id);
    if (!task) return undefined;

    const updated = {
      ...task,
      ...data,
      id: task.id, // Prevent ID changes
      createdAt: task.createdAt, // Prevent createdAt changes
      updatedAt: new Date().toISOString(),
    };

    this.tasks.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    return this.tasks.delete(id);
  }

  list(filters?: {
    status?: Status;
    priority?: Priority;
    tag?: string;
    limit?: number;
  }): Task[] {
    let tasks = Array.from(this.tasks.values());

    if (filters?.status) {
      tasks = tasks.filter((t) => t.status === filters.status);
    }

    if (filters?.priority) {
      tasks = tasks.filter((t) => t.priority === filters.priority);
    }

    if (filters?.tag) {
      tasks = tasks.filter((t) => t.tags.includes(filters.tag));
    }

    // Sort by priority and due date
    tasks.sort((a, b) => {
      const priorityOrder = { urgent: 0, high: 1, medium: 2, low: 3 };
      const aPriority = priorityOrder[a.priority];
      const bPriority = priorityOrder[b.priority];

      if (aPriority !== bPriority) {
        return aPriority - bPriority;
      }

      if (a.dueDate && b.dueDate) {
        return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
      }

      return 0;
    });

    return tasks.slice(0, filters?.limit || 10);
  }

  getStats(): {
    total: number;
    byStatus: Record<Status, number>;
    byPriority: Record<Priority, number>;
  } {
    const tasks = Array.from(this.tasks.values());

    return {
      total: tasks.length,
      byStatus: {
        [Status.TODO]: tasks.filter((t) => t.status === Status.TODO).length,
        [Status.IN_PROGRESS]: tasks.filter((t) => t.status === Status.IN_PROGRESS).length,
        [Status.DONE]: tasks.filter((t) => t.status === Status.DONE).length,
        [Status.BLOCKED]: tasks.filter((t) => t.status === Status.BLOCKED).length,
      },
      byPriority: {
        [Priority.LOW]: tasks.filter((t) => t.priority === Priority.LOW).length,
        [Priority.MEDIUM]: tasks.filter((t) => t.priority === Priority.MEDIUM).length,
        [Priority.HIGH]: tasks.filter((t) => t.priority === Priority.HIGH).length,
        [Priority.URGENT]: tasks.filter((t) => t.priority === Priority.URGENT).length,
      },
    };
  }
}

export const storage = new TaskStorage();
```

## Part 3: Implement MCP Server (25 minutes)

Create `src/index.ts`:

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { storage } from "./storage.js";
import {
  CreateTaskSchema,
  UpdateTaskSchema,
  ListTasksSchema,
  DeleteTaskSchema,
  Priority,
  Status,
} from "./types.js";

const server = new Server(
  {
    name: "task-manager",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions
const tools = [
  {
    name: "create_task",
    description: "Create a new task with title, optional description, priority, due date, and tags",
    inputSchema: {
      type: "object",
      properties: {
        title: {
          type: "string",
          description: "Task title (1-200 characters)",
          minLength: 1,
          maxLength: 200,
        },
        description: {
          type: "string",
          description: "Detailed task description (max 1000 characters)",
          maxLength: 1000,
        },
        priority: {
          type: "string",
          enum: ["low", "medium", "high", "urgent"],
          description: "Task priority level",
          default: "medium",
        },
        dueDate: {
          type: "string",
          format: "date-time",
          description: "Due date in ISO 8601 format",
        },
        tags: {
          type: "array",
          items: { type: "string" },
          description: "Array of tags for categorization",
          default: [],
        },
      },
      required: ["title"],
    },
  },
  {
    name: "update_task",
    description: "Update an existing task by ID",
    inputSchema: {
      type: "object",
      properties: {
        id: {
          type: "string",
          format: "uuid",
          description: "Task UUID",
        },
        title: {
          type: "string",
          minLength: 1,
          maxLength: 200,
        },
        description: {
          type: "string",
          maxLength: 1000,
        },
        priority: {
          type: "string",
          enum: ["low", "medium", "high", "urgent"],
        },
        status: {
          type: "string",
          enum: ["todo", "in_progress", "done", "blocked"],
        },
        dueDate: {
          type: "string",
          format: "date-time",
        },
        tags: {
          type: "array",
          items: { type: "string" },
        },
      },
      required: ["id"],
    },
  },
  {
    name: "list_tasks",
    description: "List tasks with optional filters for status, priority, and tags",
    inputSchema: {
      type: "object",
      properties: {
        status: {
          type: "string",
          enum: ["todo", "in_progress", "done", "blocked"],
          description: "Filter by task status",
        },
        priority: {
          type: "string",
          enum: ["low", "medium", "high", "urgent"],
          description: "Filter by priority level",
        },
        tag: {
          type: "string",
          description: "Filter by tag",
        },
        limit: {
          type: "integer",
          minimum: 1,
          maximum: 100,
          default: 10,
          description: "Maximum number of tasks to return",
        },
      },
    },
  },
  {
    name: "get_task",
    description: "Get a specific task by ID",
    inputSchema: {
      type: "object",
      properties: {
        id: {
          type: "string",
          format: "uuid",
          description: "Task UUID",
        },
      },
      required: ["id"],
    },
  },
  {
    name: "delete_task",
    description: "Delete a task by ID",
    inputSchema: {
      type: "object",
      properties: {
        id: {
          type: "string",
          format: "uuid",
          description: "Task UUID",
        },
      },
      required: ["id"],
    },
  },
  {
    name: "get_stats",
    description: "Get statistics about tasks (total, by status, by priority)",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
];

// Register handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "create_task": {
        const validated = CreateTaskSchema.parse(args);
        const task = storage.create({
          title: validated.title,
          description: validated.description,
          priority: validated.priority,
          dueDate: validated.dueDate,
          tags: validated.tags,
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(task, null, 2),
            },
          ],
        };
      }

      case "update_task": {
        const validated = UpdateTaskSchema.parse(args);
        const task = storage.update(validated.id, validated);
        if (!task) {
          return {
            content: [
              {
                type: "text",
                text: `Error: Task with ID ${validated.id} not found`,
              },
            ],
            isError: true,
          };
        }
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(task, null, 2),
            },
          ],
        };
      }

      case "list_tasks": {
        const validated = ListTasksSchema.parse(args || {});
        const tasks = storage.list(validated);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(tasks, null, 2),
            },
          ],
        };
      }

      case "get_task": {
        const id = (args as any).id;
        const task = storage.get(id);
        if (!task) {
          return {
            content: [
              {
                type: "text",
                text: `Error: Task with ID ${id} not found`,
              },
            ],
            isError: true,
          };
        }
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(task, null, 2),
            },
          ],
        };
      }

      case "delete_task": {
        const validated = DeleteTaskSchema.parse(args);
        const deleted = storage.delete(validated.id);
        if (!deleted) {
          return {
            content: [
              {
                type: "text",
                text: `Error: Task with ID ${validated.id} not found`,
              },
            ],
            isError: true,
          };
        }
        return {
          content: [
            {
              type: "text",
              text: `Task ${validated.id} deleted successfully`,
            },
          ],
        };
      }

      case "get_stats": {
        const stats = storage.getStats();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(stats, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Task Manager MCP server running on stdio");
}

main().catch(console.error);
```

## Part 4: Testing and Validation (15 minutes)

### Build and Run

```bash
npm run build
npm run dev
```

### Test Script

Create `test/test.ts`:

```typescript
import { spawn } from "child_process";

function sendRequest(server: any, request: any): Promise<any> {
  return new Promise((resolve) => {
    const handler = (data: Buffer) => {
      const response = JSON.parse(data.toString());
      server.stdout.off("data", handler);
      resolve(response);
    };
    server.stdout.on("data", handler);
    server.stdin.write(JSON.stringify(request) + "\n");
  });
}

async function runTests() {
  const server = spawn("tsx", ["src/index.ts"]);

  // Initialize
  await sendRequest(server, {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      clientInfo: { name: "test", version: "1.0.0" },
    },
  });

  // Create task
  const createResult = await sendRequest(server, {
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: {
      name: "create_task",
      arguments: {
        title: "Test Lab 2",
        priority: "high",
        tags: ["learning", "mcp"],
      },
    },
  });

  console.log("Created task:", createResult);

  // Get stats
  const statsResult = await sendRequest(server, {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "get_stats",
      arguments: {},
    },
  });

  console.log("Stats:", statsResult);

  server.kill();
}

runTests().catch(console.error);
```

## Part 5: Exercises (20 minutes)

### Exercise 1: Add Bulk Operations

Create tools for:
- `bulk_create`: Create multiple tasks at once
- `bulk_update`: Update multiple tasks
- `bulk_delete`: Delete multiple tasks

### Exercise 2: Add Search Tool

Implement a `search_tasks` tool that searches by:
- Title (partial match)
- Description (partial match)
- Tags (any match)

### Exercise 3: Add Task Dependencies

Extend the Task type to support dependencies:
- `dependencies`: Array of task IDs
- `blocked_by`: Computed list of blocking tasks
- Update status logic to handle blocked tasks

## Key Takeaways

- JSON Schema provides structure for tool inputs
- Zod enables runtime type validation
- TypeScript ensures compile-time type safety
- Proper error handling improves user experience
- Well-designed schemas make tools self-documenting

## Next Steps

Continue to:
- [Lab 3: Building a Database MCP Server](lab3-database-server.md)
- Review [Advanced Schema Patterns](../examples/advanced-schemas.md)

## Additional Resources

- [JSON Schema Documentation](https://json-schema.org/)
- [Zod Documentation](https://zod.dev/)
- [MCP Tool Best Practices](https://modelcontextprotocol.io/docs/best-practices)
