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

