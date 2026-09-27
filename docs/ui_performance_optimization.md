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

## Infinite Scrolling

The research news feed loads articles dynamically as the user approaches the bottom of the page, utilizing the Intersection Observer API.

### SWR Data Caching

The `swr` (Stale-While-Revalidate) library caches paginated API responses locally, instantly restoring the scroll position if the user navigates back.

## Optimistic UI

When a user submits a trade, the UI instantly updates to the 'Pending' state locally, masking the 50ms network latency of the actual API call.

### Optimistic Rollbacks

If the backend rejects the trade (e.g., margin failure), the local state is smoothly rolled back and an error toast is surfaced to the user.

## Network Optimization

WebSocket connections utilize permessage-deflate compression to reduce the bandwidth of streaming JSON market data by up to 70%.

### Protobuf Serialization

For the highest density feeds, JSON is replaced with binary Protocol Buffers over WebSockets, eliminating string parsing overhead entirely.

### Request Deduplication

If five components request the same ticker data simultaneously, the API client deduplicates the requests into a single network call.

### HTTP/2 Multiplexing

The API gateway strictly enforces HTTP/2, allowing dozens of concurrent asset requests to be multiplexed over a single TCP connection.

## Bundle Optimization

Webpack bundle analysis is run on every CI build to ensure the initial JavaScript payload remains under 150KB (gzipped).

### Dynamic Imports

Heavy dependencies (like Three.js or Recharts) are loaded via `next/dynamic` only when the user navigates to the specific dashboard requiring them.

### Tree-Shaking

We enforce strict ECMAScript module imports (e.g., `import debounce from 'lodash/debounce'`) to ensure Webpack tree-shakes unused code from the final bundle.

### Font Subsetting

The Inter and JetBrains Mono fonts are subsetted to contain only Latin characters and numbers, reducing the font payload by 85%.

## Core Web Vitals (CWV)

The dashboard is engineered to achieve a perfect 'Good' score across all three Google Core Web Vitals metrics.

### Largest Contentful Paint (LCP)

To achieve an LCP under 2.5s, the critical CSS is inlined, and the primary structural containers are rendered server-side via Next.js.

### Cumulative Layout Shift (CLS)

All image and chart containers are assigned fixed aspect ratios and min-heights, completely eliminating layout shifting as data loads asynchronously.

### First Input Delay (FID)

FID is kept below 100ms by fiercely minimizing Long Tasks (execution > 50ms) on the main thread during initial page load.

### Interaction to Next Paint (INP)

The new INP metric is optimized by yielding to the main thread via `setTimeout` during heavy client-side filtering operations.

## Memory Management

Long-running single-page applications (SPAs) are highly susceptible to memory leaks; strict cleanup protocols are enforced.

### Effect Cleanup

Every `useEffect` hook that subscribes to a WebSocket channel or adds a DOM event listener MUST return a cleanup function to unsubscribe.

### Closure Traps

Stale closures holding references to massive historical arrays are prevented by passing dependencies correctly to `useCallback` arrays.

### Memory Profiling

Engineers must profile the application using Chrome DevTools Memory Timeline, ensuring the JS heap size returns to baseline after route transitions.

### WeakMap Caching

Internal object caches utilize `WeakMap`, allowing the browser's Garbage Collector to freely destroy cached objects when they lose their DOM references.

## CSS Rendering Performance

Visual updates are offloaded to the GPU wherever possible to bypass the browser's slow layout and paint phases.

### CSS Transforms

Animating elements (like sliding sidebars) strictly uses `transform: translate()` rather than changing `margin` or `top`, preventing layout thrashing.

### Opacity Animations

Fade effects rely exclusively on animating the `opacity` property, as this is one of the only properties the GPU can composite natively.

### The will-change Property

The `will-change: transform` property is applied to highly dynamic elements (like custom cursors) to hint the browser to promote them to their own compositor layer.

### RequestAnimationFrame

Complex JS-driven animations synchronize perfectly with the monitor refresh rate by executing exclusively within `requestAnimationFrame` callbacks.

## Event Throttling

High-frequency DOM events that trigger reflows are heavily throttled to prevent crashing the render cycle.

### Mousemove Throttling

Crosshair rendering on financial charts throttles `mousemove` events to 30ms intervals, balancing visual smoothness with CPU load.

### Lazy Loading

Images, avatars, and complex components below the fold are lazy-loaded using the native Intersection Observer API.

### Next/Image Optimization

All static assets route through `next/image`, serving modern WebP formats and automatically generating `srcset` for different screen densities.

## Dependency Auditing

Heavy, outdated legacy libraries are continuously purged from the bundle to keep the application lean and fast.

### Day.js Migration

The monolithic `moment.js` library (300KB) was entirely stripped and replaced with `day.js` (2KB), preserving the API while dropping bundle weight.

### Minimal CSS Reset

We utilize a heavily stripped-down CSS reset specifically tailored for our Tailwind setup, removing unused legacy browser normalizations.

## CDN Optimization

Static assets and compiled JS/CSS are served from a global edge CDN (Cloudflare) using aggressive Brotli compression.

### Immutable Caching

Webpack-hashed asset URLs (`main.[hash].js`) are served with `Cache-Control: public, max-age=31536000, immutable`, preventing unnecessary re-validation requests.

### Resource Hints

The document `<head>` includes `<link rel="preconnect">` tags for the backend API and WebSocket domains, shaving 100ms off the initial TLS handshake.

### Critical Path CSS

Next.js Turbopack extracts and inlines only the absolute minimum CSS required to render the initial viewport, deferring the rest.

## Performance Profiling

Engineers periodically capture Chrome tracing profiles to identify bottlenecks in the GPU rasterization thread.

### Visual Regression Tests

Playwright tests capture screenshots before and after PRs, utilizing pixel-matching to ensure layout shifts are not introduced accidentally.

