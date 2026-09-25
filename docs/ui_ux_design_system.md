# Premium UI/UX Design System (Angel One Inspired)

This document outlines the modern, premium design language adopted for the ASHEN-VECTOR trading terminal.

## Aesthetic Philosophy

The UI transitions from a brutalist matte-black to a modern, high-contrast, premium aesthetic inspired by top-tier retail brokers like Angel One.

## Base Background Colors

Pure black (#000000) is replaced with a deep, rich navy blue (`#0B132B` or `#0a0e17`) to reduce eye strain while maintaining a professional dark mode.

### Primary Brand Accent

The primary accent color is set to a vibrant Indigo/Royal Blue (`#2D42ED`), injecting energy and establishing visual hierarchy.

### Secondary Accent

A secondary vibrant Orange/Coral (`#FF6B00`) is used for primary call-to-action buttons (e.g., executing trades) to draw immediate attention.

## Semantic Market Colors

The market state colors are modernized to brighter, glowing neon variants: `#00C853` (Up/Bull) and `#FF3D00` (Down/Bear).

### Alert Colors

System warnings and moderate risk alerts utilize a vibrant Amber (`#FFC107`) to stand out against the deep blue background.

## Typography

The typography system heavily leverages `Inter` for all UI text, providing excellent legibility at small sizes, typical of premium fintech apps.

### Font Weight Hierarchy

A strict hierarchy is enforced: Regular (400) for body, Medium (500) for table headers, Semibold (600) for primary metrics, and Bold (700) for tickers.

### Tabular Data

All financial figures and changing prices strictly enforce `tabular-nums` to prevent horizontal jittering during live market ticks.

## Shape and Radii

The brutalist sharp corners are softened. We adopt a standard 8px (`rounded-lg`) for internal panels and 12px (`rounded-xl`) for major structural containers.

### Border Colors

Panel borders use a subtle Slate/Navy tone (`#1E293B`) rather than harsh gray, creating a seamless separation between elevated surfaces.

## Elevation and Shadows

In a dark theme, elevation is communicated via surface lightness (lighter blue-gray) combined with very subtle, widespread drop shadows (`shadow-lg`).

### Interactive Hover States

Buttons and clickable table rows feature a slight background lightness shift combined with a subtle outer glow using the primary brand blue.

### Glassmorphism Overlays

Modals and dropdown menus utilize a backdrop blur (`backdrop-blur-md`) with a translucent navy background to create depth over the main application.

## Layout Architecture

The main dashboard content is constrained to a maximum width of 1600px, horizontally centered, preventing extreme stretching on ultrawide monitors.

### Responsive Breakpoints

The UI is strictly mobile-responsive, collapsing sidebars into hamburger menus and stacking charts vertically on screens below 768px.

### Spacing Tokens

We strictly adhere to the Tailwind spacing scale (4, 8, 16, 24, 32px), eliminating magic numbers and ensuring consistent rhythm across all views.

## Top Navigation Redesign

The top header is thickened to 64px, featuring a bold branding area on the left and a quick-access global search bar in the center.

### Sidebar Navigation

The sidebar uses distinct Lucide icons paired with Medium-weight text. Active states are highlighted with a vertical blue accent bar on the left edge.

### Micro-interactions

Navigation links utilize a 200ms `ease-in-out` transition for color and background changes, making the interface feel highly responsive and polished.

## Dashboard Layout

The primary dashboard utilizes a CSS Grid layout: a wide central column for charts and a narrower right-hand column for the live order book and execution panel.

### Portfolio Summary Cards

Top-level portfolio metrics (AUM, Day P&L, Margin) are displayed in elevated cards with glowing metric numbers and sparkline charts.

### Market Ticker Tape

A continuous, horizontally scrolling ticker tape is added below the header, displaying live index and primary watchlist prices.

## Charting Components

Chart containers maintain a 16:9 or 21:9 aspect ratio, bounded by rounded borders, with the charting library configured to match the deep navy theme.

### Recharts Tooltips

Recharts tooltips are overridden with custom CSS: dark translucent background, white text, and colored indicator dots matching the data series.

### Axis and Legend Styling

Chart axes and grid lines are muted (`#334155`) to keep focus on the data, while legends use a crisp, small sans-serif font.

## Data Tables

Financial data tables feature subtle zebra-striping (alternating `#0B132B` and `#0F172A`) with a prominent hover effect on the entire row.

### Sticky Table Headers

All tables exceeding 500px in height implement a sticky header, ensuring column context is never lost while scrolling through large position lists.

### Numerical Alignment

A strict design rule: all numerical columns (Price, Volume, P&L) are right-aligned, while textual columns (Ticker, Name) are left-aligned.

### P&L Color Logic

Cells displaying P&L automatically apply the `text-quant-up-text` or `text-quant-down-text` utility classes based on the value's sign.

### High-Density Mode

Users can toggle a 'Compact Mode' which reduces table cell padding from 12px to 4px and scales down font sizes for maximum data density.

## Order Entry Ticket

The execution ticket is redesigned as a floating, elevated modal with a distinct Orange/Blue action button to prevent accidental clicks.

### Form Inputs

Text inputs and dropdowns feature a solid dark background with no border, revealing a glowing 2px Indigo ring (`ring-2 ring-indigo-500`) upon focus.

### Quantity Selectors

Share quantity inputs include integrated +/- stepper buttons, styled with subtle hover backgrounds to encourage mouse interaction.

