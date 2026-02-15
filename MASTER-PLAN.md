# hrbr.life — Master Remediation & Build Plan

> Generated 2026-02-15 from 45-page site review across sails.to, melusina-os.org, and INSTAKYCAPP_WEBSITE.
> Reference: `site-review-log.txt`

---

## Brand Architecture

```
hrbr.life (Holding Company)
├── sails.to           — STO derivatives & capital markets platform     [Hugo]
├── melusina-os.org    — Sovereign OS for Web3 & AI era                 [Vite+React+TinaCMS]
├── kyc.lat            — Fintech/RegTech KYC self-hosted platform       [Vite+React — fork of INSTAKYCAPP]
├── pbay.app           — Pay-to-use hosted Melusina (≈ Sandstorm Oasis) [TBD]
└── static-store       — App marketplace                                [Vite — melusina-static-store repo]
```

**Reference standard:** sails.to (8/10) — all other sites should match this quality bar.

---

## Milestone 0 — Triage & Quick Wins *(same session)*

Fixes that unblock everything else. No architectural changes.

- [ ] **0.1** Fix `seo?.keywords?.join` TypeError on Roadmap & FAQ pages (main branch)
  - File: likely in SEO component or page loader
  - Fix: guard `Array.isArray(seo.keywords)` before `.join()`
- [ ] **0.2** Fix self-referencing 404 loop: 404 page → "Contact Support" → `/contact` → 404
  - Change `/contact` link to `/en-US/company` or `mailto:sales@melusina-os.org`
- [ ] **0.3** APPS dropdown — hide apps without pages
  - Show only: Bureau + "Browse App Market →" link to static-store
  - Remove: Office, Communication, Internet, Vintage, InstaKYC, InstaRemit, InstaDAO, InstaSTO
- [ ] **0.4** Demote blog from nav on melusina-os.org branch (empty — "No posts yet")
  - Move from top nav to footer or remove until content exists

---

## Milestone 1 — InstaKYC → kyc.lat Rebrand

Full find-and-replace across the INSTAKYCAPP_WEBSITE repo (both branches).

### 1A. Content files (JSON/MD)
- [ ] **1.1** Audit all `InstaKYC` / `instakyc` / `InstaKYC_Support` occurrences
  - `grep -ri "instakyc" content/ src/ public/ --include="*.json" --include="*.tsx" --include="*.ts" --include="*.md"`
- [ ] **1.2** Replace in page content JSON: `InstaKYC` → `kyc.lat`
- [ ] **1.3** Replace page titles: `"FAQ | InstaKYC"` → `"FAQ | kyc.lat"`
- [ ] **1.4** Replace page titles: `"Company | InstaKYC"` → `"Company | kyc.lat"`
- [ ] **1.5** Replace page titles: `"Knowledge Base | InstaKYC"` → `"Knowledge Base | kyc.lat"`
- [ ] **1.6** Replace: `"Compare InstaKYC vs SaaS"` → `"Compare kyc.lat vs SaaS KYC Providers"`
- [ ] **1.7** Replace Telegram: `@InstaKYC_Support` → new handle (TBD — `@kyc_lat`?)
- [ ] **1.8** Replace: `"Ready to deploy InstaKYC?"` → `"Ready to deploy kyc.lat?"`
- [ ] **1.9** Replace: `instakyc.app` → `kyc.lat` in footer descriptions

### 1B. TinaCMS content (melusina-os.org branch)
- [ ] **1.10** Update TinaCMS content files in `content/` directory
- [ ] **1.11** Verify changes render via TinaCMS admin

### 1C. French locale
- [ ] **1.12** Replace `Instakyc.app est la plateforme KYC auto-hébergée...` with kyc.lat French description
- [ ] **1.13** Update FR footer tagline to match new positioning

### 1D. Repo housekeeping
- [ ] **1.14** Rename GitHub repo `INSTAKYCAPP_WEBSITE` → `kyc-lat-website` (or similar)
- [ ] **1.15** Update `package.json` name field
- [ ] **1.16** Update README

---

## Milestone 2 — Fix Content Rendering (Main Branch)

The main branch migrated from TinaCMS to static JSON but left many components broken ("card" placeholders).

- [ ] **2.1** Audit `src/utils/content.ts` — the static content loader
  - Compare with TinaCMS GraphQL schema to find missing component mappings
- [ ] **2.2** Map all TinaCMS component types to static JSON equivalents
  - Known broken: card arrays, table components, accordion components
- [ ] **2.3** Fix card component rendering — likely missing array iteration or data shape mismatch
- [ ] **2.4** Fix table component rendering
- [ ] **2.5** Fix accordion component rendering (FAQ section on homepage)
- [ ] **2.6** Verify: Homepage, Use Cases, Compare, Plans all render without "card" text
- [ ] **2.7** Verify: French locale body content renders (not just nav)
- [ ] **2.8** Consider: TinaCMS build → static JSON export pipeline
  - `tinacms build` exports content → commit JSON → main branch reads statically

---

## Milestone 3 — Content Separation (melusina-os.org vs kyc.lat)

KYC-specific content currently lives on melusina-os.org and needs to move to kyc.lat.

### 3A. Identify content to move
- [ ] **3.1** Compare page content → kyc.lat (KYC provider comparison)
- [ ] **3.2** FAQ KYC questions → kyc.lat (deployment, compliance, KYC workflows)
- [ ] **3.3** Company page KYC messaging → kyc.lat
- [ ] **3.4** KYC glossary terms (AML, KYC, Due Diligence) → kyc.lat
- [ ] **3.5** Knowledge Base KYC articles → kyc.lat

