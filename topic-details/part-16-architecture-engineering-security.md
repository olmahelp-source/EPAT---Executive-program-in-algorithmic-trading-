# Part 16. Architecture, Engineering, and Security: Micro Details (topics 760 to 799)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 16.1 System architecture and infrastructure

760. Architecture styles (monolith, microservices, event-driven)
     - Covers: structural choices.
     - Details: a modular monolith is simpler to start with, microservices add deployment independence but also network failure modes, and event-driven designs decouple producers and consumers.
     - Pitfall: premature microservices for a small team.
     - Build: a decision record comparing options against your scale and team size.

761. Latency vs. throughput trade-offs
     - Covers: performance goals.
     - Details: batching raises throughput and adds delay. Trading paths typically favor low latency, analytics favor throughput.
     - Pitfall: optimizing the wrong metric for a component.
     - Build: separate latency and throughput targets per component.

762. Messaging and streaming (Kafka, Redis Streams, ZeroMQ)
     - Covers: moving data between components.
     - Details: Kafka offers durable logs and replay, Redis Streams are simpler, ZeroMQ is brokerless and fast. Define ordering, retention, and delivery guarantees.
     - Pitfall: assuming exactly-once delivery.
     - Build: a pipeline with replay from a stored offset.

763. Language choices (Python, C++, Rust, Java)
     - Covers: technology selection.
     - Details: Python for research and orchestration, C++, Rust, or Java for latency-critical paths. Consider team skills and library support.
     - Pitfall: rewriting everything in a fast language before profiling.
     - Build: a profile showing which components need a faster language.

764. Deployment (Docker, Kubernetes, cloud, co-location)
     - Covers: running the system.
     - Details: containers for reproducibility, orchestration for scale, co-location for latency-critical order entry.
     - Pitfall: operational complexity beyond what the system needs.
     - Build: reproducible container images and a staged deployment.

765. API design (REST, gRPC, WebSocket) and rate limiting
     - Covers: interfaces.
     - Details: REST for commands and queries, WebSocket or gRPC streams for real-time data. Rate limits protect services.
     - Pitfall: breaking changes without versioning.
     - Build: versioned API specification and rate-limit tests.

766. Databases (relational, time-series, caches)
     - Covers: storage roles.
     - Details: relational for reference data and state, time-series for market data and metrics, caches for hot data.
     - Pitfall: using one database for all workloads.
     - Build: data-store map showing what lives where and why.

767. Concurrency, async programming, fault tolerance
     - Covers: robust execution.
     - Details: avoid shared mutable state, use timeouts, retries with backoff, circuit breakers, and supervisors that restart failed workers.
     - Pitfall: race conditions in order or position state.
     - Build: tests that stress concurrent updates.

768. Configuration and secrets management
     - Covers: controlling settings.
     - Details: separate config from code, version it, and keep secrets in a vault, not in repositories.
     - Pitfall: keys committed to source control.
     - Build: secrets loaded at runtime from a manager with rotation.

## 16.2 Advanced systems engineering

769. Event sourcing, CQRS, snapshots, and state recovery
     - Covers: state as a log of events.
     - Details: store every event, derive state by replay, and snapshot periodically for fast recovery.
     - Pitfall: unbounded replay time without snapshots.
     - Build: state rebuilt from events and verified against a live copy.

770. Serialization and schema evolution (Protobuf, Avro, SBE)
     - Covers: message formats.
     - Details: compact binary formats with schemas that allow adding fields without breaking old readers.
     - Pitfall: incompatible schema changes.
     - Build: compatibility tests across schema versions.

771. Order-book data structures and algorithmic complexity
     - Covers: efficient books.
     - Details: price levels in sorted maps or arrays with hash lookup by order ID, giving O(1) or O(log n) operations.
     - Pitfall: O(n) operations on the hot path.
     - Build: benchmark add, cancel, and match at large depth.

772. Lock-free structures, memory management, garbage-collection pauses, and profiling
     - Covers: runtime performance.
     - Details: preallocate memory, avoid allocation on the hot path, and measure pauses.
     - Pitfall: optimizing without profiling.
     - Build: profiler output and targeted fixes.

773. Numerical precision (floating point vs. decimal arithmetic for money)
     - Covers: exact arithmetic.
     - Details: binary floats cannot represent many decimals exactly. Use decimal or integer ticks for prices and money.
     - Pitfall: accumulating rounding errors in P&L or fees.
     - Build: tests comparing float and decimal results over many operations.

774. Time handling (leap seconds, DST, monotonic clocks)
     - Covers: correct time logic.
     - Details: store UTC, convert for display, and use monotonic clocks for durations.
     - Pitfall: local-time arithmetic across daylight-saving changes.
     - Build: time-utility library with edge-case tests.

775. Idempotent messaging, exactly-once vs. at-least-once semantics
     - Covers: delivery guarantees.
     - Details: at-least-once delivery with idempotent consumers achieves effectively-once results.
     - Pitfall: duplicate processing of fills.
     - Build: consumer that dedupes by event ID.

776. Feature flags, versioned APIs, and configuration drift
     - Covers: safe change.
     - Details: toggle features without redeploying, and detect when running config differs from intended.
     - Pitfall: undocumented manual changes.
     - Build: config-drift detector.

777. Multi-tenancy, scalability, and cost control in the cloud
     - Covers: scaling and cost.
     - Details: isolate tenants, scale horizontally where possible, and monitor spend.
     - Pitfall: surprise cloud bills.
     - Build: cost dashboards and budgets.

