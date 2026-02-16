# Full Site QA Test — All HRBR.LIFE Properties

Run a comprehensive visual and functional QA test of all four live websites using Chrome MCP browser tools. Test each site one by one, taking screenshots and checking for issues.

## Sites to Test

| # | Domain | Type | Repo / Source |
|---|--------|------|---------------|
| 1 | https://sails.to | Hugo static site | hugo-site/ → sailsto_website (website-publish branch) |
| 2 | https://kyc.lat | Vite/React SPA | kyclat_website (publish branch) |
| 3 | https://hrbr.life | Static HTML landing | hrbrlife_website |
| 4 | https://melusina-os.org | Vite/React SPA | INSTAKYCAPP_WEBSITE |

---

## Test Procedure Per Site

For **each** site, perform every step below and record results in a summary table at the end.

### Step 1: Homepage Load
- Navigate to the site root URL
- Take a screenshot
- Verify: page loads, no blank screen, no error messages visible
- Check: title tag is correct (not generic/default/broken)
- Check: CSS/styles are applied (not unstyled HTML)
- Check: no "404", "Not Found", or error text visible

### Step 2: Navigation & Branding
- Take a snapshot (a11y tree) of the page
- Verify: navigation bar/menu is present with links
- Verify: branding is correct for that site (no cross-contamination — e.g. sails.to should NOT say "Melusina" or "KYC.lat")
- List the navigation items found

### Step 3: Subpage Testing
Test at least 3-4 internal pages per site. Navigate to each and take a screenshot.

**sails.to pages to test:**
- https://sails.to/brokers/
- https://sails.to/investors/
- https://sails.to/pricing/
- https://sails.to/company/about/
- https://sails.to/whatsails/

**kyc.lat pages to test:**
- https://kyc.lat/en/use-cases
- https://kyc.lat/en/plans
- https://kyc.lat/en/company
- https://kyc.lat/en/compare
- https://kyc.lat/en/blog

**hrbr.life pages to test:**
- (single-page site — scroll down to verify all sections load)
- Check that the portfolio section, team section, and footer are all present

**melusina-os.org pages to test:**
- https://melusina-os.org/en/use-cases
- https://melusina-os.org/en/plans
- https://melusina-os.org/en/company

### Step 4: Footer Check
- Scroll to the bottom of the homepage
- Take a screenshot of the footer
- Verify: footer is present and contains relevant links/copyright
- Check: no broken layout or missing elements

### Step 5: Mobile Responsiveness
- Resize viewport to mobile (375×812 — iPhone dimensions)
- Take a screenshot of the homepage
- Verify: content is readable, nav collapses to hamburger menu (if applicable), no horizontal overflow
- Reset viewport back to desktop after test

### Step 6: Console Errors
- List console messages (errors/warnings only)
- Report any JavaScript errors, 404s for assets, or CORS issues

### Step 7: HTTPS Check
- Confirm the site is served over HTTPS (no mixed content warnings)
- Check that HTTP redirects to HTTPS

---

## Cross-Contamination Checks

These are critical — verify NO branding leaks between sites:

| Site | Must NOT contain | Must contain |
|------|-----------------|--------------|
| sails.to | "Melusina", "KYC.lat", "InstaKYC", "HRBR" | "Sails.to" or "Sails" |
| kyc.lat | "Melusina", "Sails", "HRBR", "InstaKYC" (in visible UI) | "KYC.lat" or "kyc.lat" |
| hrbr.life | "Melusina", "KYC", "Sails" (as primary brand) | "HRBR" or "Harbour" |
| melusina-os.org | "InstaKYC", "Sails", "HRBR" | "Melusina" |

---

## Output Format

After testing all sites, produce a **summary report** in this format:

```
## QA Test Results — [DATE]

### 1. sails.to
- Homepage: ✅/❌ (notes)
- Branding: ✅/❌ (notes)
- Subpages: ✅/❌ (list any 404s or broken pages)
- Footer: ✅/❌
- Mobile: ✅/❌
- Console Errors: ✅ clean / ❌ (list errors)
- HTTPS: ✅/❌
- Cross-contamination: ✅/❌

### 2. kyc.lat
(same format)

### 3. hrbr.life
(same format)

### 4. melusina-os.org
(same format)

### Critical Issues Found
- (list any blocking issues)

### Minor Issues Found
- (list cosmetic or non-blocking issues)

### Overall Status: ✅ ALL CLEAR / ⚠️ ISSUES FOUND
```

---

## Important Notes
- Do NOT fix anything during this test — only observe and report
- Take screenshots liberally — they serve as evidence
- If a page hangs or takes >10s to load, note it as a performance issue
- Test with cache bypass where possible (use ignoreCache on reload)
- For SPAs (kyc.lat, melusina-os.org), the HTTP status code may be 404 on subpages but the page should still render correctly via client-side routing
