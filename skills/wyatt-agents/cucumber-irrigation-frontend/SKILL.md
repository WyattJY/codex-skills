---
name: cucumber-irrigation-frontend
description: Create distinctive, production-grade frontend interfaces following the cucumber-irrigation design system - Gemini Dark Theme with glass morphism, aurora backgrounds, and modern React patterns. Use this skill when building dashboard, chat/Q&A, settings, or data visualization pages.
---

# Cucumber Irrigation Frontend Design System

## Overview

This skill defines the frontend design patterns from the cucumber-irrigation project - a professional agricultural decision system UI. The design features:

- **Gemini Dark Theme** - Deep dark backgrounds with subtle accent colors
- **Glass Morphism** - Semi-transparent panels with blur effects
- **Aurora Backgrounds** - Animated gradient blobs for visual depth
- **Modern React Stack** - React 19 + TypeScript + Tailwind CSS + Zustand

## Original Design References

**IMPORTANT**: The design system is derived from 5 HTML prototype files stored in the `references/` folder of this skill. When building new pages, **READ these files first** to understand the exact implementation:

| File | Purpose | Key Patterns |
|------|---------|--------------|
| `references/cankao.html` | Dashboard / 指挥舱 | Aurora BG, Hero Card, Vision Grid |
| `references/cankao2.html` | Decision Chain / 决策链 | Step Cards, Sensor Cards, Final Decision |
| `references/cankao3.html` | Chat Q&A / 智能问答 | Gemini Chat, Parameter Cards, Formula Box |
| `references/cankao4.html` | Data Analytics / 数据分析 | Combo Charts, Heatmap, Anomaly List |
| `references/cankao5.html` | Settings / 系统设置 | Engine Selection, Toggle, Provider Config |

When asked to create a new page, **always read the relevant cankao file from this skill's references folder** to ensure design consistency.

## Tech Stack

```
React 19.2.0 + TypeScript 5.9.3
Vite 7.2.4 (build tool)
Tailwind CSS 4.1.18
Zustand 5.0.9 (state management)
TanStack React Query 5.90.12 (data fetching)
Chart.js 4.5.1 (visualization)
```

## Core Design Tokens

### Color Palette

```css
/* Background Layers */
--gemini-bg: #131314              /* Main background */
--gemini-surface: #1E1F20          /* Card/panel surface */
--gemini-surface-hover: #28292A    /* Elevated surface */
--gemini-border: #3C4043           /* Default border */
--gemini-border-hover: #5F6368     /* Hover border */

/* Text Hierarchy */
--text-primary: #E3E3E3            /* Headlines */
--text-secondary: #C4C7C5          /* Body text */
--text-muted: #9AA0A6              /* Secondary info */
--text-dim: #8E918F                /* Tertiary info */

/* Accent Colors */
--accent-primary: #A8C7FA          /* Blue - Primary CTA */
--accent-success: #6DD58C          /* Green - Success states */
--accent-warning: #FDD663          /* Yellow - Warnings */
--accent-danger: #F28B82           /* Red - Errors/Danger */
--accent-purple: #D6BBFB           /* Purple - Special/AI */
```

### Typography

```css
--font-sans: 'Inter', 'Noto Sans SC', sans-serif;  /* Body text */
--font-mono: 'JetBrains Mono', monospace;          /* Code, data */
```

### Spacing & Radius

```css
/* Spacing */
--spacing-xs: 0.25rem    --spacing-sm: 0.5rem
--spacing-md: 1rem       --spacing-lg: 1.5rem
--spacing-xl: 2rem

/* Border Radius */
--radius-sm: 0.5rem      --radius-md: 0.75rem
--radius-lg: 1rem        --radius-xl: 1.5rem
--radius-full: 9999px
```

### Shadows

```css
--shadow-glow-primary: 0 0 12px rgba(168, 199, 250, 0.25);
--shadow-glow-success: 0 0 12px rgba(109, 213, 140, 0.25);
--shadow-panel: 0 4px 24px rgba(0, 0, 0, 0.4);
--shadow-panel-hover: 0 8px 32px rgba(0, 0, 0, 0.5);
```

## Page Design Patterns

### 1. Dashboard / Command Center Pattern

The Dashboard uses a hero card + side widgets + chart grid layout.

