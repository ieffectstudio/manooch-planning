

# 📄 Product Requirements Document (PRD)
## Dastboard (دستبورد) — WASM-Powered Browser Utility Hub

---

## Document Metadata

| Field | Value |
|---|---|
| **Product Name** | Dastboard (دستبورد) |
| **Tagline (EN)** | "Your files. Your browser. Your rules." |
| **Tagline (FA)** | "فایل‌های شما. مرورگر شما. قوانین شما." |
| **Document Version** | 1.0 — MVP |
| **Author** | Product & UX Architecture Team |
| **Status** | Final — Ready for Development |
| **Scope** | Complete UI/UX specification, monetization model, content strategy, trust architecture, internationalization, and growth plan. No code, no stack decisions. |

---

## Table of Contents

1. Executive Summary
2. Vision & Why "Dastboard"
3. Target Users & Personas
4. The 5 MVP Tools
5. Complete Page Architecture
6. Component-by-Component Specification
7. The Three Interaction States
8. Theme System Specification
9. Internationalization (i18n) & RTL Architecture
10. Monetization & Ad Placement Strategy
11. SEO & Content Architecture
12. Trust, Privacy & Psychology Framework
13. Accessibility Requirements
14. Performance & Core Web Vitals Targets
15. Analytics & Success Metrics
16. Growth Roadmap (Post-MVP)
17. Risk Matrix & Blindspot Analysis
18. Appendix: Content Strings (EN/FA)

---

## 1. Executive Summary

### What is Dastboard?

Dastboard is a **free, privacy-first, browser-based utility hub** that processes files and data entirely on the user's device using WebAssembly (WASM). Unlike competitors such as TinyPNG, FreeConvert, or iLovePDF — which upload user files to remote servers — Dastboard ensures that **no file ever leaves the browser tab**.

### The Core Promise

> "Every tool runs locally. No uploads. No servers. No trust required."

### The Business Model

Dastboard is a **freemium utility SaaS** monetized through three revenue streams:

1. **Google Ads** displayed alongside the free tools
2. **Custom internal banners** that bypass ad-blockers and promote the Pro plan
3. **Dastboard Pro** — a $5/month subscription removing ads, unlocking batch processing, higher file limits, and API access

### The MVP Scope

The MVP launches with exactly **5 tools**, a single transactional page layout, full dark/light theming, and complete bilingual support in **English (LTR)** and **Persian/Farsi (RTL)**.

---

## 2. Vision & Why "Dastboard"

### The Name

**Dastboard (دستبورد)** is a deliberate fusion:

- **"Dast" (دست)** means "hand" in Persian — representing the user's direct control over their files
- **"Board"** evokes a dashboard, a control panel, a workspace
- Together it means: **"Your hands on the controls"** — reinforcing the privacy-first, local-processing philosophy

The name works in both English and Persian markets. It's memorable, brandable, has available domain potential, and phonetically communicates "dashboard" to English speakers while carrying deeper meaning for Persian speakers.

### The Vision Statement

Dastboard will become the **default utility destination** for anyone who needs to quickly compress, convert, format, encode, or hash a file — and who cares (or should care) about where their data goes.

### The Strategic Moat

| Competitor | Weakness Dastboard Exploits |
|---|---|
| TinyPNG | Uploads files to remote servers. 20 free images/month limit. No developer tools. |
| FreeConvert | Heavy ads, deceptive download buttons, server-side processing, slow upload/download cycle. |
| Squoosh (Google) | Single-image only. No batch. No developer tools. No monetization model to sustain. |
| iLovePDF | Server-side. 2-file free limit. Aggressive upselling. European privacy concerns. |

Dastboard's moat is the combination of **local processing + multi-tool hub + bilingual RTL support + ethical monetization**. No competitor offers all four.

---

## 3. Target Users & Personas

### Persona 1: The Quick-Task Professional

| Attribute | Detail |
|---|---|
| **Name** | Sarah / سارا |
| **Role** | Marketing Manager, Content Creator |
| **Age** | 25–40 |
| **Behavior** | Searches "compress image online" or "convert to PDF free" 3–5 times per week |
| **Pain** | Hates creating accounts, waiting for uploads, or worrying about file privacy |
| **Goal** | Drop file → get result → leave. Under 30 seconds. |
| **Value to Dastboard** | High volume, low engagement. Monetized via ads on each transactional page view. |

### Persona 2: The Privacy-Conscious Developer

| Attribute | Detail |
|---|---|
| **Name** | Armin / آرمین |
| **Role** | Backend/Full-Stack Developer |
| **Age** | 22–35 |
| **Behavior** | Searches "JSON formatter online" or "SHA-256 hash generator" |
| **Pain** | Paranoid about pasting API keys or JWT tokens into online tools that transmit to servers |
| **Goal** | A tool that explicitly guarantees local processing. No network requests. |
| **Value to Dastboard** | Uses ad-blocker (40% likelihood). Target for Pro upsell or custom banner fallback. Shares with dev communities. |

### Persona 3: The Persian-Speaking User

| Attribute | Detail |
|---|---|
| **Name** | مهسا (Mahsa) |
| **Role** | University Student / Freelance Designer |
| **Age** | 18–30 |
| **Behavior** | Searches in Persian: "فشرده‌سازی عکس آنلاین" (compress image online) |
| **Pain** | Most tools are English-only. RTL layouts are broken or non-existent. |
| **Goal** | A beautiful, fully Persian tool that feels native, not translated. |
| **Value to Dastboard** | Opens a massive underserved market (80M+ Persian speakers). Low competition in Persian SEO. |

