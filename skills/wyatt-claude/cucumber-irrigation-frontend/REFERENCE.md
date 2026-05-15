# Cucumber Irrigation Frontend - CSS Reference

## Complete CSS Variables

Copy this to your project's CSS file:

```css
/* ========================================
   AgriAgent - Design System CSS
   Gemini Dark Theme
   ======================================== */

:root {
  /* Gemini Color Palette */
  --gemini-bg: #131314;
  --gemini-surface: #1E1F20;
  --gemini-surface-hover: #28292A;
  --gemini-border: #3C4043;
  --gemini-border-hover: #5F6368;

  /* Text Colors */
  --text-primary: #E3E3E3;
  --text-secondary: #C4C7C5;
  --text-muted: #9AA0A6;
  --text-dim: #8E918F;

  /* Accent Colors */
  --accent-primary: #A8C7FA;
  --accent-primary-bg: #004A77;
  --accent-success: #6DD58C;
  --accent-success-bg: #0F291E;
  --accent-warning: #FDD663;
  --accent-warning-bg: #3D2C00;
  --accent-danger: #F28B82;
  --accent-danger-bg: #3F0E0E;
  --accent-purple: #D6BBFB;
  --accent-purple-bg: #3D2C4A;

  /* Fonts */
  --font-sans: 'Inter', 'Noto Sans SC', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Border Radius */
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.5rem;
  --radius-2xl: 2rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-glow-primary: 0 0 12px rgba(168, 199, 250, 0.25);
  --shadow-glow-success: 0 0 12px rgba(109, 213, 140, 0.25);
  --shadow-glow-warning: 0 0 12px rgba(253, 214, 99, 0.25);
  --shadow-panel: 0 4px 24px rgba(0, 0, 0, 0.4);
  --shadow-panel-hover: 0 8px 32px rgba(0, 0, 0, 0.5);

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-normal: 0.2s ease;
  --transition-slow: 0.3s ease;
}
```

## Base Styles

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
}

