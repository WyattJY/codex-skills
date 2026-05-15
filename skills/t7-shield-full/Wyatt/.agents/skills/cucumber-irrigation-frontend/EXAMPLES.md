# Cucumber Irrigation Frontend - Design Examples

This skill includes 5 original HTML design prototypes that serve as the source of truth for the frontend design system.

## Reference Files Location

All reference files are stored within this skill's directory:

```
references/cankao.html    - Dashboard (指挥舱)
references/cankao2.html   - Decision Chain (决策链)
references/cankao3.html   - Chat Q&A (智能问答)
references/cankao4.html   - Data Analytics (数据分析)
references/cankao5.html   - Settings (系统设置)
```

## File Descriptions

### 1. cankao.html - Dashboard / Command Center

**Theme**: Neon Green + Aurora Background
**Key Features**:
- Aurora background with animated blobs (blue, purple, green)
- Glass morphism panels with blur effect
- Hero decision card with large typography
- Environment capsules (Temp, Humidity, Light)
- Vision comparison grid (Yesterday vs Today with YOLO boxes)
- Chart.js trend visualization
- Mobile-responsive sidebar

**Color Palette**:
```
Neon Green: #00FF94
Neon Blue: #38BDF8
Neon Purple: #A78BFA
Neon Orange: #FB923C
Dark BG: #0B1120
Dark Card: #1E293B
```

### 2. cankao2.html - Decision Chain

**Theme**: Cyber Dashboard with Emerald/Cyan accents
**Key Features**:
- Step-by-step decision flow cards (Plant Response, Sanity Check, TSMixer)
- Sensor input cards with progress bars and glow effects
- Final decision hero card with gradient border
- Live camera feed placeholder with AI bounding box
- Agent insights panel with typed messages
- Real-time clock display

**Color Palette**:
```
Agri Neon: #34D399 (Emerald 400)
Agri Cyan: #22D3EE (Cyan 400)
Agri Alert: #F59E0B (Amber 500)
```

### 3. cankao3.html - Chat Q&A (Gemini Style)

**Theme**: Gemini Dark with gradient accents
**Key Features**:
- Gemini-style gradient text ("AgriAgent")
- Chat bubble layout (user right, agent left)
- Parameter cards in agent response
- KaTeX formula rendering
- Result box with green accent
- Comparison bar visualization
- Rounded input bar with icon buttons
- Shimmer/typing animations

**Color Palette**:
```
Background: #131314
Surface: #1E1F20
Primary: #A8C7FA
Green: #34D399
Text Gradient: #4285F4 → #9B72CB → #D96570
```

### 4. cankao4.html - Data Analytics

**Theme**: Clean analytics dashboard
**Key Features**:
- AI-generated summary card with gradient left bar
- Combo chart (bars + line)
- DLI bar chart with conditional coloring
- VPD heatmap grid simulation
- Anomaly detection list
- Search bar with command shortcut
- Date filter pills

**Color Palette**:
```
Primary: #A8C7FA (Blue)
Secondary: #6DD58C (Green)
Accent: #F28B82 (Red)
```

### 5. cankao5.html - System Settings

**Theme**: Material 3 inspired settings page
**Key Features**:
- Left navigation panel with active state
- Provider card with dynamic icon
- API URL/Key input fields with icons
- Model auto-fetch functionality
- Engine selection cards (TSMixer vs FAO56)
- Toggle switches (hybrid mode)
- Sensor status list
- Danger zone (factory reset)
- Save button with loading animation

**Color Palette**:
```
Primary: #A8C7FA
Success: #6DD58C
Warning: #FDD663
Danger: #F28B82
Surface Hover: #28292A
Active Nav: #004A77
```

## How to Use These References

When building new pages or components, you can:

1. **Read the reference files** to understand the exact implementation
2. **Copy design patterns** directly from these prototypes
3. **Extract CSS classes** for consistent styling

Example prompt:
```
"Create a new sensor configuration page following the design patterns from cankao5.html (Settings page)"
```

## Design Pattern Index

| Pattern | Reference File | Section |
|---------|---------------|---------|
| Aurora Background | cankao.html | `.aurora-container`, `.aurora-blob` |
| Glass Panel | cankao.html | `.glass-panel` |
| Hero Card | cankao.html | Line 345-407 |
| Sensor Card | cankao2.html | `.sensor-card` |
| Decision Flow | cankao2.html | `.step-card`, `.final-decision` |
| Chat Bubble | cankao3.html | User/Agent message styles |
| Parameter Card | cankao3.html | `.param-card` |
| Result Box | cankao3.html | Green result display |
| Analytics Card | cankao4.html | `.analytics-card` |
| Heatmap Grid | cankao4.html | VPD distribution section |
| Setting Card | cankao5.html | `.setting-card` |
| Toggle Switch | cankao5.html | `.toggle-checkbox`, `.toggle-label` |
| Input M3 Style | cankao5.html | `.input-m3` |
| Engine Selection | cankao5.html | `.card-selected` pattern |

## Animation Classes

From these reference files:

```css
/* Blob Animation (Aurora) */
.animate-blob - 20s infinite alternate

/* Fade In */
.animate-fade-in - 0.5s ease-out forwards

/* Pulse */
.animate-pulse - Standard Tailwind pulse

/* Typewriter Cursor */
.animate-typewriter - Blinking cursor effect

/* Gradient Animation */
.animate-gradient-x - Background gradient shift

/* Shimmer Loading */
.animate-shimmer - Loading skeleton effect
```

## Icon Library

All reference files use either:
- **Phosphor Icons** (`ph-*` classes) - cankao.html
- **FontAwesome** (`fa-*` classes) - cankao2-5.html

For new development, prefer Phosphor Icons for consistency with the main frontend.