---

## 4. The 5 MVP Tools

Each tool is a self-contained utility accessible from the **Tool Tab Switcher** on the homepage. In the MVP, all 5 share the same **page layout** — only the tool header, settings panel, and processing logic change.

### Tool 1: Compress Image (فشرده‌سازی تصویر)

| Property | Detail |
|---|---|
| **Input** | PNG, JPG, JPEG, WebP, AVIF, GIF, SVG |
| **Output** | Same format (compressed) or user-selected format |
| **Controls** | Output format selector, quality slider (10–100%), resize options, EXIF strip toggle, transparency preservation toggle |
| **Key Metric** | Percentage of file size reduced (displayed prominently) |
| **SEO Target Keywords** | "compress image online free", "reduce image size", "فشرده‌سازی عکس آنلاین" |

### Tool 2: Convert Image (تبدیل تصویر)

| Property | Detail |
|---|---|
| **Input** | PNG, JPG, WebP, AVIF, GIF, SVG, BMP, TIFF |
| **Output** | User-selected target format |
| **Controls** | Source format auto-detected, target format dropdown, quality slider |
| **Key Metric** | Conversion time + output file size |
| **SEO Target Keywords** | "convert PNG to JPG", "WebP to PNG online", "تبدیل عکس به JPG" |

### Tool 3: JSON Formatter (فرمت‌کننده JSON)

| Property | Detail |
|---|---|
| **Input** | Raw JSON text (pasted or uploaded) |
| **Output** | Beautified/minified/validated JSON |
| **Controls** | Beautify button, minify button, indent size (2/4/tab), copy to clipboard |
| **Key Metric** | Validation pass/fail + line count |
| **SEO Target Keywords** | "JSON formatter online", "JSON beautifier", "فرمت JSON آنلاین" |

### Tool 4: Base64 Encode/Decode (رمزگذاری Base64)

| Property | Detail |
|---|---|
| **Input** | Plain text or file upload |
| **Output** | Base64 encoded string, or decoded text/file |
| **Controls** | Encode/decode toggle, text area input, file upload option, copy result |
| **Key Metric** | Input size → output size |
| **SEO Target Keywords** | "base64 encode online", "base64 to image", "رمزگذاری Base64" |

### Tool 5: Hash Generator (مولد هش)

| Property | Detail |
|---|---|
| **Input** | Plain text or file upload |
| **Output** | Hash string in selected algorithm |
| **Controls** | Algorithm selector (MD5, SHA-1, SHA-256, SHA-512), text input, file input, copy hash |
| **Key Metric** | Hash generated in X milliseconds |
| **SEO Target Keywords** | "SHA-256 hash generator", "MD5 online", "مولد هش SHA-256" |

---

## 5. Complete Page Architecture

The Dastboard MVP is a **single-page layout** optimized for transactional conversion. Every element exists in a strict vertical hierarchy designed to minimize time-to-action.

### The Vertical Flow (Top to Bottom)

```
┌──────────────────────────────────────────────────┐
│ 1. STICKY HEADER                                 │
│    Logo | Search Bar | Lang | Theme | Login | Pro │
├──────────────────────────────────────────────────┤
│ 2. BREADCRUMB BAR                                │
│    Home / Compress Image                          │
├──────────────────────────────────────────────────┤
│ 3. AD SLOT — TOP LEADERBOARD (728×90)            │
│    Fixed 90px height (prevents CLS)              │
├──────────────────────────────────────────────────┤
│ 4. TOOL TAB SWITCHER (5 tabs in a row)           │
│    [Compress ✓] [Convert] [JSON] [Base64] [Hash] │
├──────────────────────────────────────────────────┤
│ 5. HERO SECTION — Two columns:                   │
│    ┌────────────────────┬──────────────────┐      │
│    │ TOOL PANEL         │ SIDEBAR          │      │
│    │ • Badge            │ • Settings Panel │      │
│    │ • H1 Title         │ • Ad Slot 300×250│      │
│    │ • Subtitle         │ • Pro Upsell Card│      │
│    │ • Format Tags      │                  │      │
│    │ • DROPZONE         │                  │      │
│    │   (or Processing)  │                  │      │
│    │   (or Download)    │                  │      │
│    └────────────────────┴──────────────────┘      │
├──────────────────────────────────────────────────┤
│ 6. HOW-TO SECTION (3 steps)                      │
├──────────────────────────────────────────────────┤
│ 7. FAQ SECTION (5 accordion items)               │
├──────────────────────────────────────────────────┤
│ 8. FOOTER                                        │
└──────────────────────────────────────────────────┘
```

---

## 6. Component-by-Component Specification

### 6.1 — Sticky Header

**Purpose:** Brand identity, global navigation, and quick access to settings.

| Element | Specification |
|---|---|
| **Logo** | "Dastboard" with icon (sparkle symbol). "Board" portion in brand purple. Logo icon is a 34×34px rounded square with gradient fill. |
| **Search Bar** | Centered, flexible width (max 480px). Placeholder text: "Search tools..." / "جستجوی ابزارها...". Shows ⌘K keyboard shortcut badge. Opens a CMD+K modal (future enhancement). |
| **Language Toggle** | Globe icon + text label showing "FA" (when in English, offering Persian) or "EN" (when in Persian, offering English). Single click switches language AND direction (LTR↔RTL). |
| **Theme Toggle** | Sun icon (in light mode) / Moon icon (in dark mode). Icons transition with rotation + scale animation (90° rotation, 0.5 scale out, 1.0 scale in). |
| **Log In Button** | Text-only button, secondary styling. Color: text-secondary. Hover: subtle background fill. |
| **Upgrade to Pro Button** | Primary CTA. Purple gradient background. Sparkle icon. Always visible. This is the primary monetization trigger in the header. |
| **Mobile Hamburger** | Visible only below 768px. Replaces search bar and log in button. |
| **Behavior** | Sticky to top of viewport. Background uses backdrop-filter blur (20px) with semi-transparent fill for the glassmorphism effect. 1px bottom border in border-subtle color. |

