# Surface Lens: Backend / API

Use in Mode A step 3 (and Mode B/C when the backend is touched). Evaluate options against the drivers. Never start from a favorite stack.

## Decisions to make (with real alternatives)
1. **Shape:** monolith, modular monolith (default for most new products, including production ones), or services. Services only with a driver: independent scaling, separate teams, different runtimes, or hard isolation requirements.
2. **Language & framework:** what the team knows well first. Weigh ecosystem maturity for the domain (payments, ML, real-time), hiring, and runtime cost.
3. **API style:** REST + OpenAPI (default for public/mobile clients), GraphQL (many client shapes, aggregated reads; costs caching/authorization complexity), gRPC (service-to-service, internal). One schema source of truth, with generated clients for every consuming surface.
4. **Data store(s):** relational by default; document/key-value/time-series/search only with a driver. Managed over self-hosted.
5. **Async processing:** in-process jobs → managed queue → event streaming, escalating only with drivers (volume, decoupling, fan-out).
6. **Hosting model:** PaaS/containers/serverless (decided with platform-engineer, constrained by cold starts, long-running work, cost).

## Questions to ask
- Which of the vision's flows are synchronous for the user, and which can be async?
- Expected request volume and peaks? Long-running operations?
- Which data is personal or sensitive, and what are the residency requirements?
- Which third parties are in the critical path, and what's their failure behavior?
- Will external parties (partners, public API) consume it? That changes versioning and auth.

## Production must-haves
- Versioned, backward-compatible migrations; zero-downtime deploys.
- Idempotency for unsafe operations called by mobile clients (retries happen).
- Timeouts and retries on every outbound call; structured logs, metrics and traces per the core standards.
- AuthZ enforced server-side on every endpoint; rate limiting.
- Contract tests with each client surface; an API compatibility window agreed with release-manager.

## Red flags
Microservices for one team; a GraphQL gateway in front of a single service with no client-shape driver; several databases at day one; self-hosted Kafka for low volume.

## Testing options to evaluate (Mode A step 3b)
- Unit: the language's standard framework.
- Integration: against a real instance of the same database engine (e.g. throwaway containers), never a different engine; migrations tested forward on realistic data.
- API tests: in-process HTTP tests vs black-box against a running instance.
- Contract: schema-based (validate implementation and clients against the API schema, plus breaking-change detection) vs consumer-driven contracts (each client publishes expectations). Schema-based is simpler when one team owns all surfaces; consumer-driven pays off with independent teams.
- Async: testing consumers idempotently, and producers against the event schema.
- Third parties: test doubles or recorded responses per PR; the provider sandbox on a schedule.
