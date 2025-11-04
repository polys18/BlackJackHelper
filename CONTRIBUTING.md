# Contributing to BlackJack Helper

Thank you for your interest in contributing to BlackJack Helper! This document provides guidelines and instructions for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/BlackJackHelper.git`
3. Install dependencies: `npm install`
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites

- Node.js >= 20
- npm or yarn
- React Native development environment
  - iOS: Xcode and CocoaPods
  - Android: Android Studio and Android SDK

### Setting Up Development Environment

1. Install dependencies:
```bash
npm install
```

2. For iOS development:
```bash
cd ios
pod install
cd ..
```

3. Run the app:
```bash
# iOS
npm run ios

# Android
npm run android
```

## Code Style

This project uses:
- **ESLint** for JavaScript/TypeScript linting
- **Prettier** for code formatting
- **TypeScript** for type safety

### Running Linters

```bash
npm run lint
```

### Code Formatting

The project uses Prettier. Configuration is in `.prettierrc.js`.

## Testing

### Running Tests

```bash
npm test
```

### Writing Tests

- Place tests in the `__tests__/` directory
- Use descriptive test names
- Follow the existing test structure
- Aim for good test coverage

Example test structure:
```typescript
describe('ComponentName', () => {
  describe('functionName', () => {
    it('should do something specific', () => {
      // Test implementation
    });
  });
});
```

## Project Structure

```
BlackJackHelper/
├── src/
│   ├── components/     # Reusable UI components
│   ├── screens/        # Screen components
│   ├── services/       # API and business logic
│   ├── types/          # TypeScript type definitions
│   └── utils/          # Utility functions
├── __tests__/          # Test files
├── __mocks__/          # Mock files for testing
├── android/            # Android native code
├── ios/                # iOS native code
└── ...
```

## Making Changes

### Commit Messages

Use clear and descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests when relevant

Good examples:
```
Add card detection confidence score display
Fix Ace calculation in soft hands
Update README with installation instructions
```

### Branch Naming

Use descriptive branch names:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or updates

Examples:
- `feature/add-multi-hand-support`
- `fix/ace-calculation-bug`
- `docs/update-api-guide`

## Pull Request Process

1. **Update your branch** with the latest changes from main:
```bash
git fetch upstream
git rebase upstream/main
```

2. **Run tests** and ensure they pass:
```bash
npm test
npm run lint
```

3. **Update documentation** if needed:
   - Update README.md for new features
   - Update USAGE_GUIDE.md for user-facing changes
   - Add JSDoc comments for new functions

4. **Create a pull request** with:
   - Clear title describing the change
   - Detailed description of what changed and why
   - Screenshots for UI changes
   - Reference to related issues

5. **Respond to feedback** from code reviewers

## Areas for Contribution

### High Priority

- [ ] Offline card recognition (TensorFlow Lite)
- [ ] Persistent and secure API key storage
- [ ] Game history tracking
- [ ] Multiple hand support
- [ ] Advanced strategy recommendations

### Medium Priority

- [ ] Card counting features
- [ ] Customizable strategy settings
- [ ] Dark mode support
- [ ] Localization/internationalization
- [ ] Performance optimizations

### Good First Issues

- [ ] Add more unit tests
- [ ] Improve error messages
- [ ] Add JSDoc comments
- [ ] Update documentation
- [ ] Fix linting warnings

## Code Review Guidelines

When reviewing code:
- Be respectful and constructive
- Focus on the code, not the person
- Ask questions rather than making demands
- Suggest improvements with examples
- Approve when ready, request changes when needed

## Security

If you discover a security vulnerability:
1. **Do NOT** open a public issue
2. Email the maintainers privately
3. Provide detailed information about the vulnerability
4. Wait for acknowledgment before disclosing publicly

## Questions?

If you have questions:
- Check existing issues and discussions
- Read the README and USAGE_GUIDE
- Open a new issue with the `question` label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- The project README
- Release notes for significant contributions
- The contributors list on GitHub

Thank you for contributing to BlackJack Helper! 🎉
