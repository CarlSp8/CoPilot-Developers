# Lab 3: Building a Database MCP Server

**Duration**: 75-90 minutes  
**Difficulty**: Intermediate to Advanced  
**Prerequisites**: Labs 1-2, SQLite/PostgreSQL basics

## Learning Objectives

- Connect MCP server to a real database
- Implement CRUD operations safely
- Handle connection pooling
- Use transactions
- Implement proper error handling for database operations

## Introduction

Build a production-ready MCP server that interfaces with a SQLite database to manage a library system.

## Part 1: Project Setup (15 minutes)

```bash
mkdir library-mcp-server
cd library-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk better-sqlite3
npm install --save-dev typescript @types/node @types/better-sqlite3 tsx
```

### Database Schema

Create `schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  isbn TEXT UNIQUE NOT NULL,
  published_year INTEGER,
  genre TEXT,
  available BOOLEAN DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS members (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  joined_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  due_date DATETIME NOT NULL,
  return_date DATETIME,
  FOREIGN KEY (book_id) REFERENCES books(id),
  FOREIGN KEY (member_id) REFERENCES members(id)
);

CREATE INDEX idx_loans_book ON loans(book_id);
CREATE INDEX idx_loans_member ON loans(member_id);
CREATE INDEX idx_books_isbn ON books(isbn);
```

## Part 2: Database Layer (25 minutes)

Create `src/database.ts`:

```typescript
import Database from "better-sqlite3";
import { readFileSync } from "fs";
import { join } from "path";

export interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  published_year?: number;
  genre?: string;
  available: boolean;
  created_at: string;
}

export interface Member {
  id: number;
  name: string;
  email: string;
  joined_date: string;
}

export interface Loan {
  id: number;
  book_id: number;
  member_id: number;
  loan_date: string;
  due_date: string;
  return_date?: string;
}

export class LibraryDatabase {
  private db: Database.Database;

  constructor(dbPath: string = "library.db") {
    this.db = new Database(dbPath);
    this.db.pragma("journal_mode = WAL");
    this.initialize();
  }

  private initialize() {
    const schema = readFileSync(join(__dirname, "../schema.sql"), "utf-8");
    this.db.exec(schema);
  }

  // Book operations
  addBook(book: Omit<Book, "id" | "available" | "created_at">): Book {
    const stmt = this.db.prepare(`
      INSERT INTO books (title, author, isbn, published_year, genre)
      VALUES (?, ?, ?, ?, ?)
    `);

    const info = stmt.run(
      book.title,
      book.author,
      book.isbn,
      book.published_year,
      book.genre
    );

    return this.getBook(info.lastInsertRowid as number)!;
  }

  getBook(id: number): Book | undefined {
    const stmt = this.db.prepare("SELECT * FROM books WHERE id = ?");
    return stmt.get(id) as Book | undefined;
  }

  searchBooks(query: {
    title?: string;
    author?: string;
    genre?: string;
    available?: boolean;
  }): Book[] {
    let sql = "SELECT * FROM books WHERE 1=1";
    const params: any[] = [];

    if (query.title) {
      sql += " AND title LIKE ?";
      params.push(`%${query.title}%`);
    }

    if (query.author) {
      sql += " AND author LIKE ?";
      params.push(`%${query.author}%`);
    }

    if (query.genre) {
      sql += " AND genre = ?";
      params.push(query.genre);
    }

    if (query.available !== undefined) {
      sql += " AND available = ?";
      params.push(query.available ? 1 : 0);
    }

    const stmt = this.db.prepare(sql);
    return stmt.all(...params) as Book[];
  }

  // Member operations
  addMember(member: Omit<Member, "id" | "joined_date">): Member {
    const stmt = this.db.prepare(`
      INSERT INTO members (name, email)
      VALUES (?, ?)
    `);

    const info = stmt.run(member.name, member.email);
    return this.getMember(info.lastInsertRowid as number)!;
  }

  getMember(id: number): Member | undefined {
    const stmt = this.db.prepare("SELECT * FROM members WHERE id = ?");
    return stmt.get(id) as Member | undefined;
  }

  // Loan operations with transactions
  createLoan(bookId: number, memberId: number, daysToReturn: number = 14): Loan {
    return this.db.transaction(() => {
      // Check if book is available
      const book = this.getBook(bookId);
      if (!book) {
        throw new Error(`Book with ID ${bookId} not found`);
      }
      if (!book.available) {
        throw new Error(`Book "${book.title}" is not available`);
      }

      // Check if member exists
      const member = this.getMember(memberId);
      if (!member) {
        throw new Error(`Member with ID ${memberId} not found`);
      }

      // Calculate due date
      const dueDate = new Date();
      dueDate.setDate(dueDate.getDate() + daysToReturn);

      // Create loan
      const loanStmt = this.db.prepare(`
        INSERT INTO loans (book_id, member_id, due_date)
        VALUES (?, ?, ?)
      `);

      const loanInfo = loanStmt.run(
        bookId,
        memberId,
        dueDate.toISOString()
      );

      // Mark book as unavailable
      const updateStmt = this.db.prepare(`
        UPDATE books SET available = 0 WHERE id = ?
      `);
      updateStmt.run(bookId);

      // Return loan
      const getLoanStmt = this.db.prepare("SELECT * FROM loans WHERE id = ?");
      return getLoanStmt.get(loanInfo.lastInsertRowid) as Loan;
    })();
  }

  returnBook(loanId: number): Loan {
    return this.db.transaction(() => {
      const loan = this.db
        .prepare("SELECT * FROM loans WHERE id = ?")
        .get(loanId) as Loan;

      if (!loan) {
        throw new Error(`Loan with ID ${loanId} not found`);
      }

      if (loan.return_date) {
        throw new Error("Book already returned");
      }

      // Update loan
      this.db
        .prepare(`
        UPDATE loans 
        SET return_date = CURRENT_TIMESTAMP 
        WHERE id = ?
      `)
        .run(loanId);

      // Mark book as available
      this.db
        .prepare(`
        UPDATE books 
        SET available = 1 
        WHERE id = ?
      `)
        .run(loan.book_id);

      return this.db
        .prepare("SELECT * FROM loans WHERE id = ?")
        .get(loanId) as Loan;
    })();
  }

  getActiveLoans(memberId?: number): Loan[] {
    let sql = "SELECT * FROM loans WHERE return_date IS NULL";
    const params: any[] = [];

    if (memberId !== undefined) {
      sql += " AND member_id = ?";
      params.push(memberId);
    }

    const stmt = this.db.prepare(sql);
    return stmt.all(...params) as Loan[];
  }

  getOverdueLoans(): Array<Loan & { book_title: string; member_name: string }> {
    const stmt = this.db.prepare(`
      SELECT 
        loans.*,
        books.title as book_title,
        members.name as member_name
      FROM loans
      JOIN books ON loans.book_id = books.id
      JOIN members ON loans.member_id = members.id
      WHERE loans.return_date IS NULL
        AND loans.due_date < datetime('now')
    `);

    return stmt.all() as Array<Loan & { book_title: string; member_name: string }>;
  }

  close() {
    this.db.close();
  }
}
```