**Layout Structure:**
```
┌─────────────────────────────────────────────────────┐
│ Top Bar: Date/Status + Environment Capsules        │
├───────────────────────────────┬─────────────────────┤
│                               │ Warning Card        │
│   Hero Decision Card (2/3)    ├─────────────────────┤
│   - Glow effect               │ Info Card           │
│   - Large number display      │ - Progress bar      │
│   - Stat pills                │                     │
│   - Action buttons            │                     │
├───────────────────────────────┴─────────────────────┤
│ Chart Card          │  Vision Comparison Card       │
│ - Trend lines       │  - Yesterday vs Today images  │
│ - Tab switching     │  - YOLO overlay boxes         │
│                     │  - % change badges            │
└─────────────────────┴───────────────────────────────┘
```

**Hero Card with Glow:**
```tsx
<div className="glass-panel hero-card relative overflow-hidden border-l-4 border-accent-primary min-h-[380px] p-8">
  {/* Decorative glow */}
  <div className="absolute right-0 top-0 w-[300px] h-[300px] bg-accent-primary/5 rounded-full blur-[80px]" />

  {/* Watermark */}
  <div className="absolute right-10 top-10 text-8xl font-black text-white/3 select-none">
    H2O
  </div>

  {/* Large number with gradient */}
  <div className="text-7xl font-bold bg-gradient-to-br from-text-primary to-accent-primary bg-clip-text text-transparent">
    2.4
  </div>
  <span className="text-xl font-mono text-text-dim">L/plant</span>
</div>
```

**Environment Capsules:**
```tsx
<div className="flex gap-3 flex-wrap xl:flex-nowrap">
  <div className="glass-panel env-capsule flex items-center gap-3 px-4 py-3 rounded-xl">
    <i className="ph-thermometer text-accent-warning" />
    <div>
      <span className="text-[10px] uppercase tracking-wide text-text-muted">Temp</span>
      <div className="font-mono text-base font-semibold text-text-primary">28.5°C</div>
    </div>
  </div>
  {/* Similar for Humidity, Light */}
</div>
```

**Stat Pills:**
```tsx
<div className="flex gap-4 flex-wrap mb-8">
  <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-gemini-surface-hover border border-gemini-border">
    <div className="w-10 h-10 rounded-md flex items-center justify-center bg-accent-success/15 text-accent-success">
      <i className="ph-trend-up" />
    </div>
    <div>
      <span className="text-[10px] uppercase font-semibold text-text-muted">Trend</span>
      <div className="font-semibold text-text-primary">Better</div>
    </div>
  </div>
</div>
```

**Vision Comparison Grid:**
```tsx
<div className="grid grid-cols-2 gap-4">
  {/* Yesterday */}
  <div className="relative aspect-square rounded-xl overflow-hidden border border-white/10">
    <img src={yesterdayImg} className="w-full h-full object-cover" />
    <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />
    <div className="absolute bottom-3 left-3 font-mono text-xs text-text-muted">
      MASK: 42.3%
    </div>
    {/* YOLO detection box */}
    <div className="absolute top-[20%] left-[25%] w-1/2 h-1/2 border border-accent-success/80 shadow-glow-success">
      <span className="absolute -top-4 left-0 bg-accent-success text-black text-[8px] font-bold px-1">
        leaf: 0.92
      </span>
    </div>
  </div>

  {/* Today - with green border highlight */}
  <div className="relative aspect-square rounded-xl overflow-hidden border-2 border-accent-success shadow-glow-success">
    <span className="absolute top-2 right-2 text-[10px] bg-accent-success/20 text-accent-success px-1 rounded">
      +5.2%
    </span>
    {/* ... */}
  </div>
</div>
```

### 2. Chat / Knowledge Q&A Pattern

Streaming chat interface with RAG references and suggested prompts.

**Layout Structure:**
```
┌─────────────────────────────────────────────────────┐
│ Welcome State (when no messages)                    │
│ - Gradient title "AgriAgent"                        │
│ - Suggested prompt pills                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Messages Area (scrollable)                          │
│ ┌─────────────────────────────────┐                 │
│ │ User Message (right aligned)    │ ← Green bubble  │
│ └─────────────────────────────────┘                 │
│                                                     │
│ ┌──┬─────────────────────────────────┐              │
│ │AI│ Agent Message                   │              │
│ │  │ - Streaming animation           │              │
│ │  │ - Parameter cards               │              │
│ │  │ - Formula boxes                 │              │
│ │  │ - Result boxes (green)          │              │
│ │  │ - RAG References                │              │
│ └──┴─────────────────────────────────┘              │
│                                                     │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────┐ │
│ │ 📎  Type a question...                      🔊  │ │
│ └─────────────────────────────────────────────────┘ │
│              Model info footer                      │
└─────────────────────────────────────────────────────┘
```