778. Vendor lock-in and broker abstraction layers
     - Covers: portability.
     - Details: wrap vendor APIs behind interfaces so replacement is feasible.
     - Pitfall: vendor-specific types spread through the code.
     - Build: adapter layer and a mock vendor.

## 16.3 Software engineering practices

779. Version control, branching strategy, and code review
     - Covers: collaboration.
     - Details: small changes, reviews required, protected main branch, tagged releases.
     - Pitfall: direct pushes to production branches.
     - Build: branch protection and a review checklist.

780. Reproducible environments and dependency management
     - Covers: consistent builds.
     - Details: pinned versions, lock files, containers.
     - Pitfall: unpinned dependencies changing results.
     - Build: lock file and a container build.

781. Property-based testing, fuzzing, and backtest regression testing
     - Covers: stronger tests.
     - Details: property tests generate many inputs to check invariants, fuzzers find crashes, regression tests catch changes in backtest outputs.
     - Pitfall: only example-based tests.
     - Build: invariants for order handling and a golden backtest test.

782. Exchange simulator conformance testing
     - Covers: realism of the test venue.
     - Details: confirm simulator behaves like the exchange on key scenarios.
     - Pitfall: simulator differences masking bugs.
     - Build: scenario suite compared with exchange test environment.

783. Technical-debt management and documentation standards
     - Covers: maintainability.
     - Details: track debt items, schedule paydown, document architecture and runbooks.
     - Pitfall: undocumented critical knowledge.
     - Build: architecture documents and a debt register.

784. Domain-driven design for trading systems
     - Covers: modeling the domain.
     - Details: clear domain concepts such as Order, Fill, Position, and Strategy, with bounded contexts.
     - Pitfall: anemic or inconsistent models.
     - Build: domain glossary and model diagram.

## 16.4 Frontend and user experience

785. Dashboards (charts, order entry, blotters, positions)
     - Covers: operator views.
     - Details: positions, orders, fills, P&L, and risk in one place with clear status.
     - Pitfall: clutter that hides critical alerts.
     - Build: dashboard wireframes prioritizing critical information.

786. Real-time UI (React, WebSockets, charting libraries)
     - Covers: live front ends.
     - Details: push updates over WebSocket, throttle rendering, and handle reconnects.
     - Pitfall: UI freezing under high update rates.
     - Build: update batching and a load test.

787. Alerts and notifications
     - Covers: getting attention.
     - Details: severity levels, routing, acknowledgment, and escalation.
     - Pitfall: too many low-value alerts.
     - Build: alert policy with severity definitions.

788. Strategy configuration and monitoring UIs
     - Covers: controlling strategies.
     - Details: view parameters and status, pause, resume, and edit with validation and audit.
     - Pitfall: edits without validation.
     - Build: validated parameter forms with audit log.

789. Visualization and interactive research notebooks
     - Covers: research tools.
     - Details: notebooks for exploration with standard plotting and data-access helpers.
     - Pitfall: notebooks as production code.
     - Build: shared research utilities and a notebook template.

## 16.5 Reliability and operations (technical)

790. Monitoring, logging, observability (Prometheus, Grafana, ELK)
     - Covers: seeing system behavior.
     - Details: metrics, structured logs, and traces. Track latency, error rates, queue depths, and business metrics.
     - Pitfall: logs without correlation IDs.
     - Build: dashboards and correlated logs for an order path.

791. Incident response and alerting
     - Covers: handling failures.
     - Details: define severity, on-call responsibility, communication, and escalation.
     - Pitfall: undefined ownership.
     - Build: incident runbooks and drill schedule.

792. Disaster recovery, failover, high availability
     - Covers: resilience.
     - Details: recovery time and recovery point objectives, backups, and tested failover.
     - Pitfall: backups never restored in tests.
     - Build: scheduled restore and failover tests.

793. Testing (unit, integration, replay, chaos)
     - Covers: test layers.
     - Details: unit tests for logic, integration for components, replay for realistic sequences, chaos for failure behavior.
     - Pitfall: missing integration tests with the broker adapter.
     - Build: layered test plan.

794. CI/CD and safe release practices
     - Covers: deployment pipeline.
     - Details: automated tests, staged rollout, rollback plans, and release windows outside trading hours.
     - Pitfall: deploying during market hours without a rollback.
     - Build: pipeline with approval gates and rollback.

## 16.6 Security

795. Authentication, authorization, API key management
     - Covers: access control.
     - Details: strong authentication, least privilege, key rotation, IP restrictions, withdrawal-disabled trading keys.
     - Pitfall: broad-permission keys.
     - Build: role matrix and key-rotation job.

796. Encryption in transit and at rest
     - Covers: data protection.
     - Details: TLS for connections and encrypted storage and backups.
     - Pitfall: unencrypted internal links or backups.
     - Build: encryption audit.

797. Secure credential storage
     - Covers: secret handling.
     - Details: vaults or hardware-backed stores, no secrets in logs or code.
     - Pitfall: secrets in environment dumps and logs.
     - Build: log scrubbing and secret scanning.

798. Access control, audit logs, fraud prevention
     - Covers: accountability.
     - Details: record who did what and when, and detect unusual activity.
     - Pitfall: shared accounts.
     - Build: immutable audit log and anomaly alerts.

799. Threat modeling for trading systems
     - Covers: anticipating attacks.
     - Details: identify assets, entry points, and attackers, then rank threats and controls.
     - Pitfall: focusing only on external threats.
     - Build: a threat model document reviewed periodically.