## Part 3: MCP Server Implementation (25 minutes)

Create `src/index.ts`:

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { LibraryDatabase } from "./database.js";

const db = new LibraryDatabase();

const server = new Server(
  {
    name: "library-system",
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
    name: "add_book",
    description: "Add a new book to the library catalog",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string", description: "Book title" },
        author: { type: "string", description: "Book author" },
        isbn: { type: "string", description: "ISBN number" },
        published_year: { type: "integer", description: "Publication year" },
        genre: { type: "string", description: "Book genre" },
      },
      required: ["title", "author", "isbn"],
    },
  },
  {
    name: "search_books",
    description: "Search for books by title, author, genre, or availability",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string" },
        author: { type: "string" },
        genre: { type: "string" },
        available: { type: "boolean" },
      },
    },
  },
  {
    name: "add_member",
    description: "Register a new library member",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Member name" },
        email: { type: "string", format: "email", description: "Email address" },
      },
      required: ["name", "email"],
    },
  },
  {
    name: "checkout_book",
    description: "Check out a book to a member",
    inputSchema: {
      type: "object",
      properties: {
        book_id: { type: "integer", description: "Book ID" },
        member_id: { type: "integer", description: "Member ID" },
        days: { type: "integer", default: 14, description: "Loan period in days" },
      },
      required: ["book_id", "member_id"],
    },
  },
  {
    name: "return_book",
    description: "Process a book return",
    inputSchema: {
      type: "object",
      properties: {
        loan_id: { type: "integer", description: "Loan ID" },
      },
      required: ["loan_id"],
    },
  },
  {
    name: "get_active_loans",
    description: "Get all active loans, optionally filtered by member",
    inputSchema: {
      type: "object",
      properties: {
        member_id: { type: "integer", description: "Filter by member ID" },
      },
    },
  },
  {
    name: "get_overdue_loans",
    description: "Get all overdue loans with book and member details",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
];

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "add_book": {
        const book = db.addBook(args as any);
        return {
          content: [{ type: "text", text: JSON.stringify(book, null, 2) }],
        };
      }

      case "search_books": {
        const books = db.searchBooks(args || {});
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(books, null, 2),
            },
          ],
        };
      }

      case "add_member": {
        const member = db.addMember(args as any);
        return {
          content: [{ type: "text", text: JSON.stringify(member, null, 2) }],
        };
      }

      case "checkout_book": {
        const { book_id, member_id, days = 14 } = args as any;
        const loan = db.createLoan(book_id, member_id, days);
        return {
          content: [{ type: "text", text: JSON.stringify(loan, null, 2) }],
        };
      }

      case "return_book": {
        const { loan_id } = args as any;
        const loan = db.returnBook(loan_id);
        return {
          content: [{ type: "text", text: JSON.stringify(loan, null, 2) }],
        };
      }

      case "get_active_loans": {
        const { member_id } = (args as any) || {};
        const loans = db.getActiveLoans(member_id);
        return {
          content: [{ type: "text", text: JSON.stringify(loans, null, 2) }],
        };
      }

      case "get_overdue_loans": {
        const loans = db.getOverdueLoans();
        return {
          content: [{ type: "text", text: JSON.stringify(loans, null, 2) }],
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

// Cleanup on exit
process.on("SIGINT", () => {
  db.close();
  process.exit(0);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Library MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  db.close();
  process.exit(1);
});
```

## Part 4: Exercises (20 minutes)

### Exercise 1: Add Book Reservations

Implement a reservation system:
- Members can reserve books that are currently unavailable
- When a book is returned, notify the first person in the reservation queue

### Exercise 2: Add Late Fees

- Calculate late fees based on overdue days
- Add payment tracking

### Exercise 3: Generate Reports

Create tools for:
- Most borrowed books
- Most active members
- Books never borrowed

## Key Takeaways

- Database transactions ensure data consistency
- Connection management is critical for production servers
- Proper error handling prevents data corruption
- Indexes improve query performance
- Foreign keys maintain referential integrity

## Next Steps

- [Lab 4: Integration with VS Code](lab4-vscode-integration.md)
- Review [Database Best Practices](../examples/database-patterns.md)
