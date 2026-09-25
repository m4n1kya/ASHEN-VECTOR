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