### 6.2 — Breadcrumb Bar

**Purpose:** SEO structure + user orientation.

| Element | Specification |
|---|---|
| **Structure** | Home → [Tool Name] (2 levels for MVP) |
| **Separator** | Forward slash "/". In RTL mode, the slash is visually flipped using CSS transform. |
| **Current Page** | Non-linked, brighter text color (text-secondary vs text-tertiary for links). |
| **SEO Value** | Provides structured hierarchy for search engines. Each breadcrumb link is a crawlable anchor. |

### 6.3 — Ad Slot: Top Leaderboard

**Purpose:** Primary above-the-fold ad revenue position.

| Property | Specification |
|---|---|
| **Format** | IAB Standard Leaderboard — 728×90 pixels |
| **Container Height** | FIXED at exactly 90px. Uses min-height AND max-height to prevent Cumulative Layout Shift (CLS). |
| **Background** | Slightly darker than page background (ad-bg variable). Dashed border to clearly distinguish from content. |
| **Label** | Tiny "ADVERTISEMENT" / "تبلیغات" text in top-left (top-right in RTL). 9px uppercase, muted color. |
| **AdBlock Fallback** | If ad fails to load (ad-blocker detected), the container displays a custom internal banner: "Hate Ads? Get Dastboard Pro for $5/m" with a CTA button. This ensures the space is never wasted. |
| **Mobile Behavior** | HIDDEN entirely on screens ≤768px. On mobile, the dropzone must be the first interactive element the user sees. No ad should push the primary CTA below the fold. |

### 6.4 — Tool Tab Switcher

**Purpose:** Allow users to navigate between all 5 MVP tools without leaving the page.

| Property | Specification |
|---|---|
| **Layout** | 5 equal-width cards in a single horizontal row (grid: repeat(5, 1fr)) |
| **Card Contents** | Each card shows: emoji icon (40×40), tool name (bold), one-line description (muted) |
| **Active State** | Purple border, subtle purple background gradient, pulsing dot indicator in top-right corner (top-left in RTL), purple accent line across top edge |
| **Hover State** | Card lifts 2px (translateY), shadow increases, purple top-line reveals via scaleX animation |
| **Badge Support** | Optional "New" / "جدید" badge on individual tools (amber colored) |
| **Section Header** | Left-aligned (right in RTL): pulsing purple dot + "Available Tools" / "ابزارهای موجود" label. Right side: hint text "Click any tool to switch instantly" / "روی هر ابزار کلیک کنید تا فوراً تغییر کند" |
| **Click Behavior** | Marks clicked tab as active (removes active from all others). Smooth-scrolls viewport to the hero tool panel below. In MVP, this can simply swap the active visual state. In production, it would load the corresponding tool's interface. |
| **Responsive** | 5 cols → 3 cols (≤1024px) → 2 cols (≤768px) → 1 col (≤480px) |

### 6.5 — Hero Section: Tool Panel (Left/Main Column)

This is the most critical component on the page. It contains the tool's interface and cycles through three interaction states.

#### 6.5.1 — Tool Header Area

| Element | Specification |
|---|---|
| **Privacy Badge** | Pill-shaped badge at top. Green border, green text, shield icon. Text: "100% Private — Runs Locally" / "۱۰۰٪ خصوصی — اجرا در مرورگر". Always visible regardless of state. |
| **H1 Title** | Large (32px desktop / 24px mobile), extra-bold (800 weight). Contains the tool name with the key word highlighted in gradient purple. Example: "Compress **Images** Instantly" / "فشرده‌سازی **تصاویر** در یک لحظه" |
| **Subtitle** | 15px secondary text explaining the tool's value proposition. Includes bold highlights for key phrases like "90%" and "entirely in your browser". Persian version has larger line-height (1.9) for readability. |
| **Supported Formats Strip** | Horizontal row of small tags (11px uppercase) showing file format support: PNG, JPG, JPEG, WebP, AVIF, GIF, SVG. Hidden on mobile (≤480px) to save space. |

#### 6.5.2 — The Dropzone (Upload State)

This is the **default state** when the user first visits.

| Element | Specification |
|---|---|
| **Container** | Large dashed-border rectangle. Rounded corners (16px). Subtle diagonal stripe pattern in the background. Full-width within the tool panel. |
| **Upload Icon** | 72×72px rounded box with purple gradient background. Contains an upload arrow SVG icon. On hover: floats up 4px with purple shadow glow. |
| **Instructional Text** | "Drag & drop your images here, or" / "تصاویر خود را اینجا بکشید و رها کنید، یا" |
| **Primary CTA: "Choose Files"** | THE most important button on the entire page. Must be visually impossible to confuse with any advertisement. Specifications: purple gradient background, 16px bold white text, 14px vertical padding, 36px horizontal padding, rounded corners (10px), brand shadow glow, shimmer animation on hover (a diagonal light sweep across the button), translates up 2px on hover with intensified shadow. Icon: upload arrow to the left (right in RTL) of text. |
| **Secondary Import Options** | Smaller, muted buttons for "Google Drive" and "From URL". Gray background, subtle border, small icons. These are de-emphasized alternatives. |
| **Security Badge** | Pill at the bottom of the dropzone. Shield icon (green) + text: "Max file size 1 GB · Files never leave your device" / "حداکثر حجم فایل ۱ گیگابایت · فایل‌ها هرگز از دستگاه شما خارج نمی‌شوند" |
| **Drag-Over State** | When a file is dragged over the zone: border turns solid purple, background becomes purple-tinted, zone scales up 1%, purple glow shadow appears around the entire zone. This gives immediate visual feedback that the drop target is valid. |

