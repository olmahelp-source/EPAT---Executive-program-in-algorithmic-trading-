# Part 17. Operations, Governance, Legal, and Business: Micro Details (topics 800 to 828)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 17.1 Operations and desk processes

800. Runbooks, on-call rotations, and post-mortems
     - Covers: operating discipline.
     - Details: step-by-step procedures for known failures, clear on-call duties, and blameless post-mortems with actions and owners.
     - Pitfall: runbooks that are outdated or never used.
     - Build: a runbook for each critical failure and a post-mortem template.

801. Change management and release approvals
     - Covers: controlling changes.
     - Details: record, review, and approve changes to code, config, and parameters, with a rollback plan.
     - Pitfall: urgent changes that bypass process.
     - Build: change log and approval workflow.

802. Middle- and back-office workflows (confirmations, reconciliation, breaks)
     - Covers: post-trade operations.
     - Details: confirm trades, reconcile positions and cash, investigate breaks, and manage settlement.
     - Pitfall: breaks left open and growing.
     - Build: break tracker with aging and owners.

803. Corporate-action elections and proxy handling
     - Covers: shareholder events.
     - Details: elections for rights, tenders, and mergers, plus voting rights and deadlines.
     - Pitfall: missed deadlines.
     - Build: corporate-action calendar with alerts.

804. Business continuity planning and key-person risk
     - Covers: continuity.
     - Details: documented procedures and backup people for critical functions.
     - Pitfall: one person who knows everything.
     - Build: continuity plan and cross-training matrix.

805. Vendor and service-level agreement management
     - Covers: third parties.
     - Details: track vendors, SLAs, contract terms, and exit options.
     - Pitfall: no fallback if a vendor fails.
     - Build: vendor register with criticality and alternatives.

## 17.2 Regulation, compliance, and audit

806. Regulation and compliance (MiFID II, SEC/FINRA, KYC/AML, audit trails)
     - Covers: legal framework.
     - Details: registration, reporting, algorithmic-trading controls, anti-money-laundering, and record keeping vary by jurisdiction and activity.
     - Pitfall: assuming rules for prop trading apply to managing client money.
     - Build: obligations register with owners and evidence.

807. Ethics and manipulation boundaries (spoofing, layering, wash trading)
     - Covers: prohibited conduct.
     - Details: placing orders without intent to execute, creating false volume, or misleading others is illegal in most markets.
     - Pitfall: algorithms that unintentionally resemble manipulation.
     - Build: pattern checks on your own order activity.

808. Record retention and best-execution evidence
     - Covers: keeping records.
     - Details: orders, quotes, communications, and decisions kept for required periods.
     - Pitfall: records that cannot be retrieved.
     - Build: retention policy and retrieval test.

809. Market-abuse surveillance (self-monitoring for spoofing and layering)
     - Covers: internal monitoring.
     - Details: detect high cancel ratios, layered orders, and wash-like trades.
     - Pitfall: no surveillance until a regulator asks.
     - Build: surveillance reports and review process.

810. SOC 2, ISO 27001, and audit readiness
     - Covers: assurance frameworks.
     - Details: documented controls, evidence collection, and periodic audits.
     - Pitfall: controls only on paper.
     - Build: control matrix with evidence links.

811. GDPR and data privacy
     - Covers: personal data.
     - Details: lawful basis, minimization, access and deletion rights, and breach notification for user data.
     - Pitfall: storing unnecessary personal data.
     - Build: data inventory and retention rules.

812. Intellectual property protection for strategies and open-source licensing
     - Covers: protecting and using IP.
     - Details: confidentiality agreements, access controls, and license compatibility of dependencies.
     - Pitfall: incompatible open-source licenses.
     - Build: license scan and IP policy.

813. Insurance (errors and omissions, cyber, fidelity)
     - Covers: risk transfer.
     - Details: coverage types and exclusions.
     - Pitfall: assuming trading losses are covered.
     - Build: coverage review against risk register.

814. AI governance (explainability requirements, model-risk regulation, and AI regulatory frameworks)
     - Covers: rules for AI use.
     - Details: documentation, testing, monitoring, and human oversight for AI-driven decisions.
     - Pitfall: unreviewed models in production.
     - Build: AI inventory and risk classification.

## 17.3 Governance and model oversight

815. Model validation and independent review
     - Covers: independent challenge.
     - Details: review of assumptions, data, code, and performance by someone other than the developer.
     - Pitfall: developers validating their own models.
     - Build: validation report template.

816. Investment and risk committee processes
     - Covers: decision forums.
     - Details: regular meetings with agendas, minutes, and defined authority for approvals and limit changes.
     - Pitfall: decisions without records.
     - Build: committee charter and minutes.

817. Documentation and decision logs
     - Covers: recording rationale.
     - Details: write down why parameters or strategies were chosen or changed.
     - Pitfall: lost reasoning.
     - Build: decision-log template.

## 17.4 Business and legal structure

818. Legal structure (prop, fund, RIA, CTA, CPO)
     - Covers: entity and registration choices.
     - Details: trading own capital differs from managing others' capital in registration, liability, and reporting.
     - Pitfall: operating without required registration.
     - Build: legal-structure comparison with a qualified adviser.

819. Counterparty and prime brokerage selection
     - Covers: choosing providers.
     - Details: compare financing, execution, custody, reporting, and credit risk.
     - Pitfall: single-provider dependence.
     - Build: scoring sheet and diversification policy.

820. Business model, fees, licensing
     - Covers: revenue and cost.
     - Details: management and performance fees, software licensing, or proprietary profits.
     - Pitfall: ignoring fixed costs at small scale.
     - Build: unit economics and break-even.

821. Capital raising and investor relations
     - Covers: working with investors.
     - Details: track record presentation, due-diligence responses, and reporting.
     - Pitfall: overstating results.
     - Build: due-diligence package and reporting calendar.

## 17.5 Product and platform features (if multi-user)

822. User roles, permissions, and tenant isolation
     - Covers: multi-user security.
     - Details: role-based access and strict separation of tenant data.
     - Pitfall: cross-tenant data leakage.
     - Build: permission matrix and isolation tests.

823. Customer onboarding, suitability checks, and disclosures
     - Covers: user entry.
     - Details: identity verification, risk questionnaires, and clear risk disclosure.
     - Pitfall: onboarding without required checks.
     - Build: onboarding flow with compliance review.

824. Strategy marketplace, copy trading, and social trading
     - Covers: sharing strategies.
     - Details: transparency of performance, fee sharing, and risk controls on copiers.
     - Pitfall: misleading performance claims.
     - Build: verified track-record display.

825. White-label and broker-integration marketplace
     - Covers: partner distribution.
     - Details: branding, integration standards, and responsibility boundaries.
     - Pitfall: unclear liability.
     - Build: integration certification checklist.

826. Billing, subscriptions, and customer support
     - Covers: commercial operations.
     - Details: pricing plans, invoicing, refunds, and support SLAs.
     - Pitfall: billing errors.
     - Build: billing reconciliation.

827. Mobile and notification delivery reliability
     - Covers: reaching users.
     - Details: push, SMS, and email fallbacks with delivery tracking.
     - Pitfall: critical alerts that never arrive.
     - Build: delivery monitoring and fallback paths.

828. Terms of service and liability limits
     - Covers: legal terms.
     - Details: scope of service, disclaimers, and limitations of liability reviewed by counsel.
     - Pitfall: terms that do not match actual behavior.
     - Build: reviewed terms and a change process.
