# BLOOM KYC UX & Style Guide

## Reference: What GOOD Looks Like

Compare our KYC flow to the attached bond marketplace screenshot - clean cards, clear visual hierarchy, professional styling.

---

## 🚨 CRITICAL UX RULES

### Rule 1: ONE Thing Per Screen
**BAD:** Email input + captcha + OTP on same page with show/hide
**GOOD:** 
- Screen 1: Just email input + "Continue" button
- Screen 2: Just captcha (if needed)
- Screen 3: Just OTP input + "Verify" button

**Why:** Mobile users get overwhelmed. Each step should be obvious.

### Rule 2: NO Native Browser Elements
**BAD:** `<input type="file">` with "Choose File" and "No file chosen"
**GOOD:** Custom styled upload button with:
- Large tap target (min 48x48px)
- Icon + clear label
- Drag & drop zone on desktop
- Camera icon for mobile

**Example HTML:**
```html
<label class="upload-zone">
  <div class="upload-icon">📷</div>
  <span class="upload-text">Tap to take photo or upload</span>
  <input type="file" accept="image/*" capture="environment" class="sr-only">
</label>
```

### Rule 3: Progress Should Be Visual, Not Text
**BAD:** "0%" or "50% complete" as plain text
**GOOD:** 
- Stepper component showing current step
- Visual progress bar (filled portion)
- Step icons that change state

**Example:**
```
[✓ Terms] → [✓ Contact] → [● Document] → [○ Face] → [○ Review]
```

### Rule 4: Buttons Must Be Obvious
**BAD:** No visible button after file selection
**GOOD:**
- Primary action button always visible at bottom
- Button text describes action: "Upload Document", "Take Selfie", "Submit"
- Button disabled until valid input provided
- Loading state when processing

### Rule 5: Mobile-First Input Types
**REQUIRED:**
- Email: `type="email"` (brings up @ keyboard)
- Phone: `type="tel"` (numeric pad)
- OTP: `inputmode="numeric" pattern="[0-9]*"` 
- Camera: `capture="user"` (selfie) or `capture="environment"` (document)

### Rule 6: No Random Text/States Visible
**BAD:** "0%" showing before any progress
**BAD:** Empty preview areas
**BAD:** Hidden divs that flash on load
**GOOD:** Only show elements when they have meaningful content

---

## 📐 Visual Design Standards

### Colors (TailwindCSS)
```
Primary Button: bg-blue-600 hover:bg-blue-700 text-white
Secondary Button: bg-gray-100 hover:bg-gray-200 text-gray-800
Success: bg-green-50 border-green-500 text-green-700
Error: bg-red-50 border-red-500 text-red-700
Warning: bg-yellow-50 border-yellow-500 text-yellow-700
Card: bg-white rounded-xl shadow-sm border border-gray-100
```

### Typography
```
Page Title: text-2xl font-bold text-gray-900
Section Title: text-lg font-semibold text-gray-800
Body Text: text-base text-gray-600
Help Text: text-sm text-gray-500
Label: text-sm font-medium text-gray-700
```

### Spacing
```
Card Padding: p-6 (24px)
Section Gap: space-y-6 (24px)
Form Field Gap: space-y-4 (16px)
Inline Gap: gap-3 (12px)
```

### Touch Targets (Mobile)
```
Minimum button height: 48px (h-12)
Minimum tap area: 44x44px
Input height: 48-56px
```

---

## 📱 Mobile-Specific Requirements

### 1. Viewport
- Must work at 375px width (iPhone SE)
- No horizontal scrolling ever
- Full-width buttons on mobile

### 2. File Upload on Mobile
```html
<!-- Document (back camera) -->
<input type="file" accept="image/*" capture="environment">

<!-- Selfie (front camera) -->  
<input type="file" accept="image/*" capture="user">
```

### 3. Keyboard Handling
- Form should not be obscured by keyboard
- "Next" button above keyboard or scrollable
- Auto-focus first input on step load

### 4. Touch Feedback
- Buttons must have hover/active states
- Tap feedback visible (scale or color change)