**Welcome State with Gradient:**
```tsx
<div className="text-center py-16 px-8">
  <h1 className="text-4xl font-medium bg-gradient-to-r from-[#4285F4] via-[#9B72CB] to-[#D96570] bg-clip-text text-transparent">
    AgriAgent
  </h1>
  <p className="text-2xl text-[#444746] font-medium mt-2">
    How can I help you today?
  </p>

  {/* Suggested prompts */}
  <div className="flex flex-wrap gap-2 justify-center mt-8">
    {PROMPTS.map(prompt => (
      <button className="px-4 py-2 rounded-full border border-gemini-border bg-gemini-surface text-text-secondary text-sm hover:border-accent-primary hover:bg-gemini-surface-hover transition-all">
        {prompt}
      </button>
    ))}
  </div>
</div>
```

**User Message Bubble:**
```tsx
<div className="flex justify-end animate-chat-fade-in">
  <div className="bg-gemini-surface-hover text-text-primary rounded-3xl rounded-tr-sm px-6 py-3 max-w-[80%] shadow-lg">
    {message.content}
  </div>
</div>
```

**Agent Message with Avatar:**
```tsx
<div className="flex items-start gap-4 animate-chat-fade-in">
  <div className="flex-shrink-0 mt-1">
    <i className="ph-robot text-3xl bg-gradient-to-r from-[#4285F4] via-[#9B72CB] to-[#D96570] bg-clip-text text-transparent" />
  </div>
  <div className="flex-1 overflow-hidden">
    <div className="flex items-center gap-2 mb-2">
      <span className="text-sm font-semibold text-text-primary">AgriAgent</span>
      <span className="text-xs text-text-secondary">DeepSeek-V3</span>
    </div>
    <div className="chat-prose text-text-secondary leading-relaxed">
      {content}
    </div>
  </div>
</div>
```

**Streaming Indicator:**
```tsx
<div className="flex items-center gap-2">
  <div className="flex gap-1">
    <span className="w-2 h-2 bg-accent-primary rounded-full animate-bounce" style={{animationDelay: '0s'}} />
    <span className="w-2 h-2 bg-accent-primary rounded-full animate-bounce" style={{animationDelay: '0.16s'}} />
    <span className="w-2 h-2 bg-accent-primary rounded-full animate-bounce" style={{animationDelay: '0.32s'}} />
  </div>
</div>
```

**Parameter Grid:**
```tsx
<div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4">
  <div className="param-card bg-gemini-surface border border-gemini-border rounded-xl p-3 hover:border-accent-primary transition-all">
    <div className="text-[11px] text-text-secondary mb-1">Temperature</div>
    <div className="text-lg font-mono text-accent-primary">
      28.5<span className="text-[11px] text-text-secondary ml-1">°C</span>
    </div>
  </div>
</div>
```

**Result Box:**
```tsx
<div className="mt-4 p-4 bg-accent-success-bg border border-[#146C2E] rounded-xl flex items-center justify-between">
  <div>
    <div className="text-[11px] font-semibold uppercase tracking-wide text-accent-success">Result</div>
    <div className="text-sm text-text-secondary">Reference ET₀</div>
  </div>
  <div className="text-3xl font-mono font-bold text-accent-success">
    4.23<span className="text-sm font-normal text-text-secondary ml-1">mm/day</span>
  </div>
</div>
```

**Chat Input Bar:**
```tsx
<div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-gemini-bg via-gemini-bg/95 to-transparent">
  <div className="max-w-[800px] mx-auto">
    <div className="bg-gemini-surface rounded-full flex items-center p-2 pr-4 shadow-panel border border-gemini-border focus-within:ring-2 focus-within:ring-accent-primary/30">
      <button className="w-10 h-10 rounded-full flex items-center justify-center text-text-secondary hover:bg-gemini-surface-hover">
        <i className="ph-paperclip" />
      </button>
      <input
        className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-text-dim px-2 h-10"
        placeholder="Ask about irrigation, plant status, or calculations..."
      />
      <button className="w-10 h-10 rounded-full bg-text-primary text-gemini-bg flex items-center justify-center hover:opacity-90">
        <i className="ph-arrow-up-bold" />
      </button>
    </div>
  </div>
</div>
```