body {
  background-color: var(--gemini-bg);
  color: var(--text-secondary);
  font-family: var(--font-sans);
  overflow-x: hidden;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

::selection {
  background-color: var(--accent-primary);
  color: #001D35;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--gemini-border);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--gemini-border-hover);
}
```

## Key Component Classes

### Glass Panel

```css
.glass-panel {
  background: var(--gemini-surface);
  border: 1px solid var(--gemini-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-panel);
  transition: all var(--transition-normal);
}

.glass-panel:hover {
  border-color: var(--gemini-border-hover);
  box-shadow: var(--shadow-panel-hover);
}
```

### Navigation Item

```css
.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.nav-item:hover {
  color: var(--text-primary);
  background: var(--gemini-surface-hover);
}

.nav-item.active {
  background: var(--accent-primary-bg);
  color: #C2E7FF;
}
```

### Hero Card

```css
.hero-card {
  position: relative;
  overflow: hidden;
  border-left: 4px solid var(--accent-primary);
  min-height: 380px;
  padding: 2rem;
}

.hero-card__glow {
  position: absolute;
  right: 0;
  top: 0;
  width: 300px;
  height: 300px;
  background: rgba(168, 199, 250, 0.03);
  border-radius: 50%;
  filter: blur(80px);
  transition: background var(--transition-slow);
}

.hero-card:hover .hero-card__glow {
  background: rgba(168, 199, 250, 0.06);
}

.hero-card__number {
  font-size: 5rem;
  line-height: 1;
  font-weight: 700;
  background: linear-gradient(135deg, #E3E3E3, #A8C7FA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.02em;
}
```

### Stat Pills

```css
.stat-pill {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-lg);
  background: var(--gemini-surface-hover);
  border: 1px solid var(--gemini-border);
}

.stat-pill__icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-pill__icon--green {
  background: var(--accent-success-bg);
  color: var(--accent-success);
}

.stat-pill__icon--blue {
  background: rgba(168, 199, 250, 0.15);
  color: var(--accent-primary);
}
```

### Buttons

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.btn:hover {
  transform: translateY(-2px);
}

.btn--primary {
  background: linear-gradient(90deg, var(--accent-success), #059669);
  color: black;
  box-shadow: var(--shadow-glow-success);
}

.btn--secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
}

.btn--danger {
  background: transparent;
  border: 1px solid var(--accent-danger);
  color: var(--accent-danger);
}

.btn--danger:hover {
  background: var(--accent-danger);
  color: var(--gemini-surface);
}
```

### Chat Components

```css
.chat-msg--user {
  display: flex;
  justify-content: flex-end;
  animation: chatFadeIn 0.3s ease-out;
}

.chat-msg__user-bubble {
  background: #28292A;
  color: #E3E3E3;
  border-radius: 1.5rem;
  border-top-right-radius: 0.25rem;
  padding: 0.75rem 1.5rem;
  max-width: 80%;
}

.chat-msg--agent {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  animation: chatFadeIn 0.3s ease-out;
}

.chat-input-box {
  background: #1E1F20;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
  border: 1px solid #444746;
}

.chat-input-box:focus-within {
  box-shadow: 0 0 0 2px var(--gemini-bg), 0 0 0 4px rgba(168, 199, 250, 0.3);
}
```

### Settings Components

```css
.setting-card {
  background: var(--gemini-surface);
  border: 1px solid var(--gemini-border);
  border-radius: var(--radius-lg);
  transition: all var(--transition-normal);
}

.setting-card:hover {
  border-color: var(--gemini-border-hover);
  box-shadow: var(--shadow-panel-hover);
}

.input-m3 {
  width: 100%;
  background: var(--gemini-surface-hover);
  border: 1px solid var(--gemini-border);
  border-radius: var(--radius-sm);
  padding: 0.75rem;
  color: var(--text-primary);
  font-family: var(--font-mono);
  transition: all var(--transition-normal);
}

.input-m3:focus {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(168, 199, 250, 0.15);
}

.toggle__slider {
  position: absolute;
  inset: 0;
  background: var(--text-dim);
  border-radius: 9999px;
  transition: all 0.25s ease;
}

.toggle__input:checked + .toggle__slider {
  background: var(--accent-success);
}
```

### Danger Zone

```css
.danger-zone {
  border: 1px solid rgba(242, 139, 130, 0.4);
  background: rgba(242, 139, 130, 0.05);
  border-radius: var(--radius-md);
  padding: 1.5rem;
}

.danger-zone__title {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent-danger);
}
```

## Animations

```css
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes chatFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes typingBounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

@keyframes shimmer {
  0% { background-position: 100% 50%; }
  100% { background-position: -100% 50%; }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
```

## Utility Classes

```css
.text-glow {
  text-shadow: 0 0 10px rgba(0, 255, 148, 0.5);
}

.text-glow-blue {
  text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

.animate-pulse {
  animation: pulse 2s infinite;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-blob {
  animation: blob 25s infinite alternate;
}
```

## Phosphor Icons Reference

The design uses [Phosphor Icons](https://phosphoricons.com/). Common icons used:

```
ph-thermometer      - Temperature
ph-drop             - Humidity/Water
ph-sun              - Light/Solar
ph-plant            - Plants/Growth
ph-trend-up         - Upward trend
ph-trend-down       - Downward trend
ph-minus            - Stable/Neutral
ph-brain            - AI/Machine Learning
ph-check-circle     - Selected/Complete
ph-robot            - AI Agent
ph-paperclip        - Attachments
ph-arrow-up         - Send/Submit
ph-globe            - Web/API
ph-key              - API Key/Security
ph-gear             - Settings
ph-warning          - Alerts/Warnings
ph-intersect        - Hybrid/Combine
ph-trash            - Delete
ph-info             - Information
```

## Grid Layouts

### Main Dashboard Grid

```css
.grid-main {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 1024px) {
  .grid-main {
    grid-template-columns: 2fr 1fr;
  }
}
```

### Two Column Grid

```css
.grid-charts {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 1024px) {
  .grid-charts {
    grid-template-columns: 1fr 1fr;
  }
}
```

### Settings Layout

```css
.settings-layout {
  display: flex;
  height: 100%;
}

.settings-nav {
  width: 220px;
  flex-shrink: 0;
  border-right: 1px solid var(--gemini-border);
  display: none;
}

@media (min-width: 1024px) {
  .settings-nav {
    display: block;
  }
}

.settings-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 2rem;
}
```
