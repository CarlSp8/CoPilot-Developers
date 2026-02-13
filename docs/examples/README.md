# Code Examples Index

This directory contains over 30 practical code examples for building MCP servers, organized by difficulty level.

## Basic Examples (10)

These examples demonstrate fundamental MCP concepts:

1. [Hello World Server](basic/01-hello-world.md) - Simplest possible MCP server
2. [Single Tool](basic/02-single-tool.md) - Server with one tool
3. [Multiple Tools](basic/03-multiple-tools.md) - Server with multiple related tools
4. [Input Validation](basic/04-input-validation.md) - Validating tool inputs
5. [Error Handling](basic/05-error-handling.md) - Proper error handling patterns
6. [Environment Variables](basic/06-environment-variables.md) - Using environment configuration
7. [JSON Responses](basic/07-json-responses.md) - Formatting responses as JSON
8. [File Operations](basic/08-file-operations.md) - Reading and writing files
9. [HTTP Requests](basic/09-http-requests.md) - Making external API calls
10. [Date and Time Tools](basic/10-date-time-tools.md) - Working with dates and times

## Intermediate Examples (10)

These examples show more advanced patterns:

11. [Resource Provider](intermediate/11-resource-provider.md) - Implementing resources
12. [Prompt Templates](intermediate/12-prompt-templates.md) - Creating reusable prompts
13. [State Management](intermediate/13-state-management.md) - Managing server state
14. [Async Operations](intermediate/14-async-operations.md) - Handling async workflows
15. [Progress Notifications](intermediate/15-progress-notifications.md) - Long-running operations
16. [Data Transformation](intermediate/16-data-transformation.md) - Processing and transforming data
17. [Authentication](intermediate/17-authentication.md) - Adding authentication to tools
18. [Rate Limiting](intermediate/18-rate-limiting.md) - Implementing rate limits
19. [Batch Operations](intermediate/19-batch-operations.md) - Processing multiple items
20. [Webhook Handler](intermediate/20-webhook-handler.md) - Handling webhook events

## Advanced Examples (13)

These examples demonstrate production-ready patterns:

21. [Database Connection Pool](advanced/21-connection-pool.md) - Managing database connections
22. [Transaction Management](advanced/22-transactions.md) - Database transactions
23. [Caching Strategy](advanced/23-caching.md) - Multi-level caching
24. [Circuit Breaker](advanced/24-circuit-breaker.md) - Fault tolerance pattern
25. [Request Deduplication](advanced/25-request-dedup.md) - Avoiding duplicate work
26. [Streaming Responses](advanced/26-streaming.md) - Streaming large data sets
27. [Message Queue Integration](advanced/27-message-queue.md) - Background job processing
28. [Metrics and Monitoring](advanced/28-metrics.md) - Collecting performance metrics
29. [Distributed Tracing](advanced/29-tracing.md) - Request tracing across services
30. [Plugin Architecture](advanced/30-plugin-system.md) - Dynamic tool loading
31. [Multi-Tenancy](advanced/31-multi-tenancy.md) - Supporting multiple tenants
32. [Encryption and Security](advanced/32-security.md) - Securing sensitive data
33. [Production Deployment](advanced/33-production-deploy.md) - Complete production setup

## How to Use These Examples

Each example includes:
- Complete, working code
- Explanation of key concepts
- Common use cases
- Potential pitfalls
- Related examples

Start with basic examples and progress to more advanced topics as you build confidence.

## Running Examples

Most examples can be run standalone:

```bash
cd examples/basic/01-hello-world
npm install
npm start
```

Or test with the MCP inspector:

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

## Contributing

Have an example to share? Please see our [Contributing Guide](../../CONTRIBUTING.md).
