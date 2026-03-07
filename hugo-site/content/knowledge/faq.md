---
title: "FAQ"
type: "page"
layout: "knowledge-faq"
description: "Frequently asked questions about Sails.to CrossSecurities platform. Learn about CrossSecurities, CrossConversion, compliance, costs, timelines."
keywords:
  - crosssecurities FAQ
  - tokenization questions
  - CrossConversion questions
  - compliance questions
  - how to tokenize
  - tokenization costs
ogImage: "/og-faq.png"
faqSchema: true
faqItems:
  - question: "What is Sails.to?"
    answer: "Sails.to is a CrossSecurities infrastructure platform that bridges blockchain technology with traditional finance. We enable businesses to issue compliant CrossSecurities that can be held on-chain on the Solana blockchain or CrossConverted to bankable securities with an ISIN for custody at institutions like Clearstream."
    category: "general"
  - question: "How much does it cost to launch a token?"
    answer: "Zero upfront cost. We operate on a success-based fee model. Direct investors pay 1% distribution fee, broker-introduced investors pay 6% (includes broker commission). Secondary trades incur 0.5% fee. If soft cap fails, investors get full refund."
    category: "for-issuers"
  - question: "How long does it take to launch?"
    answer: "1-2 weeks from initial onboarding to token deployment. This includes issuer KYC verification, legal structure setup, token configuration, smart contract deployment, and investor portal setup."
    category: "for-issuers"
  - question: "Who can invest on Sails.to?"
    answer: "Offerings are available to accredited investors (U.S.) and professional investors (international) only. Requirements include net worth over $1M, annual income over $200K, professional certifications, or institutional status."
    category: "for-investors"
  - question: "How do I custody my tokens?"
    answer: "Two options: Self-custody on Solana using any compatible wallet (Phantom, Solflare, Ledger), or bankable custody via ISIN at Clearstream accessible through your bank. You can CrossConvert between formats anytime."
    category: "for-investors"
  - question: "What legal structure do you provide?"
    answer: "We create a Wyoming DAO LLC with Series LLC architecture. Each offering exists as an isolated series with its own assets, liabilities, and investors, providing liability protection while maintaining operational efficiency."
    category: "compliance"
  - question: "What is the NFT authority hierarchy?"
    answer: "Sails.to uses a 4-layer NFT hierarchy on Solana: Master NFT (root authority, 3-of-5 threshold) → Reseller NFT (print editions, can issue licenses) → License NFT (per-installation, issues KYC credentials) → Share NFT (per-domain access tokens, up to 10,000 per license). This cryptographic chain of trust governs every platform operation."
    category: "technical"
  - question: "What is a Grain?"
    answer: "A Grain is the fundamental isolation unit in Sandstorm/Melusina OS. Each grain is a sandboxed application instance with its own journal store, capabilities, and lifecycle. Sails.to uses Station grains (orchestrators like DAO Manager, Broker Portal) and Instance grains (workers like Offering, KYC, Investor Self-Service)."
    category: "technical"
  - question: "How does threshold signing protect critical operations?"
    answer: "Critical platform operations require M-of-N keyholder approval using Shamir-like threshold cryptography on Solana. Master NFT operations and force transfers require 3-of-5 keyholders. Large CrossConversions over $1M require 2-of-3. Standard CrossConversions require 1-of-1 Trustee NFT authentication."
    category: "technical"
  - question: "What is a Transfer Hook?"
    answer: "A Transfer Hook is a Solana SPL-2022 extension that intercepts every token transfer and enforces compliance rules before allowing it. The hook checks both wallets have valid KYC NFTs, verifies jurisdiction whitelists, enforces lock-up periods, and validates accreditation tiers. Non-compliant transfers are rejected on-chain."
    category: "compliance"
  - question: "How does the waterfall distribution work?"
    answer: "Revenue enters the Operating Series and flows through a priority waterfall enforced on-chain: (1) Senior debt holders first, (2) Investor distributions pro-rata by token holding, (3) Platform fee of 1%, (4) Excess to Treasury Series. Investors always get paid before the platform."
    category: "for-investors"
  - question: "What is Cap'n Proto and why do you use it?"
    answer: "Cap'n Proto is a zero-copy serialization protocol used for inter-grain RPC communication. Unlike JSON or Protocol Buffers, it requires no encoding or decoding step - data is read directly from the wire format. This enables native Sandstorm integration on FD3 without an HTTP bridge, giving maximum performance for capability-based security."
    category: "technical"
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/knowledge-faq.css"
scripts:
  - "/js/pages/kb-filters.js"
  - "/js/pages/knowledge-faq.js"
date: "2026-02-24"
lastmod: "2026-02-24"
sitemap:
  priority: 0.7
  changefreq: "monthly"
---
