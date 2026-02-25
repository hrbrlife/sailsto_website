# Sails.to UX & Style Guide

## Platform Overview

Sails.to is a CrossSecurities platform for issuing tokenized securities (bonds, equity, revenue share agreements) using Wyoming DAO LLC legal structures with Solana blockchain infrastructure and TradFi integration via Clearstream for ISINs.

---

## 🎯 Target Audiences

| Audience | Profile | Key Concerns |
|----------|---------|--------------|
| **Issuers** | Companies raising $1M-$50M via bonds/securities | Cost, compliance, control, speed |
| **Investors** | Professional/accredited (high net worth) | Security, returns, liquidity, legitimacy |
| **Brokers** | Licensed securities dealers | Regulatory compliance, white-label, fees |
| **Institutions** | Trust companies, VCs, MFOs | Due diligence, custody, reporting |
| **Introducers** | Referral partners | Commission structure, easy onboarding |

---

## 🚨 CRITICAL UX RULES FOR FINANCIAL PLATFORMS

### Rule 1: Trust Above All Else
**WHY:** We're asking people to invest money. Any doubt = no conversion.

**Requirements:**
- Professional, clean aesthetic (NOT crypto-bro/meme coin vibes)
- Visible trust signals (regulated, audited, established)
- Real company info (address, team, contact methods)
- Clear legal disclosures without being overwhelming

**Good Examples:**
- Carta, AngelList, Republic, Bloomberg
- Clean cards, professional typography, muted colors

**Bad Examples:**
- Flashy animations, neon colors, rocket ship emojis
- Vague team info, hidden contact details
- Crypto jargon without explanation

### Rule 2: Clarity Over Cleverness
**WHY:** Financial products are complex. Don't add confusion.

**Requirements:**
- Explain what we do in 5 seconds (value prop first)
- Define financial/crypto terms when first used
- Use progressive disclosure (simple → detailed)
- Avoid industry jargon in headlines

**Good:**
> "Issue compliant security tokens in 30 days"

**Bad:**
> "Leveraging DLT infrastructure for capital formation optimization"

### Rule 3: One Primary Action Per Section
**WHY:** Decision fatigue kills conversions.

**Requirements:**
- Single clear CTA per hero section
- Secondary actions styled differently (ghost buttons, links)
- Progressive calls-to-action down the page
- Navigation should not compete with conversion CTAs

### Rule 4: Mobile-First is Non-Negotiable
**WHY:** Investors check opportunities on phones.

**Requirements:**
- Touch targets min 44x44px
- No horizontal scrolling
- Readable text without zooming (16px+ body)
- Forms work on mobile keyboards
- Navigation accessible via hamburger menu

### Rule 5: Load Time = Trust Time
**WHY:** Slow sites feel untrustworthy and amateurish.

**Requirements:**
- First contentful paint < 1.5s
- No layout shift after load
- Optimized images (WebP, proper sizing)
- Lazy load below-fold content

---

## 📐 Visual Design Standards

### Color Palette
```
Primary:        #1E1B4B (Deep Purple) - Headers, primary buttons
Secondary:      #3730A3 (Indigo) - Accents, links
Surface:        #F8FAFC (Light) / #0F172A (Dark) - Backgrounds
Text Primary:   #1E293B (Slate 800)
Text Secondary: #64748B (Slate 500)
Success:        #22C55E (Green 500)
Warning:        #F59E0B (Amber 500)
Error:          #EF4444 (Red 500)
Gold Accent:    #C9A227 (Brand gold)
```

### Typography
```
Font Family:    Inter, system-ui, sans-serif
H1:             text-4xl (2.25rem) font-bold tracking-tight
H2:             text-3xl (1.875rem) font-semibold
H3:             text-2xl (1.5rem) font-semibold
H4:             text-xl (1.25rem) font-medium
Body:           text-base (1rem) leading-relaxed
Small:          text-sm (0.875rem)
Caption:        text-xs (0.75rem) text-gray-500
```

