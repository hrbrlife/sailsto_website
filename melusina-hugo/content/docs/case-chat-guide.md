---
type: "doc"
title: Case Chat & Collaboration Controls
category: advanced
tags: [chat, collaboration, timeline, evidence, pin]
excerpt: Deep dive on configuring Melusina's built-in case chat, pinning workflows, notifications, and evidence exports.
readTime: 12 min read
lastUpdated: 2025-02-14
difficulty: intermediate
author: Melusina Team
stylesheets:
  - "/css/main.css"
  - "/fonts/fonts.css"
---

# Case Chat & Collaboration Controls

Melusina ships a case-scoped chat module so reviewers never leave the capability-scoped console described on the KYC System page. Chat, mentions, playbooks, and attachments stay inside the Pearl, and every message is ready for export alongside documents, screenings, wallets, and approvals.

## Architecture inside a Pearl

| Component | Role | Notes |
|-----------|------|-------|
| **Case Channel** | Lives next to queue, risk insights, and document stacks. | Automatically created for every case and inherits the case capability token. |
| **Message Service** | Persists text, reactions, and metadata. | Writes to the evidence timeline so a regulator can replay the conversation. |
| **Attachment Helper** | Scans, redacts, and tags uploads. | Re-uses the same file hygiene helpers mentioned on the landing and KYC pages. |
| **Notification Plane** | Email/SMS/Telegram brokers plus in-app toasts. | Runs through the comm helper so deliveries show up as receipts. |
| **Export Bridge** | Bundles chat into expiring, read-only evidence links. | Uses the publishing helper that powers full case exports. |

Because Pearls sit behind wildcard origins and capability headers, a chat channel is isolated per client and per case. Messages inherit the same RBAC model outlined in the security guide - operators can read/write, supervisors can pin/unpin, and auditors get read-only mirrors.

## Core objects

| Object | Description | Default retention |
|--------|-------------|-------------------|
| **Channel** | Single thread tied to a case and mirrored on the timeline. | Case lifetime + retention policy. |
| **Message** | Text body plus structured metadata (mentions, reactions, helper receipt). | Same as channel. |
| **Pin** | Highlight that anchors a message to the top of the chat and timeline export. | 7 days (configurable). |
| **Attachment** | File or voice note scanned, redacted, and virus-checked before reviewers see it. | Case lifetime unless manually purged. |
| **Playbook Trigger** | Automation snippet triggered from the chat using slash commands. | Logs stored as timeline entries. |

## Configuration

Add the chat configuration block to `.env` when you bootstrap a Pearl:

```env
# Chat module
CHAT_ENABLED=true
CHAT_RETENTION_DAYS=365
CHAT_ATTACHMENT_SCAN_MODE=clamav
CHAT_ATTACHMENT_REDACTION_POLICY=auto
CHAT_PIN_LIMIT=3
CHAT_PIN_DEFAULT_TTL_HOURS=168
CHAT_PIN_REQUIRE_SUPERVISOR=true
CHAT_NOTIFICATION_CHANNELS=email,sms,telegram,in_app
CHAT_PIN_OTP_CHANNEL=email
```

| Variable | Purpose |
|----------|---------|
| `CHAT_ENABLED` | Global switch; disable to hide chat UI entirely. |
| `CHAT_RETENTION_DAYS` | Governs how long chat artifacts stay after case closure. |
| `CHAT_ATTACHMENT_SCAN_MODE` | `clamav` or `external`; ensures files are scanned before render. |
| `CHAT_ATTACHMENT_REDACTION_POLICY` | `auto`, `manual`, or `off`. Auto redacts IDs, account numbers, and wallet seeds by default. |
| `CHAT_PIN_LIMIT` | Maximum concurrently pinned messages to avoid clutter. |
| `CHAT_PIN_DEFAULT_TTL_HOURS` | Auto-expire pins when a case moves forward. |
| `CHAT_PIN_REQUIRE_SUPERVISOR` | Forces RBAC check so only supervisors can pin/unpin. |
| `CHAT_NOTIFICATION_CHANNELS` | Ordered list of helper-backed channels that receive chat digests. |
| `CHAT_PIN_OTP_CHANNEL` | Optional OTP/PIN confirmation channel for high-signal pins (reuses the OTP approvals helper). |

Restart the Pearl after editing `.env` so helpers reload the chat manifest.

## Pinning and highlights

Supervisors can elevate any message into a pin so investigators and auditors see it above the chat feed and at the top of the evidence timeline. Pins carry structured data:

```json
{
  "message_id": "msg_92af9",
  "pinned_by": "sup_alex",
  "reason": "SAR draft needs legal sign-off",
  "ttl_hours": 72,
  "otp_receipt": "comm_helper_6f112",
  "timeline_entry": "tl_55ae3"
}
```