### 6.6 — Hero Section: Sidebar (Right Column)

#### 6.6.1 — Settings Panel

| Element | Specification |
|---|---|
| **Header** | Gear icon + "Compression Settings" / "تنظیمات فشرده‌سازی". Bottom border separator. |
| **Output Format Dropdown** | Select element with options: "Same as input (auto)", PNG, JPEG, WebP, AVIF. Custom dropdown arrow icon. In RTL: arrow moves to left side. |
| **Quality Slider** | Label "Quality" / "کیفیت" with live percentage readout (e.g., "80%") in purple. Range input styled with custom thumb (18px circle, purple fill, white border, purple shadow). |
| **Resize Dropdown** | Options: "No resize", "Max width: 1920px", "Max width: 1280px", "Max width: 800px". |
| **EXIF Toggle** | "Strip EXIF metadata" / "حذف داده‌های EXIF". Toggle switch with checked default. Switch slides left-to-right (right-to-left in RTL). |
| **Transparency Toggle** | "Preserve transparency" / "حفظ شفافیت". Same toggle style, checked default. |
| **Note** | The settings panel adapts per tool. The compress image settings shown here are specific to Tool 1. Each of the 5 tools would have its own relevant settings panel content. |

#### 6.6.2 — Ad Slot: Flank Rectangle

| Property | Specification |
|---|---|
| **Format** | IAB Medium Rectangle — 300×250 pixels |
| **Container** | Fixed height (250px), dashed border, labeled "Advertisement" / "تبلیغات" |
| **Position** | Below settings panel in sidebar |
| **Mobile** | Full-width (100%) below the tool panel |

#### 6.6.3 — Pro Upsell Card

| Element | Specification |
|---|---|
| **Header** | ⚡ emoji + "Dastboard Pro" |
| **Description** | "Remove ads, unlock batch processing, and get priority WASM workers." / Persian equivalent |
| **Feature List** | 4 items with green checkmark icons: "No ads, ever", "Batch upload (100+ files)", "Custom presets & API", "Priority support" |
| **CTA Button** | Full-width purple gradient button: "Start Free Trial →" / "← شروع دوره آزمایشی رایگان" (arrow direction flips in RTL) |
| **Visual Treatment** | Subtle purple gradient background, purple border. Feels premium and distinct from the free tool area. |

---

## 7. The Three Interaction States

The tool panel's interior transitions between three states based on user action. Only one state is visible at a time.

### State 1: Upload (Default)

**Trigger:** Page load, or "Process Another" action.

**Content:** The full dropzone as described in Section 6.5.2.

**Transition to State 2:** User drops a file, selects a file via "Choose Files" button, or imports from Drive/URL.

### State 2: Processing

**Trigger:** File has been received and WASM processing has begun.

**Visual Elements:**

| Element | Specification |
|---|---|
| **Padlock Icon** | 64px circle with green background. Contains a closed padlock SVG. The circle pulses with a green glow animation (0 → 16px radius, fading out, 2s loop). This visualizes "your file is locked inside your browser." |
| **Status Text** | "Processing locally... 🔒" / "در حال پردازش محلی... 🔒" — 18px bold |
| **Subtext** | "Your file never leaves this browser tab." / "فایل شما هرگز از این تب مرورگر خارج نمی‌شود." — 14px muted |
| **Progress Bar** | Thin (6px) horizontal bar. Max width 400px, centered. Background: bg-hover. Fill: purple gradient, animated pulse (opacity 1 → 0.7, 2s loop). |
| **Percentage** | "68% — Compressing..." / "۶۸٪ — در حال فشرده‌سازی..." — 13px muted |

**Psychology:** The padlock animation is NOT decorative. It's a **trust signal**. Users are accustomed to "processing" spinners on sites that are actually uploading their files. The padlock + "locally" text + green pulsing glow work together to communicate: "This is different. Your file is safe."

**Transition to State 3:** Processing completes (WASM returns result).

### State 3: Download Complete

**Trigger:** WASM processing finished, result file is ready in browser memory.

**Visual Elements:**

| Element | Specification |
|---|---|
| **Success Icon** | 72px circle, green background, green border. Large checkmark SVG. |
| **Title** | "Compression Complete! 🎉" / "فشرده‌سازی کامل شد! 🎉" — 22px bold |
| **Stats** | "Reduced by **73%** — from 4.2 MB to 1.1 MB" / "کاهش **۷۳٪** — از ۴.۲ مگابایت به ۱.۱ مگابایت". Percentage highlighted in green. |
| **Result Card** | Horizontal card showing: file type thumbnail icon (purple), file name (truncated with ellipsis), metadata (format, dimensions, size before → after), savings percentage in green. |
| **Download Button** | Inside the result card, right-aligned (left in RTL). Same visual treatment as the primary "Choose Files" button — purple gradient, bold text, download icon. This visual consistency trains users: "purple gradient = safe platform button." |

**Psychology:** The download state is the **highest-value moment** for keeping users in the ecosystem. After downloading, the user's task is done and they will close the tab. This is where we intervene.

