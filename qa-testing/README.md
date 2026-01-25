# Sails.to QA Testing Suite

Automated UX testing with Playwright screenshot capture and AI-powered review.

## Features

- 🖥️ **Multi-viewport testing**: Desktop (1920x1080), Tablet (768x1024), Mobile (375x812)
- 📸 **Automatic screenshots**: Captures at top, 25%, 50%, 75%, and bottom of each page
- 🤖 **AI-powered review**: Analyzes screenshots for UX issues using vision models
- 🔄 **Site comparison**: Compare pre-Hugo (drafts) vs Hugo-built site page-by-page
- 📊 **Local analysis**: Falls back to image analysis when no API key is provided
- 📝 **HTML reports**: Beautiful, interactive reports with all findings
- ⚡ **Performance metrics**: Load times, First Paint, FCP for each page

## Quick Start

```bash
# Install dependencies
npm install

# Install Playwright browsers
npm run install:browsers

# Make sure Hugo dev server is running
cd ../hugo-site && hugo server -D &

# Run full audit
npm run full-audit

# Or run steps individually:
npm run test      # Crawl and capture screenshots
npm run collages  # Generate collage images
npm run review    # Analyze with AI agent
npm run report    # Generate HTML report

# Compare original vs Hugo site (NEW!)
npm run compare   # Side-by-side comparison with AI analysis
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run test` | Crawl site and capture screenshots (all viewports) |
| `npm run test:desktop` | Capture desktop viewport only |
| `npm run test:mobile` | Capture mobile viewport only |
| `npm run collages` | Generate collage images for AI review |
| `npm run review` | Run AI agent review on screenshots |
| `npm run report` | Generate HTML report |
| `npm run full-audit` | Run complete test + collages + review + report |
| `npm run compare` | **NEW**: Compare original vs Hugo site (standard model) |
| `npm run compare:free` | Compare using free tier model (gemma-3-27b) |
| `npm run compare:standard` | Compare using standard model (gemini-2.0-flash) |
| `npm run compare:premium` | Compare using premium model (claude-3.5-sonnet) |

## Site Comparison Tool (NEW!)

The comparison tool captures both the original (drafts) site and the Hugo-built site, creates side-by-side screenshots, and uses AI vision models to identify:

- **Content differences**: Missing text, changed wording, missing sections
- **Visual differences**: Font, color, spacing, styling changes  
- **Layout differences**: Grid changes, alignment, ordering
- **Missing elements**: Icons, images, navigation items
- **Broken elements**: Raw HTML showing as text, broken images

### Model Tiers

| Tier | Model | Best For |
|------|-------|----------|
| `free` | google/gemma-3-27b-it:free | Quick checks, budget conscious |
| `standard` | google/gemini-2.0-flash-exp:free | Good balance of quality/cost |
| `premium` | anthropic/claude-3.5-sonnet | Detailed analysis, critical reviews |

### Running Comparison

```bash
# Default (standard tier)
npm run compare

# Use free model
npm run compare:free

# Use premium model (requires API credits)
MODEL_TIER=premium npm run compare
```

### Output

- `screenshots/comparison/original/` - Screenshots of original site
- `screenshots/comparison/hugo/` - Screenshots of Hugo site
- `screenshots/comparison/side-by-side/` - Side-by-side comparisons
- `screenshots/reports/comparison-results.json` - Raw analysis data
- `screenshots/reports/comparison-report.html` - Visual HTML report

## Configuration

### Environment Variables

```bash
# OpenRouter API key for AI analysis
export OPENROUTER_API_KEY=your-api-key

# Model tier selection (free, standard, premium)
export MODEL_TIER=standard

# Optional: Custom base URL (default: http://localhost:1313)
export BASE_URL=http://localhost:1313
```

### Customizing Pages

Edit `crawler.js` to modify the pages list:

```javascript
const CONFIG = {
  pages: [
    { path: '/', name: 'home' },
    { path: '/issuers/', name: 'issuers' },
    // Add more pages...
  ]
};
```

### Customizing Viewports

```javascript
const CONFIG = {
  viewports: {
    desktop: { width: 1920, height: 1080, name: 'desktop' },
    tablet: { width: 768, height: 1024, name: 'tablet' },
    mobile: { width: 375, height: 812, name: 'mobile' }
  }
};
```

## Output Structure

```
screenshots/
├── desktop/           # Desktop viewport screenshots
│   ├── home_desktop_top.png
│   ├── home_desktop_25pct.png
│   └── ...
├── tablet/            # Tablet viewport screenshots
├── mobile/            # Mobile viewport screenshots
└── reports/
    ├── crawler-results.json      # Raw crawler data
    ├── agent-review-results.json # AI analysis results
    └── qa-report.html            # Interactive HTML report
```

## UX Review Criteria

The AI agent reviews for:

1. **Visual Consistency**
   - Color scheme consistency
   - Typography consistency
   - Spacing and alignment
   - Button styles

2. **Navigation & Structure**
   - Nav visibility and clarity
   - Mobile menu accessibility
   - Footer organization

3. **Readability & Content**
   - Text contrast
   - Font sizes
   - Line lengths
   - Header hierarchy

4. **Responsive Design**
   - Content fits viewport
   - Touch target sizes
   - Image scaling
   - Layout adaptation

5. **Accessibility Indicators**
   - Color contrast
   - Interactive elements
   - Focus states

6. **Call to Action**
   - CTA prominence
   - Button clarity
   - Form structure

## Local Analysis (No API Key)

When no OpenAI API key is provided, the system performs local image analysis:

- Blank page detection
- Dark page detection (CSS issues)
- Color variance analysis
- File size checks
- Aspect ratio verification

## Example Report

The generated HTML report includes:

- Summary cards (pages tested, issues found, average score)
- Critical and high-severity issues list
- Performance metrics table
- Interactive screenshot gallery with viewport tabs
- Console errors and warnings

## Troubleshooting

### Screenshots are blank
- Ensure Hugo dev server is running on port 1313
- Check for JavaScript errors in console output

### AI analysis fails
- Verify OPENAI_API_KEY is set correctly
- Check API quota and billing

### Playwright install issues
```bash
# Try manual browser install
npx playwright install chromium --with-deps
```

## Integration with CI/CD

```yaml
# GitHub Actions example
jobs:
  qa-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - name: Install dependencies
        run: |
          cd qa-testing
          npm install
          npx playwright install chromium --with-deps
      - name: Start Hugo server
        run: |
          cd hugo-site
          hugo server -D &
          sleep 5
      - name: Run QA tests
        run: |
          cd qa-testing
          npm run test
          npm run review
          npm run report
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: qa-report
          path: qa-testing/screenshots/reports/
```

## License

MIT