### 3B. Create kyc.lat site
- [ ] **3.6** Fork INSTAKYCAPP_WEBSITE repo as `kyc-lat-website`
- [ ] **3.7** Strip OS-specific content, keep KYC content
- [ ] **3.8** Update branding: kyc.lat domain, KYC-focused hero, regtech positioning
- [ ] **3.9** Deploy to kyc.lat domain

### 3C. Clean melusina-os.org
- [ ] **3.10** Remove KYC-specific Compare page content — replace with OS comparison (vs Nextcloud, Synology, etc.)
- [ ] **3.11** Rewrite FAQ for OS questions (deployment, Pearl concept, app installation)
- [ ] **3.12** Rewrite Company page for Melusina OS positioning
- [ ] **3.13** Split glossary: keep OS terms (Pearl, Pearlbox, Bureau, Capability URL), move KYC terms
- [ ] **3.14** Verify melusina-os.org homepage → Use Cases → Plans flow is pure OS messaging

---

## Milestone 4 — sails.to Multilingual (Hugo i18n)

Add French (and future languages) to the reference standard site.

### 4A. Hugo i18n setup
- [ ] **4.1** Update `hugo.toml` with multilingual config
  ```toml
  defaultContentLanguage = "en"
  [languages]
    [languages.en]
      languageName = "English"
      weight = 1
    [languages.fr]
      languageName = "Français"
      weight = 2
  ```
- [ ] **4.2** Create `i18n/en.toml` and `i18n/fr.toml` for UI strings
- [ ] **4.3** Add language switcher partial to navbar
- [ ] **4.4** Restructure content: `content/en/` and `content/fr/` (or filename-based: `_index.fr.md`)

### 4B. French content
- [ ] **4.5** Translate homepage (`_index.md`)
- [ ] **4.6** Translate key pages: issuers, investors, brokers, pricing, signup
- [ ] **4.7** Translate nav, footer, CTAs via i18n strings
- [ ] **4.8** Verify all 15 reviewed pages work in both locales
- [ ] **4.9** Test language switcher preserves current page

---

## Milestone 5 — New Sites

### 5A. pbay.app — Hosted Melusina
- [ ] **5.1** Define positioning: "Melusina without the sysadmin" / managed hosting
- [ ] **5.2** Choose stack (Hugo for consistency with sails.to, or simple landing page)
- [ ] **5.3** Create landing page: pricing, signup, feature comparison vs self-hosted
- [ ] **5.4** Link to static-store for app browsing
- [ ] **5.5** Deploy to pbay.app domain

### 5B. hrbr.life — Holding Company
- [ ] **5.6** Define scope: portfolio page? investor relations? redirect hub?
- [ ] **5.7** Create minimal holding company page with links to all products
- [ ] **5.8** Deploy to hrbr.life domain

---

## Milestone 6 — Cross-Site Polish

### 6A. Consistent footer & legal
- [ ] **6.1** Standardize footer across all sites (© hrbr.life LLC, product links, legal)
- [ ] **6.2** Add cross-product links (each site links to siblings)
- [ ] **6.3** Privacy policy / terms — shared or per-product?

### 6B. Internal link audit
- [ ] **6.4** Crawl all sites for broken internal links (404s)
- [ ] **6.5** Crawl for broken external links
- [ ] **6.6** Verify all nav items resolve to real pages

### 6C. SEO & meta
- [ ] **6.7** Unique meta descriptions per page, per site
- [ ] **6.8** Open Graph / Twitter cards for social sharing
- [ ] **6.9** Sitemap generation for all sites
- [ ] **6.10** robots.txt per site

### 6D. Performance & accessibility
- [ ] **6.11** Lighthouse audit all sites (aim for 90+ on all scores)
- [ ] **6.12** Fix any accessibility issues found in review (skip-to-content already present)
- [ ] **6.13** Image optimization / lazy loading

---

## Milestone 7 — Blog & Content Strategy

- [ ] **7.1** Decide: one shared blog or per-product blogs?
- [ ] **7.2** Create 3-5 launch posts (product announcement, architecture deep-dive, use case story)
- [ ] **7.3** Set up blog infrastructure on chosen platform
- [ ] **7.4** Remove "Blog" from nav on sites without posts
- [ ] **7.5** Add blog to nav only when ≥3 quality posts exist

---

## Priority Matrix

| Milestone | Impact | Effort | Dependencies | Suggested Order |
|-----------|--------|--------|-------------|-----------------|
| M0 Triage | High   | Low    | None        | **Do first**    |
| M1 Rebrand | High  | Medium | None        | **Do second**   |
| M2 Content fix | High | Medium | M0       | **Do third**    |
| M3 Content split | Med | High | M1        | After M1        |
| M4 sails.to i18n | Med | Medium | None    | Parallel with M3|
| M5 New sites | Low  | High   | M1, M3     | After M3        |
| M6 Polish | Med    | Medium | M1-M5      | After all sites exist |
| M7 Blog | Low     | Medium | M6          | Last            |

---

## Open Questions (carry forward)

- [ ] Final pricing confirmation (€250K / €50K / €2K/mo — real or placeholder?)
- [ ] Launch timeline for each product
- [ ] Telegram handle for kyc.lat (replacing @InstaKYC_Support)
- [ ] pbay.app pricing model (per-user? per-instance? freemium?)
- [ ] hrbr.life scope (portfolio page vs full investor site)
- [ ] Shared design system / component library across React sites?
- [ ] CI/CD pipeline for automated deployment of all sites