**Post-Download Actions (Future Enhancement):**
- Replace sidebar ads with "Related Tools" cards (e.g., "Done compressing? Now Convert to WebP" or "Add a Watermark")
- Show a "Process another file" link to return to State 1
- Display a subtle "⭐ Bookmark Dastboard" prompt

---

## 8. Theme System Specification

Dastboard supports two complete visual themes. The user's preference is persisted across sessions.

### 8.1 — Dark Theme (Default)

| Token | Value | Usage |
|---|---|---|
| bg-primary | #09090B | Page background |
| bg-secondary | #111113 | Card/panel backgrounds |
| bg-tertiary | #18181B | Input fields, tag backgrounds |
| bg-elevated | #1E1E22 | Elevated surfaces (dropdowns, modals) |
| bg-hover | #27272A | Hover states |
| border-subtle | #27272A | Default borders |
| border-default | #3F3F46 | Stronger borders (inputs, active elements) |
| text-primary | #FAFAFA | Headings, primary content |
| text-secondary | #A1A1AA | Body text, descriptions |
| text-tertiary | #71717A | Placeholder text, labels |
| text-muted | #52525B | Disabled text, hints |
| brand-primary | #7C3AED | Buttons, active states, accents |
| brand-text | #A78BFA | Linked text, highlighted labels |
| success | #10B981 | Positive states (privacy badge, savings) |
| header-blur-bg | rgba(9, 9, 11, 0.88) | Frosted glass header |

### 8.2 — Light Theme

| Token | Value | Usage |
|---|---|---|
| bg-primary | #FFFFFF | Page background |
| bg-secondary | #FAFAFA | Card/panel backgrounds |
| bg-tertiary | #F4F4F5 | Input fields, tag backgrounds |
| bg-elevated | #FFFFFF | Elevated surfaces |
| bg-hover | #E4E4E7 | Hover states |
| border-subtle | #E4E4E7 | Default borders |
| border-default | #D4D4D8 | Stronger borders |
| text-primary | #09090B | Headings, primary content |
| text-secondary | #3F3F46 | Body text |
| text-tertiary | #52525B | Placeholder text |
| text-muted | #71717A | Disabled text |
| brand-primary | #7C3AED | Same purple (works on both) |
| brand-text | #6D28D9 | Darker purple for readability on white |
| success | #059669 | Slightly deeper green for white bg contrast |
| header-blur-bg | rgba(255, 255, 255, 0.85) | Frosted glass header |

### 8.3 — Theme Toggle Behavior

| Rule | Detail |
|---|---|
| **Default** | Dark theme on first visit |
| **Persistence** | Choice saved to localStorage under key `dastboard-theme` |
| **Transition** | All theme-affected elements transition colors over 300ms ease |
| **Toggle Icon** | Moon icon (dark mode active) → Sun icon (light mode active). Icons animate with rotation (90°) and scale (0.5 → 1.0). Both icons are always in the DOM; opacity and transform toggled via CSS attribute selector. |
| **Ad Containers** | Theme colors for ad placeholder backgrounds also change. Actual Google Ad iframes are unaffected (they render their own styles). |

---

## 9. Internationalization (i18n) & RTL Architecture

### 9.1 — Supported Languages (MVP)

| Language | Code | Direction | Font Family |
|---|---|---|---|
| English | `en` | LTR (Left-to-Right) | Inter |
| Persian (Farsi) | `fa` | RTL (Right-to-Left) | Vazirmatn |

### 9.2 — Language Toggle Behavior

| Rule | Detail |
|---|---|
| **Default** | English (LTR) on first visit |
| **Persistence** | Choice saved to localStorage under key `dastboard-lang` |
| **Toggle Button** | Globe icon + label. When in English, label shows "FA" (offering switch to Persian). When in Persian, label shows "EN". |
| **Instant Switch** | Clicking toggles the `lang` attribute on `<html>` element AND the `dir` attribute (ltr↔rtl). All visible text swaps immediately. No page reload. |

### 9.3 — Content Translation Architecture

Every user-facing string exists in **both languages** within the same HTML document, using data attributes:

```
[data-lang-en] — English content
[data-lang-fa] — Persian content
```

CSS rules show/hide the appropriate content based on the `<html lang="">` attribute. This means:
- No JavaScript string replacement needed
- No external translation files to load
- SEO bots see both languages in the source
- Switching is instant (CSS only, no DOM manipulation for content)

### 9.4 — RTL-Specific UI Adaptations

| Element | LTR Behavior | RTL Adaptation |
|---|---|---|
| Logo position | Left-aligned | Right-aligned (auto via flexbox) |
| Search bar shortcut | Shows on right side | Shows on left side (margin-inline-start) |
| Breadcrumb separator "/" | Left-to-right reading | Visually flipped via CSS transform: scaleX(-1) |
| Tool tab active dot | Top-right corner | Top-left corner (inset-inline-end) |
| Tool tab purple line | Scales from left | Scales from right (transform-origin: right) |
| Dropdown arrow | Right side of select | Left side of select |
| Toggle switch slide | Slides right when checked | Slides left when checked (translateX reversed) |
| CTA arrows ("→") | Points right | Points left ("←") |
| How-to step connectors | Left-to-right gradient line | Right-to-left gradient line |
| Ad slot labels | Top-left | Top-right (inset-inline-start) |
| Demo controls panel | Bottom-right | Bottom-left (inset-inline-end) |

### 9.5 — Persian Typography Rules

