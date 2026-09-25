# Contributing to LectureLens Edge

Thank you for helping improve LectureLens Edge. The project welcomes small,
focused contributions that make the local learning experience more reliable,
accessible, private, or understandable.

## Good first contributions

- Reproduce and document a bug.
- Improve setup instructions on Windows, macOS, or Linux.
- Add a test for an uncovered edge case.
- Improve keyboard or screen-reader behaviour.
- Extend the technical glossary with reviewed translations.
- Propose a model adapter without weakening the grounding contract.

## Development setup

LectureLens Edge currently uses the Python standard library, so setup is small:

```bash
git clone https://github.com/Shahal17/LectureLens-Edge.git
cd LectureLens-Edge
python3 run.py
```

Run the automated checks before opening a pull request:

```bash
python3 -m unittest discover -s tests -v
python3 tools/benchmark.py --runs 10 --json
```

## Contribution process

1. Search existing issues before creating a new one.
2. For a substantial feature, open an issue and describe the user problem first.
3. Create a focused branch and keep unrelated changes out of the pull request.
4. Add or update tests when behaviour changes.
5. Update documentation when an interface, command, or limitation changes.
6. Explain what you tested in the pull request.

## Product rules

Contributions must preserve these boundaries:

- Do not send transcript or audio data to an external service by default.
- Do not claim hardware acceleration unless the active runtime verifies it.
- Keep source IDs attached to generated learning material.
- Decline unsupported answers instead of inventing lecture content.
- Keep accessibility features functional.
- Do not commit model weights, recorded lectures, credentials, or personal data.

## Code style

- Prefer clear standard-library Python and small functions.
- Add type hints where they make interfaces easier to understand.
- Return structured JSON-compatible values from engine components.
- Keep browser code dependency-free unless a dependency has a clear product
  benefit and is discussed first.
- Use descriptive commit messages.

## Reporting security or privacy concerns

Do not post sensitive details in a public issue. Follow [SECURITY.md](SECURITY.md)
for private reporting guidance.
