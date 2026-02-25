# Melusina OS — Master Dogma

> This document defines who Melusina OS is, what it does, and how every expert
> should evaluate its website. Feed this to ALL agents as immutable context.

---

## Identity

**Melusina OS** is a sovereign Web3 superapp operating system. It is a
hardened fork of Sandstorm.io (battle-tested since 2014) that runs on
your own server or PC — not in someone else's cloud. You access it from
any browser. It is NOT a browser app; the PWA is a convenience shortcut.

**Tagline**: Sovereign Web3 Superapp OS

**Domain**: melusina-os.org

---

## What Melusina OS IS vs. IS NOT

| IS | IS NOT |
|----|--------|
| A server OS you run on YOUR hardware | A cloud service or SaaS |
| A Sandstorm.io fork (battle-tested since 2014) | A new, unproven platform |
| Capability-based isolation (Pearls) | Container orchestration (not Docker/K8s) |
| Self-sovereign identity via NFT trust chain | Centralized identity provider |
| Solana-native for all on-chain operations | Multi-chain / chain-agnostic |
| Infrastructure for building apps | An app itself |

---

## Relationship to Other Group Products

| Product | Relationship |
|---------|-------------|
| **Sails.to** | Sails.to runs ON Melusina OS infrastructure |
| **AiTX.pro** | AiTX.pro uses Melusina OS APIs and AI agent framework |
| **KYC.lat / InstaKYC** | KYC verification app built on Melusina OS |
| **InstaTrust** | Trust management app built on Melusina OS |
| **InstaDAO** | DAO tooling app built on Melusina OS |

Cross-contamination: Melusina OS pages should NOT present themselves as
Sails.to, AiTX.pro, or KYC.lat. They may reference these as apps that
run on Melusina OS, but the site is about the OS/platform itself.

---

## Target Audiences

1. **Decision makers** (CTOs, COOs, compliance heads) — "why should I care?"
2. **Technical evaluators** (architects, security leads) — "how does it work?"
3. **Regulators & auditors** — "can I verify this independently?"

The landing page speaks to audience #1. Architecture speaks to #2.
TrustMaster and compliance pages speak to #3.

---

## Canonical Terminology

| Correct Term | Wrong Variants | Notes |
|---|---|---|
| Melusina OS | melusina os, MelusinaOS, MelusOS, MELUSINA OS, Melusina-OS | Two words, both capitalized |
| Pearl | grain, container | Canonical term for an isolated container instance. "Grain" is legacy Sandstorm — avoid except in deep technical docs. Always capitalized. |
| Grapple | Pearlbox, Powerbox | The capability broker. Always capitalized. |
| keyholder | key holder, key-holder | One word, no hyphen |
| trust chain | trust hierarchy, trust tree | NFT-based: Foundation → Reseller → License → Shares |
| TrustMaster | Trust Master, trust master | One word, capitalized. Independent verification tool. |
| Solana | solana, SOL chain | Always capitalized. Specify "Solana blockchain" on first use. |
| Cap'n Proto | CapnProto, capnp, Captain Proto | Always "Cap'n Proto" with apostrophe |
| server or PC | cloud, browser app, device | Melusina runs on YOUR server or PC |
| soulbound | soul-bound, soul bound | NFTs that can't be transferred |

---

## Key Technical Facts (verified, do not change)

- Sandstorm.io fork, battle-tested since 2014
- NFT trust chain: Foundation → Reseller → License → Shares
- Cap'n Proto RPC backbone (created by Kenton Varda, ex-Google, Protobuf creator)
- Solana Memo transactions = immutable audit trail
- Threshold cryptography = Shamir secret sharing over GF(256) with Lagrange interpolation
- OTP is grain-blind: the grain never sees the OTP code, gets HMAC proof token back
- Push notifications are content-free: empty payloads prevent data leakage
- 3-tier wallet login: browser extension → Mobile Wallet Adapter → QR code
- DANE-pinned TLS via DNSSEC-signed TLSA records
- 44 unit tests verify the crypto

---

## The NFT Trust Chain (THE differentiator)

This is the core innovation. Every reviewer must understand it:

**Foundation NFT** (top level) → mints **Reseller NFTs** → mint **License NFTs** → mint **Share NFTs**

Each level can freeze the one below it. "Employee leaves? Freeze their
Admin NFT — access revoked in the same Solana block." TrustMaster lets
anyone independently verify the chain on-chain.

---

## Voice & Tone

- **Direct, confident, slightly confrontational** — like sails.to
- **Concrete scenarios over abstract features** — "Employee leaves? Freeze their NFT." > "Enhanced security posture"
- **Benefits before architecture** — "anyone can verify" > "cryptographically verifiable"
- **The dinner test** — if you wouldn't say it to a smart friend at dinner, rewrite it
- **No AI buzzwords** — kill "leveraging", "seamless", "cutting-edge", "revolutionize"
- **Specific is credible** — "44 unit tests", "battle-tested since 2014", "Solana block time"

---

## Made to Stick Criteria

Every piece of copy should pass the SUCCESs framework:
- **S**imple — one core message per section
- **U**nexpected — break a pattern ("Your license is a PDF in someone's inbox")
- **C**oncrete — can you picture it happening?
- **C**redible — evidence, not assertion
- **E**motional — does it make you feel something?
- **S**tories — is there a scenario a reader can see themselves in?

---

## Review Philosophy

When reviewing Melusina OS pages, every expert should ask:

1. **5-second test**: Can someone understand what Melusina OS does within 5 seconds?
2. **Audience check**: Does this page know WHO it's talking to?
3. **Pearl explanation**: Is the Pearl concept explained concretely?
4. **Trust chain**: Is the NFT trust chain explained with a scenario, not abstract hierarchy?
5. **Differentiation**: Is it clear this is NOT just another cloud platform?
6. **Jargon density**: Count words a non-technical CEO wouldn't know — each one should be explained or eliminated
7. **"So what?" test**: For every feature mentioned, does the text explain WHY I should care?