| Rule | Value |
|---|---|
| **Font** | Vazirmatn (Google Fonts) — weights: 400, 500, 600, 700, 800, 900 |
| **Fallback** | Inter → system fonts |
| **Base line-height** | 1.6 (English) → 1.9 (Persian body) → 2.0 (Persian FAQ answers) |
| **Letter-spacing** | -0.5px (English headings) → 0 (Persian headings — Persian characters don't benefit from negative tracking) |
| **Number format** | English: "73%", "4.2 MB". Persian: "۷۳٪", "۴.۲ مگابایت" (using Eastern Arabic numerals ۰۱۲۳۴۵۶۷۸۹) |

---

## 10. Monetization & Ad Placement Strategy

### 10.1 — Revenue Streams

| Stream | Description | Target |
|---|---|---|
| **Google Ads** | Display ads in designated slots | All free users without ad-blockers |
| **Custom Banners** | Internal promotional banners | Users WITH ad-blockers (fallback) |
| **Dastboard Pro** | $5/month subscription | Power users, developers, batch processors |

### 10.2 — Ad Slot Inventory (Per Page View)

| Slot | Format | Location | Desktop | Mobile |
|---|---|---|---|---|
| **Slot 1: Top Leaderboard** | 728×90 | Below breadcrumb, above tool tabs | ✅ Visible | ❌ Hidden |
| **Slot 2: Flank Rectangle** | 300×250 | Sidebar, below settings panel | ✅ Visible | ✅ Visible (inline, below tool panel) |

**Total ads per page view:** Maximum 2 (desktop) or 1 (mobile).

This is intentionally restrained. Excessive ads destroy the trust that is Dastboard's core differentiator.

### 10.3 — CLS Prevention Protocol

**The Rule:** Every ad container must have a hard-coded height that does not change when the ad loads.

| Slot | Fixed Height | Implementation |
|---|---|---|
| Leaderboard | 90px | min-height: 90px; max-height: 90px |
| Rectangle | 250px | min-height: 250px; max-height: 250px |

If the ad is 90px tall, the container is ALWAYS 90px tall — even before the ad renders, even if the ad fails to load. This prevents **Cumulative Layout Shift**, which Google Search uses as a ranking signal.

### 10.4 — AdBlocker Fallback Strategy

When an ad-blocker prevents a Google Ad from rendering:

1. The ad container detects the void (no content loaded)
2. It displays a **Custom Internal Banner** instead:
   - Message: "😤 Hate Ads? Get Dastboard Pro for $5/mo — ad-free, unlimited files, batch processing."
   - CTA button: "Try Pro Free →"
3. This ensures: No empty/broken whitespace, revenue opportunity isn't wasted, and the user sees a relevant (non-annoying) message

### 10.5 — Visual Ad Safety Protocol

**The Problem:** On sites like FreeConvert, users are terrified of clicking deceptive Google Ads that mimic "DOWNLOAD" buttons.

**The Solution:** Dastboard's primary CTA buttons (Choose Files, Download) use a **unique, consistent visual signature** that is never used by any other element on the page:

| Property | Platform Buttons | Ad Containers |
|---|---|---|
| Background | Purple gradient (brand-primary → brand-gradient-end) | Dashed border, dark/muted background |
| Text weight | 700 (bold) | Normal/medium |
| Shadow | Purple glow shadow | None |
| Hover effect | Lift + shimmer sweep | None |
| Border style | None / solid | Dashed |
| Label | None | "ADVERTISEMENT" text visible |

Users are **visually trained** within 2 seconds: "Purple gradient glow = safe Dastboard button. Everything else with dashed borders = ad zone."

### 10.6 — Dastboard Pro Feature Set

| Feature | Free | Pro ($5/mo) |
|---|---|---|
| All 5 tools | ✅ | ✅ |
| File size limit | 50 MB | 1 GB |
| Batch processing | ❌ (1 file at a time) | ✅ (100+ files) |
| Ads | ✅ Shown | ❌ Removed |
| Custom presets | ❌ | ✅ Save & reuse settings |
| API access | ❌ | ✅ REST API for automation |
| Priority WASM workers | ❌ | ✅ Faster processing via worker optimization |
| Support | Community only | Priority email support |

---

## 11. SEO & Content Architecture

### 11.1 — Per-Tool SEO Elements

Each tool's page includes dedicated SEO content **below the fold** that does not interfere with the primary transactional experience:

#### How-To Section

| Property | Specification |
|---|---|
| **Structure** | 3 numbered steps in a horizontal row |
| **Step Connectors** | Purple gradient lines connecting step circles (hidden on mobile, flipped in RTL) |
| **Content** | Each step has: numbered circle (1/2/3), H3 heading, descriptive paragraph |
| **SEO Value** | Targets "how to [action] online" queries. Provides rich content for featured snippets. |
| **Example Steps** | 1. "Upload Your Image" → 2. "Adjust Settings" → 3. "Download Result" |

#### FAQ Section

| Property | Specification |
|---|---|
| **Structure** | 5 accordion items (expandable/collapsible) |
| **Default State** | First item open, rest collapsed |
| **Animation** | Max-height transition (0 → 400px) with eased timing |
| **Chevron** | Rotates 180° when opened |
| **Content** | Targets long-tail keywords and addresses trust objections |
| **SEO Value** | FAQ structured data can generate rich results in Google Search |

#### MVP FAQ Content

1. "Is this really free?" / "آیا این واقعاً رایگان است؟"
2. "How does local processing work? Are my files private?" / "پردازش محلی چگونه کار می‌کند؟ آیا فایل‌های من خصوصی هستند؟"
3. "What is the maximum file size?" / "حداکثر حجم فایل چقدر است؟"
4. "Does this work on mobile?" / "آیا روی موبایل کار می‌کند؟"
5. "How is this different from TinyPNG or FreeConvert?" / "این چگونه با TinyPNG یا FreeConvert متفاوت است؟"

### 11.2 — Page-Level SEO

| Meta | English Value | Persian Value |
|---|---|---|
| **Title Tag** | "Dastboard — Free Browser-Based Tools \| 100% Private, Local Processing" | "دستبورد — ابزارهای رایگان مرورگری \| ۱۰۰٪ خصوصی، پردازش محلی" |
| **Meta Description** | "Free browser-based tools. Compress images, format JSON, encode Base64 — all processed locally. No uploads, 100% private." | "ابزارهای رایگان مرورگری. فشرده‌سازی تصاویر، فرمت JSON، رمزگذاری Base64 — همه به صورت محلی پردازش می‌شوند. بدون آپلود، ۱۰۰٪ خصوصی." |
| **H1** | One per tool, containing primary keyword + gradient styling |
| **Canonical URL** | Self-referencing canonical on each tool page |
| **Open Graph** | Title, description, image (branded social card), type: website |

---

## 12. Trust, Privacy & Psychology Framework

### 12.1 — The "Fake Download Button" Anxiety

**The Problem:** Users on converter sites have been conditioned to fear clicking buttons because many Google Ads disguise themselves as "DOWNLOAD NOW" or "START FREE" CTAs that install malware or redirect to scam pages.

**Dastboard's Solution:**

1. **Visual Training:** All Dastboard interactive buttons use an exclusive purple gradient + glow shadow that NO other element shares
2. **Ad Labeling:** All ad containers are clearly labeled and use dashed borders
3. **Consistent Language:** Platform buttons always say specific action words ("Choose Files", "Download", "انتخاب فایل", "دانلود") — never generic phrases like "Click Here" or "Start"

### 12.2 — Visualizing Privacy

**The Problem:** Claiming "local processing" in text is not enough. Users see these claims on many sites that don't actually deliver.

**Dastboard's Solution:**

1. **Static Trust Signals:** Green shield badge in dropzone, privacy badge at tool header
2. **Animated Trust Signal:** During processing, the padlock icon pulses with a green glow — making the abstract concept of "browser processing" feel tangibly secure
3. **Verifiable Claim:** The FAQ explicitly tells users: "Disconnect from the internet after loading the page and the tools still work" — this is a **provable claim** that builds exceptional trust

### 12.3 — The Frictionless Next Step

**The Problem:** After downloading, the user's task is complete. They will close the tab (100% certain).

**Dastboard's Solution:** The download state includes prompts for the next logical action:
- "Process another file" returns to State 1
- Related tool suggestions keep them in the ecosystem
- Subtle bookmark prompt encourages return visits

### 12.4 — Persian Market Trust

**The Problem:** Persian-speaking users are accustomed to poorly translated or broken RTL interfaces. A tool that is clearly "translated from English" feels untrustworthy.

**Dastboard's Solution:**
- Native Vazirmatn font (not a generic Arabic font)
- Proper Eastern Arabic numerals (۰۱۲۳۴۵۶۷۸۹)
- Natural Persian phrasing (not Google Translate output)
- Every UI element properly mirrors for RTL
- Cultural sensitivity in color choices and iconography

---

## 13. Accessibility Requirements

| Requirement | Specification |
|---|---|
| **Color Contrast** | All text meets WCAG AA contrast ratios in BOTH themes. Minimum 4.5:1 for body text, 3:1 for large text. |
| **Focus States** | All interactive elements must have visible focus rings (using brand-primary outline). |
| **Keyboard Navigation** | All buttons, links, toggles, and accordions must be operable via keyboard (Tab, Enter, Space, Arrow keys). |
| **Screen Reader Support** | All images have alt text. All icon-only buttons have aria-label. Ad containers have role="complementary". |
| **Motion Sensitivity** | Animations should respect prefers-reduced-motion media query. Disable pulse animations and shimmering effects for users who prefer reduced motion. |
| **Touch Targets** | Minimum 44×44px touch targets on mobile for all interactive elements. |
| **Language Declaration** | `<html lang="en">` or `<html lang="fa">` must always reflect the active language for screen readers. |
| **Direction Declaration** | `<html dir="ltr">` or `<html dir="rtl">` must always reflect the active text direction. |

---

## 14. Performance & Core Web Vitals Targets

| Metric | Target | Why |
|---|---|---|
| **Largest Contentful Paint (LCP)** | < 2.5 seconds | The dropzone/CTA must render fast. Users leave if the main interaction area is slow. |
| **First Input Delay (FID)** | < 100ms | The "Choose Files" button must respond instantly on click. |
| **Cumulative Layout Shift (CLS)** | < 0.1 | Fixed-height ad containers prevent layout jumping. No element should move after initial paint. |
| **Time to Interactive (TTI)** | < 3.5 seconds | WASM modules can be lazy-loaded. The UI shell should be interactive before WASM finishes loading. |
| **Total Page Weight** | < 500KB (initial load, excluding WASM) | HTML + CSS + fonts + SVGs. WASM loaded on-demand when user initiates an action. |

---

## 15. Analytics & Success Metrics

### 15.1 — Key Performance Indicators (KPIs)

| KPI | Definition | Target (Month 3) |
|---|---|---|
| **Monthly Active Users (MAU)** | Unique users who visit at least once per month | 50,000 |
| **Tool Completions** | Number of successful file processes (State 1 → State 3) | 30,000/month |
| **Completion Rate** | % of users who drop/upload a file AND download the result | > 70% |
| **Ad Revenue RPM** | Revenue per 1,000 page views | $3–8 (varies by geo) |
| **Pro Conversion Rate** | % of free users who subscribe to Pro | 1.5–3% |
| **Bounce Rate** | % of users who leave without interacting | < 40% |
| **Return Rate** | % of users who come back within 30 days | > 25% |

### 15.2 — Events to Track

| Event | When |
|---|---|
| `page_view` | Every page load |
| `tool_selected` | User clicks a tool tab |
| `file_upload_started` | File is dropped/selected |
| `processing_started` | WASM begins processing |
| `processing_completed` | WASM returns result |
| `file_downloaded` | User clicks Download |
| `ad_impression` | Google Ad renders successfully |
| `adblocker_detected` | Ad fails to load → fallback shown |
| `pro_cta_clicked` | Any Pro upgrade button clicked |
| `theme_toggled` | User switches theme |
| `language_toggled` | User switches language |
| `faq_opened` | User expands an FAQ item |

---

## 16. Growth Roadmap (Post-MVP)

### Phase 2 — Tool Expansion (Month 2–3)

| New Tools | Category |
|---|---|
| Resize Image | Image |
| Crop Image | Image |
| Compress PDF | PDF |
| Merge PDF | PDF |
| Word Counter | Text |
| CSV to JSON | Developer |

**UI Change:** When tools exceed 5, the Tool Tab Switcher transitions to a **Category Tab Filter** (All / Image / PDF / Dev / Text) with card grid below.

### Phase 3 — Community & Engagement (Month 4–6)

| Feature | Purpose |
|---|---|
| CMD+K search modal | Instant access to any tool |
| User accounts | Save preferences, history |
| Batch processing | Pro feature — multi-file upload |
| PWA / Offline mode | Full offline capability via Service Worker |
| API access | Pro feature — REST API for automation |

### Phase 4 — Market Expansion (Month 6–12)

| Feature | Purpose |
|---|---|
| Arabic language support | 300M+ Arabic speakers |
| Turkish language support | 80M+ Turkish speakers |
| SEO landing pages per tool | Individual URLs (/compress-image, /json-formatter) for targeted search traffic |
| Affiliate program | Users earn revenue by referring Pro subscribers |
| Enterprise tier | $49/month — custom branding, SSO, admin dashboard |

---

## 17. Risk Matrix & Blindspot Analysis

| 🚨 Risk | Probability | Impact | 🛡️ Mitigation |
|---|---|---|---|
| **Google Ads CLS penalty** | High (if not handled) | Severe (SEO ranking drop) | Fixed-height ad containers with skeleton loading |
| **AdBlocker adoption (40% of devs)** | High | Moderate (revenue loss) | Custom fallback banners + Pro upsell |
| **"Fake download button" confusion** | Medium | Severe (trust destruction) | Exclusive purple gradient for platform buttons only |
| **Mobile ad overcrowding** | High (if not handled) | Severe (conversion loss) | Hide leaderboard ad on mobile; dropzone first |
| **Persian translation feels robotic** | Medium | Moderate (trust loss in FA market) | Native Persian speaker review all strings |
| **WASM loading delay** | Medium | Low (UI still works) | Lazy-load WASM; show UI shell immediately |
| **Privacy claim skepticism** | Medium | Moderate | Provable claim: "disconnect internet, still works" |
| **Single-page architecture limits SEO** | High | Moderate | Plan Phase 4 individual URLs per tool |
| **Competitor copies local processing model** | Low (short term) | Moderate | Build brand loyalty and tool breadth as moat |

---

## 18. Appendix: Brand Guidelines

### Logo

| Property | Value |
|---|---|
| **Mark** | 34×34px rounded square, gradient fill (brand-primary → brand-gradient-end), contains sparkle/star SVG icon in white |
| **Wordmark** | "Dastboard" — Inter/Vazirmatn 800 weight. "Dast" in text-primary. "board" in brand-text. |
| **Spacing** | 10px gap between mark and wordmark |
| **Minimum Size** | 24px mark height for digital |

### Brand Colors

| Name | Hex | Usage |
|---|---|---|
| **Electric Indigo** | #7C3AED | Primary actions, CTAs, brand signature |
| **Deep Violet** | #9333EA | Gradient end, hover states |
| **Soft Lavender** | #A78BFA | Text links (dark mode), highlights |
| **Dark Violet** | #6D28D9 | Text links (light mode) |
| **Emerald** | #10B981 | Privacy/success signals |
| **Amber** | #F59E0B | Warnings, "New" badges |

### Voice & Tone

| Context | Tone |
|---|---|
| **Headlines** | Bold, confident, direct. "Compress Images Instantly." |
| **Descriptions** | Clear, reassuring, technical but accessible. |
| **Privacy claims** | Factual, verifiable, never hyperbolic. |
| **Pro upsell** | Friendly, not aggressive. "Hate ads? Here's an option." |
| **Error states** | Empathetic, helpful. "Something went wrong. Your file is safe — it never left your browser." |
| **Persian tone** | Formal-friendly (رسمی-دوستانه). Not overly casual, not stiff. Natural modern Persian. |

---

**End of Document**

*This PRD defines the complete product specification for Dastboard MVP. No code implementation details, framework choices, or stack decisions are included. This document serves as the single source of truth for designers, developers, and stakeholders to build from.*

---

**Document Status:** ✅ Final — Approved for Development

**Next Step:** Hand this document to the engineering team for technical architecture decisions and sprint planning.