---

## ✅ Step-by-Step Checklist

### For EVERY Step Screen:
- [ ] Clear title explaining what to do
- [ ] Only 1-2 inputs maximum  
- [ ] Primary action button visible without scrolling
- [ ] Button text is action-specific (not "Submit" or "OK")
- [ ] Progress indicator shows current position
- [ ] No unused/empty UI elements visible
- [ ] Works at 375px width
- [ ] Touch targets >= 44px

### For File Upload Steps:
- [ ] Custom styled upload (no native file input visible)
- [ ] Clear instructions on what to photograph
- [ ] Preview shows after selection
- [ ] "Retake" option available
- [ ] Continue button appears after valid upload
- [ ] Mobile has `capture` attribute

### For OTP/Code Entry:
- [ ] Large, centered input
- [ ] Numeric keyboard on mobile (`inputmode="numeric"`)
- [ ] Auto-submit when complete (optional)
- [ ] Clear "Resend" option with timer
- [ ] Shows where code was sent

### For Review/Confirm Steps:
- [ ] Extracted data displayed clearly
- [ ] Each field is editable
- [ ] Photo previews visible
- [ ] Final "Confirm & Submit" button
- [ ] Clear what happens next

---

## 🔴 Automatic Failures (Score = 0)

The following issues should result in BLOCKING scores:

1. **Native file input visible** - "Choose File | No file chosen"
2. **No continue/submit button** visible after completing input
3. **More than 3 inputs** on single mobile screen
4. **Random percentages** showing (0%, 50%) without context
5. **Horizontal scrolling** required on mobile
6. **Touch targets < 44px**
7. **Missing form labels**
8. **No error messages** when validation fails

---

## 📊 Scoring Guide

### Usability Score (1-10)
- **10**: Perfect single-step, clear action, beautiful UI
- **8-9**: Good focus, minor polish issues
- **6-7**: Functional but cluttered or unclear
- **4-5**: Multiple issues, confusing flow
- **1-3**: Broken, inaccessible, or unusable

### Mobile Score (1-10)
- **10**: Native-app quality on mobile
- **8-9**: Works well, minor touch issues
- **6-7**: Usable but not optimized
- **4-5**: Difficult to use on mobile
- **1-3**: Broken on mobile

### Step Focus Score (1-10)
- **10**: Single focused action
- **8-9**: 1-2 related inputs
- **6-7**: 3 inputs or minor bundling
- **4-5**: 4+ inputs bundled
- **1-3**: Kitchen sink approach

---

## Example: Good vs Bad

### BAD: Current Face Upload
```
Face Verification
Please upload or capture a clear photo...
Upload Face Photo *
  📷 Upload Face Photo [Choose File] No file chosen
Accepted formats: PNG, JPEG (max 20MB)
0%
• Face the camera directly
• Ensure good lighting
...
```

**Problems:**
- Native file input showing
- "0%" random text
- No submit button
- Bullet points take up space

### GOOD: Ideal Face Upload
```
┌─────────────────────────────────┐
│         Take a Selfie           │
│                                 │
│  ┌─────────────────────────┐   │
│  │                         │   │
│  │    [Camera Preview]     │   │
│  │         📷              │   │
│  │   Tap to take photo     │   │
│  │                         │   │
│  └─────────────────────────┘   │
│                                 │
│  Tips: Good lighting, face     │
│  camera directly, neutral      │
│  expression                    │
│                                 │
│  ┌─────────────────────────┐   │
│  │    📸 Take Photo        │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

**Better because:**
- Clear title (action-focused)
- Large visual tap zone
- Tips condensed to one line
- Clear primary button
- No random text/percentages

---

## Implementation Priority

1. **P0 - BLOCKING:** Fix native file inputs, add continue buttons
2. **P1 - HIGH:** Split bundled steps into single-focus screens  
3. **P2 - MEDIUM:** Improve visual styling, add stepper
4. **P3 - LOW:** Polish animations, micro-interactions