### 3. Settings Page Pattern

Two-column layout with left navigation and right content sections.

**Layout Structure:**
```
┌──────────┬──────────────────────────────────────────┐
│ Settings │                              [Saved ✓]  │
├──────────┼──────────────────────────────────────────┤
│          │                                          │
│ • Model  │  ┌────────────────────────────────────┐  │
│   Config │  │  Language Model Configuration      │  │
│          │  │  Provider selector + Status        │  │
│ • Engine │  │  ┌─────────────┬─────────────────┐ │  │
│          │  │  │ API Endpoint │ API Key         │ │  │
│ • Sensor │  │  └─────────────┴─────────────────┘ │  │
│          │  │  Model selection + Fetch button   │  │
│ • Alert  │  └────────────────────────────────────┘  │
│          │                                          │
│          │  ┌────────────────────────────────────┐  │
│          │  │  Decision Engine                   │  │
│          │  │  ┌──────────┐  ┌──────────┐        │  │
│          │  │  │ AI-based │  │ Physics  │        │  │
│          │  │  │ TSMixer  │  │ FAO56    │        │  │
│          │  │  └──────────┘  └──────────┘        │  │
│          │  │  [ ] Hybrid Mode Toggle            │  │
│          │  └────────────────────────────────────┘  │
│          │                                          │
│          │  ⚠️ Danger Zone: Reset to defaults      │
└──────────┴──────────────────────────────────────────┘
```

**Settings Navigation:**
```tsx
<nav className="w-[220px] flex-shrink-0 bg-gemini-bg border-r border-gemini-border p-6 hidden lg:block">
  <h3 className="text-[11px] font-semibold text-text-muted uppercase tracking-wider mb-4 px-3">
    Categories
  </h3>
  <div className="flex flex-col gap-1">
    {SECTIONS.map(section => (
      <button
        key={section.id}
        onClick={() => scrollTo(section.id)}
        className={cn(
          "flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
          activeSection === section.id
            ? "bg-accent-primary-bg text-[#C2E7FF]"
            : "text-text-secondary hover:bg-gemini-surface-hover hover:text-text-primary"
        )}
      >
        <i className={section.icon} />
        {section.label}
      </button>
    ))}
  </div>
</nav>
```

**Provider Card with Status:**
```tsx
<div className="setting-card p-6 relative overflow-hidden">
  <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
    <div className="flex items-center gap-3.5">
      <div className="w-11 h-11 rounded-xl bg-gemini-surface-hover border border-gemini-border flex items-center justify-center text-xl text-text-secondary">
        <i className={providerIcon} />
      </div>
      <div>
        <div className="text-[11px] text-text-muted uppercase tracking-wide font-medium mb-1">
          Provider
        </div>
        <select className="bg-transparent text-text-primary font-semibold text-base border-none cursor-pointer">
          <option value="deepseek">DeepSeek</option>
          <option value="openai">OpenAI</option>
          <option value="ollama">Ollama (Local)</option>
        </select>
      </div>
    </div>

    {/* Status indicator */}
    <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-accent-success/10 border border-accent-success/25">
      <div className="w-2 h-2 rounded-full bg-accent-success animate-pulse" />
      <span className="text-xs font-mono font-medium text-accent-success">
        Connected · 42ms
      </span>
    </div>
  </div>

  {/* Input fields */}
  <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
    <div className="flex flex-col gap-2">
      <label className="text-[11px] text-text-secondary uppercase tracking-wide font-semibold">
        API Endpoint
      </label>
      <div className="relative">
        <i className="ph-globe absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted text-sm" />
        <input
          className="w-full bg-gemini-surface-hover border border-gemini-border rounded-lg py-3 px-3.5 pl-11 text-text-primary text-sm font-mono placeholder:text-text-dim focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/15 transition-all"
          placeholder="https://api.deepseek.com/v1"
        />
      </div>
    </div>
  </div>
</div>
```

