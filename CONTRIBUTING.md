# Contributing to Build Your Own Copilot

Thank you for your interest in contributing! This guide will help you get started.

## Ways to Contribute

- **Report Bugs**: Open an issue describing the bug
- **Suggest Features**: Propose new examples or labs
- **Improve Documentation**: Fix typos, clarify instructions, or add examples
- **Add Code Examples**: Share your MCP server implementations
- **Review PRs**: Help review contributions from others

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/CoPilot-Developers.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Description of changes"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Code Examples Guidelines

When adding new code examples:

### Structure

- Place basic examples in `docs/examples/basic/`
- Place intermediate examples in `docs/examples/intermediate/`
- Place advanced examples in `docs/examples/advanced/`
- Update `docs/examples/ALL-SNIPPETS.md` with your example

### Format

Each example should include:

```markdown
# Example Title

Brief description of what this example demonstrates.

## Code

```typescript
// Your code here
```

## Key Concepts

- Concept 1
- Concept 2

## Usage

How to use this example.

## Common Pitfalls

What to watch out for.

## Next Steps

Links to related examples.
```

### Quality Standards

- **Working Code**: All code must be tested and working
- **Clear Comments**: Explain non-obvious parts
- **Error Handling**: Include proper error handling
- **Type Safety**: Use TypeScript with strict types
- **Best Practices**: Follow MCP and TypeScript best practices

## Lab Guidelines

When creating new labs:

- **Duration**: Estimate completion time (45-120 minutes)
- **Difficulty**: Mark as Beginner, Intermediate, or Advanced
- **Prerequisites**: List required knowledge and prior labs
- **Learning Objectives**: Clear list of what students will learn
- **Structure**: Follow the existing lab format:
  - Introduction
  - Multiple parts with step-by-step instructions
  - Exercises for practice
  - Verification checklist
  - Key takeaways
  - Next steps

## Documentation Guidelines

- Use clear, concise language
- Include code examples
- Add links to related content
- Test all commands and code
- Use proper markdown formatting
- Add images/diagrams when helpful

## Testing

Before submitting:

1. **Test Code**: Ensure all code examples run without errors
2. **Test Labs**: Walk through lab instructions step-by-step
3. **Check Links**: Verify all links work
4. **Review Markdown**: Check formatting renders correctly
5. **Spell Check**: Fix typos and grammar errors

## Code Style

### TypeScript

```typescript
// Use modern ES features
const myFunction = async (param: string): Promise<Result> => {
  // Implementation
};

// Use proper typing
interface MyInterface {
  property: string;
}

// Use const for immutable values
const config = {
  // ...
};
```

### Markdown

- Use headers hierarchically (h1 → h2 → h3)
- Include blank lines between sections
- Use code blocks with language specifiers
- Use bullet points for lists
- Use tables for structured data

## Commit Messages

Follow conventional commits:

- `feat: Add new code example for caching`
- `fix: Correct typo in Lab 2`
- `docs: Update quick start guide`
- `refactor: Improve example organization`
- `test: Add tests for examples`

## Pull Request Process

1. **Title**: Clear, descriptive title
2. **Description**: Explain what and why
3. **Testing**: Describe how you tested
4. **Screenshots**: Include if relevant
5. **Breaking Changes**: Note any breaking changes
6. **Issues**: Link related issues

Example PR description:

```markdown
## Description
Adds a new example for implementing rate limiting in MCP servers.

## Changes
- Added `intermediate/18-rate-limiting.md`
- Updated `ALL-SNIPPETS.md` with new snippet
- Added rate limiter class implementation

## Testing
- Tested code example locally
- Verified markdown renders correctly
- Checked all links

## Related Issues
Closes #42
```

## Review Process

All contributions go through review:

1. Automated checks run (linting, link checking)
2. Maintainers review the code and documentation
3. Feedback is provided if changes needed
4. Once approved, PR is merged

## Questions?

- Open an issue for questions
- Check existing issues for similar questions
- Review the documentation first

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
