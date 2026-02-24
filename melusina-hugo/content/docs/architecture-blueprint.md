---
type: "doc"
title: Pearl architecture blueprint
category: advanced
tags: [pearls, helpers, isolation]
excerpt: Lay down the control planes, helpers, and isolation layers that make every Melusina Pearl sovereign.
readTime: 8 min read
lastUpdated: 2025-01-12
featured: true
author: Platform engineering
difficulty: advanced
stylesheets:
  - "/css/main.css"
  - "/fonts/fonts.css"
---

## Pearl-per-client isolation with helper-guarded egress

Follow this walkthrough to ship a Pearl ring, register helpers, and keep every action evidentiary by default.

## Executive summary — Three planes keep Pearls honest

Each Pearl is a hardened, sovereign container. Capability tokens broker access, helpers enforce any outbound motion, and evidence drops on the timeline the moment it happens.

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Pearl grid** | Namespace isolation | Every case lives in its own namespace with rotating hostnames. |
| **Helper mesh** | Audited egress | Outbound HTTP, mail, OTP, AI, and publishing flow through audited helpers. |
| **Timeline** | Immutable evidence | Every helper receipt, decision, and file action leaves an immutable breadcrumb. |

## Pearl layout

A Pearl bundles the UI, GraphQL API, storage, and evidence timeline behind a wildcard origin.

Each Pearl is immutable at build time and configurable at runtime via manifests shipped from the control plane.

### Wildcard origins

Sessions land on random subdomains so browsers cannot share localStorage, IndexedDB, or cookies across Pearls.

### Capability headers

UI and helper calls arrive with capability headers describing the exact permissions granted by the case owner.

### Inline AI lane

Pearls call local LLM helpers through capability-scoped sockets so prompts and completions never leave the tenant cluster. *(Beta)*

> **Sizing guidance**: 1 Pearl vCPU per 300 concurrent reviewers keeps UI p95 < 250 ms. Scale storage separately via object-store mounts.

## Helper mesh — Outbound traffic is always mediated

Helpers live outside the Pearl but cannot move without a signed capability and policy attached to the request.

### HTTP helper

Applies allowlists, header signing, payload hashing, and writes receipts before touching any sanctions or CRM endpoint.

### Comm helper

Delivers email, SMS, and Telegram messages from your infrastructure while logging proof-of-delivery and redacting payloads.

### Publishing helper

Builds static, expiring evidence portals so regulators can view bundles without getting Pearl accounts.

> **Helper posture**: Treat helpers like tier-0 workloads — mTLS everywhere, signed container images, and read-only file systems.

## Timeline — Evidence that keeps auditors happy

Nothing leaves the Pearl without a breadcrumb. Each helper writes receipts that include hashes, timestamps, and operator context.

### Dual-write automations

Every automation emits an internal log plus an export-friendly event with the actor, helper receipt, and evidence pointer.

### Retention controls

Keep full-fidelity events in the Pearl while shipping hashed digests to your SIEM for anomaly detection.

> **Regulator ready**: Timeline export bundles include helper receipts, reviewer context, screenshots, and signature files so an auditor can replay the case offline.

## Pre-go-live checklist

- [x] **Register wildcard DNS entries** — Point `*.melusina.local` to the front door with 1-minute TTLs.
- [ ] **Bootstrap helper trust** — Issue mTLS certs from your CA and load capability signing keys into the vault-managed secret store. *(In progress)*
- [ ] **Wire SIEM sinks** *(optional)* — Forward timeline digests and helper receipts to Splunk or Elastic with namespace labels.

## Deployment timeline

| Phase | Title | Description | Status |
|-------|-------|-------------|--------|
| Week 0 | Sandbox Pearl ring | Deploy base images, configure wildcard DNS, and validate TLS termination. | Complete |
| Week 1 | Helper registration | HTTP, comms, OTP, AI, and publishing helpers request scoped capabilities and log receipts. | In progress |
| Week 2 | Timeline validation | Trigger synthetic cases and confirm every helper writes receipts plus evidence attachments. | Not started |

## Resources

- [Architecture overview](/architecture/) — Platform architecture pillars and security design.
- [Helper hardening checklist](https://reference.melusina-os.org/helpers/hardening) — Security baselines for every helper type plus remediation flow.
- [Timeline export sample](https://reference.melusina-os.org/timeline-sample) — Inspect the JSON export auditors receive when requesting evidence.