**Engine Selection Cards:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <div
    className={cn(
      "engine-card relative p-5 rounded-xl border cursor-pointer transition-all",
      selectedEngine === 'ai'
        ? "border-accent-primary bg-gemini-surface-hover shadow-glow-primary"
        : "border-gemini-border bg-gemini-surface hover:bg-gemini-surface-hover"
    )}
    onClick={() => setEngine('ai')}
  >
    <i className={cn(
      "ph-check-circle absolute top-4 right-4 text-xl",
      selectedEngine === 'ai' ? "text-accent-primary" : "text-text-dim"
    )} />

    <div className="w-12 h-12 rounded-xl bg-accent-purple/15 text-accent-purple flex items-center justify-center text-2xl mb-4">
      <i className="ph-brain" />
    </div>

    <h4 className="font-semibold text-text-primary mb-2">TSMixer</h4>
    <p className="text-sm text-text-muted leading-relaxed">
      AI-driven time series forecasting with 96-hour context window
    </p>

    <div className="mt-4 pt-4 border-t border-gemini-border">
      <div className="flex justify-between items-center text-sm">
        <span className="text-text-secondary">Lookback</span>
        <span className="font-mono font-medium text-accent-purple">96h</span>
      </div>
      <div className="w-full h-1 bg-gemini-surface-hover rounded-full mt-2.5 overflow-hidden">
        <div className="h-full w-[75%] bg-gradient-to-r from-[#A78BFA] to-accent-purple rounded-full" />
      </div>
    </div>
  </div>
</div>
```

**Toggle Switch:**
```tsx
<div className="hybrid-card mt-4 p-4 rounded-xl border border-gemini-border bg-gemini-surface flex items-center justify-between">
  <div className="flex items-center gap-3.5">
    <i className="ph-intersect text-xl text-accent-primary" />
    <div>
      <div className="text-sm font-medium text-text-primary">Hybrid Mode</div>
      <div className="text-xs text-text-muted">Use FAO56 to validate AI predictions</div>
    </div>
  </div>

  <label className="relative w-11 h-6 cursor-pointer">
    <input type="checkbox" className="sr-only peer" checked={hybridMode} onChange={toggle} />
    <div className="absolute inset-0 bg-text-dim rounded-full peer-checked:bg-accent-success transition-colors" />
    <div className="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform" />
  </label>
</div>
```

**Danger Zone:**
```tsx
<div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-xl border border-accent-danger/40 bg-accent-danger/5">
  <div>
    <h4 className="text-sm font-semibold uppercase tracking-wide text-accent-danger mb-1">
      Danger Zone
    </h4>
    <p className="text-sm text-text-secondary">
      Reset all settings to factory defaults. This action cannot be undone.
    </p>
  </div>
  <button className="px-5 py-2.5 rounded-lg border border-accent-danger text-accent-danger text-sm font-semibold hover:bg-accent-danger hover:text-gemini-surface transition-all whitespace-nowrap">
    Reset All
  </button>
</div>
```

## Component Library

### Glass Panel (Base Card)

```tsx
interface CardProps {
  hover?: boolean;
  className?: string;
  children: React.ReactNode;
}

const Card = ({ hover = true, className, children }: CardProps) => (
  <div className={cn(
    "bg-gemini-surface border border-gemini-border rounded-xl shadow-panel transition-all",
    hover && "hover:border-gemini-border-hover hover:shadow-panel-hover",
    className
  )}>
    {children}
  </div>
);
```

### Button Variants

```tsx
// Primary (Green gradient)
<button className="px-5 py-3 rounded-lg bg-gradient-to-r from-accent-success to-emerald-600 text-black font-semibold shadow-glow-success hover:-translate-y-0.5 transition-all">
  Execute
</button>

// Secondary (Ghost)
<button className="px-5 py-3 rounded-lg bg-white/5 border border-white/10 text-text-secondary hover:bg-white/10 hover:text-text-primary transition-all">
  Cancel
</button>

// Danger (Red outline)
<button className="px-5 py-3 rounded-lg border border-accent-danger text-accent-danger hover:bg-accent-danger hover:text-gemini-surface transition-all">
  Delete
</button>

// Primary Blue
<button className="px-5 py-3 rounded-lg bg-accent-primary text-[#001D35] font-semibold shadow-glow-primary hover:opacity-90 transition-all">
  Save Changes
</button>
```

### Badge Component

```tsx
// Success
<span className="px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wide bg-accent-success/15 text-accent-success border border-accent-success/30">
  Online
</span>

// Warning
<span className="px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wide bg-accent-warning/15 text-accent-warning border border-accent-warning/30">
  Pending
</span>

// Info
<span className="px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wide bg-accent-primary/15 text-accent-primary border border-accent-primary/30">
  AI-Generated
