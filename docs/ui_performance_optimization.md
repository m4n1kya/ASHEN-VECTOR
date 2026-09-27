# Frontend Performance & UI Smoothness

This document outlines the extreme performance optimizations required to maintain 60FPS in a high-frequency trading dashboard.

## The 16.6ms Budget

To maintain a smooth 60 frames per second, the main thread must process all React reconciliation, state updates, and layout calculations in under 16.6ms.

## React Rendering Optimization

Unnecessary re-renders are the primary cause of UI stutter. We strictly enforce shallow equality checks before allowing a component to update.

### Memoization Boundaries

All heavy charting and tabular components are wrapped in `React.memo()`, ensuring they only re-render when their specific primitive props change.

### Expensive Computations

Calculations like sorting arrays or filtering large tick datasets are wrapped in `useMemo` to prevent recalculation on every render cycle.

### Stable Event Handlers

Event handlers passed to deeply nested child components are wrapped in `useCallback` to prevent breaking `React.memo` reference equality checks.

### Object Instantiation

Inline object and array instantiation (e.g., `style={{ margin: 10 }}`) is strictly prohibited in render functions of high-frequency components.

### React Server Components

Static shells and initial data fetching are offloaded to React Server Components (RSC) to drastically reduce the JavaScript payload sent to the client.

### Boundary Separation

The `'use client'` directive is pushed as deep down the component tree as possible, keeping interactivity isolated to the leaves of the DOM.

### Concurrent Rendering

React 18's concurrent features (`useTransition`) allow the UI to remain responsive during heavy charting updates by yielding control back to the browser.

## Web Worker Architecture

The browser's main thread is reserved strictly for UI manipulation; all heavy data crunching is offloaded to Web Workers.

### JSON Parsing Pool

Large historical datasets (e.g., 100k OHLCV bars) are deserialized in a background Web Worker pool to prevent main thread blocking.

### OffscreenCanvas

Chart rendering is delegated to an `OffscreenCanvas` inside a Web Worker, ensuring that rapid tick updates never freeze the DOM.

### Worker RPC (Comlink)

The `Comlink` library wraps the native `postMessage` API, allowing the main thread to call Worker functions natively via Proxies.

### Zero-Copy Transfer

To pass gigabytes of tick data to Workers instantly, we transfer ownership of raw `ArrayBuffer` objects instead of using structured cloning.

## WebAssembly (Wasm)

Complex client-side risk calculations (e.g., local VaR approximations) are written in Rust and compiled to WebAssembly for near-native execution speed.

### Wasm SIMD

WebAssembly SIMD (Single Instruction, Multiple Data) is enabled, allowing the client to process 4 floating-point operations in a single CPU cycle.

## State Management (Zustand)

We utilize Zustand for global state management, avoiding the boilerplate and performance overhead of Redux context propagation.

### Atomic Selection

Components must select the exact slice of state they require (e.g., `useStore(state => state.theme)`) rather than subscribing to the entire store object.

### Transient State

For ultra-high-frequency data (like bid/ask prices), state is mutated directly via `useStore.setState` and DOM refs without triggering a full React render.

## Data Visualization Rendering

SVGs are limited to UI icons; all data-dense charts have been migrated to the HTML5 `<canvas>` element for massive performance gains.

### TradingView Integration

The primary price charts utilize TradingView's Lightweight Charts library, capable of rendering millions of data points flawlessly.

### WebGL Volatility Surfaces

Options volatility surfaces are rendered in 3D using WebGL (via Three.js), leveraging the user's local GPU for rendering complex geometry.

### Retina Display Crispness

Canvas internal dimensions are multiplied by `window.devicePixelRatio` and scaled down via CSS to prevent blurriness on high-DPI Apple displays.

## DOM Virtualization

Rendering thousands of DOM nodes crashes browsers. We implement strict DOM virtualization for any list exceeding 50 items.

### Order Book Virtualization

The Level 3 Order Book utilizes `react-window` to only render the 30 rows currently visible in the viewport, discarding off-screen rows.

### Dynamic Row Heights

Virtualization handles variable-height rows efficiently using a `ResizeObserver` cache to measure and position elements asynchronously.

### Overscanning

The virtual list renders an extra 5 'overscan' items above and below the viewport to prevent white flashes during rapid scrolling.

