# Security and Privacy Policy

LectureLens Edge processes educational content locally and treats transcript data
as sensitive.

## Supported version

The latest commit on the `main` branch is the currently supported development
version. The project has not yet published a stable production release.

## Report a vulnerability

Use GitHub's private vulnerability reporting feature for this repository when it
is available. If that option is unavailable, contact the repository owner
privately instead of opening a public issue.

Include:

- the affected file or endpoint;
- steps to reproduce the problem;
- the expected and observed behaviour;
- the possible privacy or security impact;
- a suggested fix, if known.

Do not include real lecture recordings, student information, access tokens, or
other personal data in the report.

## Current security boundaries

- The server binds to `127.0.0.1` by default.
- API request bodies are limited to 1 MB.
- API responses disable caching and MIME-type sniffing.
- The default app uses no remote scripts, analytics, cloud model calls, or
  accounts.
- Export requires an explicit user action.

Running with a non-loopback `--host` exposes the application to that network and
is not the recommended personal-use configuration.

## Known limitations

- This is a development-stage local application, not a hardened multi-user
  service.
- There is no authentication because the default server is intended only for the
  current computer.
- Exported Markdown or JSON files are not encrypted by the application.
- Future model adapters must be reviewed for network calls, telemetry, model
  licences, and prompt-injection risks before they are enabled by default.