### Spacing System
```
Section Padding:  py-16 md:py-24 (64px / 96px)
Card Padding:     p-6 (24px)
Section Gap:      space-y-8 (32px)
Element Gap:      space-y-4 (16px)
Inline Gap:       gap-3 (12px)
```

### Component Standards

#### Buttons
```
Primary:    bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-6 py-3 font-medium
Secondary:  bg-white border border-gray-200 hover:bg-gray-50 text-gray-900 rounded-lg px-6 py-3
Ghost:      text-indigo-600 hover:text-indigo-800 hover:underline
Disabled:   bg-gray-200 text-gray-400 cursor-not-allowed
Min Height: 48px for mobile touch targets
```

#### Cards
```
Base:       bg-white rounded-xl shadow-sm border border-gray-100
Hover:      hover:shadow-md transition-shadow
Padding:    p-6
Gap:        space-y-4
```

#### Forms
```
Input:      w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500
Label:      text-sm font-medium text-gray-700 mb-2
Error:      border-red-500 text-red-600 text-sm mt-1
Help:       text-sm text-gray-500 mt-1
```

---

## 📱 Responsive Breakpoints

```
Mobile:     < 640px  (sm)
Tablet:     640-1024px (md)
Desktop:    > 1024px (lg)
Wide:       > 1280px (xl)
```

### Mobile Requirements
- Full-width buttons
- Stacked layouts (no side-by-side cards)
- Hamburger navigation
- Larger touch targets
- No hover-dependent interactions

---

## ✅ Page-Type Checklists

### Landing Pages (Issuers, Investors, Brokers, etc.)
- [ ] Clear value proposition in hero (5-second test)
- [ ] Primary CTA visible without scrolling
- [ ] Trust signals present (regulatory, security, social proof)
- [ ] Benefits before features
- [ ] Mobile navigation works
- [ ] Page loads in < 2s
- [ ] No broken images or links

### Trust Pages (Security, Compliance, Oversight)
- [ ] Authoritative, factual tone
- [ ] Specific claims (not vague promises)
- [ ] Links to verification where possible
- [ ] Legal disclaimers appropriately placed
- [ ] Contact method available

### Knowledge Pages (Blog, Glossary, Docs)
- [ ] Clear hierarchy and navigation
- [ ] Readable typography (line height, width)
- [ ] Related content links
- [ ] Search or filter available for indexes
- [ ] Breadcrumb navigation

### Conversion Pages (Signup, Contact)
- [ ] Minimal fields (ask only what's needed)
- [ ] Progress indicator if multi-step
- [ ] Error messages are helpful
- [ ] Success state is clear
- [ ] Privacy/terms links present

---

## 🔍 Common UX Issues to Flag

### High Severity
- Page doesn't load or shows errors
- CTA button doesn't work
- Forms are broken
- Trust signals missing on conversion pages
- Mobile navigation broken
- Horizontal scrolling

### Medium Severity
- Slow load time (> 3s)
- Confusing value proposition
- Multiple competing CTAs
- Poor color contrast
- Missing alt text on images
- Inconsistent styling between pages

### Low Severity
- Minor spacing inconsistencies
- Hover states could be improved
- Could use better iconography
- Content could be more concise

---

## 📊 Scoring Framework

| Score | Description | Action |
|-------|-------------|--------|
| 9-10 | Exceptional | Ship it, iterate later |
| 7-8 | Good | Minor polish, low priority |
| 5-6 | Adequate | Needs attention, medium priority |
| 3-4 | Problematic | Significant issues, high priority |
| 1-2 | Critical | Blocking issues, fix immediately |

---

## 🔗 Reference Sites

**Good Examples (Professional Finance):**
- carta.com - Clean, professional, trustworthy
- angellist.com - Modern but serious
- republic.com - Accessible securities investing
- stripe.com - Technical excellence, clarity

**Avoid These Patterns:**
- Excessive animations/parallax
- Crypto meme aesthetics (rocket ships, moon references)
- Vague buzzword-heavy copy
- Dark patterns or pushy CTAs
- Missing contact/company info
