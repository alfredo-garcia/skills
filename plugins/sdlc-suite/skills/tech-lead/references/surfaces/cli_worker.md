# Surface Lens: CLI & Worker

## CLI
- **Runtime & distribution:** single binary (e.g. Go/Rust) vs interpreted (Node/Python) with a package manager; installation channels (Homebrew, npm, pip, direct download); auto-update.
- **UX contract:** commands/flags naming, exit codes, machine-readable output (`--json`), config files and env vars, auth flow for a CLI (device code, tokens in the OS keychain).
- **Production must-haves:** versioning and changelog (release-manager), signed binaries where applicable, telemetry only with consent.

## Worker (jobs/consumers without a public API)
- **Trigger model:** schedule, queue consumer, event stream, or webhook receiver.
- **Guarantees:** idempotency, retries with backoff, dead-lettering, poison-message handling, concurrency limits, graceful shutdown.
- **Observability:** job-level metrics (duration, failures, lag), alert on backlog/failed jobs, trace propagation from the producer.
- **Red flags:** a separate worker deployable when in-process jobs suffice; no visibility into failed jobs.

## Testing options to evaluate (Mode A step 3b)
- CLI: unit tests plus golden-output tests for commands (stdout, exit codes, `--json`), tested on every OS distributed to.
- Worker: idempotency and retry tests, poison-message handling, tests against a real broker instance in CI where feasible.