</span>
```

### Confidence Bar

```tsx
<div className="w-full">
  <div className="flex justify-between text-xs mb-1.5">
    <span className="text-text-muted">Confidence</span>
    <span className="font-mono font-medium text-accent-success">87%</span>
  </div>
  <div className="h-2 bg-gemini-surface-hover rounded-full overflow-hidden">
    <div
      className="h-full bg-gradient-to-r from-accent-success to-emerald-400 rounded-full transition-all"
      style={{ width: '87%' }}
    />
  </div>
</div>
```

### Trend Badge

```tsx
// Improving
<span className="flex items-center gap-1 text-sm font-medium text-accent-success">
  <i className="ph-trend-up" />
  Improving
</span>

// Stable
<span className="flex items-center gap-1 text-sm font-medium text-accent-primary">
  <i className="ph-minus" />
  Stable
</span>

// Declining
<span className="flex items-center gap-1 text-sm font-medium text-accent-danger">
  <i className="ph-trend-down" />
  Declining
</span>
```

## Aurora Background Component

```tsx
const AuroraBackground = () => (
  <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none opacity-40">
    <div className="aurora-blob absolute -top-[10%] -left-[10%] w-[50vw] h-[50vw] bg-gradient-radial from-accent-primary/20 to-transparent rounded-full blur-[100px] animate-blob" />
    <div className="aurora-blob absolute -bottom-[10%] -right-[10%] w-[60vw] h-[60vw] bg-gradient-radial from-accent-purple/15 to-transparent rounded-full blur-[100px] animate-blob animation-delay-5000" />
    <div className="aurora-blob absolute top-[40%] left-[40%] w-[40vw] h-[40vw] bg-gradient-radial from-accent-success/10 to-transparent rounded-full blur-[100px] animate-blob animation-delay-10000" />
  </div>
);

// CSS Animation
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}
```

## Animation Keyframes

```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Chat Message Fade */
@keyframes chatFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Typing Bounce */
@keyframes typingBounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* Shimmer (for loading states) */
@keyframes shimmer {
  0% { background-position: 100% 50%; }
  100% { background-position: -100% 50%; }
}
```

## Tailwind Config Extensions

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'gemini-bg': '#131314',
        'gemini-surface': '#1E1F20',
        'gemini-surface-hover': '#28292A',
        'gemini-border': '#3C4043',
        'gemini-border-hover': '#5F6368',
        'text-primary': '#E3E3E3',
        'text-secondary': '#C4C7C5',
        'text-muted': '#9AA0A6',
        'text-dim': '#8E918F',
        'accent-primary': '#A8C7FA',
        'accent-success': '#6DD58C',
        'accent-warning': '#FDD663',
        'accent-danger': '#F28B82',
        'accent-purple': '#D6BBFB',
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans SC', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'glow-primary': '0 0 12px rgba(168, 199, 250, 0.25)',
        'glow-success': '0 0 12px rgba(109, 213, 140, 0.25)',
        'panel': '0 4px 24px rgba(0, 0, 0, 0.4)',
        'panel-hover': '0 8px 32px rgba(0, 0, 0, 0.5)',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      },
    },
  },
};
```

## Best Practices

1. **Color Usage**
   - Use `accent-primary` (#A8C7FA blue) for primary CTAs and links
   - Use `accent-success` (#6DD58C green) for success states and primary actions
   - Use `accent-purple` (#D6BBFB) for AI-related elements
   - Always use semi-transparent backgrounds for overlays

2. **Typography**
   - Headlines: `text-text-primary font-semibold`
   - Body: `text-text-secondary`
   - Labels: `text-text-muted text-xs uppercase tracking-wide`
   - Data/Values: `font-mono text-accent-primary`

3. **Spacing**
   - Card padding: `p-6` (1.5rem)
   - Section gaps: `gap-6` (1.5rem)
   - Element gaps: `gap-3` or `gap-4`

4. **Borders & Radius**
   - Cards: `rounded-xl` (1rem)
   - Buttons: `rounded-lg` (0.75rem)
   - Pills/Capsules: `rounded-full`
   - Default border: `border-gemini-border`

5. **Hover States**
   - Border lightens: `hover:border-gemini-border-hover`
   - Background elevates: `hover:bg-gemini-surface-hover`
   - Shadow deepens: `hover:shadow-panel-hover`
   - Use `transition-all` for smooth animations

6. **Icons**
   - Use Phosphor Icons (ph-* classes)
   - Icon colors should match their context
   - Size: `text-lg` or `text-xl` for UI icons