### Pin workflow

1. Reviewer clicks **Pin** on a message.
2. System checks `CHAT_PIN_LIMIT` and RBAC.
3. If `CHAT_PIN_REQUIRE_SUPERVISOR` is true, supervisors get an OTP (email/SMS/Telegram). That OTP acts as the short-lived PIN confirmation.
4. On approval, the message gets a `pin` badge, the evidence timeline logs it, and related playbooks (escalation, legal review, etc.) can trigger automatically.
5. When TTL expires or the supervisor unpins, the timeline records the removal.

### Pin API

```bash
# Pin a message for 48 hours
curl -X POST https://kyc.example.com/api/v1/cases/{case_id}/chat/pins \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "message_id": "msg_92af9",
        "reason": "Escalated to compliance",
        "ttl_hours": 48
      }'

# Remove a pin
curl -X DELETE https://kyc.example.com/api/v1/cases/{case_id}/chat/pins/{pin_id} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Pins are included in `/api/v1/cases/{case_id}/exports/full` so regulators immediately see the highest-signal items without reading the entire transcript.

## Notification settings

All chat notifications use the communication helper highlighted in the KYC System copy. Configure channel behavior per role:

| Channel | Typical Use | Notes |
|---------|-------------|-------|
| **In-app toast** | Real-time nudges inside the reviewer cockpit. | Mirrors the Bootstrap Lab toast placement examples; can pin to any corner. |
| **Email** | Digest of overnight messages. | Signed via your SMTP helper with DMARC alignment. |
| **SMS** | Hot-case escalations. | Configurable quiet hours per reviewer. |
| **Telegram** | Ops war-room mirroring. | Uses bot tokens stored in the helper vault. |

Example subscription payload:

```bash
curl -X POST https://kyc.example.com/api/v1/cases/{case_id}/chat/subscriptions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
        "user_id": "rev_mina",
        "channels": ["in_app", "email"],
        "notify_on": ["mention", "pin_created", "attachment_uploaded"]
      }'
```

## Attachments and redaction pipeline

- Uploads land in the case namespace and are hashed before they leave the browser.
- The attachment helper scans with ClamAV (or your configured engine), redacts IDs, wallet numbers, and biometric data, and stores both clean and original copies with different capability tokens.
- Every attachment inherits the chat message retention policy and is listed in the evidence timeline with a pointer back to the chat transcript.
- Overrides require reviewers to drop a note - the same override rules used for document verification stay consistent here.

## Evidence exports and publishing

When you build an evidence pack, chat is bundled automatically so you get the "docs, chat, screenings, wallets, approvals" promise from the landing page:

```bash
curl -X POST https://kyc.example.com/api/v1/cases/{case_id}/exports/full \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"include_chat": true, "format": "pdf"}'
```

Exports include:

- Chronological transcript with pin markers and OTP receipts.
- Attachment manifest (redacted + original hash).
- Mention map (who was tagged, when, and whether they acknowledged).
- Helper receipts showing which notification channel delivered each alert.

The publishing helper can also make a read-only chat viewer for regulators with expiring signed URLs.

## Automation and playbooks

Chat integrates with playbooks so reviewers can launch templated tasks without leaving the conversation:

- `/playbook escalate` -> Creates a task, pins the triggering message, and notifies legal.
- `/playbook remind` -> Schedules OTP reminders (email/SMS/Telegram) via the comm helper.
- `/playbook ai-summary` -> Calls the inline AI lane inside the Pearl to summarize the conversation and pins the output.

Playbook executions show up as timeline entries, satisfying the "inline collaboration" promise on the KYC page.

## Observability and auditing

Operations teams can trend chat health in the same dashboards that track identity, AI, screening, and wallet events:

- **Metrics**: message rate, attachment count, pin velocity, notification latency.
- **Logs**: OTP receipts, helper delivery proofs, pin/unpin actions.
- **Alerts**: threshold-based toasts (for example, auto-pin if no response after X hours).

Forward logs to your SIEM the same way you do for helper telemetry so auditors see tamper-evident chains.

## Operational checklist

1. **Enable chat** in `.env` and redeploy Pearls.
2. **Map roles** (viewer, operator, supervisor, auditor) to chat permissions alongside existing RBAC.
3. **Tune pins**: set TTL, OTP requirements, and pin limit so only critical context floats to the top.
4. **Wire notifications** through comm helpers and confirm delivery receipts on the evidence timeline.
5. **Review retention** to ensure chat aligns with your jurisdictional data policies.
6. **Test exports** to confirm chat, pins, and attachments appear in regulator-ready bundles.
7. **Document playbooks** so reviewers know which slash commands trigger automations.

With these controls, case chat stops being an informal channel and becomes an auditable, policy-enforced collaboration surface that matches the rest of the Melusina stack.
